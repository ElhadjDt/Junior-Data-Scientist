import pandas as pd


df = pd.read_csv("1503_program_descriptions_x_section.csv")

print(df.info())
print(df.head(3))

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 50)  # 50 caractères max par cellule

print(df.head(3))
