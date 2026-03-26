''' Tests for roundcorners() with degenerate inputs.

    Verifies fix for issue #103: roundcorners() crashed with
    ZeroDivisionError on duplicate or backtracking vertices.
'''
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from schemdraw.segments import roundcorners


def test_normal_polygon():
    ''' Normal square polygon should work '''
    verts = [(0, 0), (1, 0), (1, 1), (0, 1)]
    result = roundcorners(verts, radius=0.1)
    assert len(result) > len(verts)


def test_duplicate_vertices():
    ''' Duplicate adjacent vertices should not crash '''
    verts = [(0, 0), (1, 0), (1, 0), (1, 1), (0, 1)]
    result = roundcorners(verts, radius=0.1)
    assert len(result) > 0


def test_backtracking_vertices():
    ''' Backtracking vertices (same direction) should not crash '''
    verts = [(0, 0), (1, 0), (0, 0), (0, 1)]
    result = roundcorners(verts, radius=0.1)
    assert len(result) > 0


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
