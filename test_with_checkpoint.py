import os, pathlib, json, io, six, collections

import matplotlib
import matplotlib.pyplot as plt

import scipy.misc
import numpy as np
from six import BytesIO
from PIL import Image
from six.moves.urllib.request import urlopen

import tensorflow as tf

tf.get_logger().setLevel('ERROR')

import time
from object_detection.utils import label_map_util
from object_detection.utils import config_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder

MODEL_DIR = "/scratch/ohda/web/error_report/workspace/training_demo/exported-models/frcnn_resnet50_v1/"
LABEL_DIR = "/scratch/ohda/web/error_report/workspace/training_demo/annotations/label_map.pbtxt"
PATH_TO_CFG = MODEL_DIR + "/pipeline.config"
PATH_TO_CKPT = MODEL_DIR + "/checkpoint"

#Load pipeline config and build a detection model
configs = config_util.get_configs_from_pipeline_file(PATH_TO_CFG)
model_config = configs['model']
detection_model = model_builder.build(model_config=model_config, is_training=False)

#restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join(PATH_TO_CKPT, 'ckpt-0')).expect_partial()

@tf.function
def object_detection_model(image):
    """Detect objects in image."""

    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)

    return detections

category_index = label_map_util.create_category_index_from_labelmap(LABEL_DIR, use_display_name=True)
print(category_index)

def load_image_into_numpy_array(path):
    image = None
    if(path.startswith('http')):
        response = urlopen(path)
        image_data = response.read()
        image_data = BytesIO(image_data)
        image = Image.open(image_data)
    else:
        image_data = tf.io.gfile.GFile(path, 'rb').read()
        image = Image.open(BytesIO(image_data))

    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape((1, im_height, im_width, 3)).astype(np.uint8), (im_width, im_height)

def get_box_to_display_array(image, boxes, classes, scores, category_index, max_boxes_to_draw=20, min_score_thresh=.5):
    box_label_pred_map = dict()
    if not max_boxes_to_draw:
        max_boxes_to_draw = boxes.shape[0]
    for i in range(boxes.shape[0]):
        if max_boxes_to_draw == len(box_label_pred_map):
            break
        if scores is None or scores[i] > min_score_thresh:
            box = tuple(boxes[i].tolist())
            display_str = ''
            if classes[i] in six.viewkeys(category_index):
                category_name = category_index[classes[i]]['name']
            else:
                category_name = 'N/A'
            #pred_score = ("{0:.4f}".format(scores[i]))
            display_str = '{}: {}'.format(category_name, scores[i])
            box_label_pred_map[box] = display_str

    return box_label_pred_map

def get_prediction_box_label(box_label_pred_map, img_index, img_size):
    pred_result = dict()
    img_width, img_height = img_size
    img_label_val = labels_val[img_index]
    pred_result['index'] = img_index
    pred_result['name'] = img_label_val['name']
    pred_result['labels'] = []
    label_index_num = 0
    for box, pred_val in box_label_pred_map.items():
        ymin, xmin, ymax, xmax = box
        label, score = pred_val.split(":")
        each_label = dict()
        each_label['category'] = label
        each_label['score'] = score
        box_loc = dict()
        box_loc['x1'] = xmin * img_width
        box_loc['y1'] = ymin * img_height
        box_loc['x2'] = xmax * img_width
        box_loc['y2'] = ymax * img_height
        each_label['box2d'] = box_loc
        each_label['id'] = label_index_num

        pred_result['labels'].append(each_label)
        label_index_num += 1

    return pred_result

val_img_folder = "/scratch/ohda/web/error_report/workspace/training_demo/images/val/"
val_img_dir = pathlib.Path(val_img_folder)
print(val_img_dir.exists())

val_labels_dir = "bdd100k/labels/det_val.json"
with open(val_labels_dir) as f:
    labels_val = json.load(f)

val_img_list = list(val_img_dir.glob("*.jpg"))
print(len(val_img_list))

prediction_result = []
for img_index in range(len(val_img_list)):
#for img_index in range(50):
    img_path = str(val_img_list[img_index])
    img_array, img_size = load_image_into_numpy_array(img_path)
    img_tensor = tf.convert_to_tensor(img_array, dtype = tf.float32)
    detection_results = object_detection_model(img_tensor)
    result = {key:value.numpy() for key,value in detection_results.items()}

    label_id_offset = 1
    image_np_with_detections = img_array.copy()

    box_label_pred_map = get_box_to_display_array(
        image_np_with_detections[0],
        result['detection_boxes'][0],
        (result['detection_classes'][0] + label_id_offset).astype(int),
        result['detection_scores'][0],
        category_index,
        max_boxes_to_draw=200,
        min_score_thresh=.20)

    pred_result = get_prediction_box_label(box_label_pred_map, img_index, img_size)
    prediction_result.append(pred_result)


    if img_index % 500 == 0:
                    print("current image index: ", img_index)
                    box_to_color_map= viz_utils.visualize_boxes_and_labels_on_image_array(
                        image_np_with_detections[0],
                        result['detection_boxes'][0],
                        (result['detection_classes'][0] + label_id_offset).astype(int),
                        result['detection_scores'][0],
                        category_index,
                        use_normalized_coordinates=True,
                        max_boxes_to_draw=200,
                        min_score_thresh=.20,
                        agnostic_mode=False,
                        keypoints=None,
                        keypoint_scores=None,
                        keypoint_edges=None)
                    plt.figure(figsize=(24,32))
                    plt.imshow(image_np_with_detections[0])
                    plt.savefig("result_imgs/cam_checkpoint21_"+str(img_index)+".png")
                    plt.close()

with open("data/prediction_result_checkpoint21.json", "w") as outfile:
  json.dump(prediction_result, outfile, indent = 4)