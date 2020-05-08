import os
import collections
import matplotlib.pyplot as plt
import paths

categories = {}
for f in os.listdir(paths.N_SCOUT_IMG_DIR):
    categories[f] = (len(os.listdir(paths.N_SCOUT_IMG_DIR + f)))

labels, values = [], []
for w in sorted(categories, key=categories.get, reverse=True)[:8]:
    labels.append(w)
    values.append(categories[w])

plt.bar(labels,values)
plt.show()

