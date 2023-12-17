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

#    i18n = I18n.create('en_us')
#    rm = ResourceManager('tfcgyres_veinbuffs', 'src_veinbuffs')
#    make_book(rm, i18n, nohints=True)
#    i18n.flush()

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

    print('Done')

def make_book(rm: ResourceManager, i18n: I18n, local_instance: bool = False, nohints = False, reverse_translate: bool = False ):
    #buff_desc = "Some of the current veins were too small and too rare.$(br2)Coal veins are now much larger horizontal discs with fewer inclusions. Most other mineral veins are larger and more common, but occur at the same depths."
    #ore_desc = '$(bold)Ore Veins on the Brink$()$(br2)Exploring the depths and heights of the world may be more rewarding! New veins below y-level 0 now exist for all metamorphic and igneous intrusive ores: metal, mineral, and diamonds/emeralds. These veins may be larger, denser, and purer.$(br2)In the mountains, new dense iron, copper and sulfur veins spawn.'
    #ore_summary = 'Ore veins are enriched, especially at the top and bottom of the world.'

    '''if nohints:
        rm.domain = 'tfcgyres_veinbuffs'  # DOMAIN CHANGE
        book = Book(rm, 'field_guide', {}, i18n, local_instance, reverse_translate)

        book.category('tfcgyres_veinbuffs', 'Ore Spawning', ore_summary, 'tfc:metal/propick/steel', is_sorted=True, entries=(
            entry('veinbuffs', 'Ore Vein Tweaks', 'tfc:ore/graphite', pages=(
                text('Ore veins seem too difficult to find, so why not make it a bit easier? ' + buff_desc),
                text(ore_desc))),
        ))
'''
#    else:
#    rm.domain = 'tfcgyres_orehints'  # DOMAIN CHANGE
    book = Book(rm, 'field_guide', {}, i18n, local_instance, reverse_translate)

    book.category('tfcgyres_orehints', 'Ore Hints and Spawning', 'Mineral veins now have hint rocks like metal veins have small nuggets! $(br2)Thanks to AnodeCathode of TechNodeFirmaCraft for the "hint rock" idea and initial rock selections.$(br2)Additional rich iron veins spawn in the mountains above y=90.', 'tfc:metal/propick/steel', is_sorted=True, entries=(
        entry('orehints', 'Mineral Hints', 'tfc:ore/graphite', pages=(
            text('Finding TFC mineral veins is easier with OreHints!$(br2)Hint rocks generate in the world near mineral veins just like nuggets for metal ores. Coal and halite do not currently have working indicators.$(br)Find these rocks on the surface where they don\'t match, and in caves, and there\'s likely a mineral vein around! Underground indicators for every metal vein also spawn.'),
            text('$(bold){:_<12s}'.format('Ore') + '{:_>16s}'.format('Hint Rock$(br)')+'$()'+''.join([('$(l:the_world/ores_and_minerals#{0}){1:_<16s}$(){2:_>10s}').format(min, min.title(), PUB_INDICATORS[min].title())+'$(br)' for min in PUB_INDICATORS])))),
    ))

    book.build()

if __name__ == '__main__':
    main_with_args()

