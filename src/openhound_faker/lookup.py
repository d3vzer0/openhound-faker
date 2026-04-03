from duckdb import DuckDBPyConnection
from functools import lru_cache
from openhound.core.lookup import LookupManager
import duckdb


class RandomLookup(LookupManager):

    def __init__(self, client: DuckDBPyConnection, schema: str = "faker"):
        super().__init__(client, schema)
        self.schema = schema
        self.client = client
        self.node_limit = 10

    @lru_cache
    def find_computers(self, resource_type: str):
        return self._find_all_objects(
            f"""SELECT
                hostname,
                mac_address,
                ip_address
            FROM {self.schema}.fake_computer
            WHERE hostname GLOB ? LIMIT ?;""",
            [resource_type, self.node_limit],
        )
