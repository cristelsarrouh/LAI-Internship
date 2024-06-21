import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('articles_per_year.csv')

# Filter data for the specific queries
queries_of_interest1 = ['T cell adhesion', 'T cell activation', 'T cell spreading']
filtered_df1 = df[df['query'].isin(queries_of_interest1)]

queries_of_interest2 = ['lymphocyte activation', 'T lymphocyte activation', 'lymphocyte adhesion', 'T lymphocyte adhesion', 'immune synapse', 'phase transition']
filtered_df2 = df[df['query'].isin(queries_of_interest2)]

queries_of_interest3 = ['T cell spreading AND activation', 'phase transition AND immune cell', 'T cell adhesion OR T lymphocyte adhesion', 'T cell mechanotransduction OR T lymphocyte mechanotransduction']
filtered_df3 = df[df['query'].isin(queries_of_interest3)]

queries_of_interest4 = ['lymphocyte activation', 'T lymphocyte activation', 'lymphocyte activation [Title]', 'T lymphocyte activation [Title]']
filtered_df4 = df[df['query'].isin(queries_of_interest4)]


# Aggregate the data by year to get the total count of articles
total_articles_by_year = df.groupby('Year')['Count'].sum().reset_index()

# Set the theme for the plot
sns.set_theme(style="white")

# Create the first plot
plt.figure(figsize=(5,4), dpi=150)
sns.lineplot(x="Year", y="Count", hue="query", data=filtered_df1)
# plt.title('PubMed: Non-specific query + [Title/Abstract] ')
plt.xlabel('Year')
plt.ylabel('Articles Count')
plt.legend(title='Query', loc='upper left', fontsize='7')
plt.grid(False)  # Turn off grid lines
plt.xlim(1970, 2020)
plt.tight_layout()
plt.show()

# Create the second plot
plt.figure(figsize=(5,4), dpi=150)
sns.lineplot(x="Year", y="Count", hue="query", data=filtered_df2)
# plt.title('PubMed: Specific query + [Title/Abstract] ')
plt.xlabel('Year')
plt.ylabel('Articles Count')
plt.legend(title='Query', loc='upper left', fontsize='7')
plt.grid(False)  # Turn off grid lines
plt.xlim(1970, 2020)
plt.tight_layout()
plt.show()

# Create the third plot
plt.figure(figsize=(5, 4), dpi=150)
sns.lineplot(x="Year", y="Count", hue="query", data=filtered_df3)
# plt.title('PubMed: Non-specific query + condition + [Title/Abstract] ')
plt.xlabel('Year')
plt.ylabel('Articles Count')
plt.legend(title='Query', loc='upper left', fontsize='6')
plt.grid(False)  # Turn off grid lines
plt.xlim(1970, 2020)
plt.tight_layout()
plt.show()

# Create the fourth
plt.figure(figsize=(5,4), dpi=150)
sns.lineplot(x="Year", y="Count", hue="query", data=filtered_df4)
# plt.title('PubMed: Query comparison')
plt.xlabel('Year')
plt.ylabel('Articles Count')
plt.legend(title='Query', loc='upper left', fontsize='6')
plt.grid(False)  # Turn off grid lines
plt.xlim(1970, 2020)
plt.tight_layout()
plt.show()

# Create the fourth plot for total number of articles over the years
plt.figure(figsize=(5,4), dpi=150)
sns.lineplot(x="Year", y="Count", data=total_articles_by_year, color='black')
# plt.title('Combined queries')
plt.xlabel('Year')
plt.ylabel('Total Articles Count')
plt.grid(False)  # Turn off grid lines
plt.xlim(1970, 2020)
plt.tight_layout()
plt.show()

