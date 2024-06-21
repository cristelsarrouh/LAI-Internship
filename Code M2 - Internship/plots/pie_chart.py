import matplotlib.pyplot as plt
import seaborn as sns

labels_1 = ['Introduction', 'Materials & Methods', 'Results', 'Discussion']
sizes_1 = [23, 13, 6, 21]

labels_2 = ['4', '3', '2', '1']
sizes_2 = [1, 4, 7, 33]

# Total number of references
total_references_1 = sum(sizes_1)
total_references_2 = sum(sizes_2)

# Define a custom pastel color palette with blue instead of green and green instead of orange
custom_colors = sns.color_palette(["#FFB3BA", "#BAFFC9", "#FFFFBA", "#BAE1FF", "#FFDFBA"])

# Plot first pie chart
plt.figure(figsize=(7, 6))
plt.pie(sizes_1, labels=labels_1, autopct='%1.1f%%', wedgeprops={"linewidth": 1, "edgecolor": "white"}, colors=custom_colors[:len(sizes_1)], radius=0.65)

# Plot second pie chart
plt.figure(figsize=(6, 6))
plt.pie(sizes_2, labels=labels_2, autopct='%1.1f%%', wedgeprops={"linewidth": 1, "edgecolor": "white"}, colors=custom_colors[:len(sizes_2)], radius=0.65)

plt.show()
