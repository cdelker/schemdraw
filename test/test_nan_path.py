''' Tests for NaN/inf handling in SVG path generation.

    Verifies fix for issue #108: str(x)=='nan' replaced with
    math.isfinite() to also handle inf values.
'''
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import math
from schemdraw.backends.svg import Figure
from schemdraw.types import BBox


def _make_fig():
    return Figure(bbox=BBox(0, 0, 100, 100), inches_per_unit=0.5)


def test_nan_in_path():
    ''' NaN coordinates should start a new subpath, not crash '''
    fig = _make_fig()
    fig.plot([0, 1, float('nan'), 3, 4], [0, 1, float('nan'), 1, 0])
    svg = fig.getimage().decode()
    assert 'nan' not in svg.lower(), 'NaN leaked into SVG output'
    assert 'M' in svg  # Should have a move command


def test_inf_in_path():
    ''' Inf coordinates should start a new subpath, not produce inf in SVG '''
    fig = _make_fig()
    fig.plot([0, 1, float('inf'), 3, 4], [0, 1, float('inf'), 1, 0])
    svg = fig.getimage().decode()
    assert 'inf' not in svg.lower(), 'Inf leaked into SVG output'


def test_negative_inf_in_path():
    ''' Negative inf should also be handled '''
    fig = _make_fig()
    fig.plot([0, 1, float('-inf'), 3, 4], [0, 1, float('-inf'), 1, 0])
    svg = fig.getimage().decode()
    assert 'inf' not in svg.lower(), '-Inf leaked into SVG output'


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
