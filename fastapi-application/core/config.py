from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class ApiPrefix(BaseModel):  # Префикс для API-роутов по умолчанию
    prefix: str = "/api"


class DatabaseConfig(BaseModel):
    url: PostgresDsn  # строчка для подключения к PostgreSQL, чтобы вручную не строить эту ссылку для подключения.
    # PostgresDsn - валидация. Не ставим значение по умолчанию, т.к. ничего в класс не передаём.
    echo: bool = False  # Вкл/Выкл логирования SQL-запросов. Не использовать в проде!
    echo_pool: bool = False  # Логирование операций пула соединений.
    pool_size: int = 50  # Максимальное количество постоянных соединений в пуле. Слишком большой размер перегрузит СУБД. Должно быть меньше max_connections
    max_overflow: int = 10  # Максимальное количество временных соединений поверх pool_size. (превышение pool_size при высокой нагрузке)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),  # каждый следующий элемент в кортеже переопределяет предыдущий
        case_sensitive=False,  # регистрозависимость переменных окружения
        env_nested_delimiter="__",  # по db_url будет разделяться __
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig


settings = Settings()
