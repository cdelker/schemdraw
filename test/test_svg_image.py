''' Tests for SVG image loading edge cases.

    Verifies fix for issue #109: loading an SVG image with missing or
    zero width attribute caused ZeroDivisionError.
'''
import sys
import os
import io
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from schemdraw.backends.svg import Figure
from schemdraw.types import BBox


def _make_fig():
    return Figure(bbox=BBox(0, 0, 200, 200), inches_per_unit=0.5)


def test_svg_image_zero_width_raises():
    ''' SVG image with width="0" should raise ValueError, not ZeroDivisionError '''
    fig = _make_fig()
    svg_data = b'<svg width="0" height="100" xmlns="http://www.w3.org/2000/svg"><rect/></svg>'
    try:
        fig.image(image=io.BytesIO(svg_data), xy=(0, 0), width=50, height=50, imgfmt='svg')
        assert False, 'Should have raised ValueError'
    except ValueError as e:
        assert 'width' in str(e).lower()
    except ZeroDivisionError:
        assert False, 'Got ZeroDivisionError instead of ValueError'


def test_svg_image_missing_width_raises():
    ''' SVG image with no width attribute should raise ValueError '''
    fig = _make_fig()
    svg_data = b'<svg height="100" xmlns="http://www.w3.org/2000/svg"><rect/></svg>'
    try:
        fig.image(image=io.BytesIO(svg_data), xy=(0, 0), width=50, height=50, imgfmt='svg')
        assert False, 'Should have raised ValueError'
    except ValueError as e:
        assert 'width' in str(e).lower()
    except ZeroDivisionError:
        assert False, 'Got ZeroDivisionError instead of ValueError'


def test_svg_image_valid_width():
    ''' SVG image with valid width should work '''
    fig = _make_fig()
    svg_data = b'<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><rect/></svg>'
    fig.image(image=io.BytesIO(svg_data), xy=(0, 0), width=50, height=50, imgfmt='svg')
    assert len(fig.svgelements) == 1


if __name__ == '__main__':
    tests = [v for k, v in sorted(globals().items()) if k.startswith('test_')]
    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            print(f'  PASS: {test.__name__}')
            passed += 1
        except Exception as e:
            print(f'  FAIL: {test.__name__}: {e}')
            failed += 1
    print(f'\n{passed} passed, {failed} failed, {passed + failed} total')
    sys.exit(1 if failed else 0)
