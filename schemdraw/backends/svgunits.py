''' CSS/SVG Unit Conversions per
    https://www.w3.org/TR/css-values/#absolute-lengths
'''
PT_PER_IN = 72.
PX_PER_IN = 96.
CM_PER_IN = 2.54
MM_PER_IN = CM_PER_IN * 10
PC_PER_IN = 6.

PX_PER_PT = PX_PER_IN / PT_PER_IN

TO_PX = {
    'in': PX_PER_IN,
    'cm': PX_PER_IN / CM_PER_IN,
    'mm': PX_PER_IN / MM_PER_IN,
    'pt': PX_PER_IN / PT_PER_IN,
    'pc': PX_PER_IN / PC_PER_IN,
    'px': 1,
}


def parse_size_to_px(value: str) -> float:
    ''' Convert SVG size string (such as `2in`) to pixels '''
    try:
        value_px = float(value)
    except ValueError:
        unit = value[-2:]
        value_px = float(value[:-2]) * TO_PX.get(unit, 1)
    return value_px
