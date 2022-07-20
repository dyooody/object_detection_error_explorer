<script>
  import { onMount } from "svelte";

  export let show_detection = true;

  function show_groundTruth(){
    show_detection = !show_detection;
  }

	let class_lists = {
		"car":{checked: false, color: "#EC7063"},
		"bus":{checked: false, color: "#AF7AC5"},
		"bicycle":{checked: false, color: "#2E86C1"},
		"motorcycle":{checked: false, color:"#76D7C4"},
		"truck":{checked: false, color:"#F8C471"},
		"traffic sign":{checked: false, color: "#F1C40F"},
		"traffic light":{checked: false, color:"#CA6F1E"},
		"pedestrian":{checked: false, color:"#1F618D"},
		"rider":{checked: false, color:"#85C1E9"},
		"train":{checked: false, color:"#F4ECF7"},
		"other vehicle":{checked: false, color:"#28B463"},
		"other person":{checked: false, color:"#85C1E9"},
		"trailer" :{checked: false, color:"#F5B7B1"}
	};

	let image_source_val = [];
  let image_idx_src = [];
	let imageWidth = 1280, imageHeight=720, setWidth= 300, setHeight=168;
	let x1,x2,y1,y2,boxHeight, boxWidth, X, Y;
  let view_default_img = true;

  let image_val_lists = [];
  onMount(async ()=>{
    image_idx_src = [];
    image_source_val = [];
    view_default_img = true;
    fetch('/default_image_show/').then(res=>res.json()).then(result=>{

      image_val_lists = result;
      for (var i =0; i< image_val_lists.length; i++){
        let image_path = "";
        let class_bbox = [];
        let dtype_bbox = [];
        let gt_bbox = [];
        let data = image_val_lists[i];
        image_path = data['image_dir'];
        image_idx_src.push(data['image_dir']);
        image_idx_src = image_idx_src;
        for (var j=0; j<Object.keys(data['total_dt']).length; j++){
          var cl_name = Object.keys(data['total_dt'])[j];
          class_bbox[cl_name] = data['total_dt'][cl_name];
        }
        for (var l=0; l<Object.keys(data['total_gt']).length; l++){
          var gt_name = Object.keys(data['total_gt'])[l];
          gt_bbox[gt_name] = data['total_gt'][gt_name];
        }
        class_bbox = class_bbox;
        dtype_bbox = dtype_bbox;
        gt_bbox = gt_bbox;
        image_source_val[image_path] = [];
        image_source_val[image_path]['cl_bbox'] = class_bbox;
        image_source_val[image_path]['gt_bbox'] = gt_bbox;
      }
    });
  });
</script>

<div id ="images_view">
  {#if view_default_img == true}
  {#each image_idx_src as img_src}
    <div class = "multiple_images">
      <!-- svelte-ignore a11y-missing-attribute -->
      <img class = "images" id="selected_image" src = {img_src} width = {setWidth} height={setHeight}>
      <svg class = "bboxes" id="image_box" width={setWidth} height={setHeight}>
        {#each Object.keys(image_source_val[img_src]['cl_bbox']) as cl_name}
          {#each Object.keys(image_source_val[img_src]['cl_bbox'][cl_name]) as cl_key}
            {x1 = image_source_val[img_src]['cl_bbox'][cl_name][cl_key]['x1']}
            {x2 = image_source_val[img_src]['cl_bbox'][cl_name][cl_key]['x2']}
						{y1 = image_source_val[img_src]['cl_bbox'][cl_name][cl_key]['y1']}
						{y2 = image_source_val[img_src]['cl_bbox'][cl_name][cl_key]['y2']}
            {boxWidth = (Math.abs(x2-x1)/imageWidth)*setWidth}
						{boxHeight = (Math.abs(y2-y1)/imageHeight)*setHeight}
						{X = (x1/imageWidth)*setWidth}
						{Y = (y1/imageHeight)*setHeight}
            <rect x={X} y={Y} width={boxWidth} height={boxHeight} stroke={class_lists[cl_name]['color']}/>
          {/each}
        {/each}
      </svg>

      <svg class = "gt_bboxes" id="image_box" width={setWidth} height={setHeight}>
        {#each Object.keys(image_source_val[img_src]['gt_bbox']) as gt_name}
          {#each Object.keys(image_source_val[img_src]['gt_bbox'][gt_name]) as gt_key}
            {x1 = image_source_val[img_src]['gt_bbox'][gt_name][gt_key]['x1']}
            {x2 = image_source_val[img_src]['gt_bbox'][gt_name][gt_key]['x2']}
            {y1 = image_source_val[img_src]['gt_bbox'][gt_name][gt_key]['y1']}
            {y2 = image_source_val[img_src]['gt_bbox'][gt_name][gt_key]['y2']}
            {boxWidth = (Math.abs(x2-x1)/imageWidth)*setWidth}
            {boxHeight = (Math.abs(y2-y1)/imageHeight)*setHeight}
            {X = (x1/imageWidth)*setWidth}
            {Y = (y1/imageHeight)*setHeight}
            <rect x={X} y={Y} width={boxWidth} height={boxHeight} stroke={class_lists[gt_name]['color']}/>
          {/each}
        {/each}
      </svg>
    </div>
  {/each}
  {/if}
</div>

<style>

  .multiple_images{
    position: relative;
    display: inline-block;
  }
  .multiple_images .images{
    display: block;
    margin-right: 2px;
  }
  .multiple_images .bboxes{
    position: absolute;
    top: 0;
    stroke-width: 1.5px;
    fill: none;
  }
  .multiple_images .gt_bboxes{
    position: absolute;
    top: 0;
    stroke-width: 1.5px;
    fill: none;
    stroke-dasharray: 5,5;
  }

</style>