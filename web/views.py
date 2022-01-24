"""codethesaur.us views"""
import json
import random

from django.http import (
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
    HttpResponseServerError
)
from django.shortcuts import render
from django.utils.html import escape, strip_tags
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name

from web.models import Language, MetaInfo
from web.thesaurus_template_generators import generate_language_template


def index(request):
    """
    Renders the home page (/)

    :param request: HttpRequest object
    :return: HttpResponse object with rendered object of the page
    """
    with open("web/thesauruses/meta_info.json", 'r') as meta_file:
        meta_data = meta_file.read()
    meta_info = json.loads(meta_data)
    meta_data_langs = {
        id: {
            "name": lang["name"],
            "versions": ", ".join(lang["versions"])
        }
        for (id, lang) in meta_info["languages"].items()
    }
    random_langs = random.sample(list(meta_data_langs.values()), k=3)

    content = {
        'title': 'Welcome',
        'languages': meta_data_langs,
        'structures': meta_info["structures"],
        'randomLanguages': random_langs,
        'description': 'Code Thesaurus: A polyglot developer reference tool'
    }
    return render(request, 'index.html', content)


def about(request):
    """
    Renders the about page (/about)

    :param request: HttpRequest object
    :return: HttpResponse object with rendered object of the page
    """
    content = {
        'title': 'About',
        'description': 'Code Thesaurus: A polyglot developer reference tool'
    }
    return render(request, 'about.html', content)


# pylint: disable=too-many-branches
# pylint: disable=too-many-return-statements
def compare(request):
    """
    Renders the page comparing two language structures (/compare)

    :param request: HttpRequest object
    :return: HttpResponse object with rendered object of the page
    """
    lang1_string = escape(strip_tags(request.GET.get('lang1', '')))
    lang2_string = escape(strip_tags(request.GET.get('lang2', '')))
    structure_query_string = escape(strip_tags(request.GET.get('concept', '')))

    errors = []
    if not structure_query_string:
        errors.append("The URL didn't specify a structure/concept to look up.")
    if not lang1_string:
        errors.append("The URL didn't specify a first language to look up.")
    if not lang2_string:
        errors.append("The URL didn't specify a second language to look up.")

    if errors:
        error_page_data = {
            "errors": errors
        }
        response = render(request, 'errormisc.html', error_page_data)

        return HttpResponseNotFound(response)

    try:
        metainfo = MetaInfo()
        meta_structure = metainfo.structure(structure_query_string)
    except FileNotFoundError:
        error_page_data = {
            "errors": ["The structure/concept isn't valid. Double-check your URL and try again."]
        }
        response = render(request, "errormisc.html", error_page_data)

        return HttpResponseNotFound(response)

    try:
        lang1 = Language(
            lang1_string, metainfo.language_friendly_name(lang1_string))
        lang1.load_concepts(meta_structure.key)
    except FileNotFoundError:
        response = render(request, "error_missing_structure.html", {
            "name": meta_structure.friendly_name,
            "lang": lang1_string,
            "key": meta_structure.key,
            "template": generate_language_template(
                lang1_string,
                meta_structure.key
            )
        })
        return HttpResponseNotFound(response)
    except KeyError:
        error_page_data = {
            "errors": [f"The first language ({lang1_string}) isn't valid. \
                Double-check your URL and try again."]
        }
        response = render(request, "errormisc.html", error_page_data)
        return HttpResponseNotFound(response)

    try:
        lang2 = Language(
            lang2_string, metainfo.language_friendly_name(lang2_string))
        lang2.load_concepts(meta_structure.key)
    except FileNotFoundError:
        response = render(request, "error_missing_structure.html", {
            "name": meta_structure.friendly_name,
            "lang": lang2_string,
            "key": meta_structure.key,
            "template": generate_language_template(
                lang2_string,
                meta_structure.key
            )
        })
        return HttpResponseNotFound(response)
    except KeyError:
        error_page_data = {
            "errors": [f"The second language ({lang2_string}) isn't valid. \
                Double-check your URL and try again."]
        }
        response = render(request, "errormisc.html", error_page_data)
        return HttpResponseNotFound(response)

    both_categories = []

    for (category_key, category) in meta_structure.categories.items():
        concepts = [concept_comparision(id, name, lang1, lang2)
                    for (id, name) in category.items()]

        both_categories.append({
            "id": category_key,
            "concepts": concepts
        })

    response = {
        "title": f"Comparing {lang1.friendly_name} and {lang2.friendly_name}",
        "concept": meta_structure.key,
        "concept_friendly_name": meta_structure.friendly_name,
        "lang1": lang1.key,
        "lang2": lang2.key,
        "lang1_friendlyname": lang1.friendly_name,
        "lang2_friendlyname": lang2.friendly_name,
        "categories": both_categories,
        "description": f"Code Thesaurus: Comparing {lang1.friendly_name} \
                and {lang2.friendly_name}"
    }

    return render(request, 'compare.html', response)


def reference(request):
    """
    Renders the page showing one language structure for reference (/reference)

    :param request: HttpRequest object
    :return: HttpResponse object with rendered object of the page
    """
    lang_string = escape(strip_tags(request.GET.get('lang', '')))
    structure_query_string = escape(strip_tags(request.GET.get('concept', '')))

    errors = []
    if not structure_query_string:
        errors.append("The URL didn't specify a structure/concept to look up.")
    if not lang_string:
        errors.append("Thr URL didn't specify a language to look up.")
    if errors:
        error_page_data = {
            "errors": errors
        }
        response = render(request, 'errormisc.html', error_page_data)

        return HttpResponseNotFound(response)

    try:
        metainfo = MetaInfo()
        meta_structure = metainfo.structure(structure_query_string)
    except FileNotFoundError:
        error_page_data = {
            "errors": ["The structure/concept isn't valid. Double-check your URL and try again."]
        }
        response = render(request, "errormisc.html", error_page_data)

        return HttpResponseNotFound(response)

    try:
        lang = Language(
            lang_string, metainfo.language_friendly_name(lang_string))
        lang.load_concepts(meta_structure.key)
    except FileNotFoundError:
        ctx = {
            "name": meta_structure.friendly_name,
            "lang": lang_string,
            "key": meta_structure.key,
            "template": generate_language_template(
                lang_string,
                meta_structure.key
            )
        }
        response = render(request, "error_missing_structure.html", ctx)
        return HttpResponseNotFound(response)
    except KeyError:
        error_page_data = {
            "errors": [f"The language ({lang_string}) isn't valid. \
                        Double-check your URL and try again."]
        }
        response = render(request, "errormisc.html", error_page_data)
        return HttpResponseNotFound(response)

    categories = []

    for (category_key, category) in meta_structure.categories.items():
        concepts = [concept_reference(id, name, lang)
                    for (id, name) in category.items()]
        categories.append({
            "id": category_key,
            "concepts": concepts
        })

    response = {
        "title": f"Reference for {lang.key}",
        "concept": meta_structure.key,
        "concept_friendly_name": meta_structure.friendly_name,
        "lang": lang.key,
        "lang_friendlyname": lang.friendly_name,
        "categories": categories,
        "description": f"Code Thesaurus: Reference for {lang.key}"
    }

    return render(request, 'reference.html', response)


def error_handler_400_bad_request(request, _exception):
    """
    Renders the page for a generic client error (HTTP 400)

    :param request: HttpRequest object
    :param exception: details about the exception
    :return: HttpResponse object with rendered object of the page
    """
    response = render(request, 'error400.html')
    return HttpResponseBadRequest(response)


def error_handler_403_forbidden(request, _exception):
    """
    Renders the page for a forbidden error (HTTP 403)

    :param request: HttpRequest object
    :param exception: details about the exception
    :return: HttpResponse object with rendered object of the page
    """
    response = render(request, 'error403.html')
    return HttpResponseForbidden(response)


def error_handler_404_not_found(request, _exception):
    """
    Renders the page for a file not found error (HTTP 404)

    :param request: HttpRequest object
    :param exception: details about the exception
    :return: HttpResponse object with rendered object of the page
    """
    response = render(request, 'error404.html')
    return HttpResponseNotFound(response)


def error_handler_500_server_error(request):
    """
    Renders the page for a generic server error (HTTP 500)

    :param request: HttpRequest object
    :return: HttpResponse object with rendered object of the page
    """
    response = render(request, 'error500.html')
    return HttpResponseServerError(response)


# Helper functions
def format_code_for_display(concept_key, lang):
    """
    Returns the formatted HTML formatted syntax-highlighted text for a concept key (from a meta
            language file) and a language

    :param concept_key: name of the key to format
    :param lang: language to format it (in meta language/syntax highlighter format)
    :return: string with code with applied HTML formatting
    """
    if lang.concept_unknown(concept_key) or lang.concept_code(concept_key) is None:
        return "Unknown"
    if lang.concept_implemented(concept_key):
        return highlight(
            lang.concept_code(concept_key),
            get_lexer_by_name(lang.key, startinline=True),
            HtmlFormatter()
        )
    return None


def format_comment_for_display(concept_key, lang):
    """
    Returns the formatted HTML formatted comment text for a concept key (from a meta language
            file) and a language

    :param concept_key: the concept key located in the meta language JSON file
    :param lang: the ID of the language to fetch concept key from
    :return: formatted HTML for the comment
    """
    if not lang.concept_implemented(concept_key) and lang.concept_comment(concept_key) == "":
        return "Not Implemented In This Language"
    return lang.concept_comment(concept_key)


def concept_comparision(concept_id, name, lang1, lang2):
    """
    Generates the comparision object of a single concept

    :param id: id of the concept
    :param name: name of the concept
    :param lang1: first language to compare
    :param lang2: other language to compare
    :return: string with code with applied HTML formatting
    """
    return {
        "id": concept_id,
        "name": name,
        "code1": format_code_for_display(concept_id, lang1),
        "code2": format_code_for_display(concept_id, lang2),
        "comment1": format_comment_for_display(concept_id, lang1),
        "comment2": format_comment_for_display(concept_id, lang2)
    }


def concept_reference(concept_id, name, lang):
    """
    Generates the reference object of a single concept

    :param id: id of the concept
    :param name: name of the concept
    :param lang: language to get the reference for
    :return: string with code with applied HTML formatting
    """
    return {
        "id": concept_id,
        "name": name,
        "code": format_code_for_display(concept_id, lang),
        "comment": format_comment_for_display(concept_id, lang)
    }
