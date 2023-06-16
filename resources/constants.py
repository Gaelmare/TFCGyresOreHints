#  Work under Copyright. Licensed under the EUPL.
#  See the project README.md and LICENSE.txt for more information.

from typing import Dict, List, Set, NamedTuple, Sequence, Optional, Literal, Tuple, Any

class Rock(NamedTuple):
    category: str
    sand: str

class Ore(NamedTuple):
    metal: Optional[str]
    graded: bool
    required_tool: str
    tag: str

class OreGrade(NamedTuple):
    weight: int
    grind_amount: int

class Vein(NamedTuple):
    ore: str
    type: str
    rarity: int
    size: int
    min_y: int
    max_y: int
    density: int
    poor: float
    normal: float
    rich: float
    rocks: List[str]
    spoiler_ore: str
    spoiler_rarity: int
    spoiler_rocks: List[str]
    biomes: Optional[str]
    height: Optional[int]
    deposits: bool


ROCK_CATEGORIES = ('sedimentary', 'metamorphic', 'igneous_extrusive', 'igneous_intrusive')
ROCK_CATEGORY_ITEMS = ('axe', 'hammer', 'hoe', 'javelin', 'knife', 'shovel')

ROCKS: Dict[str, Rock] = {
    'granite': Rock('igneous_intrusive', 'white'),
    'diorite': Rock('igneous_intrusive', 'white'),
    'gabbro': Rock('igneous_intrusive', 'black'),
    'shale': Rock('sedimentary', 'black'),
    'claystone': Rock('sedimentary', 'brown'),
    'limestone': Rock('sedimentary', 'white'),
    'conglomerate': Rock('sedimentary', 'green'),
    'dolomite': Rock('sedimentary', 'black'),
    'chert': Rock('sedimentary', 'yellow'),
    'chalk': Rock('sedimentary', 'white'),
    'rhyolite': Rock('igneous_extrusive', 'red'),
    'basalt': Rock('igneous_extrusive', 'red'),
    'andesite': Rock('igneous_extrusive', 'red'),
    'dacite': Rock('igneous_extrusive', 'red'),
    'quartzite': Rock('metamorphic', 'white'),
    'slate': Rock('metamorphic', 'brown'),
    'phyllite': Rock('metamorphic', 'brown'),
    'schist': Rock('metamorphic', 'green'),
    'gneiss': Rock('metamorphic', 'green'),
    'marble': Rock('metamorphic', 'yellow')
}

ORES: Dict[str, Ore] = {
    'native_copper': Ore('copper', True, 'copper', 'copper'),
    'native_gold': Ore('gold', True, 'copper', 'gold'),
    'hematite': Ore('cast_iron', True, 'copper', 'iron'),
    'native_silver': Ore('silver', True, 'copper', 'silver'),
    'cassiterite': Ore('tin', True, 'copper', 'tin'),
    'bismuthinite': Ore('bismuth', True, 'copper', 'bismuth'),
    'garnierite': Ore('nickel', True, 'bronze', 'nickel'),
    'malachite': Ore('copper', True, 'copper', 'copper'),
    'magnetite': Ore('cast_iron', True, 'copper', 'iron'),
    'limonite': Ore('cast_iron', True, 'copper', 'iron'),
    'sphalerite': Ore('zinc', True, 'copper', 'zinc'),
    'tetrahedrite': Ore('copper', True, 'copper', 'copper'),
    'bituminous_coal': Ore(None, False, 'copper', 'coal'),
    'lignite': Ore(None, False, 'copper', 'coal'),
    'kaolinite': Ore(None, False, 'copper', 'kaolinite'),
    'gypsum': Ore(None, False, 'copper', 'gypsum'),
    'graphite': Ore(None, False, 'copper', 'graphite'),
    'sulfur': Ore(None, False, 'copper', 'sulfur'),
    'cinnabar': Ore(None, False, 'bronze', 'redstone'),
    'cryolite': Ore(None, False, 'bronze', 'redstone'),
    'saltpeter': Ore(None, False, 'copper', 'saltpeter'),
    'sylvite': Ore(None, False, 'copper', 'sylvite'),
    'borax': Ore(None, False, 'copper', 'borax'),
    'halite': Ore(None, False, 'bronze', 'halite'),
    'amethyst': Ore(None, False, 'steel', 'amethyst'),  # Mohs: 7
    'diamond': Ore(None, False, 'black_steel', 'diamond'),  # Mohs: 10
    'emerald': Ore(None, False, 'steel', 'emerald'),  # Mohs: 7.5-8
    'lapis_lazuli': Ore(None, False, 'wrought_iron', 'lapis'),  # Mohs: 5-6
    'opal': Ore(None, False, 'wrought_iron', 'opal'),  # Mohs: 5.5-6.5
    'pyrite': Ore(None, False, 'copper', 'pyrite'),
    'ruby': Ore(None, False, 'black_steel', 'ruby'),  # Mohs: 9
    'sapphire': Ore(None, False, 'black_steel', 'sapphire'),  # Mohs: 9
    'topaz': Ore(None, False, 'steel', 'topaz')  # Mohs: 8
}
ORE_GRADES: Dict[str, OreGrade] = {
    'normal': OreGrade(50, 5),
    'poor': OreGrade(30, 3),
    'rich': OreGrade(20, 7)
}

MINERAL_INDICATORS: Dict[str, str] = {
    'bituminous_coal': 'basalt',
    'lignite': 'basalt',
    'kaolinite': 'marble',
    'graphite': 'claystone',
    'cinnabar': 'gneiss',
    'cryolite': 'slate',
    'saltpeter': 'diorite',
    'sulfur': 'shale',
    'sylvite': 'dolomite',
    'borax': 'chert',
    'lapis_lazuli': 'andesite',
    'gypsum': 'quartzite',
    'halite': 'phyllite',
    'diamond': 'chalk'
}

def vein(ore: str, vein_type: str, rarity: int, size: int, min_y: int, max_y: int, density: int, poor: float, normal: float, rich: float, rocks: List[str], spoiler_ore: Optional[str] = None, spoiler_rarity: int = 0, spoiler_rocks: List[str] = None, biomes: str = None, height: int = 2, deposits: bool = False):
    # Factory method to allow default values
    return Vein(ore, vein_type, rarity, size, min_y, max_y, density, poor, normal, rich, rocks, spoiler_ore, spoiler_rarity, spoiler_rocks, biomes, height, deposits)


def preset_vein(ore: str, vein_type: str, rocks: List[str], spoiler_ore: Optional[str] = None, spoiler_rarity: int = 0, spoiler_rocks: List[str] = None,
                biomes: str = None, height: int = 2, preset: Tuple[int, int, int, int, int, int, int, int] = None, deposits: bool = False):
    assert preset is not None
    return Vein(ore, vein_type, preset[0], preset[1], preset[2], preset[3], preset[4], preset[5], preset[6], preset[7], rocks, spoiler_ore, spoiler_rarity, spoiler_rocks, biomes, height, deposits)


# Default parameters for common ore veins
# rarity, size, min_y, max_y, density, poor, normal, rich
REALLY_DEEP_METAL_ORE = (100, 30, -94, -16, 80, 5, 20, 75)
HIGH_METAL_ORE = (15, 15, 120, 210, 80, 10, 30, 60)
# TFC defaults for comparison:
# POOR_METAL_ORE = (80, 15, 0, 100, 40, 40, 30, 10)
# NORMAL_METAL_ORE = (60, 20, -32, 75, 60, 20, 50, 30)
# DEEP_METAL_ORE = (100, 30, -64, 30, 70, 10, 30, 60)

REALLY_DEEP_MINERAL_ORE = (100, 30, -80, -16, 80, 0, 0, 0)
DEEP_MINERAL_ORE = (60, 15, -48, 100, 60, 0, 0, 0)
HIGH_MINERAL_ORE = (60, 15, 0, 210, 60, 0, 0, 0)
REALLY_HIGH_MINERAL_ORE = (15, 15, 120, 210, 80, 0, 0, 0)
# TFC defaults for comparison:
# DEEP_MINERAL_ORE = (90, 10, -48, 100, 60, 0, 0, 0)
# HIGH_MINERAL_ORE = (90, 10, 0, 210, 60, 0, 0, 0)

# Coal seams are almost homogenous and huge, but still rarer
DEEP_COAL_ORE = (90, 25, -48, 100, 90, 0, 0, 0)
HIGH_COAL_ORE = (90, 25, 0, 210, 90, 0, 0, 0)

HIGH_ORE_VEINS: Dict[str, Vein] = {
    'high_hematite': preset_vein('hematite', 'cluster', ['igneous_extrusive'], preset=HIGH_METAL_ORE),
    'high_native_copper': preset_vein('native_copper', 'cluster', ['igneous_extrusive'], preset=HIGH_METAL_ORE),
    'high_magnetite': preset_vein('magnetite', 'cluster', ['sedimentary'], preset=HIGH_METAL_ORE),
    'high_limonite': preset_vein('limonite', 'cluster', ['sedimentary'], 'ruby', 20, ['limestone', 'shale'], preset=HIGH_METAL_ORE),
}

#dropped all sedimentary only veins here, since they'll never spawn in the bottom layer
DEEP_ORE_VEINS: Dict[str, Vein] = {
    'really_deep_gold': preset_vein('native_gold', 'cluster', ['igneous_intrusive'], 'pyrite', 20, ['igneous_intrusive'], preset=REALLY_DEEP_METAL_ORE),
    'really_deep_silver': preset_vein('native_silver', 'cluster', ['granite', 'gneiss'], preset=REALLY_DEEP_METAL_ORE),
    'really_deep_cassiterite': preset_vein('cassiterite', 'cluster', ['igneous_intrusive'], 'topaz', 10, ['granite'], preset=REALLY_DEEP_METAL_ORE),
    'really_deep_bismuthinite': preset_vein('bismuthinite', 'cluster', ['igneous_intrusive'], preset=REALLY_DEEP_METAL_ORE),
    'really_deep_garnierite': preset_vein('garnierite', 'cluster', ['gabbro'], preset=REALLY_DEEP_METAL_ORE),
    'really_deep_malachite': preset_vein('malachite', 'cluster', ['marble'], preset=REALLY_DEEP_METAL_ORE),
    'really_deep_sphalerite': preset_vein('sphalerite', 'cluster', ['metamorphic'], preset=REALLY_DEEP_METAL_ORE),
    'really_deep_tetrahedrite': preset_vein('tetrahedrite', 'cluster', ['metamorphic'], preset=REALLY_DEEP_METAL_ORE),
}

#spawn rates tweaked or not, these are here for indicator rock settings
MINERAL_VEINS: Dict[str, Vein] = {
    'high_sulfur': preset_vein('sulfur', 'cluster', ['igneous_extrusive'], 'gypsum', 20, ['rhyolite'], preset=REALLY_HIGH_MINERAL_ORE),
    'bituminous_coal': preset_vein('bituminous_coal', 'disc', ['sedimentary'], preset=DEEP_COAL_ORE, height=3),
    'lignite': preset_vein('lignite', 'disc', ['sedimentary'], preset=HIGH_COAL_ORE, height=3),
    'kaolinite': preset_vein('kaolinite', 'cluster', ['sedimentary'], preset=HIGH_MINERAL_ORE),
    'graphite': preset_vein('graphite', 'cluster', ['gneiss', 'marble', 'quartzite', 'schist'], preset=DEEP_MINERAL_ORE),
    'cinnabar': preset_vein('cinnabar', 'cluster', ['igneous_extrusive', 'quartzite', 'shale'], 'opal', 10, ['quartzite'], preset=DEEP_MINERAL_ORE),
    'cryolite': preset_vein('cryolite', 'cluster', ['granite'], preset=DEEP_MINERAL_ORE),
    'saltpeter': preset_vein('saltpeter', 'cluster', ['sedimentary'], 'gypsum', 10, ['limestone'], preset=DEEP_MINERAL_ORE),
    'sulfur': preset_vein('sulfur', 'cluster', ['igneous_extrusive'], 'gypsum', 20, ['rhyolite'], preset=HIGH_MINERAL_ORE),
    'sylvite': preset_vein('sylvite', 'cluster', ['shale', 'claystone', 'chert'], preset=HIGH_MINERAL_ORE),
    'borax': preset_vein('borax', 'cluster', ['claystone', 'limestone', 'shale'], preset=HIGH_MINERAL_ORE),
    'gypsum': vein('gypsum', 'disc', 120, 20, 30, 90, 60, 0, 0, 0, ['metamorphic']),
    'lapis_lazuli': preset_vein('lapis_lazuli', 'cluster', ['limestone', 'marble'], preset=DEEP_MINERAL_ORE),
    'halite': vein('halite', 'disc', 120, 30, 30, 90, 80, 0, 0, 0, ['sedimentary']),
    'diamond': vein('diamond', 'pipe', 60, 60, -64, 100, 40, 0, 0, 0, ['gabbro'], 'graphite', 10, ['gabbro']),
    'volcanic_sulfur': vein('sulfur', 'disc', 10, 15, 80, 180, 80, 0, 0, 0, ['igneous_extrusive', 'igneous_intrusive'], biomes='#tfc:is_volcanic', height=6),
}

DEEP_MINERAL_VEINS = {
    'deep_graphite': preset_vein('graphite', 'cluster', ['gneiss', 'marble', 'quartzite', 'schist'], preset=REALLY_DEEP_MINERAL_ORE),
    'deep_cinnabar': preset_vein('cinnabar', 'cluster', ['quartzite'], 'opal', 10, ['quartzite'], preset=REALLY_DEEP_MINERAL_ORE),
    'deep_cryolite': preset_vein('cryolite', 'cluster', ['granite'], preset=REALLY_DEEP_MINERAL_ORE),
    'deep_lapis_lazuli': preset_vein('lapis_lazuli', 'cluster', ['marble'], preset=REALLY_DEEP_MINERAL_ORE),
    'deep_diamond': vein('diamond', 'pipe', 60, 60, -64, 0, 60, 0, 0, 0, ['gabbro'], 'graphite', 10, ['gabbro']),
    'deep_emerald': vein('emerald', 'pipe', 80, 60, -64, 0, 60, 0, 0, 0, ['igneous_intrusive']),
}

SURPRISE_VEINS = {
    'surprise_diamond': vein('diamond', 'pipe', 240, 60, -64, 100, 60, 0, 0, 0, ['gabbro']),
    'surprise_emerald': vein('emerald', 'pipe', 240, 60, -64, 100, 60, 0, 0, 0, ['igneous_intrusive']),
}


# This is here because it's used all over, and it's easier to import with all constants
def lang(key: str, *args) -> str:
    return ((key % args) if len(args) > 0 else key).replace('_', ' ').replace('/', ' ').title()


# This is here as it's used only once in a generic lang call by generate_resources.py
DEFAULT_LANG = {
    # Misc
    'tfc.field_guide.book_name': 'TerraFirmaCraft',
    'tfc.field_guide.book_landing_text': 'Welcome traveller! This book will be the source of all you need to know as you explore the world of TerraFirmaCraft (TFC).'
}


