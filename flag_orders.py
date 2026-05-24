import pandas as pd

# Load the Superstore dataset
df = pd.read_excel("sample_-_superstore.xls", engine="xlrd")

# Identify orders where profit is negative
flagged = df[df["Profit"] < 0][
    ["Order ID", "Customer Name", "Product Name", "Sales", "Profit"]
].copy()

flagged = flagged.sort_values("Profit")

print(f"Total rows: {len(df)}")
print(f"Flagged (unprofitable) orders: {len(flagged)}\n")
print(flagged.to_string(index=False))
