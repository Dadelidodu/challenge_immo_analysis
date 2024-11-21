import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import os

# Load your dataset
script_dir = os.path.dirname(os.path.abspath(__file__))
normalized_dataset_path = os.path.join(script_dir, 'heatmap_dataset.csv')
zipcode_path = os.path.join(script_dir, 'json_files/georef-belgium-postal-codes.geojson')
muncode_path = os.path.join(script_dir, 'json_files/georef-belgium-submunicipality.parquet')
df = pd.read_csv(normalized_dataset_path)

# Load Belgium's shapefile or GeoJSON containing postal codes

belgium_map = gpd.read_file(zipcode_path)
belgium_map['postcode'] = belgium_map['postcode'].astype(int)
belgium_map['mun_code'] = belgium_map['mun_code'].fillna(0).astype(int)

belgium_municipalities = gpd.read_parquet(muncode_path)
belgium_municipalities['mun_code'] = belgium_municipalities['mun_code'].astype(int)

belgium_map_merged = belgium_municipalities.merge(belgium_map[['postcode','mun_code']], left_on='mun_code', right_on='mun_code', how='left')


# Create Price/m2 column and finetune outliers
df['Price/m2'] = df['Price'] / df['Livable Space (m2)']
df = df[(df['Price/m2'] >= (df['Price/m2'].mean() - 0.5 * df['Price/m2'].std())) & 
        (df['Price/m2'] <= (df['Price/m2'].mean() + 2 * df['Price/m2'].std()))]

# Aggregate prices by zip code
df_sorted = df.sort_values(by=['Zip Code', 'Price/m2'], ascending=[True, True])
price_stats = df_sorted.groupby('Zip Code', as_index=False)['Price/m2'].agg(mean_price=('mean'))

# Merge your dataset with the geospatial data on Zip Code
df_merged = belgium_map_merged.merge(price_stats, left_on='postcode', right_on='Zip Code', how='left')
df_merged = df_merged.drop(columns='geo_point_2d')
df_merged = df_merged.set_geometry('geo_shape')
print(df_merged.columns)
print(df_merged.geometry.head())


# Plot the heatmap as usual
fig, ax = plt.subplots(1, 1, figsize=(12, 10))

# Plot the heatmap with property price data
df_merged.plot(column='mean_price', 
              cmap='coolwarm',  # You can use a different colormap if desired
              linewidth=0.8, 
              ax=ax, 
              edgecolor='0.8', 
              legend=True, 
              legend_kwds={'label': "Price/m2"})

# Customize the plot
plt.title('Belgium Property Price Heatmap with Province Outlines', fontsize=15)
plt.axis('off')  # Remove axis
plt.show()