''' Sphinx directive for listing Schemdraw Elements

    Use with `.. element_list::` in rst files.
'''
import re

from docutils.parsers.rst import directives
from docutils import nodes

from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective
from sphinx.util.typing import ExtensionMetadata


class SchemElement(SphinxDirective):
    option_spec = {
        'ncols': directives.positive_int,
        'nolabel': directives.flag,
        'module': str,
        'hide_anchors': str,
    }
    has_content = True

    def run(self) -> list[nodes.Node]:
        self.assert_has_content()
        ncols = self.options.get('ncols', 3)
        showlabel = not 'nolabel' in self.options
        module = self.options.get('module', 'elm')

        hide_anchors = [
            'center', 'start', 'end', 'istart', 'iend',
            'isource', 'idrain', 'iemitter', 'icollector', 'xy',
            'input_component.istart', 'input_component.iend',
            'input_component.start', 'input_component.end', 'input_component.center',
            'output_component.istart', 'output_component.iend',
            'output_component.start', 'output_component.end', 'output_component.center',
            'input_component.common', 'output_component.common'
            ]

        hide_anchors.extend(self.options.get('hide_anchors', '').split())

        names = [re.findall('(.*)\(', line)[0] for line in self.content]
        args = [re.findall('\((.*)\)', line)[0] for line in self.content]

        text = f'''
.. grid:: {ncols}
    :gutter: 0

'''

        for name, arg in zip(names, args):

            text += f'''
    .. grid-item-card::
        :class-body: sd-text-nowrap sd-fs-6

        {name}'''

            if arg:
                text += f'({arg})'

            text += f'''

        .. jupyter-execute::
            :hide-code:

            e = {module}.{name}({arg}).right()
'''
            if showlabel:
                text += f'''
            for aname in e.anchors.keys():
                if aname not in {hide_anchors}:
                    e.label(aname, loc=aname, color='blue', fontsize=10)
'''
            text += '''
            e
'''
        self.content = text
        nodes = self.parse_content_to_nodes()
        return nodes


def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_directive('element_list', SchemElement)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
