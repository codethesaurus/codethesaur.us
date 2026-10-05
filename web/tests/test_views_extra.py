import re
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from web.models import LookupData, MissingLookup, SiteVisit


class TestViewsExtra(TestCase):
    def test_concepts_invalid_structure(self):
        url = reverse('index') + '?concept=invalid_struct&entry=python%3B3'
        response = self.client.get(url)
        # Should show errors
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertContains(response, "structure/concept isn", status_code=HTTPStatus.NOT_FOUND)

    def test_concepts_invalid_entry(self):
        url = reverse('index') + '?concept=data_types&entry=invalid_lang%3B1'
        response = self.client.get(url)
        # Should show errors
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertContains(response, "entry", status_code=HTTPStatus.NOT_FOUND)
        self.assertContains(response, "isn", status_code=HTTPStatus.NOT_FOUND)
        self.assertContains(response, "valid", status_code=HTTPStatus.NOT_FOUND)

    def test_concepts_missing_version_file(self):
        # python exists, but let's try a version that doesn't have data_types.json
        # Note: If it doesn't exist at all, it might be a MissingEntryError if not in meta_info.json
        # but if it is in meta_info but file is missing, it's MissingStructureError.
        # Python 2 is likely in meta_info but might not have all files.
        url = reverse('index') + '?concept=queries&entry=python%3B3'
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateUsed(response, "error_missing_structure.html")

    def test_single_entry_reference(self):
        url = reverse('index') + '?concept=data_types&entry=python%3B3'
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Reference for Python (version 3)')

    def test_api_reference_invalid(self):
        url = reverse('api.reference', kwargs={
            'structure_key': 'invalid_struct',
            'lang': 'python',
            'version': '3'
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_api_compare_invalid_lang(self):
        url = reverse('api.compare', kwargs={
            'structure_key': 'data_types',
            'lang1': 'python',
            'version1': '3',
            'lang2': 'invalid_lang',
            'version2': '1'
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_statistics_view(self):
        url = reverse('statistics')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'statistics.html')

    def test_about_view(self):
        url = reverse('about')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'about.html')

    def test_compare_intro_names_the_concept(self):
        """the intro sentence must name the concept, not render a blank gap"""
        url = reverse('index') + '?concept=functions&entry=python%3B3&entry=javascript'
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Functions, Methods, and Subroutines')
        self.assertNotContains(response, 'show the  syntax')

    def test_compare_intro_lists_both_entries(self):
        url = reverse('index') + '?concept=functions&entry=python%3B3&entry=javascript'
        response = self.client.get(url)
        self.assertContains(response, 'Python (version 3)')
        self.assertContains(response, 'JavaScript')

    def test_reference_intro_is_not_broken_grammar(self):
        """a single-language reference sheet must not say 'side by side'"""
        url = reverse('index') + '?concept=data_types&entry=python%3B3'
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Data Types')
        self.assertNotContains(response, 'side by side</p>')

    def test_unknown_concept_is_not_rendered_as_code(self):
        """the literal string 'Unknown' must never be styled as a code sample"""
        url = reverse('index') + '?concept=functions&entry=python%3B3&entry=javascript'
        response = self.client.get(url)
        self.assertNotContains(response, '>Unknown<')

    def test_not_implemented_uses_a_placeholder_block(self):
        """not-implemented concepts get a styled placeholder, not bare prose"""
        url = reverse('index') + '?concept=functions&entry=python%3B3&entry=lua;5'
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotContains(response, '>Not Implemented<')
        self.assertContains(response, 'ct-placeholder')

    def test_missing_entries_alert_is_styled(self):
        """`alert-link` is not a Bootstrap 5 class, so the warning rendered unstyled"""
        url = reverse('index') + '?concept=functions&entry=python%3B3&entry=lua;5'
        response = self.client.get(url)
        self.assertNotContains(response, 'alert alert-link')
        self.assertContains(response, 'alert alert-warning')

    def test_concepts_page_has_no_duplicate_ids(self):
        """`start-of-row` was repeated once per column, producing duplicate DOM ids"""
        url = reverse('index') + '?concept=functions&entry=python%3B3&entry=javascript'
        response = self.client.get(url)
        ids = re.findall(r'\sid="([^"]+)"', response.content.decode('utf-8'))
        duplicates = {i for i in ids if ids.count(i) > 1}
        self.assertEqual(duplicates, set())

    def test_index_does_not_expose_unused_context(self):
        """`randomLanguages` is computed in the view but never used by any template"""
        url = reverse('index')
        response = self.client.get(url)
        self.assertNotIn('randomLanguages', response.context)

    def test_compare_cards_label_their_language(self):
        """stacked mobile cards must each name their language, not rely on a detached header"""
        url = reverse('index') + '?concept=functions&entry=python%3B3&entry=javascript'
        response = self.client.get(url)
        html = response.content.decode('utf-8')

        # every card in a row is labelled: the concept cell plus each implementation
        cards = html.count(' ct-entry-card"')
        concept_cells = html.count(' ct-concept-cell"')
        self.assertGreater(cards, 0)
        self.assertGreater(concept_cells, 0)
        self.assertEqual(cards + concept_cells, html.count('class="ct-cell-label"'))
        # both columns are labelled
        self.assertIn('ct-cell-label-name">Python</span>', html)
        self.assertIn('ct-cell-label-name">JavaScript</span>', html)

    def test_reference_cards_label_their_language(self):
        url = reverse('index') + '?concept=data_types&entry=python%3B3'
        response = self.client.get(url)

        self.assertContains(response, 'ct-cell-label-name">Python</span>')


class TestHeadingOrder(TestCase):
    """headings must descend one level at a time so screen readers can navigate them"""

    def _levels(self, html):
        return [int(m) for m in re.findall(r'<h([1-6])\b', html)]

    def _assert_no_skipped_levels(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        levels = self._levels(response.content.decode('utf-8'))
        self.assertGreater(len(levels), 0)
        self.assertEqual(levels[0], 1, "each page must start with a single h1")
        for index in range(1, len(levels)):
            self.assertLessEqual(
                levels[index] - levels[index - 1], 1,
                f"heading jumps from h{levels[index - 1]} to h{levels[index]}"
            )

    def test_home_headings_do_not_skip_levels(self):
        self._assert_no_skipped_levels(reverse('index'))

    def test_about_headings_do_not_skip_levels(self):
        self._assert_no_skipped_levels(reverse('about'))

    def test_statistics_headings_do_not_skip_levels(self):
        self._assert_no_skipped_levels(reverse('statistics'))

    def test_concepts_headings_do_not_skip_levels(self):
        self._assert_no_skipped_levels(
            reverse('index') + '?concept=functions&entry=python%3B3&entry=javascript'
        )


class TestStatisticsPage(TestCase):
    """the statistics page needs readable headers and non-visual alternatives to its charts"""

    def _html(self):
        response = self.client.get(reverse('statistics'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        return response.content.decode('utf-8')

    def test_light_header_never_carries_white_text(self):
        """white on Bootstrap's cyan `bg-info` is 1.96:1"""
        html = self._html()
        self.assertNotIn('bg-info text-white', html)

    def test_charts_expose_a_text_alternative(self):
        """canvas is invisible to assistive tech, so each needs a name and a data table"""
        html = self._html()

        for chart_id in ('languagesChart', 'conceptLangsChart', 'structuresChart'):
            with self.subTest(chart=chart_id):
                tag = re.search(rf'<canvas[^>]*id="{chart_id}"[^>]*>', html)
                self.assertIsNotNone(tag, f"{chart_id} must exist")
                self.assertIn('role="img"', tag.group(0))
                self.assertIn('aria-label=', tag.group(0))

        # one collapsible data table per chart
        self.assertEqual(html.count('<details>'), 3)
        self.assertEqual(html.count('class="ct-chart-data"'), 3)
        self.assertEqual(html.count('View data as a table'), 3)

    def test_contributors_image_alt_reads_as_a_link_destination(self):
        """the link wraps only this image, so its alt text is the link's accessible name"""
        response = self.client.get(reverse('about'))
        html = response.content.decode('utf-8')

        match = re.search(r'<a href="[^"]*graphs/contributors">\s*<img[^>]*>', html, re.DOTALL)
        self.assertIsNotNone(match)
        alt = re.search(r'alt="([^"]*)"', match.group(0)).group(1)
        with self.subTest(alt=alt):
            self.assertNotIn('An image', alt)
            self.assertIn('contributors', alt)

    def test_data_tables_are_wrapped_for_horizontal_overflow(self):
        """unwrapped wide tables pushed the whole statistics page sideways on phones"""
        visit = SiteVisit.objects.create(
            url='https://codethesaur.us/', user_agent='pytest', referer='')
        LookupData.objects.create(
            entry1='python', version1='3', entry2='javascript', version2='',
            structure='functions', site_visit=visit)
        LookupData.objects.create(
            entry1='ruby', version1='', entry2='', version2='', structure='functions',
            site_visit=visit)
        MissingLookup.objects.create(
            item_type='language', item_value='cobol', language_context='', site_visit=visit)

        html = self._html()

        tables = re.findall(r'<table class="table table-hover table-sm">', html)
        self.assertEqual(len(tables), 3)
        self.assertEqual(html.count('<div class="table-responsive">'), 3)

    def test_chart_data_is_collapsed_so_it_cannot_widen_the_page(self):
        """a visually-hidden wide table still forced horizontal scrolling on phones"""
        html = self._html()

        blocks = re.findall(r'<div class="ct-chart-data">(.*?)</details>', html, re.DOTALL)
        self.assertEqual(len(blocks), 3)
        for block in blocks:
            with self.subTest(block=block[:40]):
                # the table sits inside a collapsed <details>, so it is out of the layout
                self.assertLess(block.index('<details'), block.index('<table'))

    def test_data_tables_are_rendered_server_side(self):
        """the fallback tables must not depend on JavaScript to exist"""
        html = self._html()

        self.assertIn('Language', html)
        self.assertIn('Concept', html)

    def test_every_column_header_is_scoped(self):
        """column headers must be programmatically associated with their cells"""
        html = self._html()

        headers = re.findall(r'<th\b[^>]*>', html)
        self.assertGreater(len(headers), 0)
        for header in headers:
            with self.subTest(header=header):
                self.assertIn('scope="col"', header)

    def test_decorative_icons_are_hidden_from_assistive_tech(self):
        """font-awesome glyphs inside headings should not be announced"""
        html = self._html()

        icons = re.findall(r'<i class="fas fa-[a-z-]+"[^>]*></i>', html)
        self.assertGreater(len(icons), 0, "sanity check: the page still uses these icons")
        for icon in icons:
            with self.subTest(icon=icon):
                self.assertIn('aria-hidden="true"', icon)


class TestSiteChrome(TestCase):
    """the shared shell: skip link, navigation state, and back-to-top"""

    def _pages(self):
        """(path, nav href) for each page, built with reverse to keep the trailing slashes"""
        return [
            (reverse('index'), reverse('index')),
            (reverse('about'), reverse('about')),
            (reverse('statistics'), reverse('statistics')),
        ]

    def test_skip_link_is_first_and_resolves(self):
        """keyboard users need a way past the nav, and its target must exist"""
        for path, _ in self._pages():
            with self.subTest(path=path):
                html = self.client.get(path).content.decode('utf-8')

                link = re.search(r'<a[^>]*class="skip-link[^"]*"[^>]*href="#([^"]+)"', html)
                self.assertIsNotNone(link, f"{path} needs a skip link")
                target = link.group(1)
                self.assertLess(
                    html.index('class="skip-link'), html.index('<nav'),
                    "the skip link must come before the navigation"
                )
                self.assertIn(f'id="{target}"', html, "the skip link target must exist")

    def test_exactly_one_nav_item_marks_the_current_page(self):
        """`active`/`aria-current` was hardcoded to Home, so it was wrong everywhere else"""
        for path, expected_href in self._pages():
            with self.subTest(path=path):
                html = self.client.get(path).content.decode('utf-8')
                nav = re.search(r'<nav\b.*?</nav>', html, re.DOTALL)
                self.assertIsNotNone(nav)

                current = re.findall(r'aria-current="page"', nav.group(0))
                self.assertEqual(len(current), 1, f"{path} must mark exactly one nav item")

                # the marked link must be the one whose href matches this page
                marked = re.search(
                    r'<a[^>]*aria-current="page"[^>]*href="([^"]*)"', nav.group(0)
                ) or re.search(r'<a[^>]*href="([^"]*)"[^>]*aria-current="page"', nav.group(0))
                self.assertIsNotNone(marked)
                self.assertEqual(marked.group(1), expected_href)

    def test_external_nav_links_open_safely(self):
        html = self.client.get(reverse('index')).content.decode('utf-8')
        nav = re.search(r'<nav\b.*?</nav>', html, re.DOTALL).group(0)

        for href in ('https://docs.codethesaur.us', 'https://docs.codethesaur.us/contributing/'):
            with self.subTest(href=href):
                anchor = re.search(rf'<a[^>]*href="{re.escape(href)}"[^>]*>', nav, re.DOTALL)
                self.assertIsNotNone(anchor)
                self.assertIn('rel="noopener"', anchor.group(0))

    def test_back_to_top_points_at_a_real_target(self):
        """`href="#"` went nowhere"""
        html = self.client.get(reverse('index')).content.decode('utf-8')

        anchor = re.search(r'<a[^>]*class="toTop"[^>]*href="#([^"]*)"', html, re.DOTALL)
        self.assertIsNotNone(anchor)
        self.assertNotEqual(anchor.group(1), '', 'back-to-top must not link to an empty fragment')
        self.assertIn(f'id="{anchor.group(1)}"', html)
