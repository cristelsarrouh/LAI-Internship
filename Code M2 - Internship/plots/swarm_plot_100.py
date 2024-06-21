from statannotations.Annotator import Annotator
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load data
file_path = r'C:\Users\phpue\Desktop\cristell\plots\swarm_plot_100.csv'
df = pd.read_csv(file_path)

# Ensure the 'Year' column is unique and fetch unique values
years = df['Year'].unique()
print(years)

# Define pairs for annotation and order for plotting
pairs = [(years[0], years[1]), (years[0], years[2]), (years[0], years[3]),
         (years[1], years[2]), (years[1], years[3]), (years[2], years[3])]
order = [years[0], years[1], years[2], years[3]]

# Set style without grid lines
sns.set(style="white", rc={"axes.grid": False})

# Plot 1: Stripplot and Boxplot for 'wcmm'
plt.figure(figsize=(10, 7))
ax = sns.stripplot(x='Year', y='wcmm', data=df, dodge=True, order=order, color="black", alpha=0.5)
sns.boxplot(x='Year', y='wcmm', data=df, order=order, color="white")

plt.xlabel('Year range')
plt.ylabel('Word count (Mat&Met)')
plt.legend(title='')

annotator = Annotator(ax, pairs, data=df, x='Year', y='wcmm', order=order)
annotator.configure(test='Mann-Whitney', text_format='star', loc='inside')
annotator.apply_and_annotate()

plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Plot 2: Combined Stripplot and Boxplot for 'wcmm'
plt.figure(figsize=(4, 7))
ax = sns.stripplot(y='wcmm', data=df, color="black", alpha=0.5)
sns.boxplot(y='wcmm', data=df, color="white")

plt.xlabel('Combined')
plt.ylabel('Word count (Mat&Met)')
plt.legend(title='')

plt.tight_layout()

# Plot 3: Stripplot for 'page'
plt.figure(figsize=(4, 7))
sns.stripplot(x='Year', y='page', data=df, dodge=True, order=order, color="black", alpha=0.5)

plt.xlabel('Year range')
plt.ylabel('Pages')
plt.legend(title='')

plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Plot 4: Stripplot and Boxplot for 'wc_pages'
plt.figure(figsize=(10, 7))
ax = sns.stripplot(x='Year', y='wc_pages', data=df, dodge=True, order=order, color="black", alpha=0.5)
sns.boxplot(x='Year', y='wc_pages', data=df, order=order, color="white")

plt.xlabel('Year range')
plt.ylabel('Word count (Mat&Met) / Pages')
plt.legend(title='')

annotator = Annotator(ax, pairs, data=df, x='Year', y='wc_pages', order=order)
annotator.configure(test='Mann-Whitney', text_format='star', loc='inside')
annotator.apply_and_annotate()

plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Plot 5: Combined Stripplot and Boxplot for 'wc_pages'
plt.figure(figsize=(4, 7))
ax = sns.stripplot(y='wc_pages', data=df, color="black", alpha=0.5)
sns.boxplot(y='wc_pages', data=df, color="white")

plt.xlabel('Combined')
plt.ylabel('Word count (Mat&Met) / Pages')
plt.legend(title='')

plt.tight_layout()

# Show all plots
plt.show()
