import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Read the CSV file into a DataFrame

script_dir = os.path.dirname(os.path.abspath(__file__))
scraping_results_path = os.path.join(script_dir, '../data/cleaned_dataset.csv')
df = pd.read_csv(scraping_results_path)

# New Column for Price/m2 
df = df[df['Surface of the Land (m2)'] != 0]
df = df[df['Livable Space (m2)'] != 0]

df['Price/m2'] = df['Price'] / df['Livable Space (m2)']
df['Price Ratio'] = df['Price'] / df['Price'].max()
df['Price/m2 Ratio'] = df['Price/m2'] / df['Price/m2'].max()

# Calculate the mean of 'Price Ratio' grouped by Column Type

zip_code = df.groupby('Zip Code')['Price Ratio'].mean()
subtype = df.groupby('Subtype of Property')['Price Ratio'].mean()
rooms_number = df.groupby('Number of Rooms')['Price Ratio'].mean()
livable_space = df.groupby('Livable Space (m2)')['Price Ratio'].median()
land = df.groupby('Surface of the Land (m2)')['Price Ratio'].median()
building = df.groupby('State of the Building')['Price Ratio'].mean()


# Map the mean values back to the DataFrame as a new column

df['Zip Code Score'] = df['Zip Code'].map(zip_code)
df['Zip Code Score'] = df['Zip Code Score'] / df['Zip Code Score'].max()

df['Subtype of Property Score'] = df['Subtype of Property'].map(subtype)
df['Subtype of Property Score'] = df['Subtype of Property Score'] / df['Subtype of Property Score'].max()

df['Number of Rooms Score'] = df['Number of Rooms'].map(rooms_number)
df['Number of Rooms Score'] = df['Number of Rooms Score'] / df['Number of Rooms Score'].max()

df['Livable Space (m2) Score'] = df['Livable Space (m2)'].map(livable_space)
df['Livable Space (m2) Score'] = df['Livable Space (m2) Score'] / df['Livable Space (m2) Score'].max()

df['Surface of the Land (m2) Score'] = df['Surface of the Land (m2)'].map(land)
df['Surface of the Land (m2) Score'] = df['Surface of the Land (m2) Score'] / df['Surface of the Land (m2) Score'].max()

df['State of the Building Score'] = df['State of the Building'].map(building)
df['State of the Building Score'] = df['State of the Building Score'] / df['State of the Building Score'].max()


normalized_dataset_path = os.path.join(script_dir, '../data/normalized_dataset.csv')
df.to_csv(normalized_dataset_path, index=False)

# Select numerical columns for correlation
numerical_columns = ['Zip Code Score', 'Subtype of Property Score', 
    'Number of Rooms Score', 'Livable Space (m2) Score', 
    'Surface of the Land (m2) Score','State of the Building Score', 'Price'
]

# Compute the correlation matrix
correlation_matrix = df[numerical_columns].corr()

# Create a heatmap using seaborn
plt.figure(figsize=(10, 8))  # Set figure size
sns.heatmap(
    correlation_matrix, 
    annot=True,             # Annotate each cell with correlation value
    cmap='coolwarm',        # Use a diverging color palette
    fmt='.2f',              # Format the annotations to two decimal places
    linewidths=0.5          # Add space between cells
)

# Set titles and labels
plt.title("Correlation Map", fontsize=16)
plt.xticks(rotation=75)  # Rotate x-axis labels for readability
plt.yticks(rotation=0)   # Keep y-axis labels horizontal

# Display the heatmap
plt.tight_layout()
plt.show()