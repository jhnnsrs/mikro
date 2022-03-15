from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4
import uuid
from graphql import NamedTypeNode
from mikro.datalayer import DataLayer
from rath.links.parsing import ParsingLink
from rath.operation import Operation
from graphql.language import NonNullTypeNode
import xarray as xr
import asyncio
import pandas as pd
from pyarrow import Table
import pyarrow.parquet as pq


def filter_dataframe_nodes(operation: Operation):
    try:
        return [
            v
            for v in operation.node.variable_definitions
            if (
                (
                    isinstance(v.type, NonNullTypeNode)
                    and v.type.type.name.value == "DataFrame"
                )
                or (
                    isinstance(v.type, NamedTypeNode)
                    and v.type.name.value == "DataFrame"
                )
            )
        ]
    except AttributeError:
        return []


class ParquetConversionException(Exception):
    pass


class DataLayerParquetUploadLink(ParsingLink):
    FILEVERSION = "0.1"

    def __init__(self, datalayer: DataLayer, bucket: str = "parquet") -> None:
        self.datalayer = datalayer
        self.bucket = bucket
        self.connected = False
        self._lock = False

    def store_df(self, df: pd.DataFrame) -> None:

        random_ui = uuid.uuid4()
        table: Table = Table.from_pandas(df)
        s3_path = f"{self.bucket}/{random_ui}"
        pq.write_table(table, s3_path, filesystem=self.datalayer.fs)
        return s3_path

    def parse(self, operation: Operation) -> Operation:

        for node in filter_dataframe_nodes(operation):
            array = operation.variables[node.variable.name.value]

            if isinstance(array, pd.DataFrame):
                operation.variables[node.variable.name.value] = self.store_df(array)

            else:
                raise NotImplementedError("Can only store XArray at this moment")

        return operation

    async def aparse(self, operation: Operation) -> Operation:

        if not self._lock:
            self._lock = asyncio.Lock()

        shrinky = filter_dataframe_nodes(operation)
        if shrinky:
            shrinked_v = []
            shrinked_f = []

            with ThreadPoolExecutor(max_workers=4) as executor:
                for node in shrinky:
                    array = operation.variables[node.variable.name.value]
                    co_future = executor.submit(self.store_df, array)
                    shrinked_f.append(asyncio.wrap_future(co_future))
                    shrinked_v.append(node.variable.name.value)

                shrinked_x = await asyncio.gather(*shrinked_f)

            update_dict = {v: x for v, x in zip(shrinked_v, shrinked_x)}
            operation.variables.update(update_dict)

        return operation
