# Object Detection Error Analyzer

## Introduction <br/>


## File locations and explanations

**1. used BDD 100k image for object detection experience** <br/>

**2. object detection models and python files** <br/>
(1) 

**3. json datafiles**
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
