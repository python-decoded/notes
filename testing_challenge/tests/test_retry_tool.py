import pytest

from tasks.retry_tool import retry


def test_retry_does_not_affect_result():

    @retry()
    def func(a, b):
        return a + b

    assert func(2, 5) == 7


def test_retry_infinite_tries(mocker):

    mock = mocker.MagicMock(side_effect=[
        ValueError,
        ValueError,
        ValueError,
        5
    ])
    decorated = retry()(mock)
    assert decorated() == 5
    assert mock.call_count == 4


def test_retry_finite_tries_failure(mocker):

    mock = mocker.MagicMock(side_effect=[
        ValueError,
        ValueError,
        ValueError
    ])
    decorated = retry(times=3)(mock)

    with pytest.raises(ValueError):
        decorated()

    assert mock.call_count == 3


def test_retry_finite_tries_success(mocker):

    mock = mocker.MagicMock(side_effect=[
        ValueError,
        ValueError,
        ValueError,
        5
    ])
    decorated = retry(times=4)(mock)
    assert decorated() == 5
    assert mock.call_count == 4
