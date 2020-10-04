from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
import json


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
    #JSON updates:
    # language => id
    # language_name => friendly_label

    # TODO: try/catch

    with open("web/thesauruses/meta_info.json", 'r') as meta_file:
        meta_data = meta_file.read()
    meta_data_langs = json.loads(meta_data)["languages"]

    lang1 = request.GET.get('lang1', '')
    lang2 = request.GET.get('lang2', '')
    lang1_directory = meta_data_langs[lang1]
    lang2_directory = meta_data_langs[lang2]

    concept = request.GET.get('concept', '')

    with open("web/thesauruses/" + lang1_directory + "/" + concept + ".json", 'r') as lang1_file:
        data = lang1_file.read()
    # parse file
    lang1_file_json = json.loads(data)
    lang1_concept = lang1_file_json[concept]
    lang1_friendlyname = lang1_file_json["meta"]["language_name"]

    with open("web/thesauruses/" + lang2_directory + "/" + concept + ".json", 'r') as lang2_file:
        data = lang2_file.read()
    # parse file
    lang2_file_json = json.loads(data)
    lang2_concept = lang2_file_json[concept]
    lang2_friendlyname = lang2_file_json["meta"]["language_name"]

    common_concepts =[]
    for key in list(set.union(set(lang1_concept.keys()), set(lang2_concept.keys()))):
        common_concepts.append({
            "key": key,
            "lang1": lang1_concept[key],
            "lang2": lang2_concept[key]
        })


    # DB equivalent of full outer join
    response = {
        "title": "Comparing" + lang1 + " " + lang2,
        "concept": concept,
        "lang1": lang1,
        "lang2": lang2,
        "lang1_friendlyname": lang1_friendlyname,
        "lang2_friendlyname": lang2_friendlyname,
        "common_concepts": common_concepts
    }

    return render(request, 'compare.html', response)

# add in compare with /compare/lang1/lang2 in the future


def reference(request):
    # TODO: try/catch

    with open("web/thesauruses/meta_info.json", 'r') as meta_file:
        meta_data = meta_file.read()
    meta_data_langs = json.loads(meta_data)["languages"]

    lang = request.GET.get('lang', '')
    lang_directory = meta_data_langs[lang]

    concept = request.GET.get('concept', '')

    with open("web/thesauruses/" + lang_directory + "/" + concept + ".json", 'r') as lang_file:
        data = lang_file.read()
    # parse file
    lang_file_json = json.loads(data)
    lang_concept = lang_file_json[concept]
    lang_friendlyname = lang_file_json["meta"]["language_name"]

    common_concepts =[]
    for key in list(lang_concept.keys()):
        common_concepts.append({
            "key": key,
            "lang": lang_concept[key]
        })

    response = {
        "title": "Reference for " + lang,
        "concept": concept,
        "lang": lang,
        "lang_friendlyname": lang_friendlyname,
        "common_concepts": common_concepts
    }

    return render(request, 'reference.html', response)

