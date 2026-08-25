"""
Entrypoint for all common scripting infrastructure.

Invoke like 'python resources <actions>'
Where actions can be any list of actions to take.

"""

from argparse import ArgumentParser
from mcresources import ResourceManager, utils
from typing import Optional

import os
import sys
import json
import difflib

import constants
import world_gen
import generate_book
import format_lang

BOOK_LANGUAGES = ('en_us',) # don't see these atm?, 'ko_kr', 'pt_br', 'uk_ua', 'zh_cn', 'zh_tw')
MOD_LANGUAGES = ('en_us',) # don't see these either? , 'es_es', 'ja_jp', 'ko_kr', 'pt_br', 'ru_ru', 'tr_tr', 'uk_ua', 'zh_cn', 'zh_tw')
RESOURCE_DIR = 'src'
TEST_RESOURCE_DIR = 'testsrc'


def main():
    parser = ArgumentParser(description='Entrypoint for all common scripting infrastructure.')
    parser.add_argument('actions', nargs='+', choices=(
        'clean',  # clean all resources (assets / data), including book
        'validate',  # validate no resources are changed when re-running
        'all', # generate all resources (assets / data / book)
        'worldgen',  # only world gen data (excluding tags)
        'book',  # generate the book
        'format_lang',  # format language files
        'update_lang',  # useful to update localizations after a change to the base which renders some translations incorrect
    ))
    parser.add_argument('--translate', type=str, default='en_us', help='Runs the book translation using a single provided language')
    parser.add_argument('--translate-all', action='store_false', dest='translate_all', help='Runs the book against all provided translations')
    parser.add_argument('--reverse-translate', action='store_true', dest='reverse_translate', help='Reverses a book translation, creating a <lang>.json from translated book files')
    parser.add_argument('--local', type=str, default=None, help='Points to a local minecraft instance. Used for \'book\', to generate a hot reloadable book, and used for \'clean\', to clean said instance\'s book')
    parser.add_argument('--hotswap', action='store_true', dest='hotswap', help='Causes resource generation to also generate to --hotswap-dir')
    parser.add_argument('--hotswap-main', type=str, default='./out/production/resources', help='Used for \'--hotswap\'')
    parser.add_argument('--hotswap-test', type=str, default='./out/test/resources', help='Used for \'--hotswap\'')

    args = parser.parse_args()

    # Validate the working directory is correct (we should find `build.gradle.kts`)
    if not os.path.exists('build.sh'):
        print('ERROR')
        print('Unable to verify that working directory contains TFC sources')
        print('Working directory must be basemod/, not /basemod/resources/ !')
        return
    for action in args.actions:
        if action == 'clean':
            clean(args.local)
        elif action == 'validate':
            validate_resources()
        elif action == 'worldgen':
            touched: set[str] = resources_at(
                ResourceManager('tfc', resource_dir=RESOURCE_DIR),
                ResourceManager('minecraft', resource_dir=RESOURCE_DIR),
                ResourceManager('tfc', resource_dir=TEST_RESOURCE_DIR)
            )
            if args.hotswap:
                resources_at(
                    ResourceManager('tfc', resource_dir=args.hotswap_main),
                    ResourceManager('minecraft', resource_dir=args.hotswap_main),
                    ResourceManager('tfc', resource_dir=args.hotswap_test)
                )
            print('Removed Stale =', utils.clean_generated_resources(RESOURCE_DIR, touched))
        elif action == 'all':
            touched: set[str] = resources_at(
                ResourceManager('tfc', resource_dir=RESOURCE_DIR),
                ResourceManager('minecraft', resource_dir=RESOURCE_DIR),
                ResourceManager('tfc', resource_dir=TEST_RESOURCE_DIR)
            )
            if args.hotswap:
                resources_at(
                    ResourceManager('tfc', resource_dir=args.hotswap_main),
                    ResourceManager('minecraft', resource_dir=args.hotswap_main),
                    ResourceManager('tfc', resource_dir=args.hotswap_test)
                )
            touched |= format_lang.main(False, 'tfc', MOD_LANGUAGES)
            for lang in BOOK_LANGUAGES:  # Translate all
                touched |= generate_book.main(lang, args.local, False)
            print('Removed Stale =', utils.clean_generated_resources(RESOURCE_DIR, touched))
        elif action == 'book':
            if args.translate_all:
                for lang in BOOK_LANGUAGES:
                    generate_book.main(lang, args.local, validate=False, reverse_translate=args.reverse_translate)
            else:
                generate_book.main(args.translate, args.local, validate=False, reverse_translate=args.reverse_translate)
        elif action == 'format_lang':
            format_lang.main(False, 'tfc', MOD_LANGUAGES)


def validate_resources():
    """ Validates all resources are unchanged. """
    resources_at(
        rm := ValidatingResourceManager('tfc', RESOURCE_DIR),
        vanilla_rm := ValidatingResourceManager('minecraft', RESOURCE_DIR),
        test_rm := ValidatingResourceManager('tfc', TEST_RESOURCE_DIR)
    )

    error = rm.error_files != 0 or test_rm.error_files != 0

    for lang in BOOK_LANGUAGES:
        try:
            generate_book.main(lang, None, True, rm)
            error |= rm.error_files != 0
        except AssertionError as e:
            print(e)
            error = True

    for lang in MOD_LANGUAGES:
        try:
            format_lang.main(True, 'tfc', (lang,))
        except AssertionError as e:
            print(e)
            error = True

    assert not error, 'Validation Errors Were Present'


def resources_at(
    rm: ResourceManager,
    vanilla_rm: ResourceManager,
    test_rm: ResourceManager,
    do_hints: bool = True
) -> set[str]:
    # Do lang keys first, because it's ordered intentionally
    rm.lang(constants.DEFAULT_LANG)

    # generic assets / data
    world_gen.generate(rm, do_hints)
    rm.flush()

    print('New = %d, Modified = %d, Unchanged = %d, Errors = %d' % (
        rm.new_files + test_rm.new_files + vanilla_rm.new_files,
        rm.modified_files + test_rm.modified_files + vanilla_rm.modified_files,
        rm.unchanged_files + test_rm.unchanged_files + vanilla_rm.unchanged_files,
        rm.error_files + test_rm.error_files + vanilla_rm.error_files))

    return rm.written_files | vanilla_rm.written_files

class ValidatingResourceManager(ResourceManager):

    def __init__(self, domain: str, resource_dir):
        super(ValidatingResourceManager, self).__init__(domain, resource_dir)
        self.validation_error = False

    def write(self, path_parts, data_to_write):
        data_to_write = utils.del_none({'__comment__': 'This file was automatically created by mcresources', **data_to_write})
        path = os.path.normpath(os.path.join(self.resource_dir, *path_parts)) + '.json'
        try:
            if not os.path.isfile(path):
                print('Error: resource generation created new file \'%s\'' % path, file=sys.stderr)
                self.error_files += 1
                return
            with open(path, 'r', encoding='utf-8') as file:
                old_data = json.load(file)
            if old_data != data_to_write:
                old_text = json.dumps(old_data, indent=self.indent)
                text = json.dumps(data_to_write, indent=self.indent)
                diff = '\n'.join(difflib.unified_diff(old_text.split('\n'), text.split('\n'), 'old', 'new', n=1))
                print('Error: resource generation modified file \'%s\' Diff:\n%s\n' % (path, diff), file=sys.stderr)
                self.error_files += 1
        except Exception as e:
            self.on_error(path, e)
            self.error_files += 1


def clean(local: Optional[str]):
    """ Cleans all generated resources files """
    clean_at('./src')
#    clean_at('./src_veinbuffs')
    if local:
        clean_at(local)

def clean_at(location: str):
    for tries in range(1, 1 + 3):
        try:
            utils.clean_generated_resources(location)
            print('Clean %s' % location)
            return
        except OSError:
            print('Failed, retrying (%d / 3)' % tries)
    print('Clean Aborted')


if __name__ == '__main__':
    main()
