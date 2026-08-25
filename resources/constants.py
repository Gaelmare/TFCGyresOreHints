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
    simple_blocks: bool = False


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
    rivers_only: bool
    montane: bool
    height: int
    radius: int
    deposits: bool
    indicator_rarity: int  # Above-ground indicators
    underground_rarity: int  # Underground indicators
    underground_count: int
    project: bool | None  # Project to surface
    project_offset: bool | None  # Project offset
    near_lava: bool | None
    simple_blocks: bool

    @staticmethod
    def new(
        ore: str,
        rarity: int,
        size: int,
        min_y: int,
        max_y: int,
        density: float,
        rocks: tuple[str, ...],
        rivers_only: bool = False,
        montane: bool = False,
        vein_type: str = 'cluster',
        grade: tuple[int, int, int] = (),
        height: int = 2,  # For disc type veins, `size` is the width
        radius: int = 5,  # For pipe type veins, `size` is the height
        deposits: bool = False,
        indicator: int = 12,  # Indicator rarity
        deep_indicator: tuple[int, int] = (1, 0),  # Pair of (rarity, count) for underground indicators
        project: str | bool = None,  # Projects to surface. Either True or 'offset'
        near_lava: bool | None = None,
        simple_blocks: bool = False,
    ):
        assert 0 < density < 1
        assert isinstance(rocks, tuple), 'Forgot the trailing comma in a single element tuple: %s' % repr(rocks)
        assert vein_type in ('cluster', 'disc', 'pipe')
        assert project is None or project is True or project == 'offset'

        underground_rarity, underground_count = deep_indicator
        return Vein(ore, 'tfc:%s_vein' % vein_type, rarity, size, min_y, max_y, density, grade, rocks, rivers_only, montane, height, radius, deposits, indicator, underground_rarity, underground_count, None if project is None else True, None if project != 'offset' else True, near_lava, simple_blocks)

    def config(self) -> dict[str, Any]:
        cfg = {
            'rarity': self.rarity,
            'density': self.density,
            'min_y': self.min_y,
            'max_y': self.max_y,
            'project': self.project,
            'project_offset': self.project_offset,
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

ROCKS: dict[str, Rock] = {
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
    'tuff': Rock('sedimentary', 'black'),
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

ORES: dict[str, Ore] = {
    'native_copper': Ore('copper', True, 'copper', 'copper', 'orange'),
    'native_gold': Ore('gold', True, 'copper', 'gold', 'yellow'),
    'hematite': Ore('cast_iron', True, 'copper', 'iron', 'red'),
    'native_silver': Ore('silver', True, 'copper', 'silver', 'light_gray'),
    'cassiterite': Ore('tin', True, 'copper', 'tin', 'gray'),
    'bismuthinite': Ore('bismuth', True, 'copper', 'bismuth', 'green'),
    'garnierite': Ore('nickel', True, 'copper', 'nickel', 'brown'),
    'malachite': Ore('copper', True, 'copper', 'copper', 'green'),
    'magnetite': Ore('cast_iron', True, 'copper', 'iron', 'gray'),
    'limonite': Ore('cast_iron', True, 'copper', 'iron', 'yellow'),
    'sphalerite': Ore('zinc', True, 'copper', 'zinc', 'gray'),
    'tetrahedrite': Ore('copper', True, 'copper', 'copper', 'gray'),
    'bituminous_coal': Ore(None, False, 'copper', 'coal', simple_blocks=True),
    'lignite': Ore(None, False, 'copper', 'coal', simple_blocks=True),
    'gypsum': Ore(None, False, 'copper', 'gypsum'),
    'graphite': Ore(None, False, 'copper', 'graphite'),
    'sulfur': Ore(None, False, 'copper', 'sulfur'),
    'cinnabar': Ore(None, False, 'copper', 'redstone'),
    'cryolite': Ore(None, False, 'copper', 'redstone'),
    'saltpeter': Ore(None, False, 'copper', 'saltpeter'),
    'sylvite': Ore(None, False, 'copper', 'sylvite'),
    'borax': Ore(None, False, 'copper', 'borax'),
    'halite': Ore(None, False, 'copper', 'halite', simple_blocks=True),
    'amethyst': Ore(None, False, 'copper', 'amethyst'),  # Mohs: 7
    'diamond': Ore(None, False, 'copper', 'diamond'),  # Mohs: 10
    'emerald': Ore(None, False, 'copper', 'emerald'),  # Mohs: 7.5-8
    'lapis_lazuli': Ore(None, False, 'copper', 'lapis'),  # Mohs: 5-6
    'opal': Ore(None, False, 'copper', 'opal'),  # Mohs: 5.5-6.5
    'pyrite': Ore(None, False, 'copper', 'pyrite'),
    'ruby': Ore(None, False, 'copper', 'ruby'),  # Mohs: 9
    'sapphire': Ore(None, False, 'copper', 'sapphire'),  # Mohs: 9
    'topaz': Ore(None, False, 'copper', 'topaz')  # Mohs: 8
}
ORE_GRADES = ('poor', 'normal', 'rich')

ALL_MINERALS = ('bituminous_coal', 'lignite', 'graphite', 'cinnabar', 'cryolite', 'saltpeter', 'sulfur', 'sylvite', 'borax', 'gypsum', 'lapis_lazuli', 'halite', 'diamond', 'emerald', 'sulfur', 'amethyst', 'opal', 'deep ruby')

MINERAL_INDICATORS: Dict[str, str] = {
    'bituminous_coal': 'basalt',
    'lignite': 'basalt',
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

POOR = 70, 25, 5  # = 1550
NORMAL = 35, 40, 25  # = 2400
RICH = 15, 25, 60  # = 2550

PUB_INDICATORS = MINERAL_INDICATORS.copy()
#1.21 config starts here

ORE_VEINS_NOHINTS: dict[str, Vein] = {
    # Added iron in mountains, much more common because terrain this high is rare
    # OH: TFC 1.21 added iron in mountains, but we change the grade to rich. These rarities are less common than OreHints 1.20, but more than vanilla 1.21
    'montane_hematite': Vein.new('hematite', 12, 20, 90, 250, 0.5, ('igneous_extrusive',), grade=RICH, indicator=24, montane=True),
    'montane_magnetite': Vein.new('magnetite', 25, 20, 90, 250, 0.5, ('sedimentary',), grade=RICH, indicator=24, montane=True),
    'montane_limonite': Vein.new('limonite', 25, 20, 90, 250, 0.5, ('sedimentary',), grade=RICH, indicator=24, montane=True),
    # OH: Rarity 2 here in vanilla was way too high
    'montane_cassiterite': Vein.new('cassiterite', 4, 15, 80, 300, 0.4, ('igneous_intrusive',), grade=NORMAL, deposits=True, montane=True),
}


ORE_VEINS: dict[str, Vein] = {
    # Copper
    # Native - only in IE, only surface and montane, and common to compensate for the y-level getting cut off.
    # Malachite + Tetrahedrite - Sed + MM, can spawn in larger deposits, hence more common. Tetrahedrite also spawns at high altitude MM
    # All copper have high indicator rarity because it's necessary early on
    # OH: These were retuned in vanilla 1.21, so not changing these weights yet.
    # 'surface_native_copper': Vein.new('native_copper', 36, 20, 40, 100, 0.25, ('igneous_extrusive',), grade=POOR, deposits=True, indicator=14),
    # 'surface_malachite': Vein.new('malachite', 48, 20, 40, 100, 0.25, ('marble', 'limestone', 'chalk', 'dolomite'), grade=POOR, indicator=14),

    # 'montane_native_copper': Vein.new('native_copper', 16, 20, 100, 300, 0.25, ('igneous_extrusive',), grade=POOR, deposits=True, indicator=14, montane=True),
    # 'montane_malachite': Vein.new('malachite', 11, 20, 40, 300, 0.25, ('marble', 'limestone', 'chalk', 'dolomite'), grade=POOR, indicator=14, montane=True),
    # 'montane_tetrahedrite': Vein.new('tetrahedrite', 3, 20, 90, 270, 0.25, ('metamorphic',), grade=POOR, indicator=8, montane=True),

    # 'normal_malachite': Vein.new('malachite', 45, 30, -30, 70, 0.5, ('marble', 'limestone', 'chalk', 'dolomite'), grade=NORMAL, indicator=25),
    # 'normal_tetrahedrite': Vein.new('tetrahedrite', 40, 30, -30, 70, 0.5, ('metamorphic',), grade=NORMAL, indicator=25),

    # Native Gold - IE and II at all y levels, larger deeper
    # OH: no change
    # 'normal_native_gold': Vein.new('native_gold', 90, 15, 0, 70, 0.25, ('igneous_extrusive', 'igneous_intrusive'), grade=NORMAL, indicator=40),
    # 'rich_native_gold': Vein.new('native_gold', 50, 40, -80, 20, 0.5, ('igneous_intrusive',), grade=RICH, indicator=0, deep_indicator=(1, 4)),

    # OH: No changes for troll veins!
    # In the same area as native gold deposits, pyrite veins - vast majority pyrite, but some native gold - basically troll veins
    #'fake_native_gold': Vein.new('pyrite', 16, 15, -50, 70, 0.35, ('igneous_extrusive', 'igneous_intrusive'), indicator=0),

    # Silver - black bronze (T2 with gold), or for black steel. Rare and small in uplift mountains via high II or plentiful near bottom of world
    # OH: no change
    # 'montane_native_silver': Vein.new('native_silver', 7, 10, 90, 280, 0.2, ('granite', 'diorite'), grade=POOR, montane=True),
    # 'normal_native_silver': Vein.new('native_silver', 25, 25, -80, 20, 0.6, ('granite', 'diorite', 'gneiss', 'schist'), grade=RICH, indicator=0, deep_indicator=(1, 9)),

    # Tin - bronze T2, rare situation (II uplift mountain) but common and rich.
    # OH: Decreased rarity because 2 was too much
    'montane_cassiterite': Vein.new('cassiterite', 4, 15, 80, 300, 0.4, ('igneous_intrusive',), grade=NORMAL, deposits=True, montane=True),

    # Bismuth - bronze T2 surface via Sed, deep and rich via II
    # OH: increase rarity!
    'surface_bismuthinite': Vein.new('bismuthinite', 64, 20, 40, 100, 0.3, ('sedimentary',), grade=POOR, indicator=14),
    'montane_bismuthinite': Vein.new('bismuthinite', 32, 20, 100, 220, 0.3, ('sedimentary',), grade=POOR, indicator=14, montane=True),
    # OH: no change
    # 'normal_bismuthinite': Vein.new('bismuthinite', 45, 40, -80, 20, 0.6, ('igneous_intrusive',), grade=RICH, indicator=0, deep_indicator=(1, 4)),

    # Zinc - bronze T2, requires different source from bismuth, surface via IE, or deep via II
    # OH: no change, don't add hint rocks
    # 'surface_sphalerite': Vein.new('sphalerite', 40, 20, 40, 100, 0.3, ('igneous_extrusive',), grade=POOR),
    # 'montane_sphalerite': Vein.new('sphalerite', 20, 20, 100, 220, 0.3, ('igneous_extrusive',), grade=POOR, montane=True),
    # 'normal_sphalerite': Vein.new('sphalerite', 45, 40, -80, 20, 0.6, ('igneous_intrusive',), grade=RICH, indicator=0, deep_indicator=(1, 5)),

    # Iron - all occur on surface or in mountains via IE and Sed. IE has one, Sed has two, so the two are higher rarity, we decrease the rarity of the IE one to compensate. All are small veins, but the Sed ones are more common and larger.
    # OH: decrease rarity of surface veins
    'surface_hematite': Vein.new('hematite', 35, 20, 10, 90, 0.4, ('igneous_extrusive',), grade=NORMAL, indicator=24),
    'surface_magnetite': Vein.new('magnetite', 70, 20, 10, 90, 0.4, ('sedimentary',), grade=NORMAL, indicator=24),
    'surface_limonite': Vein.new('limonite', 70, 20, 10, 90, 0.4, ('sedimentary',), grade=NORMAL, indicator=24),

    # OH: TFC 1.21 added iron in mountains, but we change the grade to rich and density to 0.5.  These rarities are less common than OreHints 1.20, but more than vanilla 1.21
    'montane_hematite': Vein.new('hematite', 12, 20, 90, 250, 0.5, ('igneous_extrusive',), grade=RICH, indicator=24, montane=True),
    'montane_magnetite': Vein.new('magnetite', 25, 20, 90, 250, 0.5, ('sedimentary',), grade=RICH, indicator=24, montane=True),
    'montane_limonite': Vein.new('limonite', 25, 20, 90, 250, 0.5, ('sedimentary',), grade=RICH, indicator=24, montane=True),

    # Nickel - only deep spawning II. Extra veins in gabbro, add deep indicators
    # OH: no change, although that's a lot of nickel nuggets!
    # 'normal_garnierite': Vein.new('garnierite', 25, 18, -80, 0, 0.3, ('igneous_intrusive',), grade=NORMAL),
    #'gabbro_garnierite': Vein.new('garnierite', 20, 30, -80, 0, 0.6, ('gabbro',), grade=RICH, indicator=0, deep_indicator=(1, 7)),

    # Graphite - for steel, found in low MM. Along with Kao, which is high altitude sed (via clay deposits)
    'graphite': Vein.new('graphite', 20, 20, -30, 60, 0.4, ('gneiss', 'marble', 'quartzite', 'schist')),

    # Coal, spawns roughly based on IRL grade (lignite -> bituminous -> anthracite), big flat discs
    # OH: increase rarity
    'lignite': Vein.new('lignite', 210, 40, -20, -8, 0.85, ('sedimentary',), vein_type='disc', height=2, project='offset', simple_blocks=True),
    'bituminous_coal': Vein.new('bituminous_coal', 250, 50, -35, -12, 0.9, ('sedimentary',), vein_type='disc', height=3, project='offset', simple_blocks=True),

    # Sulfur spawns near lava level in any low-level rock, common, but small veins, or in tuff near the surface
    'sulfur': Vein.new('sulfur', 4, 18, -64, -45, 0.25, ('igneous_intrusive', 'metamorphic'), vein_type='disc', height=5, near_lava=True),
    'tuff_sulfur': Vein.new('sulfur', 2, 18, 40, 200, 0.45, ('tuff',), vein_type='disc', height=4),

    # Redstone: Cryolite is deep II, cinnabar is deep MM or Uplift Mountains, both are common enough within these rocks but rare to find
    'cryolite': Vein.new('cryolite', 16, 18, -70, -10, 0.7, ('granite', 'diorite')),
    'normal_cinnabar': Vein.new('cinnabar', 14, 18, -70, 10, 0.6, ('quartzite', 'phyllite', 'gneiss', 'schist')),
    'montane_cinnabar': Vein.new('cinnabar', 14, 14, 120, 280, 0.6, ('quartzite', 'phyllite', 'gneiss', 'schist'), montane=True),

    # Misc minerals - all spawning in discs, mostly in sedimentary rock. Rare, but all will spawn together
    # Gypsum is decorative, so more common, and Borax is sad, so more common (but smaller)
    # Veins that spawn in all sedimentary are rarer than those that don't
    'saltpeter': Vein.new('saltpeter', 110, 35, 40, 100, 0.4, ('sedimentary',), vein_type='disc', height=5),
    'sylvite': Vein.new('sylvite', 60, 35, 40, 100, 0.35, ('shale', 'claystone', 'chert'), vein_type='disc', height=5),
    'borax': Vein.new('borax', 40, 23, 40, 100, 0.2, ('claystone', 'limestone', 'shale'), vein_type='disc', height=3),
    'gypsum': Vein.new('gypsum', 70, 25, 40, 100, 0.3, ('sedimentary',), vein_type='disc', height=5),
    'halite': Vein.new('halite', 110, 35, -45, -12, 0.85, ('sedimentary',), vein_type='disc', height=4, project='offset', simple_blocks=True),

    # Gems - these are all fairly specific but since we don't have a gameplay need for gems they can be a bit niche
    'lapis_lazuli': Vein.new('lapis_lazuli', 30, 30, -20, 80, 0.12, ('limestone', 'marble')),

    'diamond': Vein.new('diamond', 30, 60, -64, 100, 0.15, ('gabbro',), vein_type='pipe', radius=5),
    'emerald': Vein.new('emerald', 80, 60, -64, 100, 0.15, ('igneous_intrusive',), vein_type='pipe', radius=5),

    # OH: no change, no hint rocks for these
    # 'amethyst': Vein.new('amethyst', 25, 8, 40, 60, 0.2, ('sedimentary', 'metamorphic'), vein_type='disc', rivers_only=True, height=4),
    # 'opal': Vein.new('opal', 25, 8, 40, 60, 0.2, ('sedimentary', 'igneous_extrusive'), vein_type='disc', rivers_only=True, height=4),
    # 'deep_ruby': Vein.new('ruby', 80, 22, -70, -10, 0.2, ('marble',)),
}

SURPRISE_VEINS = {
    'surprise_diamond': Vein.new('diamond', 240, 60, -64, 100, 0.4, ('gabbro',), vein_type='pipe', radius=5),
    'surprise_emerald': Vein.new('emerald', 240, 60, -64, 100, 0.4, ('igneous_intrusive',), vein_type='pipe', radius=4),
}

# This is here because it's used all over, and it's easier to import with all constants
def lang(key: str, *args) -> str:
    return ((key % args) if len(args) > 0 else key).replace('_', ' ').replace('/', ' ').strip().title()


# This is here as it's used only once in a generic lang call by generate_resources.py
DEFAULT_LANG = {
    # Misc
    'tfc.field_guide.book_name': 'TerraFirmaCraft',
    'tfc.field_guide.book_landing_text': 'Welcome traveller! This book will be the source of all you need to know as you explore the world of TerraFirmaCraft (TFC).'
}


