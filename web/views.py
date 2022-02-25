"""codethesaur.us views"""
import random
import os

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

from web.models import MetaInfo, SiteVisit, LookupData, MissingStructureError, MissingLanguageError
from web.thesaurus_template_generators import generate_language_template

from codethesaurus.settings import BASE_DIR


def store_url_info(request):
    if 'HTTP_USER_AGENT' in request.META:
        user_agent = request.META['HTTP_USER_AGENT']
    else:
        user_agent = ""

    if 'HTTP_REFERER' in request.META:
        referer = request.META['HTTP_REFERER']
    else:
        referer = ""

    visit = SiteVisit(
        url=request.get_full_path(),
        user_agent=user_agent,
        referer=request
    )
    visit.save()
    return visit


def store_lookup_info(request, visit, language1, version1, language2, version2, structure):
    info = LookupData(
        language1=language1,
        version1=version1,
        language2=language2,
        version2=version2,
        structure=structure,
        site_visit=visit
    )
    info.save()


def index(request):
    """
    Renders the home page (/)

    :param request: HttpRequest object
    :return: HttpResponse object with rendered object of the page
    """

    store_url_info(request)
    if "lang" in request.GET and "concept" in request.GET:
        return concepts(request)

    meta_info = MetaInfo()

    meta_data_langs = dict()
    for key in meta_info.languages:
        lang = meta_info.language(key)
        meta_data_langs[key] = [{
            "name": lang.friendly_name,
            "version": version,
            "availStructs": []
        } for version in lang.versions()]

    random_langs = random.sample(list(meta_data_langs.values()), k=3)

    thesauruses_dir = f'{BASE_DIR}/web/thesauruses'
    meta_dir = f'{thesauruses_dir}/_meta'
    meta_concepts = os.listdir(meta_dir)
    for lang in os.listdir(thesauruses_dir):
        if 'meta' in lang:
            continue
        for ver in os.listdir(f'{thesauruses_dir}/{lang}'):
            for concept_json in meta_concepts:
                concept_name = concept_json.split('.')[0]
                if concept_json in os.listdir(f'{thesauruses_dir}/{lang}/{ver}'):
                    for i in meta_data_langs[lang]:
                        if i['version'] == ver:
                            i['availStructs'].append(concept_name)
                            break

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
    store_url_info(request)

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
    visit = store_url_info(request)

    language_strings, structure_key, errors = clean_concepts_parameters(request.GET)
    if errors:
        return render_errors(request, errors)

    meta_info = MetaInfo()
    try:
        meta_structure = meta_info.structure(structure_key)
    except KeyError:
        return render_errors(request, ["The structure/concept isn't valid. \
                Double-check your URL and try again."])

    try:
        languages = meta_info.load_languages(language_strings, meta_structure)
    except MissingStructureError as missing_structure:
        return HttpResponseNotFound(render(
            request,
            "error_missing_structure.html",
            {
                "key": missing_structure.structure.key,
                "name": missing_structure.structure.friendly_name,
                "lang": missing_structure.language_key,
                "lang_name": missing_structure.language_name,
                "version": missing_structure.language_version,
                "template": generate_language_template(
                    missing_structure.language_key,
                    missing_structure.structure.key,
                    missing_structure.language_version
                )
            }
        ))
    except MissingLanguageError as missing_language:
        errors.append(f"The language \"{missing_language.key}\" isn't valid. \
                        Double-check your URL and try again.")

    if errors:
        return render_errors(request, errors)

    if len(languages) == 2:
        store_lookup_info(
            request,
            visit,
            languages[0].key,
            languages[0].version,
            languages[1].key,
            languages[1].version,
            meta_structure.key
        )

    all_categories = []

    for (category_key, category) in meta_structure.categories.items():
        concepts_list = [concepts_data(key, name, languages) for (key, name) in category.items()]

        all_categories.append({
            "id": category_key,
            "concepts": concepts_list
        })

    language_name_versions = [f"{l.friendly_name} ({l.version})" for l in languages]
    if len(languages) == 1:
        title = f"Reference for {language_name_versions[0]}"
    else:
        title = f"Comparing {', '.join(language_name_versions[:-1])}\
                and {language_name_versions[-1]}"


    response = {
        "title": title,
        "concept": meta_structure.key,
        "concept_friendly_name": meta_structure.friendly_name,
        "languages": [
            {
                "key": language.key,
                "version": language.version,
                "friendly_name": language.friendly_name
            }
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
    store_url_info(request)

    response = render(request, 'error400.html')
    return HttpResponseBadRequest(response)


def error_handler_403_forbidden(request, _exception):
    """
    Renders the page for a forbidden error (HTTP 403)

    :param request: HttpRequest object
    :param exception: details about the exception
    :return: HttpResponse object with rendered object of the page
    """
    store_url_info(request)

    response = render(request, 'error403.html')
    return HttpResponseForbidden(response)


def error_handler_404_not_found(request, _exception):
    """
    Renders the page for a file not found error (HTTP 404)

    :param request: HttpRequest object
    :param exception: details about the exception
    :return: HttpResponse object with rendered object of the page
    """
    store_url_info(request)

    response = render(request, 'error404.html')
    return HttpResponseNotFound(response)


def error_handler_500_server_error(request):
    """
    Renders the page for a generic server error (HTTP 500)

    :param request: HttpRequest object
    :return: HttpResponse object with rendered object of the page
    """
    store_url_info(request)

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


def clean_concepts_parameters(parameters):
    """Verify and clean up the parameters for concepts view"""

    language_strings = list(parameters.getlist('lang'))
    # legacy parameter names
    if "lang1" in parameters:
        language_strings.append(parameters['lang1'])
    if "lang2" in parameters:
        language_strings.append(parameters['lang2'])

    language_keys_versions = []
    for lang in language_strings:
        key_version = escape(strip_tags(lang)).split(";")
        try:
            language_keys_versions.append((key_version[0], key_version[1]))
        except IndexError:
            language_keys_versions.append((key_version[0], None))
    structure_key = escape(strip_tags(parameters.get('concept', '')))

    errors = []
    if not structure_key:
        errors.append("The URL didn't specify a structure/concept to look up.")
    if not language_keys_versions:
        errors.append("The URL didn't specify any languages to look up.")
    return language_keys_versions, structure_key, errors
