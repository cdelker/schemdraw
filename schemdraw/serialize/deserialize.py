''' Serialize a Drawing to/from TOML or JSON

    TOML is read-only since tomllib doesn't have write ability as of
    Python 3.15. The to_dict method converts a Drawing to dictionary
    that coulud be serialized to TOML using a third-party dependency.
'''
from typing import Type, Any
from contextlib import suppress
import ast
import operator
import tomllib
import json

from ..util import Point
from .. import schemdraw
from .. import elements as elm
from .. import logic
from .. import flow
from .. import dsp
from .. import pictorial


def get_element(name: str) -> Type[elm.Element]:
    ''' Get an element by name from the submodules '''
    with suppress(AttributeError):
        return getattr(elm, name)
    with suppress(AttributeError):
        return getattr(flow, name)
    with suppress(AttributeError):
        return getattr(logic, name)
    with suppress(AttributeError):
        return getattr(dsp, name)

    if '.' in name:
        # Use "pictorial.XXX" because they duplicate some names
        module, element = name.split('.')
        return getattr(globals().get(module.strip()), element.strip())

    raise AttributeError(f'Element `{name}` not found')


def named_args_to_element(rawargs: dict, named: dict, subdrawings: dict) -> dict:
    ''' Read named positions (such as "R1.start") and convert to attributes
        of Element instances
    '''
    args = {}
    for arg, value in rawargs.items():
        if isinstance(value, str):
            try:
                name, anchor = value.split('.')
            except ValueError:
                name, anchor = value, None

            if name in named and anchor is None:
                args[arg] = named[value]
            elif name in named:
                assert anchor is not None
                args[arg] = getattr(named[name], anchor)
            elif name in subdrawings:
                args[arg] = subdrawings[name]
            else:
                args[arg] = value

        elif isinstance(value, (list, tuple)):
            arglist = []
            for v in value:
                if isinstance(v, str) and v in named:
                    arglist.append(named[v])
                else:
                    arglist.append(v)
            args[arg] = arglist
        else:
            args[arg] = value
    return args


def math_eval(node):
    ''' 4-function eval of node, for safely parsing "unit*2", e.g. '''
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg}

    match node:
        case ast.Constant(value) if isinstance(value, (float, int)):
            return value
        case ast.BinOp(left, op, right):
            return operators[type(op)](math_eval(left), math_eval(right))
        case ast.UnaryOp(op, operand):
            return operators[type(op)](math_eval(operand))
        case _:
            raise TypeError(node)


def get_distance(x, unit):
    ''' Read a distance, which may be a float or some '''
    if isinstance(x, str):
        xnode = x.replace('unit', f'({unit})')
        node = ast.parse(xnode, mode='eval').body
        try:
            return math_eval(node)
        except (KeyError, TypeError) as ex:
            raise TypeError(f'Cannot parse distance `{x}`')
    return x



def add_elements(d: schemdraw.Drawing|elm.Container, elements: list, subdrawings: dict, unit: float):
    ''' Add elements from the list to the drawing '''
    named: dict[str, elm.Element] = {}
    newelm: elm.Element

    for element in elements:
        name = element.pop('name', 'Line')
        elmid = element.pop('id', None)
        rawargs = element.pop('args', {})
        args = named_args_to_element(rawargs, named, subdrawings)

        if name == 'moveto':
            moveargs = named_args_to_element({'ref': element.get('to')}, named, subdrawings)
            dx = get_distance(element.get('dx', 0), unit)
            dy = get_distance(element.get('dy', 0), unit)
            d.move_from(moveargs['ref'], dx, dy)
            continue
        elif name == 'move':
            dx = get_distance(element.get('dx', 0), unit)
            dy = get_distance(element.get('dy', 0), unit)
            d.move(dx, dy)
            continue
        elif name == 'push':
            d.push()
            continue
        elif name == 'pop':
            d.pop()
            continue

        elif name == 'Container':
            c = elm.Container(drawing=d)
            subelements = element.pop('elements', [])
            setup_element(c, element, named, unit)
            add_elements(c, subelements, subdrawings, unit)
            d.add(c)
            continue

        elif name in subdrawings:
            newelm = elm.ElementDrawing(subdrawings[name])

        else:  # Regular element
            newelm = get_element(name)(**args)

        setup_element(newelm, element, named, unit)
        d.add(newelm)
        if elmid:
            named[elmid] = newelm


def setup_element(newelm: elm.Element, element: dict, named: dict, unit: float):
    ''' Configure the element '''
    for param, value in element.items():
        match param:
            case 'flip' | 'reverse' | 'hold' | 'dot' | 'idot':
                if value:
                    getattr(newelm, param)()

            case 'd' | 'dir' | 'direction':
                assert value in ['up', 'left', 'right', 'down']
                getattr(newelm, value)()

            case 'length':
                getattr(newelm, param)(get_distance(value, unit))

            case 'anchor' | 'color' | 'fill' | 'theta' | 'shift' | 'linestyle' | 'linewidth' | 'scale' | 'scalex' | 'scaley' | 'zorder':
                getattr(newelm, param)(value)

            case 'tox' | 'toy':
                if isinstance(value, str):
                    pos = position(value, named)
                    getattr(newelm, param)(pos)
                else:
                    getattr(newelm, param)(value)

            case 'drop':
                if isinstance(value, (list, tuple)):
                    pos = Point(value)
                    getattr(newelm, param)(pos)
                getattr(newelm, param)(value)

            case 'at' | 'to':
                if isinstance(value, str):
                    pos = position(value, named)
                    getattr(newelm, param)(pos)
                elif isinstance(value, (list, tuple)):
                    pos = Point(value)
                    getattr(newelm, param)(pos)
                else:
                    getattr(newelm, param)(value)

            case 'endpoints':
                if isinstance(value, str):
                    start, end = value.split(',')
                    newelm.endpoints(position(start, named), position(end, named))
                else:
                    newelm.endpoints(value[:2], value[2:])

            case 'label':
                text = value.pop('text', '')
                newelm.label(text, **value)

            case 'labels':
                for label in value.values():
                    text = label.pop('text', '')
                    newelm.label(text, **label)

            case 'gradient_fill':
                newelm.gradient_fill(*value)

            # Ic-specific parameters
            case 'pin':
                newelm.pin(**value)

            case 'pins':
                for pin in value:
                    newelm.pin(**pin)

            case 'sides':
                for name, side in value.items():
                    newelm.side(name, **side)

            case _:
                raise ValueError(f'Unknown parameter `{param}={value}`')


def position(s: str, named: dict):
    ''' Extract position from string (e.g. "R1.start") '''
    try:
        e, anchor = s.split('.', maxsplit=1)
    except ValueError as exc:
        # No anchor, return Element instance (eg for VoltageLabelArc)
        return named.get(s.strip())
    return getattr(named.get(e.strip()), anchor.strip())


def from_dict(dwg_dict: dict[str, Any]) -> schemdraw.Drawing:
    ''' Build a Drawing from the configuration dictionary '''
    elements = dwg_dict.get('elements', [])
    subdrawings = {}

    if (style := dwg_dict.get('style')):
        if style == 'IEC':
            elm.style(elm.STYLE_IEC)
        elif style == 'IEEE':
            elm.style(elm.STYLE_IEEE)

    for subname, subdwg in dwg_dict.get('subdrawings', {}).items():
        subdrawings[subname] = from_dict(subdwg)

    for elmname, defaults in dwg_dict.get('defaults', {}).items():
        for param, default in defaults.items():
            e = get_element(elmname).defaults[param] = default

    d = schemdraw.Drawing()

    if (config := dwg_dict.get('config')):
        d.config(**config)

    add_elements(d, elements, subdrawings, d.unit)
    return d


def from_toml(s: str) -> schemdraw.Drawing:
    ''' Build a Drawing from TOML string '''
    config = tomllib.loads(s)
    return from_dict(config)


def from_json(s: str) -> schemdraw.Drawing:
    ''' Build a Drawing from JSON string '''
    config = json.loads(s)
    return from_dict(config)
