"""Generator functions for thesaurus files"""
import json
from web.models import MetaInfo


def generate_language_template(language_key, structure_key, version=None):
    """Generate a template for the given language and structure"""
    meta_info = MetaInfo()
    if structure_key not in meta_info.structures:
        raise ValueError
    language_name = meta_info.languages.get(
        language_key,
        'Human-Readable Language Name'
    )
    meta = {
        'language': language_key,
        'language_name': language_name,
        'structure': structure_key,
    }

    if version:
        meta['language_version'] = version

    concepts = {
        key: {
            'name': name,
            'code': [""],
        }
        for category in meta_info.structure(structure_key).categories.values()
        for (key, name) in category.items()
    }

    return json.dumps({'meta': meta, 'concepts': concepts}, indent=2)


def generate_meta_template(structure_key, structure_name):
    """Generate a template for a `meta file`"""
    meta = {
        'structure': structure_key,
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
