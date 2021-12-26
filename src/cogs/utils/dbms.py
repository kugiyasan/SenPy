import os
import psycopg2
from tenacity import retry, wait_exponential, stop_after_attempt
from typing import Any, Callable, List, Optional, Tuple, TypeVar


T = TypeVar("T")

# https://stackoverflow.com/questions/42385391/auto-reconnect-postgresq-database
def reconnect(f: Callable[..., T]) -> Callable[..., T]:
    def wrapper(storage: "DbStorage", *args: Any, **kwargs: Any) -> T:
        if not storage.connected():
            storage.connect()

        try:
            return f(storage, *args, **kwargs)
        except psycopg2.Error:
            storage.close()
            raise

    return wrapper


class DbStorage:
    def __init__(self, conn: str):
        self._conn = conn
        self._connection: Optional[Any] = None

    def connected(self) -> bool:
        return self._connection is not None and self._connection.closed == 0

    def connect(self) -> None:
        self.close()
        self._connection = psycopg2.connect(self._conn)

    def close(self) -> None:
        if self.connected():
            try:
                self._connection.close()
            except Exception:
                pass

        self._connection = None

    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    @reconnect
    def get_data(self, query: str, args: Tuple[Any, ...]=tuple()) -> List[Tuple[Any, ...]]:
        """
        Execute the query and let psycopg2 protect from SQL injection
        """
        cur = self._connection.cursor()
        cur.execute(query, args)
        return cur.fetchall()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    @reconnect
    def set_data(self, query: str, args: Tuple[Any, ...]) -> None:
        """
        Execute the query and let psycopg2 protect from SQL injection
        """
        cur = self._connection.cursor()
        with self._connection:
            cur.execute(query, args)


if "DATABASE_URL" not in os.environ.keys():
    from dotenv import load_dotenv

    load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
db = DbStorage(DATABASE_URL)
db.connect()
