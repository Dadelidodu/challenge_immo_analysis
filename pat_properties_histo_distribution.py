import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Load the dataset
# Load the dataset
file_path = r"C:\Users\Administrator\BXL-Bouman-8\challenge_immo_analysis\data\normalized_dataset.csv"
file_cp_region_path = r"C:\Users\Administrator\BXL-Bouman-8\challenge_immo_analysis\data\cp_region.csv"
data = pd.read_csv(file_path)
cp_region_data = pd.read_csv(file_cp_region_path)

data = pd.merge(data, cp_region_data[['Zip Code', 'region_name_fr']], on='Zip Code', how='left')

# Add derived column: Price per square meter
#data['Price per Square Meter'] = data['Price'] / data['Livable Space (m2)']

# Filter data by region
data_belgium = data.copy()
data_wallonia = data[data['region_name_fr'] == 'Région wallonne']
data_flanders = data[data['region_name_fr'] == 'Région flamande']
data_brussels = data[data['region_name_fr'] == 'Région de Bruxelles-Capitale']

# Professional color palette
colors = {
    "Belgium": "#1f77b4",  # Blue
    "Wallonia": "#ff7f0e",  # Orange
    "Flanders": "#2ca02c",  # Green
    "Brussels": "#9467bd",  # Purple
}

# Set Seaborn theme for professional styling
sns.set_theme(style="whitegrid", font="Arial", rc={"axes.titlesize": 14, "axes.labelsize": 12})

# Function to format axes with commas
def format_ticks(x, _):
    return f'{int(x):,}'

# Function to plot histograms with density curves
def plot_seaborn_histogram_with_kde(data, column, title, color, ax):
    avg_value = data[column].mean()
    median_value = data[column].median()
    
    # Plot histogram with density curve
    sns.histplot(data[column], kde=True, bins=20, color=color, ax=ax, alpha=0.7, line_kws={"linewidth": 2})
    
    # Add average and median lines
    ax.axvline(avg_value, color='red', linestyle='--', linewidth=1.5, label=f'Avg: {avg_value:,.2f}')
    ax.axvline(median_value, color='green', linestyle='--', linewidth=1.5, label=f'Median: {median_value:,.2f}')
    
    # Customize the plot's appearance
    ax.set_title(title, weight='bold', color="#333333")
    ax.set_xlabel(f"{column} (€)", fontsize=12, weight='bold')
    ax.set_ylabel("Frequency", fontsize=12, weight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
    
    # Format x-axis ticks with commas
    ax.xaxis.set_major_formatter(FuncFormatter(format_ticks))

# Plot Price Distribution with Density Curves
fig, axes = plt.subplots(2, 2, figsize=(18, 12), tight_layout=True)
plot_seaborn_histogram_with_kde(data_belgium, 'Price', "Belgium - Price Distribution", colors["Belgium"], axes[0, 0])
plot_seaborn_histogram_with_kde(data_wallonia, 'Price', "Wallonia - Price Distribution", colors["Wallonia"], axes[0, 1])
plot_seaborn_histogram_with_kde(data_flanders, 'Price', "Flanders - Price Distribution", colors["Flanders"], axes[1, 0])
plot_seaborn_histogram_with_kde(data_brussels, 'Price', "Brussels - Price Distribution", colors["Brussels"], axes[1, 1])
plt.show()

# Plot Price per Square Meter Distribution with Density Curves
fig, axes = plt.subplots(2, 2, figsize=(18, 12), tight_layout=True)
plot_seaborn_histogram_with_kde(data_belgium, 'Price/m2', "Belgium - Price per Square Meter", colors["Belgium"], axes[0, 0])
plot_seaborn_histogram_with_kde(data_wallonia, 'Price/m2', "Wallonia - Price per Square Meter", colors["Wallonia"], axes[0, 1])
plot_seaborn_histogram_with_kde(data_flanders, 'Price/m2', "Flanders - Price per Square Meter", colors["Flanders"], axes[1, 0])
plot_seaborn_histogram_with_kde(data_brussels, 'Price/m2', "Brussels - Price per Square Meter", colors["Brussels"], axes[1, 1])
plt.show()
