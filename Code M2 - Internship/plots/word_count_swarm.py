import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# file_path = 'Untitled1.csv'
file_path = 'wc_swarm.csv'
df = pd.read_csv(file_path)

# Ensure the 'Ratio' column is numeric
if 'Ratio' in df.columns:
    df['Ratio'] = pd.to_numeric(df['Ratio'].str.replace(',', '.'), errors='coerce')

df['Word count'] = df['Word count'].replace({0:np.nan})

custom_palette = {"manually":"white","llama": "white", "grobid": "white"}
custom_palette2 = {"manually":"grey","llama": "orange", "grobid": "blue"}
plt.figure(figsize=(10, 7))
sns.boxplot(x='Journal', y='Word count', hue='Tool', data=df, dodge=True, palette=custom_palette)

sns.stripplot(x='Journal', y='Word count', hue='Tool', data=df, dodge=True, palette=custom_palette2, alpha=0.5)
plt.xlabel('Journal')
plt.ylabel('Word count extracted manually')
plt.legend(title='Tool')

# plt.axhspan(-0.05,0.05, color='red', alpha=0.25)
plt.axvspan(0.5,1.5, color='grey', alpha=0.05)
plt.axvspan(2.5,3.5, color='grey', alpha=0.05)
plt.axvspan(4.5,5.5, color='grey', alpha=0.05)
plt.axvspan(6.5,7.5, color='grey', alpha=0.05)
plt.axvspan(8.5,9.5, color='grey', alpha=0.05)



plt.xticks(rotation=45, ha='right')
# plt.yscale('log')
plt.ylim(0,)
plt.legend().remove()
plt.tight_layout()
plt.show()
