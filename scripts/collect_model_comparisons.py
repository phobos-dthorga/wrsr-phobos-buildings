"""Record measurements, identifiers and attribution, never donor artwork.
Copyright (c) 2026 Phobos A. D'thorga. MIT.
"""
import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import shlex
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.measure_nmf import measure

REFERENCES = [
    ('2844662248', 'cieplownia', 'Big heating plant'),
    ('2913038245', 'elektrownia', 'Coal power plant'),
    ('2930412481', 'elektrownia', 'Big coal power plant'),
    ('3442736806', 'huta', 'Steel mill'),
    ('3035907116', 'coalpowerplant', 'Combined Heat and Power Plant (Coal)'),
    ('3035907116', 'gaspowerplant', 'Combined Heat and Power Plant (Gas)'),
    ('3035907116', 'geothermalhp', 'Geothermal heating plant'),
    ('3035907116', 'kohlekraftwerk', 'Coal plant (kohlekraftwerk)'),
    ('3035907116', 'gaskraftwerk', 'Gas plant (gaskraftwerk)'),
    ('3035907116', 'mediumgas', 'Gas plant (mediumgas)'),
    ('2951506229', 'vorkonvoi', 'KWU Baulinie 3'),
    ('2951506229', 'wwer70', 'WWER-70'),
    ('2951506229', 'snr300', 'SNR-300'),
    ('2951506229', 'umspannwerk', 'Substation (umspannwerk)'),
    ('2807104839', 'petrochemicalcombine', 'Petrochemical Combine'),
    ('2807104839', 'chemicalplant1', 'Chemical plant 1'),
    ('2807104839', 'hydrogenplant', 'Hydrogen plant'),
    ('2467860304', 'minimill', 'Mini mill'),
    ('2467860304', 'konverter', 'Converter steelworks'),
    ('2572446961', '221-1-174_main_building', 'School type 221-1-174'),
]


def collect(workshop):
    audit = json.loads((ROOT / 'research/evidence/workshop-license-screening.json').read_text(encoding='utf-8'))
    authors = {str(item['workshop_id']): item for item in audit['items']}
    records = []
    for item, folder, label in REFERENCES:
        author = authors[item]
        config = workshop / item / folder / 'renderconfig.ini'
        models = []
        for line in config.read_text(encoding='utf-8-sig', errors='replace').splitlines():
            tokens = shlex.split(line)
            if not tokens or tokens[0].lstrip('$') not in ('MODEL', 'MODEL_LOD', 'MODEL_LOD1', 'MODEL_LOD2'):
                continue
            path = (config.parent / tokens[1]).resolve()
            if not path.is_relative_to((workshop / item).resolve()):
                raise ValueError('Model outside inspected Workshop item')
            stats = measure(path)
            models.append({'role': tokens[0], 'asset': path.relative_to(workshop / item).as_posix(),
                           'distance_m': float(tokens[2]) if len(tokens) > 2 else None, **stats})
        if not models:
            raise ValueError('No model declarations: ' + folder)
        records.append({'workshop_id': item, 'workshop_url': author['workshop_url'],
                        'package_title': author['title'], 'building_label': label,
                        'label_note': 'Descriptive label; folder suffix retained where an exact translated in-game name was not verified.',
                        'publisher_name': author['publisher_name'], 'publisher_profile_url': author['publisher_profile_url'],
                        'publisher_is_not_automatically_original_author': True,
                        'folder': folder, 'renderconfig_sha256': hashlib.sha256(config.read_bytes()).hexdigest(),
                        'models': models})
    own = ROOT / 'mods/electric-heating-works/source/assembly-a05/native/plant.nmf'
    return {'schema_version': 1, 'measurement_date': date.today().isoformat(),
            'method': 'Read-only static NMF parsing and renderconfig inspection; native X/Z bounds measure footprint, Y measures height. Identity transforms verified. No runtime performance measurements.',
            'limitations': ['One placeable model per row, not a collection total.',
                           'Bounds include modelled pipes/chimneys; ground decals and separate unreferenced scene elements are not included.',
                           'Subsets/materials/nodes are rendering-cost indicators, not measured draw calls.',
                           'No external LOD declaration plus one embedded level means none found in the inspected configuration; not a claim about other releases.',
                           'Reference inspection grants no asset reuse licence. All original authors retain their rights.',
                           'Static reader rejects unsupported animation, hierarchy and vertex formats. Do not apply these building budgets to vehicles.'],
            'baseline': {'author': "Phobos A. D'thorga / phobosgekko", 'revision': 'p01/a05',
                         'asset': own.relative_to(ROOT).as_posix(), **measure(own)}, 'references': records}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workshop', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    evidence = collect(args.workshop.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    print('Recorded', len(evidence['references']), 'building references; no artwork copied.')
