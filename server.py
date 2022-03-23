from flask import Flask, send_from_directory, render_template, request, jsonify
import random, logging, sys, json

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
app = Flask(__name__)

with open("client/public/datafiles/overall_summary.json") as f:
    overall = json.load(f)

# Path for our main Svelte page
@app.route("/")
def base():
    return send_from_directory('client/public', 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)

@app.route("/json_trial/<instance_id>/<label_id>")
def printout_function(instance_id, label_id):
    print("instance_id, label_id: {}, {}".format(instance_id, label_id))
    with open("client/public/datafiles/prediction_result_subset.json") as f:
        result_file = json.load(f)
    inst = result_file[int(instance_id)]
    print(inst.keys())
    label = inst['labels'][int(label_id)]
    print(label.keys())
    return jsonify(label)

@app.route("/class_values/")
def get_class_vals():
    print("def get_class_vals()")
    print(overall['class_summary'].keys())
    return jsonify(overall['class_summary'])

@app.route("/detection_types/")
def get_detection_types():
    print("def get_detection_types()")
    print(overall['detection_type_summary'].keys())
    return jsonify(overall['detection_type_summary'])

@app.route("/class_detection_types/")
def class_detection_types():
    print("class_detection_Types()")
    print(overall["category_detected"].keys())
    return jsonify(overall['category_detected'])

@app.route("/detect_type_description/")
def get_detect_type_desc():
    with open("client/public/datafiles/detection_type_description.json") as f:
        desc_file = json.load(f)
    print(desc_file)
    return jsonify(desc_file)

@app.route("/more_than_n_labels/<num_of_labels>")
def filter_images(num_of_labels):
    return True

if __name__ == "__main__":
    app.run(debug=True)