''' Tests for util.linspace() edge cases.

    Verifies fix for issue #93: linspace(start, stop, num=1) raised
    ZeroDivisionError.
'''
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from schemdraw.util import linspace


def test_linspace_num_1():
    ''' linspace with num=1 should return [start] '''
    result = linspace(0, 10, num=1)
    assert result == [0], f'Expected [0], got {result}'


def test_linspace_num_0():
    ''' linspace with num=0 should return empty list '''
    result = linspace(0, 10, num=0)
    assert result == [], f'Expected [], got {result}'


def test_linspace_num_2():
    ''' linspace with num=2 should return [start, stop] '''
    result = linspace(0, 10, num=2)
    assert len(result) == 2
    assert result[0] == 0
    assert result[1] == 10


def test_linspace_default():
    ''' linspace with default num should return 50 elements '''
    result = linspace(0, 1)
    assert len(result) == 50
    assert result[0] == 0
    assert abs(result[-1] - 1.0) < 1e-10


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
