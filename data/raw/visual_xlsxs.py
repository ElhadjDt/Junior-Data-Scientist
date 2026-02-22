import pandas as pd

df1 = pd.read_excel("1503_discipline.xlsx")
df2 = pd.read_excel("1503_program_master.xlsx")

print(df1)
print()

pd.set_option('display.max_columns', None)
print(df2.head(3))
print(df2.info())
print(df2.describe())
print(len(df2["discipline_id"].unique()))
