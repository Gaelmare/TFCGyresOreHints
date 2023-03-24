import os
from argparse import ArgumentParser

from mcresources import ResourceManager, utils
from mcresources.type_definitions import ResourceIdentifier, JsonObject

from constants import MINERAL_INDICATORS
from patchouli import *
from i18n import I18n


class LocalInstance:
    INSTANCE_DIR = os.getenv('LOCAL_MINECRAFT_INSTANCE')  # The location of a local .minecraft directory, for testing in external minecraft instance (as hot reloading works much better)

    @staticmethod
    def wrap(rm: ResourceManager):
        def data(name_parts: ResourceIdentifier, data_in: JsonObject):
            return rm.write((LocalInstance.INSTANCE_DIR, '/'.join(utils.str_path(name_parts))), data_in)

        if LocalInstance.INSTANCE_DIR is not None:
            rm.data = data
            return rm
        return None

def main():
    rm = ResourceManager('tfcgyres_orehints', '../src')
    i18n = I18n.create('en_us')

    print('Writing book')
    make_book(rm, i18n)

    i18n.flush()

    if LocalInstance.wrap(rm):
        print('Copying into local instance at: %s' % LocalInstance.INSTANCE_DIR)
        make_book(rm, I18n.create('en_us'), local_instance=True)

    print('Done')

def make_book(rm: ResourceManager, i18n: I18n, local_instance: bool = False):
    rm.domain = 'tfcgyres_orehints'  # DOMAIN CHANGE
    book = Book(rm, 'field_guide', {}, i18n, local_instance, reverse_translate=False)

    book.category('tfcgyres_orehints', 'Ore Hints and Spawning', 'Mineral veins now have hint rocks like metal veins have small nuggets! Ore veins are better, especially at the bottom of the world.', 'tfc:metal/propick/steel', is_sorted=True, entries=(
        entry('orehints', 'Mineral Hints', 'tfc:ore/kaolinite', pages=(
            text('Finding TFC mineral veins is easier. Hint rocks now generate in the world above mineral veins just like small metal nuggets from metal ores.$(br)Look for these rocks on the surface where they don\'t belong, and there\'s likely a mineral vein beneath!'),
            text('$(bold){:_<12s}'.format('Ore') + '{:_>16s}'.format('Hint Rock$(br)') +'$()'+''.join([('{0:_<16s}{1:_>10s}').format(min, MINERAL_INDICATORS[min]).title()+'$(br)' for min in MINERAL_INDICATORS])),
            empty_last_page()
        )),
        entry('spawnbuffs', 'Ore Spawn Buffs', 'tfc:ore/graphite', pages=(
            text('Adding hint rocks required restating the TFC spawn data for mineral veins. Some of the veins were too small and too rare, so sizes, spawn chances, and some shapes changed!$(br)Coal veins are now much larger horizontal discs with fewer inclusions. Most other mineral veins are more common and doubled in size. Y-level restrictions are the same.'),
            text('Exploring the bottom of the world may be profitable! Deep veins (below y=-16) were added for all non-sedimentary ores: metal, mineral, and non-river gem. These veins may be also larger, denser, and purer.'),
            empty_last_page()
        )),
    ))

    book.build()



# Firmalife Pages

if __name__ == '__main__':
    main()

