from distutils.log import error
from flask import Flask, send_from_directory, jsonify
import logging, sys, json, random


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
app = Flask(__name__)

detected_names = {
    'correct detection' : 'type 1',
    'localization error': 'type 3',
    'classification error': 'type 2',
    'cls and loc error': 'type 4',
    'duplication error': 'type 5',
    'back detect error': 'type 6',
    'min-overlap error' : 'type 8'
}

gt_names = {
    'match + correct' : '1',
    'match + cls' : '2',
    'match + loc' : '3',
    'match + cls and loc' : '4',
    'match + incorrect': '5',
    'matches + cor, dup': '6',
    'matches + cor, cls' : '7',
    'matches + cor, loc': '8',
    'matches + with cor': '9',
    'matches + incor': '10',
    'missed detected': '11'
}

# Load some basic json files first
with open("client/public/datafiles/nms_summary.json") as f:
    overall = json.load(f)
with open("client/public/datafiles/prediction_result.json") as f:
    pred_result = json.load(f)
with open("client/public/datafiles/det_val_gt_cate.json") as f:
    gt_val = json.load(f)
with open("client/public/datafiles/detection_type_description.json") as f:
    desc_result = json.load(f)


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

@app.route("/gt_values/")
def get_gt_vals():
    print("def get_gt_vals()")
    print(overall['gt_summary'].keys())
    return jsonify(overall['gt_summary'])

@app.route("/dt_types/")
def get_detection_types():
    return jsonify(desc_result['detection'])

@app.route("/gt_types/")
def get_gt_types():
    return jsonify(desc_result['ground_truth'])

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

def image_bbox_values(image_id, selected_cate, selected_dtype):
    if selected_dtype != None:
        selected_dtype = int(selected_dtype)
    img_name = pred_result[int(image_id)]['name']
    img_dir = "../bdd100k/images/100k/val/"+str(img_name)
    labels = pred_result[int(image_id)]['labels']
    detected_label_vals = dict()
    detected_label_vals['image_dir'] = img_dir
    detected_label_vals['bbox_cate'] = dict()
    detected_label_vals['bbox_cate']['box'] = dict()
    detected_label_vals['bbox_cate']['gt_id'] = dict()
    detected_label_vals['bbox_cate']['gt_bbox'] = dict()
    detected_label_vals['bbox_cate']['gt_cate'] = dict()

    detected_label_vals['gt_bbox'] = dict()

    detected_label_vals['total_dt'] = dict()
    detected_label_vals['total_gt'] = dict()
    if selected_cate != None:
        detected_label_vals['cate_dtype'] = dict()
        detected_label_vals['cate_dtype']['box'] = []
        detected_label_vals['cate_dtype']['score'] = []
        detected_label_vals['cate_dtype']['pred'] = []
        detected_label_vals['cate_dtype']['gt'] = []
        detected_label_vals['cate_dtype_gt'] = dict()
        detected_label_vals['cate_dtype_gt']['gt_id'] = set()
        detected_label_vals['cate_dtype_gt']['gt_bbox'] = dict()
        detected_label_vals['cate_dtype_gt']['gt_cate'] = dict()



    for i in range(len(labels)):
        inst = labels[i]
        if inst['nms'] == True:
            cate = inst['category']
            dtype = inst['detected_type']
            if cate not in detected_label_vals['bbox_cate']['box']:
                detected_label_vals['bbox_cate']['box'][cate] = dict()
                detected_label_vals['bbox_cate']['gt_id'][cate] = dict()
                detected_label_vals['bbox_cate']['gt_bbox'][cate] = dict()
                detected_label_vals['bbox_cate']['gt_cate'][cate] = dict()
                detected_label_vals['total_dt'][cate] = []
            if dtype not in detected_label_vals['bbox_cate']['box'][cate]:
                detected_label_vals['bbox_cate']['box'][cate][dtype] = []
                detected_label_vals['bbox_cate']['gt_id'][cate][dtype] = set()
                detected_label_vals['bbox_cate']['gt_bbox'][cate][dtype] = []
                detected_label_vals['bbox_cate']['gt_cate'][cate][dtype] = []
            detected_label_vals['total_dt'][cate].append(inst['box2d'])
            detected_label_vals['bbox_cate']['box'][cate][dtype].append(inst['box2d'])
            if 'max_iou_index_from_truth' in inst.keys():
                detected_label_vals['bbox_cate']['gt_id'][cate][dtype].add(inst['max_iou_index_from_truth'])
            if selected_cate != None:
                if cate == selected_cate and dtype == selected_dtype:
                    detected_label_vals['cate_dtype']['box'].append(inst['box2d'])
                    detected_label_vals['cate_dtype']['score'].append(inst['score'])
                    detected_label_vals['cate_dtype']['pred'].append(inst['category'])
                if 'max_iou_index_from_truth' in inst.keys():
                    if cate == selected_cate and dtype == selected_dtype:
                        detected_label_vals['cate_dtype_gt']['gt_id'].add(inst['max_iou_index_from_truth'])
                        detected_label_vals['cate_dtype']['gt'].append(inst['max_iou_value_category'])

    gt_name = gt_val[int(image_id)]['name']
    if gt_name != img_name:
        print("ERROR!!")
    else:
        gt_labels = gt_val[int(image_id)]['labels']
        for cate in detected_label_vals['bbox_cate']['gt_id'].keys():
            for dtype in detected_label_vals['bbox_cate']['gt_id'][cate].keys():
                gt_ids = detected_label_vals['bbox_cate']['gt_id'][cate][dtype]
                detected_label_vals['bbox_cate']['gt_id'][cate][dtype] = list(detected_label_vals['bbox_cate']['gt_id'][cate][dtype])
                for j in range(len(gt_labels)):
                    inst = gt_labels[j]
                    id = inst['id']
                    if id in gt_ids:
                        '''if cate not in detected_label_vals['gt_bbox'].keys():
                            detected_label_vals['gt_bbox'][cate] = dict()
                        if dtype not in detected_label_vals['gt_bbox'][cate].keys():
                            detected_label_vals['gt_bbox'][cate][dtype] = []
                        detected_label_vals['gt_bbox'][cate][dtype].append(inst['box2d'])'''
                        detected_label_vals['bbox_cate']['gt_bbox'][cate][dtype].append(inst['box2d'])
                        detected_label_vals['bbox_cate']['gt_cate'][cate][dtype].append(inst['category'])
        for j in range(len(gt_labels)):
            inst = gt_labels[j]
            cate = inst['category']
            if cate not in detected_label_vals['total_gt'].keys():
                detected_label_vals['total_gt'][cate] = []
            detected_label_vals['total_gt'][cate].append(inst['box2d'])
            # because of detected type 7

            '''if 'detected_type' in inst.keys():
                dtype = inst['detected_type']
                if dtype not in detected_label_vals["bbox_dtype"]['box']:
                    detected_label_vals["bbox_dtype"]['box'][dtype] = []
                    detected_label_vals["bbox_dtype"]['score'][dtype] = []
                    detected_label_vals["bbox_dtype"]['pred'][dtype] = []
                if selected_cate != None:
                    if cate == selected_cate and dtype == selected_dtype:
                        detected_label_vals['cate_dtype']['box'].append(inst['box2d'])
                        detected_label_vals['cate_dtype']['score'].append(0)
                        detected_label_vals['cate_dtype']['pred'].append('None')
                detected_label_vals['bbox_dtype']['box'][dtype].append(inst['box2d'])
                detected_label_vals['bbox_dtype']['score'][dtype].append(0)'''

    if selected_cate != None:
        idx_list = detected_label_vals['cate_dtype_gt']['gt_id']
        gt_labels = gt_val[int(image_id)]['labels']
        for k in range(len(gt_labels)):
            inst = gt_labels[k]
            id = inst['id']
            gt_type = inst['gt_category']
            if id in idx_list:
                if gt_type not in detected_label_vals['cate_dtype_gt']['gt_bbox']:
                    detected_label_vals['cate_dtype_gt']['gt_bbox'][gt_type] = []
                if gt_type not in detected_label_vals['cate_dtype_gt']['gt_cate']:
                    detected_label_vals['cate_dtype_gt']['gt_cate'][gt_type] = []
                detected_label_vals['cate_dtype_gt']['gt_bbox'][gt_type].append(inst['box2d'])
                detected_label_vals['cate_dtype_gt']['gt_cate'][gt_type].append(inst['category'])

        detected_label_vals['cate_dtype_gt']['gt_id'] = list(detected_label_vals['cate_dtype_gt']['gt_id'])

    return detected_label_vals

@app.route("/default_image_show/")
def default_image_show():
    print("def default_image_show()")
    default_img_value_list = []


    for i in range(200):
        img_idx = pred_result[i]['index']
        detected_label_vals = image_bbox_values(img_idx, None, None)
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

def gt_image_bbox_values(image_id, selected_cate, selected_gtype):
    img_name = gt_val[int(image_id)]['name']
    img_dir = "../bdd100k/images/100k/val/"+str(img_name)
    #labels = pred_result[int(image_id)]['labels']
    gt_labels = gt_val[int(image_id)]['labels']

    gt_label_vals = dict()
    gt_label_vals['image_dir'] = img_dir
    gt_label_vals['cate_dtype'] = dict()
    gt_label_vals['cate_dtype']['box'] = []

    for i in range(len(gt_labels)):
        inst = gt_labels[i]
        cate = inst['category']
        gtype = inst['gt_category']
        if cate == selected_cate and gtype == int(selected_gtype):
            gt_label_vals['cate_dtype']['box'].append(inst['box2d'])

    return gt_label_vals

@app.route("/ground_truth_images/<selected_class>/<selected_head>")
def get_detailed_gt_info(selected_class, selected_head):
    type_val = gt_names[selected_head]
    gt_values = overall['gt_summary'][selected_class]['gt_type'][type_val]['img_idx']

    print("num :::: ", overall['gt_summary'][selected_class]['gt_type'][type_val]['num'])
    img_idx_list = []
    for key in gt_values.keys():
        img_idx_list.extend(gt_values[key])
    print(len(img_idx_list))

    image_value_list = []
    for img_id in img_idx_list:
        gt_label_vals = gt_image_bbox_values(img_id, selected_class, type_val)
        image_value_list.append(gt_label_vals)

    gt_values = dict()
    gt_values['image_values'] = image_value_list[:300]
    gt_values['gtype'] = type_val

    return jsonify(gt_values)

@app.route("/detailed_class_info/<selected_class>/<selected_head>")
def get_detailed_class_info(selected_class, selected_head):
    type_name = detected_names[selected_head]
    dtype = type_name.split(" ")[-1]
    print("selected_class ::: ", selected_class)
    print("selected_head ::: ", dtype)
    error_value = overall['result_summary'][selected_class]['dt_result'][dtype]
    chart_value = overall['linear_chart'][selected_class][dtype]

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
            if key not in others:
                if error_value[key] != 'null':
                    for k in error_value['index_list'].keys():
                        img_idx_list.extend(error_value['index_list'][k])

    result = dict()
    result['total_num'] = error_value['total_num']
    result['bbox_size'] = get_bbox_size_dist(error_value['bbox_size']['val_list'])
    result['iou'] = get_iou_val_dist(error_value['iou']['val_list'])
    result['detection_score'] = get_score_val_dist(error_value['detection_score']['val_list'])
    result['chart_iou'] = chart_value['iou']
    result['chart_bbox'] = chart_value['bbox']
    result['chart_score'] = chart_value['score']

    print(result['bbox_size'][3000][:10])
    result['dtype'] = dtype
    if dtype == '2':
        result['inc_classes'] = incorrect_class

    img_val_list = []
    for i in range(len(img_idx_list)):
        img_id = img_idx_list[i]
        detected_label_vals = image_bbox_values(img_id, selected_class, dtype)
        img_val_list.append(detected_label_vals)

    print("image len:::: ", len(img_val_list))

    result['image_values'] = img_val_list[:300]

    return jsonify(result)

@app.route("/get_chart_detail_info/<selected_class>/<selected_dtype>/<selected_key>/<chart_type>/")
def get_chart_detail_info(selected_class, selected_dtype, selected_key, chart_type):
    error_value = overall['result_summary'][selected_class]['dt_result'][selected_dtype]
    #others = ['total_num', 'iou', 'bbox_size', 'detection_score']
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
        error_value = error_value[selected_key]
        print("chart type == type_class")
        res = []
        if selected_dtype != '2':
            print('error')
        else:
            print(list(error_value.keys()))
            for key in list(error_value['img_idx'].keys()):
                res.extend(error_value['img_idx'][key])



    img_val_list = []
    img_idx_list = list(set(res))[:300]
    print(img_idx_list[:30])
    for i in range(len(img_idx_list)):
        img_id = img_idx_list[i]
        detected_label_vals = image_bbox_values(img_id, selected_class, selected_dtype)
        img_val_list.append(detected_label_vals)

    return jsonify(img_val_list)


@app.route("/get_file_bbox_vals/<image_id>")
def get_file_bbox_vals(image_id):
    print("get_file_bbox_vals({})".format(image_id))
    detected_label_vals = image_bbox_values(image_id, None, None)

    return jsonify(detected_label_vals)




if __name__ == "__main__":
    app.run(debug=True)