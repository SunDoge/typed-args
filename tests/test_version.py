import toml
from typed_args import __version__


def test_package_version():
    with open("pyproject.toml", "r") as f:
        pyproject_config = toml.load(f)

    assert pyproject_config["tool"]["poetry"]["version"] == __version__
