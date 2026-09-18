"""codethesaur.us views"""
import logging
import os
import random

from django.conf import settings
from django.http import (
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
    HttpResponseServerError
)
from django.db import transaction
from django.db.models import Count, Q
from django.shortcuts import HttpResponse, render
from django.utils.html import escape, strip_tags
from django.views.decorators.http import require_http_methods
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

from codethesaurus.settings import BASE_DIR
from web.models import (
    ThesaurusEntry,
    LookupData,
    ThesaurusMetaInfo,
    MissingEntryError,
    MissingLookup,
    MissingStructureError,
    SiteVisit,
)
from web.thesaurus_template_generators import generate_entry_template


def store_url_info(request):
    try:
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
            referer=referer,
        )
        with transaction.atomic():
            visit.save()
        return visit
    except Exception as e:
        logging.error(f"Failed to store URL info: {e}")
        return None


def store_lookup_info(request, visit, entry1, version1, entry2, version2, structure):
    if not visit:
        return
    try:
        info = LookupData(
            entry1=entry1,
            version1=version1,
            entry2=entry2,
            version2=version2,
            structure=structure,
            site_visit=visit
        )
        with transaction.atomic():
            info.save()
    except Exception as e:
        logging.error(f"Failed to store lookup info: {e}")


def store_missing_info(visit, item_type, item_value, language_context=None):
    if not visit:
        return
    try:
        info = MissingLookup(
            item_type=item_type,
            item_value=item_value,
            language_context=language_context,
            site_visit=visit
        )
        with transaction.atomic():
            info.save()
    except Exception as e:
        logging.error(f"Failed to store missing info: {e}")


@require_http_methods(['GET'])
def index(request):
    """
    Renders the home page (/)

    :param request: HttpRequest object
    :return: HttpResponse object with rendered object of the page
    """

    store_url_info(request)
    if "entry" in request.GET and "concept" in request.GET:
        return concepts(request)

    meta_info = ThesaurusMetaInfo()
    thesauruses_dir = os.path.join(BASE_DIR, 'web', 'thesauruses')
    meta_dir = os.path.join(thesauruses_dir, '_meta')
    meta_concepts = os.listdir(meta_dir)

    meta_data_entries = dict()
    for key in meta_info.languages:
        entry = meta_info.entry(key)
        # Find which category this entry belongs to
        category_name = "Other"
        for cat_key, cat_label in meta_info.categories.items():
            if os.path.exists(os.path.join(thesauruses_dir, cat_key, key)):
                category_name = cat_label
                break
        
        meta_data_entries[key] = {
            "name": entry.name,
            "category": category_name,
            "versions": [{
                "name": entry.name,
                "version": version,
                "availStructs": []
            } for version in entry.versions()]
        }

    random_entries = random.sample(list(meta_data_entries.values()), k=min(3, len(meta_data_entries)))

    for category in os.listdir(thesauruses_dir):
        category_path = os.path.join(thesauruses_dir, category)
        if category == '_meta' or not os.path.isdir(category_path):
            continue
        for entry_dir in os.listdir(category_path):
            entry_path = os.path.join(category_path, entry_dir)
            if not os.path.isdir(entry_path):
                continue
            for ver in os.listdir(entry_path):
                ver_path = os.path.join(entry_path, ver)
                if not os.path.isdir(ver_path):
                    continue
                for concept_json in meta_concepts:
                    concept_name = concept_json.split('.')[0]
                    if concept_json in os.listdir(ver_path):
                        if entry_dir in meta_data_entries:
                            for i in meta_data_entries[entry_dir]['versions']:
                                if i['version'] == ver:
                                    i['availStructs'].append(concept_name)
                                    break

    # Group meta_data_entries by category for the template
    grouped_entries = []
    for cat_key, cat_label in meta_info.categories.items():
        category_data = {
            "key": cat_key,
            "label": cat_label,
            "entries": {},
            "structures": meta_info.category_structures.get(cat_key, {})
        }
        for key, data in meta_data_entries.items():
            if data['category'] == cat_label:
                category_data["entries"][key] = data['versions']
        
        if category_data["entries"]:
            grouped_entries.append(category_data)

    content = {
        'title': 'Welcome',
        'languages': grouped_entries,
        'structures': meta_info.structures,
        'randomLanguages': random_entries,
        'description': 'Code Thesaurus: A polyglot developer reference tool'
    }
    return render(request, 'index.html', content)


@require_http_methods(['GET'])
def statistics(request):
    """
    Renders the statistics page (/statistics/)

    :param request: HttpRequest object
    :return: HttpResponse object with rendered object of the page
    """
    store_url_info(request)

    meta_info = ThesaurusMetaInfo()

    # Most popular languages (considering both language1 and language2)
    # We need to aggregate counts for each language across both fields.
    # A simple way is to get counts for each and then merge them in Python.
    entry1_counts = LookupData.objects.values('entry1').annotate(count=Count('entry1'))
    entry2_counts = LookupData.objects.exclude(entry2='').values('entry2').annotate(count=Count('entry2'))

    combined_counts = {}
    for item in entry1_counts:
        entry = item['entry1']
        combined_counts[entry] = combined_counts.get(entry, 0) + item['count']
    for item in entry2_counts:
        entry = item['entry2']
        combined_counts[entry] = combined_counts.get(entry, 0) + item['count']

    sorted_langs = sorted(combined_counts.items(), key=lambda x: x[1], reverse=True)
    popular_languages = []
    for lang_key, count in sorted_langs[:10]:
        try:
            name = meta_info.entry_name(lang_key)
        except (KeyError, MissingEntryError):
            name = lang_key
        popular_languages.append({'name': name, 'count': count})

    # Most popular structures
    structure_counts = LookupData.objects.values('structure').annotate(count=Count('structure')).order_by('-count')[:10]
    popular_structures = []
    for item in structure_counts:
        try:
            name = meta_info.structure_name(item['structure'])
        except (KeyError, MissingStructureError):
            name = item['structure']
        popular_structures.append({'name': name, 'count': item['count']})

    # Most popular comparisons
    # Using a technique to ensure (lang1, lang2) is treated the same as (lang2, lang1) if we wanted to,
    # but let's keep it simple and just look at pairs as they are.
    comparison_counts = LookupData.objects.exclude(entry2='').values('entry1', 'entry2').annotate(count=Count('id')).order_by('-count')[:10]
    popular_comparisons = []
    for item in comparison_counts:
        try:
            name1 = meta_info.entry_name(item['entry1'])
        except (KeyError, MissingEntryError):
            name1 = item['entry1']
        try:
            name2 = meta_info.entry_name(item['entry2'])
        except (KeyError, MissingEntryError):
            name2 = item['entry2']
        popular_comparisons.append({'lang1': name1, 'lang2': name2, 'count': item['count']})

    total_visits = SiteVisit.objects.count()
    total_lookups = LookupData.objects.count()

    # Unique language comparisons
    unique_comparisons_count = LookupData.objects.exclude(entry2='').values('entry1', 'entry2').distinct().count()

    # Unique concept categories (structures) looked up
    unique_structures_count = LookupData.objects.values('structure').distinct().count()

    # Most popular concept-language pairs (e.g., Javascript functions)
    concept_lang_counts = {}
    for entry in LookupData.objects.all():
        # Count for language 1
        key1 = (entry.entry1, entry.structure)
        concept_lang_counts[key1] = concept_lang_counts[key1] + 1 if key1 in concept_lang_counts else 1
        # Count for language 2 if it exists
        if entry.entry2:
            key2 = (entry.entry2, entry.structure)
            concept_lang_counts[key2] = concept_lang_counts[key2] + 1 if key2 in concept_lang_counts else 1
    
    sorted_concept_langs = sorted(concept_lang_counts.items(), key=lambda x: x[1], reverse=True)
    popular_concept_langs = []
    for (lang_key, struct_key), count in sorted_concept_langs[:10]:
        try:
            lang_name = meta_info.entry_name(lang_key)
        except (KeyError, MissingEntryError):
            lang_name = lang_key
        try:
            struct_name = meta_info.structure_name(struct_key)
        except (KeyError, MissingStructureError):
            struct_name = struct_key
        popular_concept_langs.append({
            'label': f"{lang_name} {struct_name}",
            'lang': lang_name,
            'struct': struct_name,
            'count': count
        })

    # Recent lookups
    recent_lookups_query = LookupData.objects.order_by('-date_time')[:10]
    recent_lookups = []
    for item in recent_lookups_query:
        try:
            name1 = meta_info.entry_name(item.entry1)
        except (KeyError, MissingEntryError):
            name1 = item.entry1
        try:
            name2 = meta_info.entry_name(item.entry2) if item.entry2 else None
        except (KeyError, MissingEntryError):
            name2 = item.entry2
        
        try:
            struct_name = meta_info.structure_name(item.structure)
        except (KeyError, MissingStructureError):
            struct_name = item.structure

        recent_lookups.append({
            'lang1': name1,
            'lang2': name2,
            'structure': struct_name,
            'date_time': item.date_time
        })

    # Missing items statistics
    missing_items_counts = MissingLookup.objects.values('item_type', 'item_value', 'language_context') \
        .annotate(count=Count('id')).order_by('-count')[:15]
    
    missing_items = []
    for item in missing_items_counts:
        label = item['item_value']
        if item['item_type'] == 'language':
            label = f"ThesaurusEntry: {item['item_value']}"
        elif item['item_type'] == 'structure':
            try:
                lang_name = meta_info.entry_name(item['language_context'])
            except (KeyError, MissingEntryError):
                lang_name = item['language_context']
            label = f"Structure: {item['item_value']} (for {lang_name})"
        elif item['item_type'] == 'concept':
            try:
                lang_name = meta_info.entry_name(item['language_context'])
            except (KeyError, MissingEntryError):
                lang_name = item['language_context']
            label = f"Concept: {item['item_value']} (missing in {lang_name})"
        
        missing_items.append({
            'label': label,
            'count': item['count'],
            'type': item['item_type']
        })

    import json
    context = {
        'title': 'Statistics',
        'popular_languages': popular_languages,
        'popular_structures': popular_structures,
        'popular_comparisons': popular_comparisons,
        'popular_concept_langs': popular_concept_langs,
        'recent_lookups': recent_lookups,
        'missing_items': missing_items,
        'total_visits': total_visits,
        'total_lookups': total_lookups,
        'unique_comparisons_count': unique_comparisons_count,
        'unique_structures_count': unique_structures_count,
        'popular_languages_json': json.dumps(popular_languages),
        'popular_structures_json': json.dumps(popular_structures),
        'popular_concept_langs_json': json.dumps(popular_concept_langs),
    }

    return render(request, 'statistics.html', context)


@require_http_methods(['GET'])
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


@require_http_methods(['GET'])
def concepts(request):
    """
    Renders the page comparing two language structures (/compare)

    :param request: HttpRequest object
    :return: HttpResponse object with rendered object of the page
    """
    visit = store_url_info(request)

    entry_strings, structure_key, errors = clean_concepts_parameters(request.GET)
    if errors:
        return render_errors(request, errors)

    meta_info = ThesaurusMetaInfo()
    try:
        meta_structure = meta_info.structure(structure_key)
    except KeyError:
        return render_errors(request, ["The structure/concept isn't valid. Double-check your URL and try again."])

    try:
        entries = meta_info.load_entries(entry_strings, meta_structure)
    except MissingStructureError as missing_structure:
        store_missing_info(
            visit,
            'structure',
            missing_structure.structure.key,
            missing_structure.entry_key
        )
        return HttpResponseNotFound(render(
            request,
            "error_missing_structure.html",
            {
                "key": missing_structure.structure.key,
                "name": missing_structure.structure.name,
                "entry": missing_structure.entry_key,
                "entry_name": missing_structure.entry_name,
                "version": missing_structure.entry_version,
                "template": generate_entry_template(
                    missing_structure.entry_key,
                    missing_structure.structure.key,
                    missing_structure.entry_version
                )
            }
        ))
    except MissingEntryError as missing_entry:
        store_missing_info(visit, 'language', missing_entry.key)
        errors.append(f"The entry \"{missing_entry.key}\" isn't valid. Double-check your URL and try again.")

    if errors:
        return render_errors(request, errors)
        
    store_lookup_info(
        request,
        visit,
        entries[0].key,
        entries[0].version,
        entries[1].key if len(entries) > 1 else "",
        entries[1].version if len(entries) > 1 else "",
        meta_structure.key
    )

    lexers = [get_highlighter(entry.key) for entry in entries]
    all_categories = []

    for (category_key, category) in meta_structure.categories.items():
        concept_keys = list(category.keys())
        concepts_list = [concepts_data(key, name, entries, lexers, visit) for (key, name) in category.items()]

        category_entry = {
            "key": category_key,
            "concepts": concepts_list,
            "is_incomplete": []
        }

        for entry in entries:
            is_incomplete = False
            # If nothing in this category is implemented for this language
            if not entry.has_any_implemented_in_category(concept_keys):
                is_incomplete = True
            # OR if at least one concept is missing code/comment
            elif entry.is_category_incomplete(concept_keys):
                is_incomplete = True
            
            category_entry["is_incomplete"].append(is_incomplete)
            
        all_categories.append(category_entry)

    for i, entry in enumerate(entries):
        entry._is_incomplete = any(cat["is_incomplete"][i] for cat in all_categories)

    return render_concepts(request, entries, meta_structure, all_categories)


@require_http_methods(['GET'])
def render_concepts(request, entries, structure, all_categories):
    """Renders the `structure` page for all `entries`"""

    entry_name_versions = [f"{l.name} (version {l.version})" for l in entries]
    if len(entries) == 1:
        title = f"Reference for {entry_name_versions[0]}"
    else:
        title = f"Comparing {', '.join(entry_name_versions[:-1])} and {entry_name_versions[-1]}"


    response = {
        "title": title,
        "concept": structure.key,
        "concept_name": structure.name,
        "languages": [
            {
                "key": entry.key,
                "version": entry.version,
                "name": entry.name,
                "is_incomplete": entry._is_incomplete,
            }
            for entry in entries
        ],
        "categories": all_categories,
        "description": f"Code Thesaurus: {title}"
    }

    return render(request, 'concepts.html', response)


def error_handler_400_bad_request(request, exception):
    """
    Renders the page for a generic client error (HTTP 400)

    :param request: HttpRequest object
    :param exception: details about the exception
    :return: HttpResponse object with rendered object of the page
    """
    store_url_info(request)

    logging.error(exception)
    response = render(request, 'error400.html')
    return HttpResponseBadRequest(response)


def error_handler_403_forbidden(request, exception):
    """
    Renders the page for a forbidden error (HTTP 403)

    :param request: HttpRequest object
    :param exception: details about the exception
    :return: HttpResponse object with rendered object of the page
    """
    store_url_info(request)

    logging.error(exception)
    response = render(request, 'error403.html')
    return HttpResponseForbidden(response)


def error_handler_404_not_found(request, exception):
    """
    Renders the page for a file not found error (HTTP 404)

    :param request: HttpRequest object
    :param exception: details about the exception
    :return: HttpResponse object with rendered object of the page
    """
    store_url_info(request)

    logging.info(request)
    response = render(request, 'error404.html')
    return HttpResponseNotFound(response)


def error_handler_500_server_error(request):
    """
    Renders the page for a generic server error (HTTP 500)

    :param request: HttpRequest object
    :return: HttpResponse object with rendered object of the page
    """
    try:
        store_url_info(request)
    except Exception:
        pass

    logging.error(f"500 error at {request.get_full_path()}")
    response = render(request, 'error500.html')
    return HttpResponseServerError(response)

#get lexer 
def get_highlighter(entry_key):
    SIMILAR_LEXERS = settings.SIMILAR_LEXERS
    try:
        lexer = get_lexer_by_name(entry_key, startinline=True)
    except ClassNotFound:
        lexer = get_lexer_by_name(SIMILAR_LEXERS.get(entry_key, "text"), startinline=True)
    return lexer

# Helper functions
def format_code_for_display(concept_key, entry, lexer=None):
    """
    Returns the formatted HTML formatted syntax-highlighted text for a concept key (from a meta
            thesaurus file) and an entry

    :param concept_key: name of the key to format
    :param entry: entry to format it (in meta entry/syntax highlighter format)
    :param lexer: optional pre-fetched lexer
    :return: string with code with applied HTML formatting
    """

    if entry.concept_unknown(concept_key) or entry.concept_code(concept_key) is None:
        return "Unknown"
    if entry.concept_implemented(concept_key):
        if lexer is None:
            lexer = get_highlighter(entry.key)
        return highlight(
            entry.concept_code(concept_key),
            lexer,
            HtmlFormatter()
        )
    return None


def format_comment_for_display(concept_key, entry):
    """
    Returns the formatted HTML formatted comment text for a concept key (from a meta thesaurus
            file) and an entry

    :param concept_key: the concept key located in the meta thesaurus JSON file
    :param entry: the entry to fetch concept key from
    :return: formatted HTML for the comment
    """
    if not entry.concept_implemented(concept_key) and entry.concept_comment(concept_key) == "":
        return "Not Implemented"
    return entry.concept_comment(concept_key)


def concepts_data(key, name, entries, lexers=None, visit=None):
    """
    Generates the comparison object of a single concept

    :param key: key of the concept
    :param name: name of the concept
    :param entries: list of entries to compare / get a reference for
    :param lexers: optional list of pre-fetched lexers corresponding to entries
    :param visit: optional SiteVisit for logging missing items
    :return: dict with code and comment for each entry
    """
    data = []
    for i, entry in enumerate(entries):
        lexer = lexers[i] if lexers else None
        
        # Log if concept is not implemented
        if visit and not entry.concept_implemented(key):
            store_missing_info(visit, 'concept', key, entry.key)
            
        data.append({
            "code": format_code_for_display(key, entry, lexer),
            "comment": format_comment_for_display(key, entry)
        })

    return {
        "key": key,
        "name": name,
        "data": data,
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

    entry_strings = list(parameters.getlist('entry'))
    # legacy parameter names
    if "lang" in parameters:
        entry_strings.append(parameters['lang'])
    if "lang1" in parameters:
        entry_strings.append(parameters['lang1'])
    if "lang2" in parameters:
        entry_strings.append(parameters['lang2'])

    entry_keys_versions = []
    for entry_str in entry_strings:
        key_version = escape(strip_tags(entry_str)).split(";")
        try:
            entry_keys_versions.append((key_version[0], key_version[1]))
        except IndexError:
            entry_keys_versions.append((key_version[0], None))
    structure_key = escape(strip_tags(parameters.get('concept', '')))

    errors = []
    if not structure_key:
        errors.append("The URL didn't specify a structure/concept to look up.")
    if not entry_keys_versions:
        errors.append("The URL didn't specify any entries to look up.")
    return entry_keys_versions, structure_key, errors


# API functions

def api_reference(request, structure_key, lang, version):
    """
    Returns the filled template for a given language and concept

    :param request: HttpRequest object
    :param structure_key: concept
    :param lang: language
    :param version: version
    :return: HttpResponse filled template of concept
    """
    visit = store_url_info(request)

    entry_obj = ThesaurusEntry(lang, "")

    try:
        response = entry_obj.load_filled_concepts(structure_key, version)
    except Exception as e:
        # Determine if it's a language or structure issue
        # If ThesaurusEntry(lang, "") failed to find versions, it might be a language issue
        if not entry_obj.versions():
            store_missing_info(visit, 'language', lang)
        else:
            store_missing_info(visit, 'structure', structure_key, lang)
        return error_handler_404_not_found(request, e)

    if response is False:
        store_missing_info(visit, 'structure', structure_key, lang)
        return HttpResponseNotFound()

    store_lookup_info(
        request,
        visit,
        lang,
        version,
        "",
        "",
        structure_key
    )

    return HttpResponse(response, content_type="application/json")

def api_compare(request, structure_key, lang1, version1, lang2, version2):
    """
    Returns the comparison between two languages for a given structure

    :param request: HttpRequest object
    :param structure_key: concept
    :param lang1: language 1
    :param version1: version 1
    :param lang2: language 2
    :param version2: version 2
    :return: HttpResponse response
    """
    visit = store_url_info(request)

    try:
        response = ThesaurusEntry(lang1, "").load_comparison(structure_key, lang2, version2, version1)
    except Exception:
        # Simple logging for now
        store_missing_info(visit, 'structure', structure_key, f"{lang1}/{lang2}")
        return HttpResponseNotFound()

    if response is False:
        store_missing_info(visit, 'structure', structure_key, f"{lang1}/{lang2}")
        return HttpResponseNotFound()

    store_lookup_info(
        request,
        visit,
        lang1,
        version1,
        lang2,
        version2,
        structure_key
    )

    return HttpResponse(response, content_type="application/json")
