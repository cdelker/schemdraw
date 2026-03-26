''' Test that raster images are not duplicated in SVG output.

    Verifies fix for issue #92: the SVG backend's image() method was
    appending raster image elements to svgelements twice.
'''
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from schemdraw.backends.svg import Figure
from schemdraw.types import BBox


def test_raster_image_not_duplicated():
    ''' A raster image should appear exactly once in svgelements '''
    fig = Figure(bbox=BBox(0, 0, 200, 200), inches_per_unit=0.5, fontsize=14, font='sans-serif')

    # Use the existing test PNG in the test directory
    test_png = os.path.join(os.path.dirname(__file__), 'ArduinoUNO.png')
    if not os.path.exists(test_png):
        print('  SKIP: test PNG not found')
        return

    fig.image(image=test_png, xy=(0, 0), width=100, height=100)
    image_count = sum(1 for _, el in fig.svgelements if el.tag == 'image')
    assert image_count == 1, f'Expected 1 image element, got {image_count}'


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
