import numpy
import pandas
import pyarrow

df = pandas.DataFrame({'one': [-1, numpy.nan, 2.5],
                       'two': ['foo', 'bar', 'baz'],
                       'three': [True, False, True]},
                      index=list('abc'))
table = pyarrow.Table.from_pandas(df)
pyarrow.parquet.write_table(table, 'example.parquet')

table_from_file = pyarrow.parquet.read_table('example.parquet')