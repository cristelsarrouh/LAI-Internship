import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv('before_after.csv')

xcol = 'Tool'
ycol = 'Words'
match = 'Article'

plt.figure(figsize=(3, 6))
sns.set_palette("dark")
sns.scatterplot(data=data, x=xcol, y=ycol, hue=match, s=100, alpha=0.5)
sns.lineplot(data=data, x=xcol, y=ycol, hue=match)

plt.xlabel('Tool')
plt.ylabel('Number of Words')
plt.xticks(rotation=45, ha='right')

plt.axvspan(0.5,1.5, color='lightgreen', alpha=0.3)
# plt.yscale('log')
plt.tight_layout()

plt.legend().remove()

plt.show()
