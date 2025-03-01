''' Validate drawing style strings '''
from typing import Union
import re

from . import default_canvas


# https://developer.mozilla.org/en-US/docs/Web/CSS/named-color
NAMED_COLORS = [
    'black',
    'silver',
    'gray',
    'white',
    'maroon',
    'red',
    'purple',
    'fuchsia',
    'green',
    'lime',
    'olive',
    'yellow',
    'navy',
    'blue',
    'teal',
    'aqua',
    'aliceblue',
    'antiquewhite',
    'aqua',
    'aquamarine',
    'azure',
    'beige',
    'bisque',
    'black',
    'blanchedalmond',
    'blue',
    'blueviolet',
    'brown',
    'burlywood',
    'cadetblue',
    'chartreuse',
    'chocolate',
    'coral',
    'cornflowerblue',
    'cornsilk',
    'crimson',
    'cyan',
    'darkblue',
    'darkcyan',
    'darkgoldenrod',
    'darkgray',
    'darkgreen',
    'darkgrey',
    'darkkhaki',
    'darkmagenta',
    'darkolivegreen',
    'darkorange',
    'darkorchid',
    'darkred',
    'darksalmon',
    'darkseagreen',
    'darkslateblue',
    'darkslategray',
    'darkslategrey',
    'darkturquoise',
    'darkviolet',
    'deeppink',
    'deepskyblue',
    'dimgray',
    'dimgrey',
    'dodgerblue',
    'firebrick',
    'floralwhite',
    'forestgreen',
    'fuchsia',
    'gainsboro',
    'ghostwhite',
    'gold',
    'goldenrod',
    'gray',
    'green',
    'greenyellow',
    'grey',
    'honeydew',
    'hotpink',
    'indianred',
    'indigo',
    'ivory',
    'khaki',
    'lavender',
    'lavenderblush',
    'lawngreen',
    'lemonchiffon',
    'lightblue',
    'lightcoral',
    'lightcyan',
    'lightgoldenrodyellow',
    'lightgray',
    'lightgreen',
    'lightgrey',
    'lightpink',
    'lightsalmon',
    'lightseagreen',
    'lightskyblue',
    'lightslategray',
    'lightslategrey',
    'lightsteelblue',
    'lightyellow',
    'lime',
    'limegreen',
    'linen',
    'magenta',
    'maroon',
    'mediumaquamarine',
    'mediumblue',
    'mediumorchid',
    'mediumpurple',
    'mediumseagreen',
    'mediumslateblue',
    'mediumspringgreen',
    'mediumturquoise',
    'mediumvioletred',
    'midnightblue',
    'mintcream',
    'mistyrose',
    'moccasin',
    'navajowhite',
    'navy',
    'oldlace',
    'olive',
    'olivedrab',
    'orange',
    'orangered',
    'orchid',
    'palegoldenrod',
    'palegreen',
    'paleturquoise',
    'palevioletred',
    'papayawhip',
    'peachpuff',
    'peru',
    'pink',
    'plum',
    'powderblue',
    'purple',
    'rebeccapurple',
    'red',
    'rosybrown',
    'royalblue',
    'saddlebrown',
    'salmon',
    'sandybrown',
    'seagreen',
    'seashell',
    'sienna',
    'silver',
    'skyblue',
    'slateblue',
    'slategray',
    'slategrey',
    'snow',
    'springgreen',
    'steelblue',
    'tan',
    'teal',
    'thistle',
    'tomato',
    'turquoise',
    'violet',
    'wheat',
    'white',
    'whitesmoke',
    'yellow',
    'yellowgreen'
]


def color_hex(color: str) -> bool:
    ''' Is the color string a valid hex color? '''
    match = re.match(
        r'#[A-Fa-f\d]{3}(?:[A-Fa-f\d]{3}|(?:[A-Fa-f\d]{5})?)\b',
        color, flags=re.IGNORECASE)
    return match is not None


def color_rgb(color: str) -> bool:
    ''' Is the color string a valid rgb(...) color? '''
    match = re.match(
        r'rgb(\s*)\((\s*)(?:\d*\.?\d*\%?)(\s*),(\s*)(?:\d*\.?\d*\%?)(\s*),(\s*)(?:\d*\.?\d*\%?)(\s*)\)',
        color, flags=re.IGNORECASE)
    return match is not None


def color_rgba(color: str) -> bool:
    ''' Is the color string a valid rgba(...) color? '''
    match = re.match(
        r'rgba(\s*)\((\s*)(?:\d*\.?\d*\%?)(\s*),(\s*)(?:\d*\.?\d*\%?)(\s*),(\s*)(?:\d*\.?\d*\%?)(\s*),(\s*)(?:\d*\.?\d*\%?)(\s*)\)',
        color, flags=re.IGNORECASE)
    return match is not None


def color_hsl(color: str) -> bool:
    ''' Is the color string a valid hsl(...) color? '''
    match = re.match(
        r'hsl(\s*)\((\s*)(?:-?\d*\.?\d*)(\s*),(\s*)(?:-?\d*\.?\d*\%)(\s*),(\s*)(?:-?\d*\.?\d*\%)(\s*)\)',
        color, flags=re.IGNORECASE)
    return match is not None


def color_hsla(color: str) -> bool:
    ''' Is the color string a valid hsla(...) color? '''
    match = re.match(
        r'hsla(\s*)\((\s*)(?:-?\d*\.?\d*)(\s*),(\s*)(?:-?\d*\.?\d*\%)(\s*),(\s*)(?:-?\d*\.?\d*\%)(\s*),(\s*)(?:-?\d*\.?\d*\%?)(\s*)\)',
        color, flags=re.IGNORECASE)
    return match is not None


def dasharray(ls: str) -> bool:
    ''' Is the linestyle a valid dasharray? '''
    match = re.match(
        r'(\d+\.?\d*)(,\s*\d+\.?\d*)*$',
        ls, flags=re.IGNORECASE)
    return match is not None


def validate_color(color: Union[str, bool, tuple[int,int,int], None]) -> None:
    ''' Raise if not a valid CSS color '''
    if color in [None, True, False]:
        return

    if isinstance(color, tuple):
        if (len(color) != 3
                or not isinstance(color[0], (int, float))
                or not isinstance(color[1], (int, float))
                or not isinstance(color[2], (int, float))):
            raise ValueError(f'Invalid color tuple {color}')
        return

    assert color is not None
    assert isinstance(color, str)

    if default_canvas.default_canvas == 'matplotlib':
        if (color not in NAMED_COLORS + ['bg']
                and not color_hex(color)):
            raise ValueError(f'Invalid (matplotlib) color name {color}')

    elif (color not in NAMED_COLORS + ['bg']
            and not color_hex(color)
            and not color_rgb(color)
            and not color_rgba(color)
            and not color_hsl(color)
            and not color_hsla(color)):
        raise ValueError(f'Invalid color name {color}')


def validate_linestyle(ls: str) -> None:
    ''' Raise if ls is not a valid line style or dasharray '''
    dashes = [None, '', ' ', '-', '--', ':', '-.', 'dashed', 'dotted', 'dashdot']
    if ls not in dashes and not dasharray(ls):
        raise ValueError(f'Invalid line style {ls}')
