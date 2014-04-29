from unittest import TestCase
from jinja2 import Environment
from lib.jinja2.htmlcompress import HtmlCompress, SelectiveHtmlCompress


class TestHtmlCompress(TestCase):
    def test_html_compress(self):
        env = Environment(extensions=[HtmlCompress])
        template = env.from_string(
            '''
            <div>
               <p>{{ text }}</p>
            </div>
            '''
        )
        self.assertEquals(
            '<div><p>test</p></div>',
            template.render(text='test')
        )

    def test_selective_html_compress(self):
        env = Environment(extensions=[SelectiveHtmlCompress])
        template = env.from_string(
            ''' white space {% strip %}
            <div>
               <p>{{ text }}</p>
            </div>
            {% endstrip %} white space '''
        )
        self.assertEquals(
            'white space <div><p>test</p></div> white space',
            template.render(text='test')
        )
