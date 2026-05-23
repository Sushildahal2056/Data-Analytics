import pandas as pd
import matplotlib.pyplot as plt


data = {
    'category': ['A', 'B', 'C'],
    'sales': [18010, 22154, 18213],
    'quantity': [282, 343, 273],
    'transaction_count': [33, 36, 31]
}
df = pd.DataFrame(data)


df['avg_sales_per_trans'] = df['sales'] / df['transaction_count']
df['avg_qty_per_trans'] = df['quantity'] / df['transaction_count']

print("--- Descriptive Analysis Summary ---")
print(df)


plt.figure(figsize=(8, 5))
plt.bar(df['category'], df['sales'], color=['skyblue', 'salmon', 'lightgreen'])
plt.title('Total Sales by Category')
plt.xlabel('Category')
plt.ylabel('Total Sales ($)')
plt.savefig('sales_summary.png')
plt.show()