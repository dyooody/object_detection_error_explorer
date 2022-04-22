<script>
  import { createEventDispatcher } from 'svelte';

  export let isOpenModal;

  const dispatch = createEventDispatcher();
  function closeModal(){
    isOpenModal = false;
    dispatch('closeModal', {isOpenModal});
  }

  let class_lists = {
		"car":{checked: true, color: "#884EA0"},
		"bus":{checked: true, color: "#A93226 "},
		"bicycle":{checked: true, color: "#2E86C1"},
		"motorcycle":{checked: true, color:"#17A589"},
		"truck":{checked: true, color:"#2ECC71"},
		"traffic sign":{checked: true, color: "#F1C40F"},
		"traffic light":{checked: true, color:"#CA6F1E"},
		"pedestrian":{checked: true, color:"#F7F9F9"},
		"rider":{checked: true, color:"#FEF5E7"},
		"train":{checked: true, color:"#F4ECF7"},
		"other vehicle":{checked: true, color:"#28B463"},
		"other person":{checked: true, color:"#85C1E9"},
		"trailer" :{checked: true, color:"#F5B7B1"}
	};

	let detected_types = {
		"1":{name:"correctly classified", checked: false, color: "#884EA0"},
		"2":{name:"classification error", checked: false, color: "#A93226 "},
		"3":{name:"localization error", checked: false, color: "#2E86C1"},
		"4":{name:"cls + loc error", checked: false, color:"#2ECC71"},
		"5":{name:"duplicate error", checked: false, color: "#F1C40F"},
		"6":{name:"background error", checked: false, color:"#F7F9F9"},
		"7":{name:"missed GT error", checked: false, color:"#FEF5E7"},
		"8":{name:"incorrectly classified", checked: false, color:"#28B463"},
	};

  let cur_img_src;
  let cur_img_bbox_val;
  let show_class_bbox = true;
  let show_groundTruth = false;
  let cl_key = [];
  let dt_key = [];
  let gt_key = [];
  let actualWidth = 1280, actualHeight=720, givenWidth= 700, givenHeight=450;
  let boxHeight, box_area, boxWidth, X, Y;
  export function get_instance_val(img_src, img_bbox_val){
    show_class_bbox = true;
    show_groundTruth = false;
    cur_img_src = img_src;
    cur_img_src = cur_img_src;
    cur_img_bbox_val = img_bbox_val;
    cl_key = Object.keys(cur_img_bbox_val['cl_bbox']);
    dt_key = Object.keys(cur_img_bbox_val['dt_bbox']);
    gt_key = Object.keys(cur_img_bbox_val['gt_bbox']);
    console.log("img_bbox_val['gt_bbox'] ::: ", cur_img_bbox_val['gt_bbox']);
    console.log("img_bbox_val['cl_bbox'] ::: ", cur_img_bbox_val['cl_bbox']);
  }



  function class_button_clicked(class_val){
    class_lists[class_val]['checked'] = !class_lists[class_val]['checked'];
  }

  function dtype_button_clicked(dtype_val){
    detected_types[dtype_val]['checked'] = !detected_types[dtype_val]['checked'];
  }

  function class_or_dtype(){
    show_class_bbox = !show_class_bbox;
  }

  function gt_or_detection(){
    show_groundTruth = !show_groundTruth;
    console.log("current status ::: ", show_groundTruth);
  }
</script>

<div id ="background" style="--display: {isOpenModal ? 'block' : 'none'}" on:click={closeModal}></div>
<div id="modal" style="--display : {isOpenModal ? 'block' : 'none'}">
  <div id ="image-view" class="view-panel">
    <div class = "view-title">Image Detail View</div>

    <button class= 'button-view' on:click={class_or_dtype}>class or dtype</button>
    <button class="button-view" on:click ={gt_or_detection}>show groundtruth</button>
      {#if show_class_bbox}
        {#each cl_key as cl}
          <button class= 'button-view' on:click={class_button_clicked(cl)}>{cl}</button>
        {/each}
        <div class = "show_image" width={givenWidth} height = {givenHeight}>
          <img class = "images" id = "selected_image" alt = "" src = {cur_img_src} width={givenWidth} height={givenHeight}>
            <svg class = "bboxes" id = "images_box" width={givenWidth} height={givenHeight}>
              {#each cl_key as cl}
                {#if class_lists[cl]['checked'] == true}
                  {#each cur_img_bbox_val['cl_bbox'][cl] as cl_bbox}
                    {boxWidth = (Math.abs(cl_bbox['x2'] - cl_bbox['x1'])/actualWidth)*givenWidth}
                    {boxHeight = (Math.abs(cl_bbox['y2'] - cl_bbox['y1'])/actualHeight)*givenHeight}
                    {box_area = boxWidth * boxHeight}
                    {X = (cl_bbox['x1']/actualWidth)*givenWidth}
                    {Y = (cl_bbox['y1']/actualHeight)*givenHeight}
                    <rect x= {X} y = {Y} width = {boxWidth} height = {boxHeight} stroke = {class_lists[cl]['color']}/>
                  {/each}
                {/if}
              {/each}
            </svg>

            {#if show_groundTruth == true}
              <svg class = "gt_bboxes" id = "images_box" width={givenWidth} height={givenHeight}>
                {#each gt_key as gt}
                  {#each cur_img_bbox_val['gt_bbox'][gt] as gt_bbox}
                    {boxWidth = (Math.abs(gt_bbox['x2'] - gt_bbox['x1'])/actualWidth)*givenWidth}
                    {boxHeight = (Math.abs(gt_bbox['y2'] - gt_bbox['y1'])/actualHeight)*givenHeight}
                    {box_area = boxWidth * boxHeight}
                    {X = (gt_bbox['x1']/actualWidth)*givenWidth}
                    {Y = (gt_bbox['y1']/actualHeight)*givenHeight}
                    <rect x= {X} y = {Y} width = {boxWidth} height = {boxHeight} stroke = {class_lists[gt]['color']}/>
                  {/each}
                {/each}
              </svg>
            {/if}
        </div>

      {/if}


      {#if show_class_bbox == false}
          {#each dt_key as dt}
            <button on:click={dtype_button_clicked(dt)}>{dt}</button>
          {/each}
          <div class = "show_image" width = {givenWidth} height = {givenHeight}>
            <img class = "images" id = "selected_image" alt = "" src={cur_img_src} width={givenWidth} height={givenHeight}>
            <svg class = "bboxes" id = "images_box" width={givenWidth} height ={givenHeight}>
              {#each dt_key as dt}
                {#if detected_types[dt]['checked'] == true}
                  {#each cur_img_bbox_val['dt_bbox'][dt] as dt_bbox}
                    {boxWidth = (Math.abs(dt_bbox['x2'] - dt_bbox['x1'])/actualWidth)*givenWidth}
                    {boxHeight = (Math.abs(dt_bbox['y2'] - dt_bbox['y1'])/actualHeight)*givenHeight}
                    {box_area = boxWidth * boxHeight}
                    {X = (dt_bbox['x1']/actualWidth)*givenWidth}
                    {Y = (dt_bbox['y1']/actualHeight)*givenHeight}
                    <rect x= {X} y = {Y} width = {boxWidth} height = {boxHeight} stroke = {detected_types[dt]['color']}/>
                  {/each}
                {/if}
              {/each}
            </svg>


            {#if show_groundTruth == true}
              <svg class = "gt_bboxes" id = "images_box" width={givenWidth} height={givenHeight}>
                {#each gt_key as gt}
                  {#each cur_img_bbox_val['gt_bbox'][gt] as gt_bbox}
                    {boxWidth = (Math.abs(gt_bbox['x2'] - gt_bbox['x1'])/actualWidth)*givenWidth}
                    {boxHeight = (Math.abs(gt_bbox['y2'] - gt_bbox['y1'])/actualHeight)*givenHeight}
                    {box_area = boxWidth * boxHeight}
                    {X = (gt_bbox['x1']/actualWidth)*givenWidth}
                    {Y = (gt_bbox['y1']/actualHeight)*givenHeight}
                    <rect x= {X} y = {Y} width = {boxWidth} height = {boxHeight} stroke = {class_lists[gt]['color']}/>
                  {/each}
                {/each}
              </svg>
            {/if}
          </div>
      {/if}
  </div>
</div>



<style>
  #background{
    display: var(--display);
    position: fixed;
    z-index: 1;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(245, 243, 243, 0.01);
  }

  #modal{
    display: var(--display);
    position:fixed;
    z-index: 2;
    top: 5%;
    left: 25%;
    width: 800px;
    height: 600px;
    padding: 15px;
    /*transform: translate(-50%, -50%);*/
    background: #fff;
    border: 2px solid;
  }
  .view-panel{
    border: 2px solid #eee;
    margin-bottom: 15px;
    margin-right:15px;
  }
  .view-title{
    background-color: #f3f3f3;
    font-size: 1.0rem;
    margin-bottom: 8px;
    padding: 3px 8px 5px 12px;
  }
  #image-view{
    height: 550px;
    padding: 5px;
  }

  .show_image{
    display: flex;
  }
  .show_image .images{
    position: absolute;
  }
  .show_image .bboxes{
    position: absolute;
    stroke-width: 2px;
    fill: none;
  }

  .show_image .gt_bboxes{
    position: absolute;
    stroke-width: 1.5px;
    fill: none;
    stroke-dasharray: 5,5;
  }
</style>