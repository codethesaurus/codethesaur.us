import json
import random

from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render
from django.utils.html import escape, strip_tags
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name

from web.Language import Language
from web.MetaInfo import MetaInfo


def format_code_for_display(concept_key, lang):
    """
    Returns the formatted HTML formatted syntax-highlighted text for a concept key (from a meta language file) and a language
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
    Returns the formatted HTML formatted comment text for a concept key (from a meta language file) and a language
    :param concept_key: the concept key located in the meta language JSON file
    :param lang: the ID of the language to fetch concept key from
    :return: formatted HTML for the comment
    """
    if not lang.concept_implemented(concept_key) and lang.concept_comment(concept_key) == "":
        return "Not Implemented In This Language"
    return lang.concept_comment(concept_key)


def index(request):
    """
    Renders the home page (/)
    :param request: HttpRequest object
    :return: HttpResponse object with rendered object of the page
    """
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


def compare(request):
    """
    Renders the page comparing two language structures (/compare)
    :param request: HttpRequest object
    :return: HttpResponse object with rendered object of the page
    """
    lang1 = Language(escape(strip_tags(request.GET.get('lang1', ''))))
    lang2 = Language(escape(strip_tags(request.GET.get('lang2', ''))))
    structure_query_string = escape(strip_tags(request.GET.get('concept', '')))

    error_message = ""
    if not structure_query_string:
        error_message = "The URL didn't specify a structure/concept to look up.<br />"
    if not lang1.has_key():
        error_message = error_message + "The URL didn't specify a first language to look up.<br />"
    if not lang2.has_key():
        error_message = error_message + "The URL didn't specify a second language to look up.<br />"

    if error_message:
        error_page_data = {
            "message": error_message
        }
        response = render(request, 'errormisc.html', error_page_data)

        return HttpResponseNotFound(response)

    try:
        metainfo = MetaInfo()
        meta_structure = metainfo.structure(structure_query_string)
    # pylint: disable=broad-except
    except Exception:
        error_page_data = {
            "message": "The structure/concept isn't valid. Double-check your URL and try again.<br />"
        }
        response = render(request, "errormisc.html", error_page_data)

        return HttpResponseNotFound(response)

    try:
        lang1.load_structure(meta_structure.key)
    # pylint: disable=broad-except
    except Exception:
        error_message = ""
        if lang1.lang_exists():
            error_message = f"There is no entry about this structure/concept for the \
                first language ({lang1.key}) yet.<br />"
        else:
            error_message = f"The first language ({lang1.key}) isn't valid. \
                Double-check your URL and try again.<br />"
        error_page_data = {
            "message": error_message
        }
        response = render(request, "errormisc.html", error_page_data)
        return HttpResponseNotFound(response)

    try:
        lang2.load_structure(meta_structure.key)
    # pylint: disable=broad-except
    except Exception:
        error_message = ""
        if lang2.lang_exists():
            error_message = f"There is no entry about this structure/concept for the \
                second language ({lang2.key}) yet.<br />"
        else:
            error_message = f"The second language ({lang2.key}) isn't valid. \
                Double-check your URL and try again.<br />"
        error_page_data = {
            "message": error_message
        }
        response = render(request, "errormisc.html", error_page_data)
        return HttpResponseNotFound(response)

    both_categories = []
    both_concepts = []
    # Ideally we should set default value of lang dict here
    # and not in template now that issue #27 is resolved

    all_category_keys = list(meta_structure.categories.keys())
    all_concept_keys = list(meta_structure.concepts.keys())

    for category_key in all_category_keys:
        both_categories.append({
            "id": category_key,
            "concepts": meta_structure.categories[category_key]
        })

    # Start Building Response Structure
    for concept_key in all_concept_keys:
        both_concepts.append({
            "id": concept_key,
            "name": meta_structure.concepts[concept_key]["name"],
            "code1": format_code_for_display(concept_key, lang1),
            "code2": format_code_for_display(concept_key, lang2),
            "comment1": format_comment_for_display(concept_key, lang1),
            "comment2": format_comment_for_display(concept_key, lang2)
        })

    # establish order listing across all languages
    # common_concepts.sort(key=lambda x: x["key"])

    # DB equivalent of full outer join
    response = {
        "title": "Comparing " + lang1.friendly_name + " " + lang2.friendly_name,
        "concept": meta_structure.key,
        "concept_friendly_name": meta_structure.friendly_name,
        "lang1": lang1.key,
        "lang2": lang2.key,
        "lang1_friendlyname": lang1.friendly_name,
        "lang2_friendlyname": lang2.friendly_name,
        "categories": both_categories,
        "concepts": both_concepts,
        "description": "Code Thesaurus: Comparing " + lang1.friendly_name + " " + lang2.friendly_name
    }

    return render(request, 'compare.html', response)


def reference(request):
    """
    Renders the page showing one language structure for reference (/reference)
    :param request: HttpRequest object
    :return: HttpResponse object with rendered object of the page
    """
    lang = Language(escape(strip_tags(request.GET.get('lang', ''))))
    structure_query_string = escape(strip_tags(request.GET.get('concept', '')))

    error_message = ""
    if not structure_query_string:
        error_message = "The URL didn't specify a structure/concept to look up.<br />"
    if not lang.has_key():
        error_message = error_message + "The URL didn't specify a language to look up.<br />"
    if error_message:
        error_page_data = {
            "message": error_message
        }
        response = render(request, 'errormisc.html', error_page_data)

        return HttpResponseNotFound(response)

    try:
        metainfo = MetaInfo()
        meta_structure = metainfo.structure(structure_query_string)
    # pylint: disable=broad-except
    except Exception:
        error_page_data = {
            "message": "The structure/concept isn't valid. Double-check your URL and try again.<br />"
        }
        response = render(request, "errormisc.html", error_page_data)

        return HttpResponseNotFound(response)

    try:
        lang.load_structure(meta_structure.key)
    # pylint: disable=broad-except
    except Exception:
        error_message = ""
        if lang.lang_exists():
            error_message = f"There is no entry about this structure/concept for the \
                language ({lang.key}) yet.<br />"
        else:
            error_message = f"The language ({lang.key}) isn't valid. \
                Double-check your URL and try again.<br />"
        error_page_data = {
            "message": error_message
        }
        response = render(request, "errormisc.html", error_page_data)
        return HttpResponseNotFound(response)

    categories = []
    concepts = []
    for category_key in lang.categories:
        categories.append({
            "id": category_key,
            "concepts": meta_structure.categories[category_key]  # meta_lang_categories[category_key]
        })

    for concept_key in lang.concepts:
        concepts.append({
            "id": concept_key,
            "name": meta_structure.concepts[concept_key]["name"],
            "code": format_code_for_display(concept_key, lang),
            "comment": format_comment_for_display(concept_key, lang)
        })

    response = {
        "title": "Reference for " + lang.key,
        "concept": meta_structure.key,
        "concept_friendly_name": meta_structure.friendly_name,
        "lang": lang.key,
        "lang_friendlyname": lang.friendly_name,
        "categories": categories,
        "concepts": concepts,
        "description": "Code Thesaurus: Reference for " + lang.key
    }

    return render(request, 'reference.html', response)


# pylint: disable=unused-argument
def error_handler_400_bad_request(request, exception):
    """
    Renders the page for a generic client error (HTTP 400)
    :param request: HttpRequest object
    :param exception: details about the exception
    :return: HttpResponse object with rendered object of the page
    """
    response = render(request, 'error400.html')
    return HttpResponseBadRequest(response)


# pylint: disable=unused-argument
def error_handler_403_forbidden(request, exception):
    """
    Renders the page for a forbidden error (HTTP 403)
    :param request: HttpRequest object
    :param exception: details about the exception
    :return: HttpResponse object with rendered object of the page
    """
    response = render(request, 'error403.html')
    return HttpResponseForbidden(response)


# pylint: disable=unused-argument
def error_handler_404_not_found(request, exception):
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
