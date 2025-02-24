import pytest
from click.testing import CliRunner, Result

from nginx_conf_tool.tree import tree


@pytest.fixture(scope="module")
def runner():
    return CliRunner()


@pytest.fixture(scope="module")
def simple_result(runner) -> Result:
    return runner.invoke(tree, ["samples/simple.conf"])


@pytest.fixture(scope="module")
def data_dir(request):
    print(request.path)
    return request.path.parent / "data"


def test_missing_file(runner):
    result = runner.invoke(tree)
    assert result.exit_code != 0


def test_simple_verify_exit_code(simple_result):
    assert simple_result.exit_code == 0


def test_simple_verify_stdout(simple_result, data_dir):
    expected = (data_dir / "simple_output.txt").read_text()
    assert simple_result.output == expected


def test_simple_dir_only(runner, data_dir):
    expected = (data_dir / "simple_dir_only.txt").read_text()
    result = runner.invoke(tree, ["-d", "samples/simple.conf"])
    assert result.exit_code == 0
    assert result.output == expected


def test_simple_level1(runner, data_dir):
    expected = (data_dir / "simple_level1.txt").read_text()
    result = runner.invoke(tree, ["-L", "1", "samples/simple.conf"])
    assert result.exit_code == 0
    assert result.output == expected
