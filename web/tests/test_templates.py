"""Tests for the templates"""
from django.test import TestCase
from django.template.loader import render_to_string


class TestTemplates(TestCase):
    """TestCase for templates"""

    def test_concept_card(self):
        """test the concept_card template"""
        # no code and no comment
        rendered_template_1 = render_to_string("concept_card.html", {}).strip()
        self.assertEquals(
            rendered_template_1,
            "<div class=\"card\">\n"
            "    <div class=\"card-body\">\n"
            "    \n"
            "    \n"
            "    </div>\n"
            "</div>"
        )

        # code (marked as safe), no comment
        rendered_template_2 = render_to_string(
            "concept_card.html", {"code": "<b>I am bold!</b>"}
        ).strip()
        self.assertEquals(
            rendered_template_2,
            "<div class=\"card\">\n"
            "    <div class=\"card-body\">\n"
            "    \n"
            "        <div class=\"syntax\"><b>I am bold!</b></div>\n"
            "    \n"
            "    \n"
            "    </div>\n"
            "</div>"
        )

        # no code, comment (with markdown format)
        rendered_template_3 = render_to_string(
            "concept_card.html", {"comment": "I am **bold** and *italic*, `let x = 1`."}
        ).strip()
        self.assertEquals(
            rendered_template_3,
            "<div class=\"card\">\n"
            "    <div class=\"card-body\">\n"
            "    \n"
            "    \n"
            "        <div>\n"
            "            I am <strong>bold</strong> and <em>italic</em>, <code>let x = 1</code>.\n"
            "        </div>\n"
            "    \n"
            "    </div>\n"
            "</div>"
        )

        # code and comment
        rendered_template_4 = render_to_string(
            "concept_card.html",
            {
                "code": "<b>I am bold!</b>",
                "comment": "I am **bold** and *italic*, `let x = 1`."
            }
        ).strip()
        self.assertEquals(
            rendered_template_4,
            "<div class=\"card\">\n"
            "    <div class=\"card-body\">\n"
            "    \n"
            "        <div class=\"syntax\"><b>I am bold!</b></div>\n"
            "    \n"
            "    \n"
            "        <div>\n"
            "            I am <strong>bold</strong> and <em>italic</em>, <code>let x = 1</code>.\n"
            "        </div>\n"
            "    \n"
            "    </div>\n"
            "</div>"
        )

        # md url in comment
        rendered_template_5 = render_to_string(
            "concept_card.html",
            {
                "comment": "I am a [url](http://url.com), I am not a url.py"
            }
        ).strip()
        self.assertEquals(
            rendered_template_5,
            "<div class=\"card\">\n"
            "    <div class=\"card-body\">\n"
            "    \n"
            "    \n"
            "        <div>\n"
            "            I am a <a href=\"http://url.com\">url</a>, I am not a url.py\n"
            "        </div>\n"
            "    \n"
            "    </div>\n"
            "</div>"
        )
