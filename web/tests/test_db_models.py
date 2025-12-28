from django.test import TestCase
from web.models import SiteVisit, LookupData

class TestDbModels(TestCase):
    def test_site_visit_creation(self):
        visit = SiteVisit.objects.create(
            url="http://example.com",
            user_agent="Mozilla/5.0",
            referer="http://google.com"
        )
        self.assertIsNotNone(visit.id)
        self.assertEqual(visit.url, "http://example.com")
        self.assertEqual(visit.user_agent, "Mozilla/5.0")
        self.assertEqual(visit.referer, "http://google.com")
        self.assertIsNotNone(visit.date_time)

    def test_lookup_data_creation(self):
        visit = SiteVisit.objects.create(
            url="http://example.com",
            user_agent="Mozilla/5.0",
            referer="http://google.com"
        )
        lookup = LookupData.objects.create(
            language1="python",
            version1="3",
            language2="javascript",
            version2="es6",
            structure="data_types",
            site_visit=visit
        )
        self.assertIsNotNone(lookup.id)
        self.assertEqual(lookup.language1, "python")
        self.assertEqual(lookup.version1, "3")
        self.assertEqual(lookup.language2, "javascript")
        self.assertEqual(lookup.version2, "es6")
        self.assertEqual(lookup.structure, "data_types")
        self.assertEqual(lookup.site_visit, visit)
