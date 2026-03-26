''' Tests for SegmentText rotation calculation.

    Verifies fix for issue #100: operator precedence bug where
    rotation + transform.theta % 360 was evaluated as
    rotation + (transform.theta % 360) instead of
    (rotation + transform.theta) % 360.
'''
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from schemdraw.segments import SegmentText
from schemdraw.transform import Transform
from schemdraw.util import Point


def test_rotation_wraps_around_360():
    ''' Rotation 350 + theta 45 should wrap to 35, not 395 '''
    seg = SegmentText(Point((0, 0)), 'test', rotation=350, rotation_global=False)
    xf = Transform(theta=45, globalshift=Point((0, 0)))
    result = seg.xform(xf)
    assert result.rotation <= 360, \
        f'Rotation {result.rotation} exceeds 360 degrees'
    assert abs(result.rotation - 35) < 0.01, \
        f'Expected rotation ~35, got {result.rotation}'


def test_rotation_no_wrap_needed():
    ''' Rotation 10 + theta 20 should be 30 (no wrap) '''
    seg = SegmentText(Point((0, 0)), 'test', rotation=10, rotation_global=False)
    xf = Transform(theta=20, globalshift=Point((0, 0)))
    result = seg.xform(xf)
    assert abs(result.rotation - 30) < 0.01, \
        f'Expected rotation ~30, got {result.rotation}'


def test_rotation_exact_360():
    ''' Rotation 180 + theta 180 should wrap to 0 '''
    seg = SegmentText(Point((0, 0)), 'test', rotation=180, rotation_global=False)
    xf = Transform(theta=180, globalshift=Point((0, 0)))
    result = seg.xform(xf)
    assert abs(result.rotation) < 0.01 or abs(result.rotation - 360) < 0.01, \
        f'Expected rotation ~0 or ~360, got {result.rotation}'


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
