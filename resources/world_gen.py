# Handles generation of all world gen objects

from typing import Union, get_args

from mcresources import ResourceManager, utils
from mcresources.type_definitions import ResourceIdentifier, JsonObject, Json, VerticalAnchor

from constants import *


def generate(rm: ResourceManager):
    # Biome Feature Tags
    # Biomes -> in_biome/<step>/<optional biome>
    # in_biome/ -> other tags in the form feature/<name>s
    # feature/ -> individual features

    # Tags: in_biome/
    placed_feature_118_hack(rm, 'in_biome/veins', *[
        *('tfc:vein/%s' % v for v in MINERAL_VEINS.keys()),
        *('tfc:vein/%s' % v for v in DEEP_MINERAL_VEINS.keys()),
        *('tfc:vein/%s' % v for v in HIGH_ORE_VEINS.keys()),
        *('tfc:vein/%s' % v for v in DEEP_ORE_VEINS.keys()),
        *('tfc:vein/%s' % v for v in SURPRISE_VEINS.keys()),
    ])

    # Ore Veins
    for vein_name, vein in MINERAL_VEINS.items():
        rocks = expand_rocks(vein.rocks, vein_name)
        vein_config = {
            'rarity': vein.rarity,
            'min_y': utils.vertical_anchor(vein.min_y, 'absolute'),
            'max_y': utils.vertical_anchor(vein.max_y, 'absolute'),
            'size': vein.size,
            'density': vein_density(vein.density),
            'blocks': [{
                'replace': ['tfc:rock/raw/%s' % rock],
                'with': mineral_ore_blocks(vein, rock)
            } for rock in rocks],
            'random_name': vein_name,
            'biomes': vein.biomes,
            'indicator': {
                'rarity': 12,
                'blocks': [{
                    'block': 'tfc:rock/loose/%s' % MINERAL_INDICATORS.get(vein.ore)
                }]
            }
        }
        if vein.type == 'pipe':
            vein_config['min_skew'] = 5
            vein_config['max_skew'] = 13
            vein_config['min_slant'] = 0
            vein_config['max_slant'] = 2
        if vein.type == 'disc':
            vein_config['height'] = vein.height
        configured_placed_feature(rm, ('vein', vein_name), 'tfc:%s_vein' % vein.type, vein_config)

    for vein_name, vein in DEEP_MINERAL_VEINS.items():
        rocks = expand_rocks(vein.rocks, vein_name)
        vein_config = {
            'rarity': vein.rarity,
            'min_y': utils.vertical_anchor(vein.min_y, 'absolute'),
            'max_y': utils.vertical_anchor(vein.max_y, 'absolute'),
            'size': vein.size,
            'density': vein_density(vein.density),
            'blocks': [{
                'replace': ['tfc:rock/raw/%s' % rock],
                'with': mineral_ore_blocks(vein, rock)
            } for rock in rocks],
            'random_name': vein_name,
            'biomes': vein.biomes,
        }
        if vein.type == 'pipe':
            vein_config['min_skew'] = 5
            vein_config['max_skew'] = 13
            vein_config['min_slant'] = 0
            vein_config['max_slant'] = 2
        if vein.type == 'disc':
            vein_config['height'] = vein.height
        configured_placed_feature(rm, ('vein', vein_name), 'tfc:%s_vein' % vein.type, vein_config)

    for vein_name, vein in HIGH_ORE_VEINS.items():
        rocks = expand_rocks(vein.rocks, vein_name)
        configured_placed_feature(rm, ('vein', vein_name), 'tfc:%s_vein' % vein.type, {
            'rarity': vein.rarity,
            'min_y': utils.vertical_anchor(vein.min_y, 'absolute'),
            'max_y': utils.vertical_anchor(vein.max_y, 'absolute'),
            'size': vein.size,
            'density': vein_density(vein.density),
            'blocks': [{
                'replace': ['tfc:rock/raw/%s' % rock],
                'with': vein_ore_blocks(vein, rock)
            } for rock in rocks],  # no indicator for deep veins!
            'random_name': vein_name,
            'biomes': vein.biomes,
            'indicator': {
                'rarity': 12,
                'blocks': [{
                    'block': 'tfc:ore/small_%s' % vein.ore
                }]
            }
        })

    for vein_name, vein in DEEP_ORE_VEINS.items():
        rocks = expand_rocks(vein.rocks, vein_name)
        configured_placed_feature(rm, ('vein', vein_name), 'tfc:%s_vein' % vein.type, {
            'rarity': vein.rarity,
            'min_y': utils.vertical_anchor(vein.min_y, 'absolute'),
            'max_y': utils.vertical_anchor(vein.max_y, 'absolute'),
            'size': vein.size,
            'density': vein_density(vein.density),
            'blocks': [{
                'replace': ['tfc:rock/raw/%s' % rock],
                'with': vein_ore_blocks(vein, rock)
            } for rock in rocks],  # no indicator for deep veins!
            'random_name': vein_name,
            'biomes': vein.biomes
        })

    for vein_name, vein in SURPRISE_VEINS.items():
        rocks = expand_rocks(vein.rocks, vein_name)
        configured_placed_feature(rm, ('vein', vein_name), 'tfc:%s_vein' % vein.type, {
            'rarity': vein.rarity,
            'min_y': utils.vertical_anchor(vein.min_y, 'absolute'),
            'max_y': utils.vertical_anchor(vein.max_y, 'absolute'),
            'size': vein.size,
            'density': vein_density(vein.density),
            'blocks': [{
                'replace': ['tfc:rock/raw/%s' % rock],
                'with': [{'weight': 90, 'block': 'tfc:ore/%s/%s' % (vein.ore, rock)},
                         {'weight': 10, 'block': 'minecraft:lava'}] #surprise! How difficult would infested TFC stone be?
            } for rock in rocks], #nod to CustomOreGen gem pipes
            'random_name': vein_name,
            'biomes': vein.biomes
        })


# Vein Helper Functions
def mineral_ore_blocks(vein: Vein, rock: str) -> List[Dict[str, Any]]:
    if vein.spoiler_ore is not None and rock in vein.spoiler_rocks:
        ore_blocks = [{'weight': 100, 'block': 'tfc:ore/%s/%s' % (vein.ore, rock)}]
        p = vein.spoiler_rarity * 0.01  # as a percentage of the overall vein
        ore_blocks.append({
            'weight': int(100 * p / (1 - p)),
            'block': 'tfc:ore/%s/%s' % (vein.spoiler_ore, rock)
        })
    else:
        ore_blocks = [{'block': 'tfc:ore/%s/%s' % (vein.ore, rock)}]
    return ore_blocks

def vein_ore_blocks(vein: Vein, rock: str) -> List[Dict[str, Any]]:
    ore_blocks = [{
        'weight': vein.poor,
        'block': 'tfc:ore/poor_%s/%s' % (vein.ore, rock)
    }, {
        'weight': vein.normal,
        'block': 'tfc:ore/normal_%s/%s' % (vein.ore, rock)
    }, {
        'weight': vein.rich,
        'block': 'tfc:ore/rich_%s/%s' % (vein.ore, rock)
    }]
    if vein.spoiler_ore is not None and rock in vein.spoiler_rocks:
        p = vein.spoiler_rarity * 0.01  # as a percentage of the overall vein
        ore_blocks.append({
            'weight': int(100 * p / (1 - p)),
            'block': 'tfc:ore/%s/%s' % (vein.spoiler_ore, rock)
        })
    elif vein.deposits:
        ore_blocks.append({
            'weight': 10,
            'block': 'tfc:deposit/%s/%s' % (vein.ore, rock)
        })
    return ore_blocks


def vein_density(density: int) -> float:
    assert 0 <= density <= 100, 'Invalid density: %s' % str(density)
    return round(density * 0.01, 2)


# Value Providers

def expand_rocks(rocks_list: List[str], path: Optional[str] = None) -> List[str]:
    rocks = []
    for rock_spec in rocks_list:
        if rock_spec in ROCKS:
            rocks.append(rock_spec)
        elif rock_spec in ROCK_CATEGORIES:
            rocks += [r for r, d in ROCKS.items() if d.category == rock_spec]
        else:
            raise RuntimeError('Unknown rock or rock category specification: %s at %s' % (rock_spec, path if path is not None else '??'))
    return rocks

def placed_feature_118_hack(rm, name_parts: ResourceIdentifier, *values: ResourceIdentifier):
    placed_feature_tag(rm, name_parts, *values)
    #configured_placed_feature(rm, name_parts, 'tfc:multiple', {'features': '#' + utils.resource_location(rm.domain, name_parts).join()})

def placed_feature_tag(rm: ResourceManager, name_parts: ResourceIdentifier, *values: ResourceIdentifier):
    return rm.tag(name_parts, 'worldgen/placed_feature', *values)

def configured_placed_feature(rm: ResourceManager, name_parts: ResourceIdentifier, feature: Optional[ResourceIdentifier] = None, config: JsonObject = None, *placements: Json):
    res = utils.resource_location(rm.domain, name_parts)
    if feature is None:
        feature = res
    rm.configured_feature(res, feature, config)
    rm.placed_feature(res, res, *placements)
