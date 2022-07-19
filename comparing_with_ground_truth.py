#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import json
import matplotlib.pyplot

with open("data/prediction_result.json") as f:
    pred_result = json.load(f)

with open("bdd100k/labels/det_val.json") as f:
    ground_truth = json.load(f)

def calculate_iou(target_coordinates, comparing_coordinates):
    #print(target_coordinates)
    #print(comparing_coordinates)
    
    Ax1 = target_coordinates['x1']
    Ay1 = target_coordinates['y1']
    Ax2 = target_coordinates['x2']
    Ay2 = target_coordinates['y2']
    
    Bx1 = comparing_coordinates['x1']
    By1 = comparing_coordinates['y1']
    Bx2 = comparing_coordinates['x2']
    By2 = comparing_coordinates['y2']
    
    area_A = (Ax2 - Ax1 + 1) * (Ay2 - Ay1 + 1)
    area_B = (Bx2 - Bx1 + 1) * (By2 - By1 + 1)
    #print(area_A)
    #print(area_B)
    
    x_inter1 = max(Ax1, Bx1)
    y_inter1 = max(Ay1, By1)
    x_inter2 = min(Ax2, Bx2)
    y_inter2 = min(Ay2, By2)
    
    inter_width = (x_inter2 - x_inter1 + 1)
    inter_height = (y_inter2 - y_inter1 + 1)
    
    if inter_width <= 0 or inter_height <= 0:
        return -1
    
    area_inter = inter_width * inter_height
    area_union = (area_A + area_B) - area_inter
    
    #print(area_inter)
    #print(area_union)
    
    IOU = area_inter / area_union
    return IOU
 

def find_most_similar_box(target_box, truth_boxes):
    #print(target_box)
    #print(len(truth_boxes))
    max_iou = -1
    iou_lists = []
    max_iou_index = -1
    max_iou_label_index = -1
    for idx in range(len(truth_boxes)):
        compare_box = truth_boxes[idx]
        if 'box2d' in compare_box.keys():
            iou = calculate_iou(target_box['box2d'], compare_box['box2d'])
            '''if iou != -1:
                iou_val = dict()
                iou_val['id'] = compare_box['id']
                iou_val['iou'] = iou
                iou_val['category'] = compare_box['category']
                iou_lists.append(iou_val)'''
            if iou >= max_iou:
                max_iou = iou
                max_iou_index = idx
                max_iou_label_index = compare_box['id']
                max_iou_category = compare_box['category']
        else:
            continue
    
    return max_iou, max_iou_index, max_iou_label_index, iou_lists, max_iou_category
    
for idx in range(len(pred_result)):
    cur = pred_result[idx]
    detected_classes = set()
    labels = cur['labels']
    for j in range(len(labels)):
        detected_classes.add(labels[j]['category'])
    cur['dt_cls'] = list(detected_classes)

for idx in range(len(pred_result)):
    cur_img_info = pred_result[idx]
    ground_truth_info = ground_truth[idx]
    iou_index_list = set()
    for jdx in range(len(cur_img_info['labels'])):
        cur_pred_res = cur_img_info['labels'][jdx]
        max_iou, max_iou_index, max_iou_label_index, iou_lists, max_iou_category = find_most_similar_box(cur_pred_res, ground_truth_info['labels'])
        if max_iou != -1:
            cur_pred_res['max_iou_index_from_truth'] = max_iou_label_index
            cur_pred_res['max_iou_value'] = max_iou
            #cur_pred_res['iou_values'] = iou_lists
            cur_pred_res['max_iou_value_category'] = max_iou_category
            iou_index_list.add(max_iou_label_index)
        '''else:
            cur_pred_res['max_iou_index_from_truth'] = None
            cur_pred_res['max_iou_value'] = None
            cur_pred_res['iou_values'] = None
            cur_pred_res['max_iou_value_category'] = None'''
    cur_img_info['gt_iou_idx'] = list(iou_index_list)

for idx in range(len(pred_result)):
    cur_img_info = pred_result[idx]
    ground_truth_info = ground_truth[idx]
    iou_index_list = set(cur_img_info['gt_iou_idx'])
    missed_num = 0
    for jdx in range(len(ground_truth_info['labels'])):
        each_label = ground_truth_info['labels'][jdx]
        if each_label['id'] not in iou_index_list:
            each_label['detected_type'] = 7
            missed_num += 1
    ground_truth_info['missed_label'] = missed_num

# calculating mAP 

'''
 TP: correct detection of a ground-truth bounding box (threshold: 0.5)
 => when predicted cate == ground-truth cate "and" max_iou > 0.5
 FP: incorrect detection of non-existing object or a misplaced detection of an existing object
 => when 
 FN: undetected ground-truth bounding box
 FP: does not apply to object detection
 
 mAP = AP/len(category_list)
'''
def get_true_false_positives(cate_name, pred_val, iou_thres = 0.5):
    true_positive = []
    true_pos_num = 0
    false_positive = []
    false_pos_num = 0
    detected_bbox_index = []
    scores = []
    for i in range(len(pred_val)):
        cur_pred = pred_val[i]
        if cur_pred['category'] == cate_name:
            scores.append(cur_pred['score'])
            if 'max_iou_value' in cur_pred.keys():
                if (cur_pred['category'] == cur_pred['max_iou_value_category'] and cur_pred['max_iou_value'] >= iou_thres 
                    and cur_pred['max_iou_index_from_truth'] not in detected_bbox_index):
                    true_positive.append(1)
                    false_positive.append(0)
                    true_pos_num += 1
                    detected_bbox_index.append(cur_pred['max_iou_index_from_truth'])
                else:
                    true_positive.append(0)
                    false_positive.append(1)
                    false_pos_num += 1
            else:
                true_positive.append(0)
                false_positive.append(1)
                false_pos_num += 1
        else:
            continue
    return scores, true_positive, true_pos_num, false_positive, false_pos_num

def compute_average_precision(precision, recall):
    mpre = np.concatenate(([0.], precision, [0.]))
    mrec = np.concatenate(([0.], recall, [1.]))
    
    for i in range(mpre.size - 1, 0, -1):
        mpre[i - 1] = np.maximum(mpre[i - 1], mpre[i])
    
    i = np.where(mrec[1:] != mrec[:-1])[0]
    
    ap = np.sum((mrec[i + 1] - mrec[i]) * mpre[i + 1])
    return ap

def get_map_val(pred, gt_cate_val):
    iou_thresholds = np.arange(start=0.2, stop=0.7, step=0.05)
    #iou_thresholds = [0.5]
    ap_vals_cate = dict()
    cate_map = []
    gt_cate_list = list(gt_cate_val.keys())
    for cate_name in gt_cate_list:
        ap_lists = []
        for iou_val in iou_thresholds:
            scores, tp, tp_num, fp, fp_num= get_true_false_positives(cate_name, pred, iou_val)
            gt_cate_num = gt_cate_val[cate_name]

            tp = np.array(tp)
            fp = np.array(fp)
            scores = np.array(scores)

            indices = np.flip(np.argsort(scores))

            true_positives = tp[indices]
            false_positives = fp[indices]

            true_positives = np.cumsum(true_positives)
            false_positives = np.cumsum(false_positives)

            # np.maximum with eps to avoid dividing with zero
            precision = true_positives / np.maximum(true_positives + false_positives, np.finfo(np.float64).eps)
            recall = true_positives / gt_cate_num

            ap = compute_average_precision(precision, recall)
            ap_lists.append(ap)
        #print(ap_lists)
        #ap_vals_cate[cate_name] = dict()
        #ap_vals_cate[cate_name]['raw_ap'] = ap_lists
        #ap_vals_cate[cate_name]['mean_ap'] = np.mean(ap_lists)
        ap_vals_cate[cate_name] = np.mean(ap_lists)
        cate_map.append(np.mean(ap_lists))
    #print("mAP : ", np.mean(cate_map))    
    return ap_vals_cate, np.mean(cate_map)


def get_pred_gt_cate_values(pred, gt):
    pred_cate_list = []
    for i in range(len(pred)):
        pred_cate = pred[i]['category']
        if pred_cate not in pred_cate_list:
            pred_cate_list.append(pred_cate)
    
    gt_cate_val = {}
    for j in range(len(gt)):
        if 'box2d' in gt[j].keys():
            gt_cate = gt[j]['category']
            if gt_cate not in gt_cate_val.keys():
                gt_cate_val[gt_cate] = 1
            else:
                gt_cate_val[gt_cate] += 1
    
    return pred_cate_list, gt_cate_val

'''
foreground threshold: tf - 0.5, background threshold: tb - 0.1
1. correctly classified: iou >= tf and correct class without duplicate error
2. classificaion error: iou >= tf and incorrect class
3. localization error: tb <= iou <= tf and correct class
4. cls and loc error: tb <= iou <= tf and incorrect class
5. duplicate detection error: more than one iou >= tf with correct class
6. background error: iou <= tb with gt class
7. missed GT error: undetected ground truth (FN) 
8. incorrectly classified: error but doesn't belong to above type
'''

def detect_error_type(pred):
    tf = 0.5
    tb = 0.1
    detected_id = dict()
    for idx in range(len(pred)):
        cur_val = pred[idx]
        if 'max_iou_value' in cur_val.keys():
            max_iou_value = cur_val['max_iou_value']
            max_iou_id = cur_val['max_iou_index_from_truth'] 
            if cur_val['max_iou_value_category'] == cur_val['category']:
                # check for correct (1), localization (3), duplicate (5), and incorrect (8) error type
                if max_iou_value >= tf:
                    # check for duplicate error or correctly classified
                    if max_iou_id not in detected_id.keys():
                        cur_val["detected_type"] = 1 # 1: correct 
                        detected_id[max_iou_id] = dict()
                        detected_id[max_iou_id]['val'] = max_iou_value
                        detected_id[max_iou_id]['id'] = cur_val['id']
                    else:
                        if (detected_id[max_iou_id]['val'] >= max_iou_value and detected_id[max_iou_id]['id'] != cur_val['id']):
                            cur_val['detected_type'] = 5 # 5: duplicate 
                        else:
                            cur_val['detected_type'] = 1
                            detected_id[max_iou_id]['val'] = max_iou_value
                            detected_id[max_iou_id]['id'] = cur_val['id']
                elif (max_iou_value >= tb and max_iou_value <tf):
                    # localization error where tb <= iou < tf
                    cur_val['detected_type'] = 3 # 3: localization
                else:
                    # if max_iou_value < tb : incorrect
                    cur_val['detected_type'] = 8 # 8: incorrect
            else:
                # cur_val['max_iou_valu_category'] != cur_val['category']
                # check for classification (2) , cls and loc error (4)
                if max_iou_value >= tf:
                    cur_val['detected_type'] = 2 #2: classification
                elif (max_iou_value >= tb and max_iou_value <tf):
                    cur_val['detected_type'] = 4 #4: classification + localization error
                else:
                    cur_val['detected_type'] = 8 
        else:
            # check for background error (6), where iou <= tb with gt_class 
            # when they detect something from the background or something not listed in gt_class
            cur_val['detected_type'] = 6 #6: background error


for img_index in range(len(pred_result)):
    pred = pred_result[img_index]['labels']
    gt = ground_truth[img_index]['labels']
    
    detect_error_type(pred)

    pred_cate_list, gt_cate_val = get_pred_gt_cate_values(pred, gt)
    ap_vals_cate, mAP = get_map_val(pred, gt_cate_val)
    if img_index % 500 == 0:
        print(mAP)

    pred_result[img_index]['mAP'] = mAP
    pred_result[img_index]['average_precisions'] = ap_vals_cate


with open("data/prediction_result_checkpoint21.json", "w") as outfile:
    json.dump(pred_result, outfile, indent = 4)

