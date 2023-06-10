from drunk_polish_calculator import op_plus, op_divide, op_minus, op_multiply, main
from unittest import mock
import pytest


def test_op_plus():
    # given
    x = 4
    y = 2
    expected_result = 6

    # when
    result = op_plus(x, y)

    # then
    assert result == expected_result
    assert op_plus(-5, 10) == 5
    assert op_plus(0, 0) == 0


def test_op_minus():
    # given
    x = 5
    y = 2
    expected_result = -3

    # when
    result = op_minus(x, y)

    # then
    assert result == expected_result
    assert op_minus(10, -5) == -15
    assert op_minus(0, 0) == 0


def test_op_multiply():
    # given
    x = 4
    y = 5
    expected_result = 20

    # when
    result = op_multiply(x, y)

    # then
    assert result == expected_result
    assert op_multiply(-5, 10) == -50
    assert op_multiply(0, 5) == 0


def test_op_divide():
    # given
    x = 10
    y = 2
    expected_result = 5.0

    # when
    result = op_divide(x, y)

    # then
    assert result == expected_result
    assert op_divide(10, -5) == -2.0
    assert op_divide(0, 5) == 0.0


@pytest.mark.parametrize('input_string, expected_output', [
    ('2 3 +', 'Expression with space delimiter: 5.0'),
    ('5 3 -', 'Expression with space delimiter: -2.0'),
    ('4 2 *', 'Expression with space delimiter: 8.0'),
    ('10 2 /', 'Expression with space delimiter: 5.0')
])
def test_integration(input_string, expected_output, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: input_string)

    with mock.patch('sys.stdout', new=mock.MagicMock()) as mock_stdout:
        main()
        assert mock_stdout.getvalue().strip() == expected_output
        