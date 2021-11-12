"""
This file contains the fixtures that are reusable by any tests within
this directory. You don't need to import the fixtures as pytest will
discover them automatically. More info here:
https://docs.pytest.org/en/latest/fixture.html
"""
from pathlib import Path
from typing import NamedTuple

from click.testing import CliRunner
from kedro import __version__ as kedro_version
from kedro.framework.startup import ProjectMetadata
from kedro.pipeline import Pipeline, node
from pytest import fixture


@fixture(name="cli_runner", scope="session")
def cli_runner():
    runner = CliRunner()
    with runner.isolated_filesystem():
        yield runner


@fixture(scope="session")
def metadata(cli_runner):  # pylint: disable=unused-argument
    # cwd() depends on ^ the isolated filesystem, created by CliRunner()
    project_path = Path.cwd()
    return ProjectMetadata(
        project_path / "pyproject.toml",
        "hello_world",
        "Hello world !!!",
        project_path,
        kedro_version,
        project_path / "src",
    )


def identity(arg):
    return arg


@fixture(scope="session")
def pipeline():
    return Pipeline(
        [node(identity, ["input"], ["output"]), node(identity, ["output"], ["final"])]
    )


@fixture(scope="session")
def context(pipeline):
    class MockContext(NamedTuple):
        pipelines: dict

    return MockContext(pipelines={"__default__": pipeline})


@fixture(scope="session")
def session(context):
    class MockSession:
        @staticmethod
        def load_context():
            return context

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, tb_):
            pass

    return MockSession()
