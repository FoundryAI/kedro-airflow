from pathlib import Path

from kedro_airflow.plugin import commands


def test_create_airflow_dag(cli_runner, mocker, metadata, session):
    dag_file = Path.cwd() / "airflow_dags" / "hello_world_dag.py"
    mocker.patch("kedro_airflow.plugin.KedroSession.create", return_value=session)
    result = cli_runner.invoke(commands, ["airflow", "create"], obj=metadata)
    assert result.exit_code == 0
    assert str(dag_file) in result.output
    assert dag_file.exists()
