import json
import xlsxwriter

import paths

history_files = ['Cabat.json', 'Goot.json', 'Baro.json', 'Pow.json', 'Haupaca.json', 'Gindaasj,zllic slinSgepet brare.json', 'Hobworos).json', 'Anddiink.json']
history_dir = '../history/'
excel_file = 'result.xlsx'
print("Export history %s into %s" % (str(history_files), excel_file))

print("Create a workbook and add a worksheet")
workbook = xlsxwriter.Workbook(excel_file)
worksheet = workbook.add_worksheet()

worksheet.write(0, 0, 'Name')
worksheet.write(0, 1, 'Accuracy')
worksheet.write(0, 2, 'Top3-accuracy')
worksheet.write(0, 3, 'Probability')
col = 1

for hist in history_files:
    print("Checking categories from %s" % hist)
    with open(history_dir + hist) as f:
        hist_json = json.load(f)

    for c, value in hist_json['test']['category_results'].items():
        worksheet.write(col, 0, c)
        worksheet.write(col,1, value['accuracy'])
        worksheet.write(col, 2, value['top3_accuracy'])
        worksheet.write(col, 3, value['avg_probabilities'])
        col += 1

workbook.close()
