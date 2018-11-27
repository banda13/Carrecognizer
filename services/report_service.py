import os
import json
import paths
from flask import Flask, render_template

from utils.json_utils import decoder_hook

template_folder = paths.ROOT_DIR + "/templates/"
statistics_folder = paths.ROOT_DIR + '/statistics'
history_location = paths.ROOT_DIR + "/history/"
app = Flask(__name__, template_folder=template_folder, static_folder=statistics_folder)


def iterate(dictionary):
    for key, value in dictionary.items():
        if isinstance(value, dict):
            iterate(value)
            continue
        if isinstance(value, str) and value.startswith(paths.STAT_DIR):
            value = value.replace(paths.STAT_DIR, "")
            print("New value: " + value)

@app.route("/")
def main_template():
    return render_template("main_report.html", reports=os.listdir(history_location))

@app.route("/template/<name>")
def get_template(name):
    with open(history_location + name, 'r') as temp:
        template_params = json.load(temp, object_hook=decoder_hook)
        template_params['cnn3_out']['plot'] = template_params['cnn3_out']['plot'].replace(paths.STAT_DIR, "")
        return render_template("report.html", report=template_params)

if __name__ == '__main__':
    app.run(debug=True)