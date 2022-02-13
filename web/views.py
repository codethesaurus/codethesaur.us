"""codethesaur.us views"""
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

from web.models import MetaInfo
from web.thesaurus_template_generators import generate_language_template


def index(request):
    """
    Renders the home page (/)

    :param request: HttpRequest object
    :return: HttpResponse object with rendered object of the page
    """
    if "lang" in request.GET and "concept" in request.GET:
        return concepts(request)

    meta_info = MetaInfo()

    meta_data_langs = dict()
    for key in meta_info.languages:
        lang = meta_info.language(key)
        meta_data_langs[key] = [{
            "name": lang.friendly_name,
            "version": version,
        } for version in lang.versions()]

    random_langs = random.sample(list(meta_data_langs.values()), k=3)

    content = {
        'title': 'Welcome',
        'languages': meta_data_langs,
        'structures': meta_info.structures,
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


def concepts(request):
    """
    Renders the page comparing two language structures (/compare)

    :param request: HttpRequest object
    :return: HttpResponse object with rendered object of the page
    """
    language_strings = [escape(strip_tags(lang)) for lang in request.GET.getlist('lang')]
    structure_query_string = escape(strip_tags(request.GET.get('concept', '')))

    errors = []
    if not structure_query_string:
        errors.append("The URL didn't specify a structure/concept to look up.")
    if not language_strings and all(language_strings):
        # legacy parameter names
        # TODO fixme
        if "lang1" not in request.GET or "lang2" not in request.GET:
            errors.append("The URL didn't specify any languages to look up.")
        else:
            language_strings = [
                escape(strip_tags(request.GET['lang1'])),
                escape(strip_tags(request.GET['lang2']))
            ]
    if errors:
        return render_errors(request, errors)


    try:
        meta_info = MetaInfo()
        meta_structure = meta_info.structure(structure_query_string)
    except KeyError:
        return render_errors(request, ["The structure/concept isn't valid. \
                Double-check your URL and try again."])

    languages = []
    for language_string in language_strings:
        try:
            language_string, version = language_string.split(";")
            language = meta_info.language(language_string)
            language.load_concepts(meta_structure.key, version)
            languages.append(language)
        except FileNotFoundError:
            response = render(request, "error_missing_structure.html", {
                "name": meta_structure.friendly_name,
                "lang": language_string,
                "key": meta_structure.key,
                "version": version,
                "template": generate_language_template(
                    language_string,
                    meta_structure.key,
                    version
                )
            })
            return HttpResponseNotFound(response)
        except KeyError:
            errors.append(f"The language \"{language_string}\" isn't valid. \
                    Double-check your URL and try again.")

    if errors:
        return render_errors(request, errors)

    all_categories = []

    for (category_key, category) in meta_structure.categories.items():
        concepts_list = [concepts_data(key, name, languages) for (key, name) in category.items()]

        all_categories.append({
            "id": category_key,
            "concepts": concepts_list
        })

    title = ""
    if len(languages) == 1:
        title = f"Reference for {languages[0].friendly_name}"
    else:
        title = f"Comparing {', '.join([l.friendly_name for l in languages[:-1]])}\
                and {languages[-1].friendly_name}"


    response = {
        "title": title,
        "concept": meta_structure.key,
        "concept_friendly_name": meta_structure.friendly_name,
        "languages": [
            { "key": language.key, "friendly_name": language.friendly_name }
            for language in languages
        ],
        "categories": all_categories,
        "description": f"Code Thesaurus: {title}"
    }

    return render(request, 'concepts.html', response)


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
    :param lang: the key of the language to fetch concept key from
    :return: formatted HTML for the comment
    """
    if not lang.concept_implemented(concept_key) and lang.concept_comment(concept_key) == "":
        return "Not Implemented In This Language"
    return lang.concept_comment(concept_key)


def concepts_data(key, name, languages):
    """
    Generates the comparision object of a single concept

    :param key: key of the concept
    :param name: name of the concept
    :param languages: list of languages to compare / get a reference for
    :return: string with code with applied HTML formatting
    """
    return {
        "id": key,
        "name": name,
        "data": [{
            "code": format_code_for_display(key, lang),
            "comment": format_comment_for_display(key, lang)
        } for lang in languages ],
    }


def render_errors(request, errors):
    """Render a list of errors with errormisc template"""
    error_page_data = {
        "errors": errors
    }
    response = render(request, 'errormisc.html', error_page_data)

    return HttpResponseNotFound(response)
