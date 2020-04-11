import pandas as pd

df = pd.read_fwf(
    "Agmip.csv",
    dtype={
        '@DATE': str,
        'YYYY': str,
        'MM': str,
        'DD': str})
print(df)
