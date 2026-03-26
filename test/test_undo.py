''' Tests for Drawing.undo() edge cases.

    Verifies fix for issue #94: undo() raised IndexError when the
    drawing had only one element.
'''
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import schemdraw
import schemdraw.elements as elm


def test_undo_single_element():
    ''' undo() with one element should not crash '''
    schemdraw.use('svg')
    with schemdraw.Drawing(show=False) as d:
        d += elm.Resistor()
        d.undo()
    # Should not raise IndexError


def test_undo_empty_drawing():
    ''' undo() on empty drawing should be a no-op '''
    schemdraw.use('svg')
    with schemdraw.Drawing(show=False) as d:
        d.undo()
    # Should not raise


def test_undo_then_add():
    ''' undo all elements then add new ones '''
    schemdraw.use('svg')
    with schemdraw.Drawing(show=False) as d:
        d += elm.Resistor()
        d.undo()
        d += elm.Capacitor()
    # Should not raise; drawing should still be valid


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
