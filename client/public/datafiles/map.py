import numpy as np
import json

with open("prediction_result.json") as f:
  pred_result = json.load(f)

with open("det_val_gt_cate.json") as f:
  ground_truth = json.load(f)
  
 for idx in range(len(pred_result)):
    cur = pred_result[idx]
    detected_classes = set()
    labels = cur['labels']
    for j in range(len(labels)):
      if labels[j]['nms'] == True:
        detected_classes.add(labels[j]['category'])
    cur['dt_cls'] = list(detected_classes)
 
for idx in range(len(pred_result)):
  cur_img_info = pred_result[idx]
  ground_truth_info = ground_truth[idx]
  iou_index_list = set()
  for jdx in range(len(cur_img_info['labels'])):
    cur_pred_res = cur_img_info['labels'][jdx]
    if cur_pred_res['nms'] == True:
      if 'max_iou_value' in cur_pred_res.keys():
        iou_index_list.add(cur_pred_res['max_iou_index_from_truth'])
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
    
def get_true_false_positives(cate_name, pred_val, iou_thres = 0.5):
    true_positive = []
    true_pos_num = 0
    false_positive = []
    false_pos_num = 0
    detected_bbox_index = []
    scores = []
    for i in range(len(pred_val)):
        cur_pred = pred_val[i]
        if cur_pred['nms'] == True:
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
        ap_vals_cate[cate_name] = np.mean(ap_lists)
        cate_map.append(np.mean(ap_lists))
    return ap_vals_cate, np.mean(cate_map)

def get_pred_gt_cate_values(pred, gt):
    pred_cate_list = []
    for i in range(len(pred)):
        if pred[i]['nms'] == True:
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
 
for img_index in range(len(pred_result)):
    pred = pred_result[img_index]['labels']
    gt = ground_truth[img_index]['labels'] 

    pred_cate_list, gt_cate_val = get_pred_gt_cate_values(pred, gt)
    ap_vals_cate, mAP = get_map_val(pred, gt_cate_val)

    pred_result[img_index]['mAP'] = mAP
    
    pred_result[img_index]['average_precisions'] = ap_vals_cate
    if img_index % 500 == 0:
        print("mAP ::: ", mAP)
        print("ap ::: ", ap_vals_cate)
