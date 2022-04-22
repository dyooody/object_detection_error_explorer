from collections import defaultdict
from distutils.log import error
from flask import Flask, send_from_directory, render_template, request, jsonify
import logging, sys, json, os, pathlib, random

from importlib_metadata import distribution

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
app = Flask(__name__)

# Load some basic json files first
with open("client/public/datafiles/result_summary.json") as f:
    overall = json.load(f)
with open("client/public/datafiles/prediction_result.json") as f:
    pred_result = json.load(f)
with open("client/public/datafiles/det_val_dtype.json") as f:
    gt_val = json.load(f)

# for test
with open("client/public/datafiles/subset_result.json") as f:
    subset_result = json.load(f)

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
    print(overall['result_summary'].keys())
    print(overall['result_summary']['motorcycle'].keys())
    return jsonify(overall['result_summary'])

@app.route("/entire_distribution_chart/")
def entire_distribution_chart():
    print("def entire_distribution_chart()")
    return jsonify(overall['distribution_summary'])

@app.route("/get_image_src/<image_id>")
def get_image_src(image_id):
    img_name = pred_result[int(image_id)]['name']
    img_dir = "../bdd100k/images/100k/val/"+str(img_name)
    return jsonify(img_dir)

# modify this as type condition
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

def image_bbox_values(image_id):
    img_name = pred_result[int(image_id)]['name']
    img_dir = "../bdd100k/images/100k/val/"+str(img_name)
    labels = pred_result[int(image_id)]['labels']
    detected_label_vals = dict()
    detected_label_vals['image_dir'] = img_dir
    detected_label_vals['bbox_cate'] = dict()
    detected_label_vals['bbox_dtype'] = dict()
    detected_label_vals['gt_bbox'] = dict()
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

    gt_name = gt_val[int(image_id)]['name']
    if gt_name != img_name:
        print("ERROR!!")
    else:
        gt_labels = gt_val[int(image_id)]['labels']
        for j in range(len(gt_labels)):
            inst = gt_labels[j]
            cate = inst['category']
            if 'detected_type' in inst.keys():
                dtype = inst['detected_type']
                if dtype not in detected_label_vals["bbox_dtype"]:
                    detected_label_vals["bbox_dtype"][dtype] = []
                detected_label_vals['bbox_dtype'][dtype].append(inst['box2d'])
            if cate not in detected_label_vals['gt_bbox']:
                detected_label_vals['gt_bbox'][cate] = []
            detected_label_vals['gt_bbox'][cate].append(inst['box2d'])

    return detected_label_vals

@app.route("/default_image_show/")
def default_image_show():
    print("def default_image_show()")
    default_img_value_list = []

    for i in range(len(subset_result)):
        img_idx = subset_result[i]['index']
        detected_label_vals = image_bbox_values(img_idx)
        default_img_value_list.append(detected_label_vals)

    return jsonify(default_img_value_list)

def get_bbox_size_dist(bbox_size_vals):
    bbox_size_dist = dict()
    bbox_size_dist[10] = []
    bbox_size_dist[100] = []
    bbox_size_dist[300] = []
    bbox_size_dist[700] = []
    bbox_size_dist[1000] = []
    bbox_size_dist[3000] = []
    bbox_size_dist[7000] = []
    bbox_size_dist[10000] = []
    bbox_size_dist[50000] = []
    bbox_size_dist[100000] = []

    for i in range(len(bbox_size_vals)):
        current = bbox_size_vals[i]
        for i in current.keys():
            bs = float(current[i])

        if bs < 100:
            bbox_size_dist[10].extend(current.keys())
        elif bs >= 100 and bs < 300:
            bbox_size_dist[100].extend(current.keys())
        elif bs >= 300 and bs < 700:
            bbox_size_dist[300].extend(current.keys())
        elif bs >= 700 and bs < 1000:
            bbox_size_dist[700].extend(current.keys())
        elif bs >= 1000 and bs < 3000:
            bbox_size_dist[1000].extend(current.keys())
        elif bs >= 3000 and bs < 7000:
            bbox_size_dist[3000].extend(current.keys())
        elif bs >= 7000 and bs < 10000:
            bbox_size_dist[7000].extend(current.keys())
        elif bs >= 10000 and bs < 50000:
            bbox_size_dist[10000].extend(current.keys())
        elif bs >= 50000 and bs < 100000:
            bbox_size_dist[50000].extend(current.keys())
        elif bs >= 100000:
            bbox_size_dist[100000].extend(current.keys())

    return bbox_size_dist

def get_iou_val_dist(iou_vals):
    iou_val_dist = dict()
    iou_val_dist[0.0] = []
    iou_val_dist[0.1] = []
    iou_val_dist[0.2] = []
    iou_val_dist[0.3] = []
    iou_val_dist[0.4] = []
    iou_val_dist[0.5] = []
    iou_val_dist[0.6] = []
    iou_val_dist[0.7] = []
    iou_val_dist[0.8] = []
    iou_val_dist[0.9] = []

    for i in range(len(iou_vals)):
        current = iou_vals[i]
        for i in current.keys():
            cur = float(current[i])

        if cur < 0.1:
            iou_val_dist[0.0].extend(current.keys())
        elif cur >= 0.1 and cur < 0.2:
            iou_val_dist[0.1].extend(current.keys())
        elif cur >= 0.2 and cur < 0.3:
            iou_val_dist[0.2].extend(current.keys())
        elif cur >= 0.3 and cur < 0.4:
            iou_val_dist[0.3].extend(current.keys())
        elif cur >= 0.4 and cur < 0.5:
            iou_val_dist[0.4].extend(current.keys())
        elif cur >= 0.5 and cur < 0.6:
            iou_val_dist[0.5].extend(current.keys())
        elif cur >= 0.6 and cur < 0.7:
            iou_val_dist[0.6].extend(current.keys())
        elif cur >= 0.7 and cur < 0.8:
            iou_val_dist[0.7].extend(current.keys())
        elif cur >= 0.8 and cur < 0.9:
            iou_val_dist[0.8].extend(current.keys())
        elif cur >= 0.9:
            iou_val_dist[0.9].extend(current.keys())
    return iou_val_dist

def get_score_val_dist(score_vals):
    score_val_dist = dict()
    score_val_dist[0.2] = []
    score_val_dist[0.3] = []
    score_val_dist[0.4] = []
    score_val_dist[0.5] = []
    score_val_dist[0.6] = []
    score_val_dist[0.7] = []
    score_val_dist[0.8] = []
    score_val_dist[0.9] = []
    score_val_dist[1.0] = []

    for i in range(len(score_vals)):
        current = score_vals[i]
        for i in current.keys():
            cur = float(current[i])

        if cur < 0.3:
            score_val_dist[0.2].extend(current.keys())
        elif cur >= 0.3 and cur < 0.4:
            score_val_dist[0.3].extend(current.keys())
        elif cur >= 0.4 and cur < 0.5:
            score_val_dist[0.4].extend(current.keys())
        elif cur >= 0.5 and cur < 0.6:
            score_val_dist[0.5].extend(current.keys())
        elif cur >= 0.6 and cur < 0.7:
            score_val_dist[0.6].extend(current.keys())
        elif cur >= 0.7 and cur < 0.8:
            score_val_dist[0.7].extend(current.keys())
        elif cur >= 0.8 and cur < 0.9:
            score_val_dist[0.8].extend(current.keys())
        elif cur >= 0.9 and cur < 1.0:
            score_val_dist[0.9].extend(current.keys())
        elif cur >= 1.0:
            score_val_dist[1.0].extend(current.keys())
        else:
            print("error")
    return score_val_dist

@app.route("/detailed_class_info/<selected_class>/<selected_head>")
def get_detailed_class_info(selected_class, selected_head):
    dtype = selected_head.split(" ")[-1]
    print("selected_class ::: ", selected_class)
    print("selected_head ::: ", dtype)
    error_value = overall['result_summary'][selected_class]['dt_result'][dtype]

    print("def get_detailed_class_info")
    others = ['total_num', 'iou', 'bbox_size', 'detection_score']
    img_idx_list = []
    if dtype == '2':
        incorrect_class = dict()
        for key in list(error_value.keys()):
            if key not in others:
                img_indices = error_value[key]['img_idx']
                incorrect_class[key] = error_value[key]["num"]
                for k in (img_indices.keys()):
                    img_idx_list.extend(img_indices[k])
    else:
        for key in list(error_value.keys()):
            print(error_value.keys())
            if key not in others:
                print(key)
                if error_value[key] != 'null':
                    for k in error_value['index_list'].keys():
                        img_idx_list.extend(error_value['index_list'][k])

    result = dict()
    result['total_num'] = error_value['total_num']
    result['bbox_size'] = get_bbox_size_dist(error_value['bbox_size']['val_list'])
    result['iou'] = get_iou_val_dist(error_value['iou']['val_list'])
    result['detection_score'] = get_score_val_dist(error_value['detection_score']['val_list'])

    print(result['bbox_size'][3000][:10])
    result['dtype'] = dtype
    if dtype == '2':
        result['inc_classes'] = incorrect_class

    img_val_list = []
    for i in range(len(img_idx_list)):
        img_id = img_idx_list[i]
        detected_label_vals = image_bbox_values(img_id)
        img_val_list.append(detected_label_vals)

    print("image len:::: ", len(img_val_list))

    result['image_values'] = img_val_list[:100]

    return jsonify(result)

@app.route("/get_chart_detail_info/<selected_class>/<selected_dtype>/<selected_key>/<chart_type>/")
def get_chart_detail_info(selected_class, selected_dtype, selected_key, chart_type):
    error_value = overall['result_summary'][selected_class]['dt_result'][selected_dtype]
    others = ['total_num', 'iou', 'bbox_size', 'detection_score']
    if chart_type == 'bbox':
        distr = get_bbox_size_dist(error_value['bbox_size']['val_list'])
        res = distr[int(selected_key)]
    elif chart_type == 'iou':
        distr = get_iou_val_dist(error_value['iou']['val_list'])
        res = distr[float(selected_key)]
    elif chart_type == 'score':
        distr = get_score_val_dist(error_value['detection_score']['val_list'])
        res = distr[float(selected_key)]
    elif chart_type == 'type_class':
        res = []
        if selected_dtype != '2':
            print('error')
        else:
            print(list(error_value.keys()))
            for key in list(error_value.keys()):
                if key not in others:
                    if error_value[key] != 'null':
                        for k in error_value[key]['img_idx'].keys():
                            res.extend(error_value[key]['img_idx'][k])



    img_val_list = []
    img_idx_list = list(set(res))[:100]
    print(img_idx_list[:30])
    for i in range(len(img_idx_list)):
        img_id = img_idx_list[i]
        detected_label_vals = image_bbox_values(img_id)
        img_val_list.append(detected_label_vals)

    return jsonify(img_val_list)


@app.route("/get_file_bbox_vals/<image_id>")
def get_file_bbox_vals(image_id):
    print("get_file_bbox_vals({})".format(image_id))
    detected_label_vals = image_bbox_values(image_id)

    return jsonify(detected_label_vals)




if __name__ == "__main__":
    app.run(debug=True)