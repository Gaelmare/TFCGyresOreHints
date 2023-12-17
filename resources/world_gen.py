# Handles generation of all world gen objects

from typing import Union, get_args

from mcresources import ResourceManager, utils
from mcresources.type_definitions import ResourceIdentifier, JsonObject, Json, VerticalAnchor

from constants import *


def generate(rm: ResourceManager, HINT_GEN=True):
    #add indicators to kaolinite
    configured_placed_feature(rm, ('vein', 'kaolin_disc'), 'tfc:kaolin_disc_vein', {
        'rarity': 40,
        'min_y': 75,
        'max_y': 110,
        'size': 18,
        'height': 6,
        'density': 1.0,
        'random_name': 'kaolin',
        'biomes': '#tfc:kaolin_clay_spawns_in',
        'blocks': [],
        'indicator': {
            'rarity': 12,
            'depth': 5,
            'underground_rarity': 1,
            'underground_count': 3,
            'blocks': [{
                'block': 'tfc:rock/loose/%s' % MINERAL_INDICATORS.get('kaolin_disc')
            }]
        }
    }, decorate_climate(min_rain=300, min_temp=18))

    # Ore Veins
    for vein_name, vein in ORE_VEINS.items():
        rocks = expand_rocks(vein.rocks)
        ore = ORES[vein.ore]  # standard ore
        if ore.graded:  # graded ore vein
            configured_placed_feature(rm, ('vein', vein_name), vein.vein_type, {
                **vein.config(),
                'random_name': vein_name,
                'blocks': [{
                    'replace': ['tfc:rock/raw/%s' % rock],
                    'with': vein_ore_blocks(vein, rock)
                } for rock in rocks],
                'indicator': {
                    'rarity': vein.indicator_rarity,
                    'depth': 35,
                    'underground_rarity': vein.underground_rarity,
                    'underground_count': vein.underground_count,
                    'blocks': [{
                        'block': 'tfc:ore/small_%s' % vein.ore
                    }]
                },
            })
        else:  # non-graded ore vein (mineral)
            vein_config = {
                **vein.config(),
                'random_name': vein_name,
                'blocks': [{
                    'replace': ['tfc:rock/raw/%s' % rock],
                    'with': mineral_ore_blocks(vein, rock)
                } for rock in rocks],
            }
            if HINT_GEN and MINERAL_INDICATORS.get(vein.ore):
                vein_config['indicator'] = {
                    'rarity': 12,
                    'depth': 35,
                    'underground_rarity': vein.underground_rarity,
                    'underground_count': vein.underground_count,
                    'blocks': [{
                        'block': 'tfc:rock/loose/%s' % MINERAL_INDICATORS.get(vein.ore)
                    }]
                }
            configured_placed_feature(rm, ('vein', vein_name), vein.vein_type, vein_config)

    for vein_name, vein in SURPRISE_VEINS.items():
        rocks = expand_rocks(vein.rocks)
        ore = ORES[vein.ore]  # standard ore
        configured_placed_feature(rm, ('vein', vein_name), vein.vein_type, {
            **vein.config(),
            'random_name': vein_name,
            'blocks': [{
                'replace': ['tfc:rock/raw/%s' % rock],
                'with': [{'weight': 90, 'block': 'tfc:ore/%s/%s' % (vein.ore, rock)},
                         {'weight': 10, 'block': 'minecraft:lava'}] # surprise! How difficult would infested TFC stone be?
            } for rock in rocks],
        })

    # Adding to in_biome/veins, other veins are already in via vanilla tfc
    rm.placed_feature_tag('in_biome/veins', *[
        'tfc:vein/mountain_hematite', 'tfc:vein/mountain_limonite', 'tfc:vein/mountain_magnetite',
        *('tfc:vein/%s' % v for v in SURPRISE_VEINS.keys()),
    ])


def vein_ore_blocks(vein: Vein, rock: str) -> List[Dict[str, Any]]:
    poor, normal, rich = vein.grade
    ore_blocks = [{
        'weight': poor,
        'block': 'tfc:ore/poor_%s/%s' % (vein.ore, rock)
    }, {
        'weight': normal,
        'block': 'tfc:ore/normal_%s/%s' % (vein.ore, rock)
    }, {
        'weight': rich,
        'block': 'tfc:ore/rich_%s/%s' % (vein.ore, rock)
    }]
    if False:  # todo: spoiler stuff?
        if vein.spoiler_ore is not None and rock in vein.spoiler_rocks:
            p = vein.spoiler_rarity * 0.01  # as a percentage of the overall vein
            ore_blocks.append({
                'weight': int(100 * p / (1 - p)),
                'block': 'tfc:ore/%s/%s' % (vein.spoiler_ore, rock)
            })
    if vein.deposits:
        ore_blocks.append({
            'weight': 10,
            'block': 'tfc:deposit/%s/%s' % (vein.ore, rock)
        })
    return ore_blocks


def mineral_ore_blocks(vein: Vein, rock: str) -> List[Dict[str, Any]]:
    if False:
        if vein.spoiler_ore is not None and rock in vein.spoiler_rocks:
            ore_blocks = [{'weight': 100, 'block': 'tfc:ore/%s/%s' % (vein.ore, rock)}]
            p = vein.spoiler_rarity * 0.01  # as a percentage of the overall vein
            ore_blocks.append({
                'weight': int(100 * p / (1 - p)),
                'block': 'tfc:ore/%s/%s' % (vein.spoiler_ore, rock)
            })
    ore_blocks = [{'block': 'tfc:ore/%s/%s' % (vein.ore, rock)}]
    return ore_blocks


def vein_density(density: int) -> float:
    assert 0 <= density <= 100, 'Invalid density: %s' % str(density)
    return round(density * 0.01, 2)


# Value Providers

def expand_rocks(rocks: list[str]) -> list[str]:
    assert all(r in ROCKS or r in ROCK_CATEGORIES for r in rocks)
    return [
        rock
        for spec in rocks
        for rock in ([spec] if spec in ROCKS else [r for r, d in ROCKS.items() if d.category == spec])
    ]


def decorate_climate(min_temp: Optional[float] = None, max_temp: Optional[float] = None, min_rain: Optional[float] = None, max_rain: Optional[float] = None, needs_forest: Optional[bool] = False, fuzzy: Optional[bool] = None, min_forest: Optional[str] = None, max_forest: Optional[str] = None) -> Json:
    return {
        'type': 'tfc:climate',
        'min_temperature': min_temp,
        'max_temperature': max_temp,
        'min_rainfall': min_rain,
        'max_rainfall': max_rain,
        'min_forest': 'normal' if needs_forest else min_forest,
        'max_forest': max_forest,
        'fuzzy': fuzzy
    }

def placed_feature_tag(rm: ResourceManager, name_parts: ResourceIdentifier, *values: ResourceIdentifier):
    return rm.tag(name_parts, 'worldgen/placed_feature', *values)

def configured_placed_feature(rm: ResourceManager, name_parts: ResourceIdentifier, feature: Optional[ResourceIdentifier] = None, config: JsonObject = None, *placements: Json):
    res = utils.resource_location(rm.domain, name_parts)
    if feature is None:
        feature = res
    rm.configured_feature(res, feature, config)
    rm.placed_feature(res, res, *placements)
