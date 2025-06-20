"""
Tests amati/validators/oas311.py
"""

from pathlib import Path
from typing import Literal, cast

from amati.amati import check, dispatch, load_file
from amati.logging import LogMixin

TEST_DATA_PATH = Path("tests/data")

type TestOptions = Literal["good"] | Literal["bad"]
type TestData = dict[TestOptions, list[Path]]


def get_test_data() -> TestData:
    """
    Gathers the set of test data.
    """

    files: TestData = {"good": [], "bad": []}

    for file in TEST_DATA_PATH.glob("**/*.*"):

        if file.suffix in (".yaml", ".yml", ".json"):
            test_style: TestOptions = cast(TestOptions, file.parts[-2])
            files[test_style].append(file)

    return files


def test_good_files():

    files = get_test_data()

    for file in files["good"]:

        data = load_file(file)

        with LogMixin.context():
            result, errors = dispatch(data)

        assert not errors
        assert result

        if file.stat().st_size < 1024 * 1024:
            check(data, result)


def test_bad_files():

    files = get_test_data()

    for file in files["bad"]:

        data = load_file(file)

        with LogMixin.context():
            result, errors = dispatch(data)

        assert errors
        assert not result
