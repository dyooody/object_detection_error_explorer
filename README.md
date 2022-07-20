# Object Detection Error Explorer

## Introduction <br/>
![main page image](/images/main-page.png)<br/>
Object detection error explorer is an interactive tool that supports the evaluation and analysis of the results of the object detection model. We categorized detected and ground-truth labels into 7 and 11 types. With this tool, users can analyze object detection results based on this categorization at three different levels: summary level, class and detection type level, and image level. This enables users to analyze a large number of and a variety of model errors from a summarized overview into individual images. <br/>

From the summary level, users can explore the overall detection results such as average precision, the number of detected labels and ground truth labels, and the number of each detection type. At the class and detection level, users can see more detailed information about a certain class and detection type and images that correspond to it. At the image level, users can click each image to get a detailed analysis. <br/>

> for more information: [presentation document](/images/error-explorer.pdf)


## File locations and explanations

**1. used BDD 100k image for object detection experience** <br/>

**2. object detection models and python files** <br/>
(1) test_with_checkpoint.py <br/>
> Fine-tuned the faster-RCNN pre-trained model trained with ms cocodataset with BDD 100K training dataset. <br/>

(2) comparing_with_ground_truth.py <br/>
> From the detection result obtained with faster-RCNN model, calculated the IoU and mAP value of the detection results. Also, categorized the detection label based on the created categories. <br/>

**3. json datafiles**<br/>
     - currently not uploaded due to the file size
```
/client/public/datafiles/
```
> (1) det_val_gt_cat.json: ground truth jsonfile <br/>
> (2) nms_summary.json: contains information for the summary tables, and image indexes for class and detection types <br/>
> (3) prediction_result.json: prediction result jsonfile <br/>
> (4) detection_type_description.json: descriptions for each categories <br/>

**4. svelte files**
> (1) App.svelte: main page <br/>
> (2) ./Components/DefaultImageView.svelte: loads images for the default image view <br/>
> (3) ./Components/Distribution.svelte: loads different charts for the default chart view <br/>
> (4) ./Components/Switch : toggle switch for result summary tables <br/>
> (5) ./Components/tooltip.js and TooltipFromAction.svelte : tooltip interface <br/>
> (6) ./Components/Modal.svelte : modal window for each image <br/>

### requirement
1. for python
```
pip3 install flask
```
2. for svelte
```
cd client
npm install d3
npm install d3-scale
```
### to run

1. bash: (dir: Code)
```
export FLASK_APP=server.py && export FLASK_ENV=development
python3 -m flask run --port=8000 (py -3 -m flask run --port=8000)
```
2. bash (dir: Code)
```
cd client
npm install
npm run dev
```
