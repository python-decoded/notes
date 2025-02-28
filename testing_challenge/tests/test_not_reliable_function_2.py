import pytest

from tasks import not_reliable_function_2
from tasks.not_reliable_function_2 import not_reliable


def test_not_reliable_function(mocker):
    mocker.patch.object(not_reliable_function_2, "choice", return_value=5)

    res = not_reliable()
    assert res == 5


def test_not_reliable_function_failure(mocker):
    mocker.patch.object(not_reliable_function_2, "choice", return_value=4)

    with pytest.raises(ValueError):
        not_reliable()
