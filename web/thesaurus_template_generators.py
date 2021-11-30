import json
from web.MetaInfo import MetaInfo


def generate_language_template(language_id, structure_id, version):
    meta_info = MetaInfo()
    if structure_id not in meta_info.data_structures:
        raise ValueError
    language_name = meta_info.languages.get(
        language_id,
        {'name': 'Human-Readable Language Name'}
    )['name']
    meta = {
        'language': language_id,
        'language_name': language_name,
        'structure': structure_id,
    }

    if version:
        meta['language_version'] = version

    concepts = {
        id: {'code': [""]}
        for category in meta_info.structure(structure_id).categories.values()
        for (id, name) in category.items()
    }

    return json.dumps({'meta': meta, 'concepts': concepts}, indent=2)


def generate_meta_template(structure_id, structure_name):
    meta = {
        'structure': structure_id,
        'structure_name': structure_name,
    }
    categories = {
        'First Category Name': {
            'concept_id1': 'Name of Concept 1',
            'concept_id2': 'Name of Concept 2'
        },
        'Second Category Name': {
            'concept_id3': 'Name of Concept 3',
            'concept_id4': 'Name of Concept 4'
        }
    }
    return json.dumps({'meta': meta, 'categories': categories})
