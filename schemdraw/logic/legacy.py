''' DEPRECATED element definitions, based on dictionaries instead of classes, translated
    into their newer class counterparts.
'''

from functools import partial

from .. import logic

orgate = logic.Or
andgate = logic.And
NOT = logic.Not
NOTNOT = logic.NotNot
BUF = logic.Buf
AND2 = partial(logic.And, inputs=2)
AND3 = partial(logic.And, inputs=3)
AND4 = partial(logic.And, inputs=4)
NAND2 = partial(logic.And, inputs=2, nand=True)
NAND3 = partial(logic.And, inputs=3, nand=True)
NAND4 = partial(logic.And, inputs=4, nand=True)
OR2 = partial(logic.Or, inputs=2)
OR3 = partial(logic.Or, inputs=3)
OR4 = partial(logic.Or, inputs=4)
NOR2 = partial(logic.Or, inputs=2, nor=True)
NOR3 = partial(logic.Or, inputs=3, nor=True)
NOR4 = partial(logic.Or, inputs=4, nor=True)
XOR2 = partial(logic.Or, inputs=2, xor=True)
XOR3 = partial(logic.Or, inputs=3, xor=True)
XOR4 = partial(logic.Or, inputs=4, xor=True)
XNOR2 = partial(logic.Or, inputs=2, xor=True, nor=True)
XNOR3 = partial(logic.Or, inputs=3, xor=True, nor=True)
XNOR4 = partial(logic.Or, inputs=4, xor=True, nor=True)
ARROWHEAD = logic.Arrowhead
LINE = logic.Line
DOT = logic.Dot