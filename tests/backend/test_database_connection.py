from importlib import reload


def test_database_connectivity(monkeypatch) -> None:
    monkeypatch.setenv('DATABASE_URL', 'sqlite+pysqlite:///:memory:')

    from app.core import config as config_module
    from app.core import database as database_module

    config_module.get_settings.cache_clear()
    reload(config_module)
    reload(database_module)

    with database_module.engine.connect() as connection:
        result = connection.exec_driver_sql('SELECT 1')

    assert result.scalar_one() == 1