from argparse import ArgumentParser
from typing import Optional

from constants import PUB_INDICATORS
from patchouli import *
from mcresources import ResourceManager
from mcresources import utils


class LocalInstance:
    INSTANCE_DIR = os.getenv('LOCAL_MINECRAFT_INSTANCE')  # The location of a local .minecraft directory, for testing in external minecraft instance (as hot reloading works much better)

    @staticmethod
    def wrap(rm: ResourceManager):
        def data(name_parts: ResourceIdentifier, data_in: JsonObject, root_domain: str = 'data'):
            return rm.write((LocalInstance.INSTANCE_DIR, '/'.join(utils.str_path(name_parts))), data_in)

        if LocalInstance.INSTANCE_DIR is not None:
            rm.data = data
            return rm
        return None


def main_with_args():
    parser = ArgumentParser('generate_book.py')
    parser.add_argument('book', type=str, default='me', help='The default action when called from main')
    parser.add_argument('--translate', type=str, default='en_us', help='The language to translate to')
    parser.add_argument('--local', type=str, default=None, help='The directory of a local .minecraft to copy into')

    args = parser.parse_args()
    main(args.translate, args.local, False)


def main(translate_lang: str, local_minecraft_dir: Optional[str], validate: bool, validating_rm: ResourceManager = None, reverse_translate: bool = False):
    LocalInstance.INSTANCE_DIR = local_minecraft_dir

    rm = ResourceManager('tfc', './src_veinbuffs')
    if validate:
        rm = validating_rm
    i18n = I18n(translate_lang, validate)

    print('Writing book at %s' % translate_lang)
    make_book(rm, i18n, local_instance=False, reverse_translate=reverse_translate, nohints=True)

    i18n.flush()

    rm = ResourceManager('tfc', './src')
    if validate:
        rm = validating_rm
    i18n = I18n(translate_lang, validate)

    print('Writing book at %s' % translate_lang)
    make_book(rm, i18n, local_instance=False, reverse_translate=reverse_translate)

    i18n.flush()

    if LocalInstance.wrap(rm):
        print('Copying %s book into local instance at: %s' % (translate_lang, LocalInstance.INSTANCE_DIR))
        make_book(rm, I18n(translate_lang, validate), local_instance=True)

    return rm.written_files


def make_book(rm: ResourceManager, i18n: I18n, local_instance: bool = False, nohints = False, reverse_translate: bool = False ):
    buff_desc = "Mountain Iron and some interesting gem pipes!"
    ore_desc = '$(bold)Ore Veins on the Brink$()$(br2)Exploring the heights of the world may be more rewarding! In the mountains, new dense iron veins spawn.'
    ore_summary = 'Some ore veins are enriched at the top of the world.'

    if nohints:
        #rm.domain = 'tfcgyres_veinbuffs'  # DOMAIN CHANGE
        book = Book(rm, 'field_guide', {}, i18n, local_instance, reverse_translate)

        book.category('tfcgyres_veinbuffs', 'Ore Spawning', ore_summary, 'tfc:metal/propick/steel', is_sorted=True, entries=(
            entry('veinbuffs', 'Ore Vein Tweaks', 'tfc:ore/magnetite', pages=(
                text(buff_desc),
                text(ore_desc))),
        ))
        book.build()

    else:
        #rm.domain = 'tfcgyres_orehints'  # DOMAIN CHANGE
        book = Book(rm, 'field_guide', {}, i18n, local_instance, reverse_translate)

        book.category('tfcgyres_orehints', 'Ore Hints and Spawning', 'Mineral veins now have hint rocks like metal veins have small nuggets!$(br2)Thanks to AnodeCathode of TechNodeFirmaCraft for the "hint rock" idea and initial rock selections.$(br2)Rich iron veins spawn in the mountains above y=90.', 'tfc:metal/propick/steel', is_sorted=True, entries=(
            entry('orehints', 'Mineral Hints', 'tfc:ore/graphite', pages=(
                text('Finding TFC mineral veins is easier with OreHints!$(br2)Hint rocks generate in the world near mineral veins just like nuggets for metal ores.$(br)Find these rocks on the surface where they don\'t match, and in caves, and there\'s likely a mineral vein around! Underground indicators for every metal vein also spawn. Kaolinite is unchanged.'),
                text('$(bold){:_<12s}'.format('Ore') + '{:_>16s}'.format('Hints$(br)')+'$()'+''.join([('$(l:the_world/ores_and_minerals#{0}){1:_<16s}$(){2:_>10s}').format(min, min.title(), PUB_INDICATORS[min].title())+'$(br)' for min in PUB_INDICATORS])+'$(l:the_world/ores_and_minerals#kaolinite)Kaolinite________$()Blood_Lily'))),
        ))

        book.build()

if __name__ == '__main__':
    main_with_args()

