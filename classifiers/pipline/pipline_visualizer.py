import json
import numpy as np
import matplotlib.pyplot as plt

# read data
result_json = "result_final.json"
with open(result_json) as f:
  data = json.load(f)

# placeholders
categories = []
all_acc = []
all_top3 = []
all_precision = []
all_miss_classification = {}
make_statistics = {}
i = 0

visualization_dest_folder = "visualization/"

# process data
for category, category_data in data.items():
    make, model = category.split('-', 1)
    acc = category_data['acc']
    top3_acc = category_data['top3_acc']
    avg_prec = category_data['avg_prec']
    miss_classified = category_data['missed_classes']
    miss_classified[category] = category_data['correct']

    if acc > 0.1: # skip irrelevant classes
        i += 1
        categories.append(category)
        all_acc.append(acc)
        all_top3.append(top3_acc)
        all_precision.append(avg_prec)
        all_miss_classification[category] = miss_classified

        if make in make_statistics.keys(): # for sure there has to be a more pythonic way to do this :/
            make_statistics[make]['count'] += 1
            make_statistics[make]['acc'].append(acc)
            make_statistics[make]['top3_acc'].append(top3_acc)
            make_statistics[make]['avg_prec'].append(avg_prec)
            make_statistics[make]['missed_classes'].append(miss_classified)
        else:
            make_statistics[make] = {
                "count": 1,
                "acc": [acc],
                "top3_acc": [top3_acc],
                "avg_prec": [avg_prec],
                "missed_classes": [miss_classified]
            }

# convert everything to numpy
categories = np.array(categories)
all_acc = np.array(all_acc)
all_top3 = np.array(all_top3)
all_precision = np.array(all_precision)

# print statistics
print("Total statistics")
print("Total number of classes: {}".format(i))
print("Total accuracy: {}".format(np.mean(all_acc)))
print("Total top3 accuracy: {}".format(np.mean(all_top3)))
print("Total precision: {}".format(np.mean(all_precision)))
print("\n")

print("Statistics for makes")
for make, make_data in make_statistics.items():
    print("Statistics for make: {}".format(make))
    print("{} number of classes: {}".format(make, make_data["count"]))
    print("{} accuracy: {}".format(make, np.mean(make_data["acc"])))
    print("{} top3 accuracy: {}".format(make, np.mean(make_data["top3_acc"])))
    print("{} precision: {}".format(make, np.mean(make_data["avg_prec"])))
    print("\n")

# plotting

# plot miss classification
for make, class_result in all_miss_classification.items():
    plt.title(make)
    plt.ylabel('Number')
    plt.xlabel('Category')
    plt.bar(class_result.keys(), class_result.values())
    plt.xticks(rotation=90)
    plt.gcf().subplots_adjust(bottom=0.4)
    plt.savefig(visualization_dest_folder + "correlations/" +  make + ".png")
    plt.close()