from django.http import (
    HttpResponse, Http404, HttpResponseRedirect,
    HttpResponseBadRequest,
)
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

import json
import os

# from .models import Question

def index(request):
    with open("web/thesauruses/meta_info.json", 'r') as meta_file:
        meta_data = meta_file.read()
    meta_data_langs = json.loads(meta_data)["languages"].keys

    content = {
        'title': 'Welcome',
        'languages': meta_data_langs
    }
    return render(request, 'index.html', content)


def about(request):
    content = {
        'title': 'About'
    }
    return render(request, 'about.html', content)


def compare(request):
    try:
        with open("web/thesauruses/meta_info.json", 'r') as meta_file:
            meta_data = meta_file.read()
        meta_data_langs = json.loads(meta_data)["languages"]

        lang1 = request.GET.get('lang1', '')
        lang2 = request.GET.get('lang2', '')
        lang1_directory = meta_data_langs.get(lang1)
        lang2_directory = meta_data_langs.get(lang2)

        # if not (lang1_directory and lang2_directory):
        #     return HttpResponseBadRequest("Lang does not exist")

        concept = request.GET.get('concept', '')

        lang1_file_path = os.path.join(
            "web", "thesauruses", lang1_directory, concept) + ".json"
        lang2_file_path = os.path.join(
            "web", "thesauruses", lang2_directory, concept) + ".json"

        with open(lang1_file_path, 'r') as lang1_file:
            data = lang1_file.read()
            # parse file
            lang1_file_json = json.loads(data)

            lang1_friendly_name = lang1_file_json["meta"]["language_name"]
            lang1_categories = lang1_file_json["categories"]
            lang1_concepts = lang1_file_json[concept]

        with open(lang2_file_path, 'r') as lang2_file:
            data = lang2_file.read()
            # parse file
            lang2_file_json = json.loads(data)

            lang2_friendly_name = lang2_file_json["meta"]["language_name"]
            lang2_categories = lang2_file_json["categories"]
            lang2_concepts = lang2_file_json[concept]

    except:
        return HttpResponse("The " + concept + " concept of either the " + lang1 + " or " + lang2 + " languages doesn't exist or hasn't been implemented yet.")

    both_categories = []
    both_concepts = []
    # XXX: Ideally we should set default value of lang dict here
    # and not in template but that will be possible after issue #27
    # is resolved

    all_category_keys = list(set.union(set(lang1_categories.keys()), set(lang2_categories.keys())))
    all_concept_keys = list(set.union(set(lang1_concepts.keys()), set(lang2_concepts.keys())))

    for category_key in all_category_keys:
        both_categories.append({
            "id": category_key,
            "concepts": lang1_categories[category_key]
        })

    for concept_key in all_concept_keys:
        if lang1_concepts.get(concept_key) is None:
            lang1_concepts[concept_key] = {
                "name": "",
                "code": ""
            }
        if lang2_concepts.get(concept_key) is None:
            lang2_concepts[concept_key] = {
                "name": "",
                "code": ""
            }

        both_concepts.append({
            "id": concept_key,
            "name1": lang1_concepts[concept_key]["name"],
            "name2": lang2_concepts[concept_key]["name"],
            "code1": lang1_concepts[concept_key]["code"],
            "code2": lang2_concepts[concept_key]["code"]
        })

    # establish order listing across all languages
    # common_concepts.sort(key=lambda x: x["key"])

    # DB equivalent of full outer join
    response = {
        "title": "Comparing" + lang1 + " " + lang2,
        "concept": concept,
        "lang1": lang1,
        "lang2": lang2,
        "lang1_friendlyname": lang1_friendly_name,
        "lang2_friendlyname": lang2_friendly_name,
        "categories": both_categories,
        "concepts": both_concepts
    }

    return render(request, 'compare.html', response)

# add in compare with /compare/lang1/lang2 in the future


def reference(request):
    try:
        with open("web/thesauruses/meta_info.json", 'r') as meta_file:
            meta_data = meta_file.read()
        meta_data_langs = json.loads(meta_data)["languages"]

        lang = request.GET.get('lang', '')
        lang_directory = meta_data_langs[lang]

        # if not (lang_directory):
        #     return HttpResponseBadRequest("Lang does not exist")

        concept = request.GET.get('concept', '')

        with open("web/thesauruses/" + lang_directory + "/" + concept + ".json", 'r') as lang_file:
            data = lang_file.read()
        # parse file
        lang_file_json = json.loads(data)
    except:
        return HttpResponse("The " + concept + " concept of the " + lang + " either doesn't exist or hasn't been implemented yet.")

    lang_friendly_name = lang_file_json["meta"]["language_name"]
    lang_categories = lang_file_json["categories"]
    lang_concepts = lang_file_json[concept]

    categories = []
    concepts = []
    for category_key in lang_categories.keys():
        categories.append({
            "id": category_key,
            "concepts": lang_categories[category_key]
        })
    for concept_key in lang_concepts.keys():
        concepts.append({
            "id": concept_key,
            "name": "" or lang_concepts[concept_key]["name"],
            "code": "" or lang_concepts[concept_key]["code"]
        })

    response = {
        "title": "Reference for " + lang,
        "concept": concept,
        "lang": lang,
        "lang_friendlyname": lang_friendly_name,
        "categories": categories,
        "concepts": concepts
    }

    return render(request, 'reference.html', response)

