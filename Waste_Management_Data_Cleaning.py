import pandas as pd

providers = pd.read_csv("providers_data.csv")
receivers = pd.read_csv("receivers_data.csv")
food = pd.read_csv("food_listings_data.csv")
claims = pd.read_csv("claims_data.csv")

print(providers.head())
print(receivers.head())
print(food.head())
print(claims.head())

print("Providers shape:", providers.shape)
print("Receivers shape:", receivers.shape)
print("Food shape:", food.shape)
print("Claims shape:", claims.shape)


providers.columns
receivers.columns
food.columns
claims.columns

providers.isnull().sum()
receivers.isnull().sum()
food.isnull().sum()
claims.isnull().sum()

providers.isnull().sum()
receivers.isnull().sum()
food.isnull().sum()
claims.isnull().sum()

print("\nMissing values in Providers")
print(providers.isnull().sum())

print("\nMissing values in Receivers")
print(receivers.isnull().sum())

print("\nMissing values in Food")
print(food.isnull().sum())

print("\nMissing values in Claims")
print(claims.isnull().sum())

print("\nDuplicate rows in Providers:", providers.duplicated().sum())
print("Duplicate rows in Receivers:", receivers.duplicated().sum())
print("Duplicate rows in Food:", food.duplicated().sum())
print("Duplicate rows in Claims:", claims.duplicated().sum())

food['Expiry_Date'] = pd.to_datetime(food['Expiry_Date'])
claims['Timestamp'] = pd.to_datetime(claims['Timestamp'])

print(food.dtypes)
print(claims.dtypes)

providers.to_csv("clean_providers.csv", index=False)
receivers.to_csv("clean_receivers.csv", index=False)
food.to_csv("clean_food_listings.csv", index=False)
claims.to_csv("clean_claims.csv", index=False)