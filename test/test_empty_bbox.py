''' Tests for get_bbox() with empty paths/vertices.

    Verifies fix for issue #110: get_bbox() raised ValueError
    on empty path/vertices lists.
'''
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from schemdraw.segments import Segment, SegmentPoly, SegmentPath


def test_segment_empty_path():
    ''' Segment with empty path should return zero bbox '''
    seg = Segment(path=[])
    bbox = seg.get_bbox()
    assert bbox.xmin == 0 and bbox.xmax == 0


def test_segmentpoly_empty_verts():
    ''' SegmentPoly with empty verts should return zero bbox '''
    seg = SegmentPoly(verts=[])
    bbox = seg.get_bbox()
    assert bbox.xmin == 0 and bbox.xmax == 0


def test_segmentpath_empty_path():
    ''' SegmentPath with empty path should return zero bbox '''
    seg = SegmentPath(path=[])
    bbox = seg.get_bbox()
    assert bbox.xmin == 0 and bbox.xmax == 0


def test_segmentpath_only_strings():
    ''' SegmentPath with only SVG commands (no points) should return zero bbox '''
    seg = SegmentPath(path=['M', 'L', 'Z'])
    bbox = seg.get_bbox()
    assert bbox.xmin == 0 and bbox.xmax == 0


def test_segment_normal_path():
    ''' Non-empty path should still work '''
    seg = Segment(path=[(0, 0), (1, 1)])
    bbox = seg.get_bbox()
    assert bbox.xmin == 0 and bbox.xmax == 1


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
