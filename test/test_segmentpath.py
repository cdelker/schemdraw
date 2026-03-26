''' Tests for SegmentPath.doreverse() and doflip().

    Verifies fix for issue #102: these methods were silent no-ops
    with commented-out implementations.
'''
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from schemdraw.segments import SegmentPath


def test_doreverse_changes_path():
    ''' doreverse should mirror x-coordinates and reverse order '''
    sp = SegmentPath(path=[(0, 0), 'M', (2, 1), 'L', (4, 0)])
    original = list(sp.path)
    sp.doreverse(centerx=2.0)
    assert sp.path != original, 'doreverse did not modify the path'


def test_doreverse_mirrors_x():
    ''' doreverse should mirror x about centerx '''
    sp = SegmentPath(path=[(0, 0), (4, 2)])
    sp.doreverse(centerx=2.0)
    # (0,0) mirrored about x=2 -> (4,0), (4,2) -> (0,2)
    # reversed order: [(0,2), (4,0)]
    points = [p for p in sp.path if not isinstance(p, str)]
    assert abs(points[0][0] - 0) < 0.01 and abs(points[0][1] - 2) < 0.01
    assert abs(points[1][0] - 4) < 0.01 and abs(points[1][1] - 0) < 0.01


def test_doreverse_preserves_strings():
    ''' SVG path commands (strings) should be preserved '''
    sp = SegmentPath(path=[(0, 0), 'M', (2, 1)])
    sp.doreverse(centerx=1.0)
    strings = [p for p in sp.path if isinstance(p, str)]
    assert 'M' in strings


def test_doflip_changes_path():
    ''' doflip should negate y-coordinates '''
    sp = SegmentPath(path=[(0, 0), 'M', (2, 3), 'L', (4, 1)])
    original_ys = [p[1] for p in sp.path if not isinstance(p, str)]
    sp.doflip()
    new_ys = [p[1] for p in sp.path if not isinstance(p, str)]
    assert new_ys != original_ys, 'doflip did not modify the path'
    for orig, new in zip(original_ys, new_ys):
        assert abs(new + orig) < 0.01, f'Expected y={-orig}, got {new}'


def test_doflip_preserves_strings():
    ''' SVG path commands (strings) should be preserved '''
    sp = SegmentPath(path=[(0, 0), 'L', (1, 1)])
    sp.doflip()
    strings = [p for p in sp.path if isinstance(p, str)]
    assert 'L' in strings


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
