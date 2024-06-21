import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

file_path = 'plot.csv'
df = pd.read_csv(file_path)

# Ensure the 'Ratio' column is numeric
if 'Ratio' in df.columns:
    df['Ratio'] = pd.to_numeric(df['Ratio'].str.replace(',', '.'), errors='coerce')

custom_palette = {"Llama": "purple", "Grobid": "blue"}

plt.figure(figsize=(10,7))
sns.stripplot(x='Journal', y='Ratio', hue='Tool', data=df, dodge=True, palette=custom_palette, alpha=0.5)
plt.xlabel('Journal')
plt.ylabel('Extracted word count / Manual word count')
plt.legend(title='Tool')
plt.axhspan(0.85, 1.15, color='lightgreen', alpha=0.3)
# plt.axhspan(-0.05,0.05, color='red', alpha=0.25)
plt.axvspan(0.5,1.5, color='grey', alpha=0.05)
plt.axvspan(2.5,3.5, color='grey', alpha=0.05)
plt.axvspan(4.5,5.5, color='grey', alpha=0.05)
plt.axvspan(6.5,7.5, color='grey', alpha=0.05)
plt.axvspan(8.5,9.5, color='grey', alpha=0.05)


plt.ylim(-0.5, 6)
plt.xticks(rotation=45, ha='right')
# plt.yscale('log')
plt.tight_layout()
plt.show()
