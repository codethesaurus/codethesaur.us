import json
import os
import random

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.html import escape, strip_tags


def index(request):
    with open("web/thesauruses/meta_info.json", 'r') as meta_file:
        meta_data = meta_file.read()
    meta_data_langs = json.loads(meta_data)["languages"]
    meta_structures = json.loads(meta_data)["structures"]
    random_langs = random.sample(list(meta_data_langs.values()), k=3)

    content = {
        'title': 'Welcome',
        'languages': meta_data_langs,
        'structures': meta_structures,
        'randomLanguages': random_langs,
    }
    return render(request, 'index.html', content)


def about(request):
    content = {
        'title': 'About'
    }
    return render(request, 'about.html', content)


class Language(object):
    def __init__(self, key):
        self.key = key

    def has_key(self):
        return self.key == ""


def compare(request):
    lang1 = Language(escape(strip_tags(request.GET.get('lang1', ''))))
    lang2 = Language(escape(strip_tags(request.GET.get('lang2', ''))))
    try:
        with open("web/thesauruses/meta_info.json", 'r') as meta_file:
            meta_data = meta_file.read()
        meta_data_structures = json.loads(meta_data)["structures"]

        concept_query_string = escape(strip_tags(request.GET.get('concept', '')))

        if not lang1.has_key and lang2.has_key:
            return HttpResponseNotFound(
                "The " + concept_query_string + " concept of either the " + lang1.key + " or " +
                lang2.key + " languages doesn't exist or hasn't been implemented yet.")

        concept_friendly_name_pos = list(meta_data_structures.values()).index(concept_query_string)
        concept_friendly_name = list(meta_data_structures.keys())[concept_friendly_name_pos]

        meta_lang_file_path = os.path.join(
            "web", "thesauruses", "_meta", concept_query_string) + ".json"
        lang1_file_path = os.path.join(
            "web", "thesauruses", lang1.key, concept_query_string) + ".json"
        lang2_file_path = os.path.join(
            "web", "thesauruses", lang2.key, concept_query_string) + ".json"

        with open(meta_lang_file_path, 'r') as meta_lang_file:
            data = meta_lang_file.read()
            # parse file
            meta_lang_file_json = json.loads(data)

            meta_lang_categories = meta_lang_file_json["categories"]
            meta_lang_concepts = meta_lang_file_json[concept_query_string]

        with open(lang1_file_path, 'r') as lang1_file:
            data = lang1_file.read()
            # parse file
            lang1_file_json = json.loads(data)

            lang1_friendly_name = lang1_file_json["meta"]["language_name"]
            lang1_categories = lang1_file_json["categories"]
            lang1_concepts = lang1_file_json[concept_query_string]

        with open(lang2_file_path, 'r') as lang2_file:
            data = lang2_file.read()
            # parse file
            lang2_file_json = json.loads(data)

            lang2_friendly_name = lang2_file_json["meta"]["language_name"]
            lang2_categories = lang2_file_json["categories"]
            lang2_concepts = lang2_file_json[concept_query_string]

    except:
        return HttpResponseNotFound(
            "The " + concept_query_string + " concept of either the " + lang1.key + " or " +
            lang2.key + " languages doesn't exist or hasn't been implemented yet.")

    both_categories = []
    both_concepts = []
    # XXX: Ideally we should set default value of lang dict here
    # and not in template but that will be possible after issue #27
    # is resolved

    all_category_keys = list(meta_lang_categories.keys())
    all_concept_keys = list(meta_lang_concepts.keys())

    for category_key in all_category_keys:
        both_categories.append({
            "id": category_key,
            "concepts": meta_lang_categories[category_key]
        })

    for concept_key in all_concept_keys:
        if lang1_concepts.get(concept_key) is None:
            lang1_concepts[concept_key] = {
                "code": "",
                "comment": ""
            }
        if lang2_concepts.get(concept_key) is None:
            lang2_concepts[concept_key] = {
                "code": "",
                "comment": ""
            }

        both_concepts.append({
            "id": concept_key,
            "name": meta_lang_concepts[concept_key]["name"],
            "code1": lang1_concepts[concept_key]["code"],
            "code2": lang2_concepts[concept_key]["code"],
            "comment1": lang1_concepts[concept_key].get("comment", ""),
            "comment2": lang2_concepts[concept_key].get("comment", "")
        })

    # establish order listing across all languages
    # common_concepts.sort(key=lambda x: x["key"])

    # DB equivalent of full outer join
    response = {
        "title": "Comparing" + lang1_friendly_name + " " + lang2_friendly_name,
        "concept": concept_query_string,
        "concept_friendly_name": concept_friendly_name,
        "lang1": lang1.key,
        "lang2": lang2.key,
        "lang1_friendlyname": lang1_friendly_name,
        "lang2_friendlyname": lang2_friendly_name,
        "categories": both_categories,
        "concepts": both_concepts
    }

    return render(request, 'compare.html', response)


def reference(request):
    try:
        with open("web/thesauruses/meta_info.json", 'r') as meta_file:
            meta_data = meta_file.read()
        meta_data_structures = json.loads(meta_data)["structures"]

        concept_query_string = escape(strip_tags(request.GET.get('concept', '')))
        lang_query_string = escape(strip_tags(request.GET.get('lang', '')))

        concept_friendly_name_pos = list(meta_data_structures.values()).index(concept_query_string)
        concept_friendly_name = list(meta_data_structures.keys())[concept_friendly_name_pos]

        if not lang_query_string:
            return HttpResponseNotFound(
                "The " + concept_query_string + " concept of the " + lang_query_string + " language doesn't exist or hasn't been implemented yet.")

        meta_lang_file_path = os.path.join(
            "web", "thesauruses", "_meta", concept_query_string) + ".json"
        lang_file_path = os.path.join(
            "web", "thesauruses", lang_query_string, concept_query_string) + ".json"

        with open(meta_lang_file_path, 'r') as meta_lang_file:
            data = meta_lang_file.read()
            # parse file
            meta_lang_file_json = json.loads(data)

            meta_lang_categories = meta_lang_file_json["categories"]
            meta_lang_concepts = meta_lang_file_json[concept_query_string]

        with open(lang_file_path, 'r') as lang_file:
            data = lang_file.read()
            # parse file
            lang_file_json = json.loads(data)

            lang_friendly_name = lang_file_json["meta"]["language_name"]
            lang_categories = lang_file_json["categories"]
            lang_concepts = lang_file_json[concept_query_string]

    except:
        return HttpResponseNotFound(
            "The " + concept_query_string + " concept of the " + lang_query_string + " language doesn't exist or hasn't been implemented yet.")

    categories = []
    concepts = []
    for category_key in lang_categories.keys():
        categories.append({
            "id": category_key,
            "concepts": meta_lang_categories[category_key]
        })
    for concept_key in lang_concepts.keys():
        concepts.append({
            "id": concept_key,
            "name": meta_lang_concepts[concept_key]["name"],
            "code": lang_concepts[concept_key]["code"],
            "comment": lang_concepts[concept_key].get("comment", "")
        })

    response = {
        "title": "Reference for " + lang_query_string,
        "concept": concept_query_string,
        "concept_friendly_name": concept_friendly_name,
        "lang": lang_query_string,
        "lang_friendlyname": lang_friendly_name,
        "categories": categories,
        "concepts": concepts
    }

    return render(request, 'reference.html', response)
