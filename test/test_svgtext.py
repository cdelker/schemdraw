''' Tests for SVG text rendering, specifically mathtextsvg() in backends/svgtext.py

    Verifies that XML special characters in math expressions (superscripts,
    subscripts, sqrt, overline) do not produce malformed SVG.
'''
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from schemdraw.backends.svgtext import mathtextsvg


def test_basic_superscript():
    ''' Basic superscript should produce valid tspan '''
    result = mathtextsvg('$x^{2}$')
    assert result is not None
    assert result.tag == 'tspan'


def test_basic_subscript():
    ''' Basic subscript should produce valid tspan '''
    result = mathtextsvg('$V_{out}$')
    assert result is not None
    assert result.tag == 'tspan'


def test_superscript_with_ampersand():
    ''' Ampersand in superscript should not crash XML parser '''
    result = mathtextsvg('$x^{a&b}$')
    assert result is not None


def test_subscript_with_angle_brackets():
    ''' Angle brackets in subscript should not crash XML parser '''
    result = mathtextsvg('$V_{<out>}$')
    assert result is not None


def test_superscript_single_char_special():
    ''' Single-char superscript with special char '''
    result = mathtextsvg('$x^>$')
    assert result is not None


def test_subscript_single_char_special():
    ''' Single-char subscript with special char '''
    result = mathtextsvg('$x_<$')
    assert result is not None


def test_overline_with_special_chars():
    ''' Overline content with special chars should not crash '''
    result = mathtextsvg(r'$\overline{a&b}$')
    assert result is not None


def test_sqrt_with_special_chars():
    ''' Sqrt content with special chars should not crash '''
    result = mathtextsvg(r'$\sqrt{a&b}$')
    assert result is not None


def test_plain_text_unchanged():
    ''' Non-math text should pass through unchanged '''
    result = mathtextsvg('Hello World')
    assert result.text == 'Hello World'


def test_mixed_math_and_text():
    ''' Text with embedded math expression '''
    result = mathtextsvg('Value: $x^{2}$ volts')
    assert result is not None


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
