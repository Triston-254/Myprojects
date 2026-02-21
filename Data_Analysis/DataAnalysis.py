import pandas as pd
import numpy as np

data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 40],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
}

df = pd.DataFrame(data)
print("=======creating DataFrames========")
print(df)
print("===============Loading csv file==============")
dff = pd.read_csv("dat.csv")
print(dff.head())
print("=======Column Names=========")
column_list = df.columns.tolist()
print(column_list)
print("==========Shape of DataFrame==============")
print( df.shape)
print("=========Summary Statistics for Age=========")
print("Mean:", df['Age'].mean())
print("Minimum:", df['Age'].min())
print("Maximum:", df['Age'].max())
print("=============Select Name and City columns============")
name_city = df[['Name', 'City']]
print(name_city)
print("=============Rows where Age >= 30=============")
age_gt_30 = df[df['Age'] >= 30]
print(age_gt_30)
print("==============Filter rows where City is New York or Chicago==========")
ny_chicago = df[df['City'].isin(['New York', 'Chicago'])]
print(ny_chicago)
data = {
    'A': [1, 2, None, 4],
    'B': [None, None, 3, 4],
    'C': [1, 2, 3, None]
}
print("=========Original DataFrame===========")
dfe = pd.DataFrame(data)
print(dfe)
print("==========Checking for missing values=============")
print(dfe.isnull())
print("===========Counting missing values per column==========")
print(dfe.isnull().sum())
df_filled = dfe.fillna(0)
print("\n==========DataFrame after filling missing values with 0==============")
print(df_filled)
print("==============Adding salary column=================")
df['Salary'] = np.random.randint(50000, 100001, size=len(df))
df['Age'] = df['Age'] + 5
print(df)
print("============= Grouping by City and Calculating Average Age =============")
avg_age = df.groupby('City')['Age'].mean()
print(avg_age)

print("\n============= Grouping by City and Calculating Total Salary =============")
total_salary = df.groupby('City')['Salary'].sum()
print(total_salary)
print("============sorting by age in descending order=============")
df_sorted_age = df.sort_values(by='Age', ascending=False)
print(df_sorted_age)
print("============sorting by city in ascending order=============")
df_sorted_city = df.sort_values(by='City', ascending=True)
print(df_sorted_city)

print("\n============= Merging DataFrames =============")
df1 = pd.DataFrame({
    'ID': [1, 2, 3],
    'Name': ['Alice', 'Bob', 'Charlie']
})
df2 = pd.DataFrame({
    'ID': [2, 3, 4],
    'Salary': [70000, 80000, 90000]
})

print("\nDataFrame 1:")
print(df1)
print("\nDataFrame 2:")
print(df2)

print("\n============= Inner Merge (only matching IDs) =============")
df_inner = pd.merge(df1, df2, on='ID', how='inner')
print(df_inner)

print("\n============= Left Merge (all from df1) =============")
df_left = pd.merge(df1, df2, on='ID', how='left')
print(df_left)

print("\n============= Right Merge (all from df2) =============")
df_right = pd.merge(df1, df2, on='ID', how='right')
print(df_right)

print("\n============= Outer Merge (all records) =============")
df_outer = pd.merge(df1, df2, on='ID', how='outer')
print(df_outer)