#  Work under Copyright. Licensed under the EUPL.
#  See the project README.md and LICENSE.txt for more information.

from typing import Dict, List, NamedTuple, Optional, Tuple, Any

class Rock(NamedTuple):
    category: str
    sand: str

class Ore(NamedTuple):
    metal: Optional[str]
    graded: bool
    required_tool: str
    tag: str
    dye_color: Optional[str] = None

class OreGrade(NamedTuple):
    grind_amount: int


class Vein(NamedTuple):
    ore: str  # The name of the ore (as found in ORES)
    vein_type: str  # Either 'cluster', 'pipe' or 'disc'
    rarity: int
    size: int
    min_y: int
    max_y: int
    density: float
    grade: tuple[int, int, int]  # (poor, normal, rich) weights
    rocks: tuple[str, ...]  # Rock, or rock categories
    biomes: str | None
    height: int
    radius: int
    deposits: bool
    indicator_rarity: int  # Above-ground indicators
    underground_rarity: int  # Underground indicators
    underground_count: int
    project: bool | None  # Project to surface
    project_offset: bool | None  # Project offset
    near_lava: bool | None


    @staticmethod
    def new(
            ore: str,
            rarity: int,
            size: int,
            min_y: int,
            max_y: int,
            density: float,
            rocks: tuple[str, ...],

            vein_type: str = 'cluster',
            grade: tuple[int, int, int] = (),
            biomes: str = None,
            height: int = 2,  # For disc type veins, `size` is the width
            radius: int = 5,  # For pipe type veins, `size` is the height
            deposits: bool = False,
            indicator: int = 12,  # Indicator rarity
            deep_indicator: tuple[int, int] = (1, 3),  # Pair of (rarity, count) for underground indicators
            project: str | bool = None,  # Projects to surface. Either True or 'offset'
            near_lava: bool | None = None,
    ):
        assert 0 < density < 1
        assert isinstance(rocks, tuple), 'Forgot the trailing comma in a single element tuple: %s' % repr(rocks)
        assert vein_type in ('cluster', 'disc', 'pipe')
        assert project is None or project is True or project == 'offset'

        underground_rarity, underground_count = deep_indicator
        return Vein(ore, 'tfc:%s_vein' % vein_type, rarity, size, min_y, max_y, density, grade, rocks, biomes, height, radius, deposits, indicator, underground_rarity, underground_count, None if project is None else True, None if project != 'offset' else True, near_lava)


    def config(self) -> dict[str, Any]:
        cfg = {
            'rarity': self.rarity,
            'density': self.density,
            'min_y': self.min_y,
            'max_y': self.max_y,
            'project': self.project,
            'project_offset': self.project_offset,
            'biomes': self.biomes,
            'near_lava': self.near_lava,
        }
        if self.vein_type == 'tfc:cluster_vein':
            cfg.update(size=self.size)
        elif self.vein_type == 'tfc:pipe_vein':
            cfg.update(min_skew=5, max_skew=13, min_slant=0, max_slant=2, sign=0, height=self.size, radius=self.radius)
        else:
            cfg.update(size=self.size, height=self.height)
        return cfg



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
    'dacite': Rock('igneous_extrusive', 'yellow'),
    'quartzite': Rock('metamorphic', 'white'),
    'slate': Rock('metamorphic', 'yellow'),
    'phyllite': Rock('metamorphic', 'brown'),
    'schist': Rock('metamorphic', 'green'),
    'gneiss': Rock('metamorphic', 'green'),
    'marble': Rock('metamorphic', 'yellow')
}

ORES: Dict[str, Ore] = {
    'native_copper': Ore('copper', True, 'copper', 'copper', 'orange'),
    'native_gold': Ore('gold', True, 'copper', 'gold'),
    'hematite': Ore('cast_iron', True, 'copper', 'iron', 'red'),
    'native_silver': Ore('silver', True, 'copper', 'silver', 'light_gray'),
    'cassiterite': Ore('tin', True, 'copper', 'tin', 'gray'),
    'bismuthinite': Ore('bismuth', True, 'copper', 'bismuth', 'green'),
    'garnierite': Ore('nickel', True, 'bronze', 'nickel', 'brown'),
    'malachite': Ore('copper', True, 'copper', 'copper', 'green'),
    'magnetite': Ore('cast_iron', True, 'copper', 'iron', 'gray'),
    'limonite': Ore('cast_iron', True, 'copper', 'iron', 'yellow'),
    'sphalerite': Ore('zinc', True, 'copper', 'zinc', 'gray'),
    'tetrahedrite': Ore('copper', True, 'copper', 'copper', 'gray'),
    'bituminous_coal': Ore(None, False, 'copper', 'coal'),
    'lignite': Ore(None, False, 'copper', 'coal'),
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
    'normal': OreGrade(5),
    'poor': OreGrade(3),
    'rich': OreGrade(7)
}

MINERAL_INDICATORS: Dict[str, str] = {
    'bituminous_coal': 'basalt',
    'lignite': 'basalt',
    'kaolin_disc': 'marble',
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
    'diamond': 'chalk',
}
#make kaolinite match TFC anchor entry
PUB_INDICATORS = MINERAL_INDICATORS.copy()
PUB_INDICATORS['kaolinite'] = PUB_INDICATORS['kaolin_disc']

del PUB_INDICATORS['kaolin_disc']


DEFAULT_FORGE_ORE_TAGS: Tuple[str, ...] = ('coal', 'diamond', 'emerald', 'gold', 'iron', 'lapis', 'netherite_scrap', 'quartz', 'redstone')

POOR = 70, 25, 5  # = 1550
NORMAL = 35, 40, 25  # = 2400
RICH = 15, 25, 60  # = 2550

def vein(ore: str, vein_type: str, rarity: int, size: int, min_y: int, max_y: int, density: int, poor: float, normal: float, rich: float, rocks: List[str], spoiler_ore: Optional[str] = None, spoiler_rarity: int = 0, spoiler_rocks: List[str] = None, biomes: str = None, height: int = 2, deposits: bool = False):
    # Factory method to allow default values
    return Vein(ore, vein_type, rarity, size, min_y, max_y, density, poor, normal, rich, rocks, spoiler_ore, spoiler_rarity, spoiler_rocks, biomes, height, deposits)


def preset_vein(ore: str, vein_type: str, rocks: List[str], spoiler_ore: Optional[str] = None, spoiler_rarity: int = 0, spoiler_rocks: List[str] = None,
                biomes: str = None, height: int = 2, preset: Tuple[int, int, int, int, int, int, int, int] = None, deposits: bool = False):
    assert preset is not None
    return Vein(ore, vein_type, preset[0], preset[1], preset[2], preset[3], preset[4], preset[5], preset[6], preset[7], rocks, spoiler_ore, spoiler_rarity, spoiler_rocks, biomes, height, deposits)

#1.20 config starts here

ORE_VEINS: dict[str, Vein] = {
    # Copper
    # Native - only in IE, only surface, and common to compensate for the y-level getting cut off.
    # Malachite + Tetrahedrite - Sed + MM, can spawn in larger deposits, hence more common. Tetrahedrite also spawns at high altitude MM
    # All copper have high indicator rarity because it's necessary early on
    'surface_native_copper': Vein.new('native_copper', 24, 20, 40, 130, 0.25, ('igneous_extrusive',), grade=POOR, deposits=True, indicator=14),
    'surface_malachite': Vein.new('malachite', 32, 20, 40, 130, 0.25, ('marble', 'limestone', 'chalk', 'dolomite'), grade=POOR, indicator=14),
    'surface_tetrahedrite': Vein.new('tetrahedrite', 7, 20, 90, 170, 0.25, ('metamorphic',), grade=POOR, indicator=8),

    'normal_malachite': Vein.new('malachite', 45, 30, -30, 70, 0.5, ('marble', 'limestone', 'chalk', 'dolomite'), grade=NORMAL, indicator=25),
    'normal_tetrahedrite': Vein.new('tetrahedrite', 40, 30, -30, 70, 0.5, ('metamorphic',), grade=NORMAL, indicator=25),

    # Native Gold - IE and II at all y levels, larger deeper
    'normal_native_gold': Vein.new('native_gold', 90, 15, 0, 70, 0.25, ('igneous_extrusive', 'igneous_intrusive'), grade=NORMAL, indicator=40),
    # no change
    # 'rich_native_gold': Vein.new('native_gold', 50, 40, -80, 20, 0.5, ('igneous_intrusive',), grade=RICH, indicator=0, deep_indicator=(1, 4)),

    # No changes for troll veins!
    # In the same area as native gold deposits, pyrite veins - vast majority pyrite, but some native gold - basically troll veins
    #'fake_native_gold': Vein.new('pyrite', 16, 15, -50, 70, 0.35, ('igneous_extrusive', 'igneous_intrusive'), indicator=0),

    # Silver - black bronze (T2 with gold), or for black steel. Rare and small in uplift mountains via high II or plentiful near bottom of world
    'surface_native_silver': Vein.new('native_silver', 15, 10, 90, 180, 0.2, ('granite', 'diorite'), grade=POOR),
    # no change
    # 'normal_native_silver': Vein.new('native_silver', 25, 25, -80, 20, 0.6, ('granite', 'diorite', 'gneiss', 'schist'), grade=RICH, indicator=0, deep_indicator=(1, 9)),

    # Tin - bronze T2, rare situation (II uplift mountain) but common and rich.
    'surface_cassiterite': Vein.new('cassiterite', 5, 15, 80, 180, 0.4, ('igneous_intrusive',), grade=NORMAL, deposits=True),

    # Bismuth - bronze T2 surface via Sed, deep and rich via II
    'surface_bismuthinite': Vein.new('bismuthinite', 32, 20, 40, 130, 0.3, ('sedimentary',), grade=POOR, indicator=14),
    # no change
    # 'normal_bismuthinite': Vein.new('bismuthinite', 45, 40, -80, 20, 0.6, ('igneous_intrusive',), grade=RICH, indicator=0, deep_indicator=(1, 4)),

    # Zinc - bronze T2, requires different source from bismuth, surface via IE, or deep via II
    'surface_sphalerite': Vein.new('sphalerite', 30, 20, 40, 130, 0.3, ('igneous_extrusive',), grade=POOR),
    # no change
    # 'normal_sphalerite': Vein.new('sphalerite', 45, 40, -80, 20, 0.6, ('igneous_intrusive',), grade=RICH, indicator=0, deep_indicator=(1, 5)),

    # Iron - both surface via IE and Sed. IE has one, Sed has two, so the two are higher rarity
    'surface_hematite': Vein.new('hematite', 35, 20, 10, 90, 0.4, ('igneous_extrusive',), grade=NORMAL, indicator=24),
    'surface_magnetite': Vein.new('magnetite', 70, 20, 10, 90, 0.4, ('sedimentary',), grade=NORMAL, indicator=24),
    'surface_limonite': Vein.new('limonite', 70, 20, 10, 90, 0.4, ('sedimentary',), grade=NORMAL, indicator=24),

    # Added iron in mountains, much more common because terrain this high is rare
    'mountain_hematite': Vein.new('hematite', 10, 20, 90, 180, 0.5, ('igneous_extrusive',), grade=RICH, indicator=12),
    'mountain_magnetite': Vein.new('magnetite', 20, 20, 90, 180, 0.5, ('sedimentary',), grade=RICH, indicator=12),
    'mountain_limonite': Vein.new('limonite', 20, 20, 90, 180, 0.5, ('sedimentary',), grade=RICH, indicator=12),

    # Nickel - only deep spawning II. Extra veins in gabbro
    'normal_garnierite': Vein.new('garnierite', 25, 18, -80, 0, 0.3, ('igneous_intrusive',), grade=NORMAL),
    # no change, although that's a lot of nickel nuggets!
    #'gabbro_garnierite': Vein.new('garnierite', 20, 30, -80, 0, 0.6, ('gabbro',), grade=RICH, indicator=0, deep_indicator=(1, 7)),

    # Graphite - for steel, found in low MM. Along with Kao, which is high altitude sed (via clay deposits)
    'graphite': Vein.new('graphite', 20, 20, -30, 60, 0.4, ('gneiss', 'marble', 'quartzite', 'schist')),

    # Coal, spawns roughly based on IRL grade (lignite -> bituminous -> anthracite), big flat discs
    'lignite': Vein.new('lignite', 160, 40, -20, -8, 0.85, ('sedimentary',), vein_type='disc', height=2, project='offset'),
    'bituminous_coal': Vein.new('bituminous_coal', 210, 50, -35, -12, 0.9, ('sedimentary',), vein_type='disc', height=3, project='offset'),

    # Sulfur spawns near lava level in any low-level rock, common, but small veins
    'sulfur': Vein.new('sulfur', 4, 18, -64, -45, 0.25, ('igneous_intrusive', 'metamorphic'), vein_type='disc', height=5, near_lava=True),

    # Redstone: Cryolite is deep II, cinnabar is deep MM, both are common enough within these rocks but rare to find
    'cryolite': Vein.new('cryolite', 16, 18, -70, -10, 0.7, ('granite', 'diorite')),
    'cinnabar': Vein.new('cinnabar', 14, 18, -70, 10, 0.6, ('quartzite', 'phyllite', 'gneiss', 'schist')),

    # Misc minerals - all spawning in discs, mostly in sedimentary rock. Rare, but all will spawn together
    # Gypsum is decorative, so more common, and Borax is sad, so more common (but smaller)
    # Veins that spawn in all sedimentary are rarer than those that don't
    'saltpeter': Vein.new('saltpeter', 110, 35, 40, 100, 0.4, ('sedimentary',), vein_type='disc', height=5),
    'sylvite': Vein.new('sylvite', 60, 35, 40, 100, 0.35, ('shale', 'claystone', 'chert'), vein_type='disc', height=5),
    'borax': Vein.new('borax', 40, 23, 40, 100, 0.2, ('claystone', 'limestone', 'shale'), vein_type='disc', height=3),
    'gypsum': Vein.new('gypsum', 70, 25, 40, 100, 0.3, ('sedimentary',), vein_type='disc', height=5),
    'halite': Vein.new('halite', 110, 35, -45, -12, 0.85, ('sedimentary',), vein_type='disc', height=4, project='offset'),

    # Gems - these are all fairly specific but since we don't have a gameplay need for gems they can be a bit niche
    'lapis_lazuli': Vein.new('lapis_lazuli', 30, 30, -20, 80, 0.12, ('limestone', 'marble')),

    'diamond': Vein.new('diamond', 30, 60, -64, 100, 0.15, ('gabbro',), vein_type='pipe', radius=5),
    'emerald': Vein.new('emerald', 80, 60, -64, 100, 0.15, ('igneous_intrusive',), vein_type='pipe', radius=5),

    # No indicators, gem veins in rivers are relatively easy to find
    #'amethyst': Vein.new('amethyst', 25, 8, 40, 60, 0.2, ('sedimentary', 'metamorphic'), vein_type='disc', biomes='#tfc:is_river', height=4),
    #'opal': Vein.new('opal', 25, 8, 40, 60, 0.2, ('sedimentary', 'igneous_extrusive'), vein_type='disc', biomes='#tfc:is_river', height=4),

}


SURPRISE_VEINS = {
    'surprise_diamond': Vein.new('diamond', 240, 60, -64, 100, .4, ('gabbro',), vein_type='pipe', radius=5),
    'surprise_emerald': Vein.new('emerald', 240, 60, -64, 100, .4, ('igneous_intrusive',), vein_type='pipe', radius=4),
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


