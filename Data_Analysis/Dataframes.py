import pandas as pd
import numpy as np
import pandas as pd

df1 = pd.DataFrame({
    'ID': [1, 2, 3],
    'Name': ['Alice', 'Bob', 'Charlie']
})

df2 = pd.DataFrame({
    'ID': [2, 3, 4],
    'Salary': [70000, 80000, 90000]
})
print("=============merging dataframes============")
merged_df = pd.merge(df1, df2, on='ID', how='inner')
print(merged_df)
titanic_df = pd.read_csv("titanic.csv")

print("=============titanic data============")
pd.set_option('display.max_column', None)

print(titanic_df.head())


print("==========column names==============")
column_list = titanic_df.columns.tolist()
print(column_list)
print("==========shape of dataframe==============")
print(titanic_df.shape)
pd.set_option('display.max_row', None)
print("=============Indexing and Slicing DataFrames============")
print("=========Access the Name column============")
print(titanic_df['Name'])
print("=========Access the row with index 3============")

print(titanic_df.iloc[3])
print("\n=======Slice rows 5 to 10 and columns Name and Age===========")
print(titanic_df.loc[5:10, ['Name', 'Age']])
print("=========Dataframe containing only rows where Age is less than 18==========")
young_passengers = titanic_df[titanic_df['Age'] < 18]

print(young_passengers)