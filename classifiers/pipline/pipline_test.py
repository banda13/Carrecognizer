"""
betölteni a modellt

végig iterálni a validation-on

számolni:
 - accuracy
 - top3 accuracy
 - egyes make pontosságokat
 - egyes modell pontosságokat
 - make helyett miket tévesztett
 - modell helyett miket téveszett

 - vizualizálni
"""
import os
import json
import operator
from classifiers.pipline.pipline import ClassifierPipline

validation_folder = "../../data/validation_old/"
limit_pre_cat = 100

print("Initialize classifier")
pipline = ClassifierPipline(160, 160)
final_result = {}
try:
    for category in os.listdir(validation_folder):
        print("Testing category: {}".format(category))
        make, model = category.split("-")[0], category.split("-")[1:]
        all, correct, top3_correct, avg_prec = 0, 0, 0, 0
        miss_classified_classes = {}
        for img in os.listdir(validation_folder + category)[:limit_pre_cat]:
            img_path = validation_folder + category + "/" + img
            result = pipline.classify(img_path)
            t = max(result.items(), key=operator.itemgetter(1))
            pred_model, pred_acc = t[0], t[1]

            all += 1
            avg_prec += (pred_acc / limit_pre_cat)
            if category in result.keys():
                top3_correct += 1

            if pred_model == category:
                correct += 1
            else:
                if pred_model in miss_classified_classes.keys():
                    miss_classified_classes[pred_model] += 1
                else:
                    miss_classified_classes[pred_model] = 1
        acc = correct / all
        top3_acc = top3_correct / all
        print("Category result : {} acc, {} top, {} avg_prec".format(acc, top3_acc, avg_prec))
        final_result[category] = {
            "acc": acc,
            "top3_acc": top3_acc,
            "all": all,
            "correct": correct,
            "top3_correct": top3_correct,
            "avg_prec": avg_prec,
            "missed_classes": miss_classified_classes
        }

    with open('result.json', 'w') as f:
        json.dump(final_result, f)
except Exception as e:
    print("Error while testing: {}".format(e))
    with open('result.json', 'w') as f:
        json.dump(final_result, f)
    raise Exception(e)
