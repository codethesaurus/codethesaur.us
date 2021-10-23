from django.test import TestCase
from django.template.loader import render_to_string


class TestTemplates(TestCase):

    def test_comparecard(self):
        # no code and no comment
        rendered_template_1 = render_to_string("comparecard.html", {}).strip()
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
            "comparecard.html", {"code": "<b>I am bold!</b>"}
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
            "comparecard.html", {"comment": "I am **bold** and *italic*, `let x = 1`."}
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

        # code and comment (single line)
        rendered_template_4 = render_to_string(
            "comparecard.html",
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

        # no code and comment (multiple lines)
        rendered_template_4 = render_to_string(
            "comparecard.html",
            {
                "code": "",
                "comment": "I am a humble\nmulti-line comment in the\nform of a haiku"
            }
        ).strip()
        self.assertEquals(
            rendered_template_3,
            "<div class=\"card\">\n"
            "    <div class=\"card-body\">\n"
            "    \n"
            "    \n"
            "        <div>\n"
            "            I am a humble<br>multi-line comment in the<br>form of a haiku\n"
            "        </div>\n"
            "    \n"
            "    </div>\n"
            "</div>"
        )