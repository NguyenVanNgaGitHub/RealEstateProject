import pandas as pd
pd.set_option("max_columns", 500)
pd.set_option("max_rows", 500)
pd.set_option("min_rows", 100)

'''
data = pd.read_csv('../crawling_real_estate_mogi.vn.csv',header=None,
                   names=['title', 'value', 'area', 'address', 'ward', 'district', 'province',
                          'type', 'description', 'sellerName', 'time', 'source', 'image'])

print("\n\n The first 10 records")
print(data.head(10))

print("\n\n Values in price")
print(data['value'].value_counts(sort=False))

print("\n\n Values in area")
print(data['area'].value_counts(sort=False))

print("\n\n Values in time")
print(data['time'].value_counts(sort=False))

print("\n\n Values in province")
print(data['province'].value_counts(sort=False))

print("\n\n Values in district")
print(data['district'].value_counts(sort=False))

print("\n\n Values in ward")
print(data['ward'].value_counts(sort=False))
'''

data = pd.read_csv('../crawling_real_estate_alonhadat.com.vn.csv',header=None,
                   names=['title', 'value', 'area', 'address', 'ward', 'district', 'province',
                          'type', 'description', 'sellerName', 'time', 'source', 'image'])
print("\n\n The first 10 records")
print(data.head(10))

print("\n\n Values in price")
print(data['value'].value_counts(sort=False))

print("\n\n Values in area")
print(data['area'].value_counts(sort=False))

print("\n\n Values in time")
print(data['time'].value_counts(sort=False))

print("\n\n Values in province")
print(data['province'].value_counts(sort=False))

print("\n\n Values in district")
print(data['district'].value_counts(sort=False))

print("\n\n Values in ward")
print(data['ward'].value_counts(sort=False))