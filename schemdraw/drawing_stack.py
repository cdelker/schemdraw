''' Drawing Stack

    This module tracks the active drawing and element for use in context
    managers, enabling of adding elements to a drawing without explicitly
    calling `d.add` or `d +=`. The stack is a dictionary (relying on being
    ordered) of drawing: element pairs. The last item in the dictionary
    is the last drawing or container to be opened by `with` block, and
    the element is the last element instantiated.
    
    Typical order of operations:

    1) A drawing is added to the stack when the `with` block is opened
    2) When an element is instantiated inside the block, it is set as
        the value of the drawing's dictionary item.
    3) When a different element is instantiated, the element in the
        stack will then be added to its drawing if it hasn't been added already.
        This allows the chained methods (such as `.up`, `.down`) to affect
        the element before it is placed.
    4) When the `with` block exits, the last element to be instantiated
        is added to the drawing, if it hasn't been already. The drawing
        is then popped from the stack.

    A `pause` attribute may be set True to prevent any stack operations.
    This may be used, for example, when adding elements to an ElementCompound.
'''
from __future__ import annotations
from typing import Union, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .schemdraw import Drawing
    from .elements import Element, Container

DrawingType = Union['Drawing', 'Container']
    
drawing_stack: dict[DrawingType, Optional['Element']] = {}  #{drawing: element}
pause: bool = False


def push_drawing(drawing: DrawingType) -> None:
    ''' Add a drawing to the stack '''
    drawing_stack[drawing] = None

def pop_drawing(drawing: DrawingType) -> None:
    ''' Remove the drawing from the stack '''
    drawing_stack.pop(drawing)
    
def push_element(element: Optional['Element']) -> None:
    ''' Add a new element to the stack, placing the existing
        one if not already placed by the user
    '''
    if not pause and len(drawing_stack) > 0:
        drawing, prev_elm = list(drawing_stack.items())[-1]
        if prev_elm is not None and prev_elm not in drawing:
            drawing.add(prev_elm)
        drawing_stack[drawing] = element

