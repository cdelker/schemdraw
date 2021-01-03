''' Module for converting a logic string expression into a schemdraw.Drawing.

Example:

>>> logicparse("a and (b or c)")

'''
import pyparsing  # type: ignore

from .. import schemdraw
from .. import logic
from ..elements import RightLines
from .buchheim import buchheim


class LogicTree():
    ''' Organize the logic gates into tree structure '''
    def __init__(self, node='and', *children):
        self.node = node
        self.children = children if children else []

    def __getitem__(self, key):
        if isinstance(key, (int, slice)):
            return self.children[key]

    def __iter__(self): return self.children.__iter__()

    def __len__(self): return len(self.children)


def parse_string(logicstr):
    ''' Parse the logic string using pyparsing '''
    and_ = pyparsing.Keyword('and')
    or_ = pyparsing.Keyword('or')
    nor_ = pyparsing.Keyword('nor')
    nand_ = pyparsing.Keyword('nand')
    xor_ = pyparsing.Keyword('xor')
    xnor_ = pyparsing.Keyword('xnor')
    not_ = pyparsing.Keyword('not')
    true_ = pyparsing.Keyword('true')
    false_ = pyparsing.Keyword('false')

    not_op = not_ | '~' | '¬'
    and_op = and_ | nand_ | '&' | '∧'
    xor_op = xor_ | xnor_ | '⊕' | '⊻'
    or_op = or_ | nor_ | '|' | '∨' | '+'

    expr = pyparsing.Forward()

    identifier = ~(and_ | or_ | nand_ | nor_ | not_ | true_ | false_) + \
                  pyparsing.Word('$' + pyparsing.alphas + '_', pyparsing.alphanums + '_' + '$')

    atom = identifier | pyparsing.Group('(' + expr + ')')
    factor = pyparsing.Group(pyparsing.ZeroOrMore(not_op) + atom)
    term = pyparsing.Group(factor + pyparsing.ZeroOrMore(and_op + factor))
    expr = pyparsing.infixNotation(true_ | false_ | identifier,
                                   [(not_op, 1, pyparsing.opAssoc.RIGHT),
                                    (and_op, 2, pyparsing.opAssoc.LEFT),
                                    (or_op, 2, pyparsing.opAssoc.LEFT),
                                    (xor_op, 2, pyparsing.opAssoc.LEFT)])

    return expr.parseString(logicstr)[0]


def to_tree(pres):
    ''' Convert the parsed logic expression into a LogicTree '''
    invertfunc = False

    if pres[0] in ['not', '~', '¬']:
        if isinstance(pres[1], str):
            return LogicTree('not', to_tree(pres[1]))
        else:
            pres = pres[1]
            invertfunc = True

    if isinstance(pres, str):
        return LogicTree(pres)

    func = pres[1]
    inputs = pres[::2]

    func = {'&': 'and', '∧': 'and',
            '|': 'or', '∨': 'or',  '+': 'or',
            '⊕': 'xor', '⊻': 'xor'}.get(func, func)

    if invertfunc:
        func = {'and': 'nand', 'or': 'nor', 'not': 'buf',
                'nand': 'and', 'nor': 'or', 'buf': 'not',
                'xor': 'xnor', 'xnor': 'xor'}.get(func)

    return LogicTree(func, *[to_tree(i) for i in inputs])


def drawlogic(tree, gateH=.7, gateW=2, outlabel=None):
    ''' Draw the LogicTree to a schemdraw Drawing

        Parameters
        ----------
        tree: LogicTree
            The tree structure to draw
        gateH: float
            Height of one gate
        gateW: float
            Width of one gate
        outlabel: string
            Label for logic output

        Returns
        -------
        schemdraw.Drawing
    '''
    drawing = schemdraw.Drawing()
    drawing.unit = gateW  # NOTs still use d.unit

    dtree = buchheim(tree)

    def drawit(root, depth=0, outlabel=None):
        ''' Recursive drawing function '''
        elmdefs = {'and': logic.And,
                   'or': logic.Or,
                   'xor': logic.Xor,
                   'nand': logic.Nand,
                   'xnor': logic.Xnor,
                   'nor': logic.Nor,
                   'not': logic.Not}
        elm = elmdefs.get(root.node, logic.And)

        x = root.y * -gateW   # buchheim draws vertical trees, so flip x-y.
        y = -root.x * gateH

        g = drawing.add(elm(d='r', at=(x, y), anchor='end',
                            l=gateW, inputs=len(root.children)))
        if outlabel:
            g.add_label(outlabel, loc='end')

        for i, child in enumerate(root.children):
            anchorname = 'start' if elm in [logic.Not, logic.Buf] else f'in{i+1}'
            if child.node not in elmdefs.keys():
                g.add_label(child.node, loc=anchorname)
            else:
                childelm = drawit(child, depth+1)  # recursive
                drawing.add(RightLines(at=(g, anchorname), to=childelm.end))
        return g

    drawit(dtree, outlabel=outlabel)
    return drawing


def logicparse(expr: str, gateW: float=2, gateH: float=.75,
               outlabel: str=None) -> schemdraw.Drawing:
    ''' Parse a logic string expression and draw the gates in a schemdraw Drawing

        Logic expression is defined by string using 'and', 'or', 'not', etc.
        for example, "a or (b and c)". Parser recognizes several symbols and
        names for logic functions:
        [and, '&', '∧']
        [or, '|', '∨', '+']
        [xor, '⊕', '⊻']
        [not, '~', '¬']

        Args:
            expr: Logic expression
            gateH: Height of one gate
            gateW: Width of one gate
            outlabel: Label for logic output

        Returns:
            schemdraw.Drawing with logic tree
    '''
    parsed = parse_string(expr)
    tree = to_tree(parsed)
    drawing = drawlogic(tree, gateH=gateH, gateW=gateW, outlabel=outlabel)
    return drawing
