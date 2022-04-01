from collections import defaultdict
from flask import Flask, send_from_directory, render_template, request, jsonify
import logging, sys, json, os, pathlib, random

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
app = Flask(__name__)

# Load some basic json files first
with open("client/public/datafiles/overall_summary.json") as f:
    overall = json.load(f)
with open("client/public/datafiles/prediction_result.json") as f:
    pred_result = json.load(f)

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
    label = inst['labels'][int(label_id)]
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
    return jsonify(desc_file)

@app.route("/detailed_class_info/<selected_class>")
def get_detailed_class_info(selected_class):
    print("selected_class ::: ", selected_class)
    print("def get_detailed_class_info")
    return jsonify("Hello")

@app.route("/get_image_src/<image_id>")
def get_image_src(image_id):
    img_name = pred_result[int(image_id)]['name']
    img_dir = "../bdd100k/images/100k/val/"+str(img_name)
    return jsonify(img_dir)

@app.route("/images_with_conditions/<conditions>") #/<num_of_class>/<mAP_val>")
def images_with_conditions(conditions):#, num_of_class, mAP_val):
    conditions = conditions.split(",")
    print("given condition:: ", conditions)
    print("num of labels: {}, num of classes: {}, mAP more than: {}, and number of \
images to show: {}".format(conditions[0], conditions[1], conditions[2], conditions[3]))
    num_of_labels = int(conditions[0])
    num_of_classes = int(conditions[1])
    overall_mAP = float(conditions[2])
    num_of_images = int(conditions[3])

    idx_lists = []
    for idx in range(len(pred_result)):
        cur = pred_result[idx]
        if ((num_of_labels-5) <= len(cur['labels']) and (len(cur['labels']) <= (num_of_labels+5))
        and (len(cur['dt_cls'])>=num_of_classes) and (cur['mAP']>=overall_mAP)):
            idx_lists.append(idx)
    chose_idx_lists = random.sample(idx_lists, num_of_images)
    print("idx list match with conditions:: ", chose_idx_lists)

    return jsonify(chose_idx_lists)



@app.route("/get_file_bbox_vals/<image_id>")
def get_file_bbox_vals(image_id):
    print("get_file_bbox_vals({})".format(image_id))
    img_name = pred_result[int(image_id)]['name']
    print("image_name ::: ", img_name)
    absolute_img_dir = "client/public/bdd100k/images/100k/val/"+str(img_name)
    img_dir = "../bdd100k/images/100k/val/"+str(img_name)
    print("img_dir::: ", img_dir)
    print("img_dir exists????? ::::::", pathlib.Path(absolute_img_dir).exists())
    labels = pred_result[int(image_id)]['labels']
    print("length of labels for image id {} is {}".format(image_id, len(labels)))
    detected_label_vals = dict()
    detected_label_vals['image_dir'] = img_dir
    detected_label_vals['bbox_cate'] = dict()
    detected_label_vals['bbox_dtype'] = dict()
    for i in range(len(labels)):
        inst = labels[i]
        cate = inst['category']
        dtype = inst['detected_type']
        if cate not in detected_label_vals['bbox_cate']:
            detected_label_vals['bbox_cate'][cate] = []
        if dtype not in detected_label_vals['bbox_dtype']:
            detected_label_vals['bbox_dtype'][dtype] = []
        detected_label_vals['bbox_cate'][cate].append(inst['box2d'])
        detected_label_vals['bbox_dtype'][dtype].append(inst['box2d'])

    return jsonify(detected_label_vals)



if __name__ == "__main__":
    app.run(debug=True)