import random

import pytest

from tasks.not_reliable_function_1 import not_reliable


def test_not_reliable_function(mocker):
    mocker.patch.object(random, "choice", return_value=5)

    res = not_reliable()
    assert res == 5


def test_not_reliable_function_failure(mocker):
    mocker.patch.object(random, "choice", return_value=4)

    with pytest.raises(ValueError):
        not_reliable()
