<script>
  import { createEventDispatcher } from 'svelte';

  export let isOpenModal;

  const dispatch = createEventDispatcher();
  function closeModal(){
    isOpenModal = false;
    gt_bbox_val = "0";
    dt_bbox_val = "0";
    gt_cate_val = "0";
    cl_key = [];
    gt_key = [];
    dtype_key = [];
    whole_key = [];
    cur_img_vals = "0";
    gt_dict = {};
    dispatch('closeModal', {isOpenModal});
  }

  let class_lists = {
		"car":{dt: false, gt: false, color: "#EC7063"},
		"bus":{dt: false, gt: false, color: "#AF7AC5"},
		"bicycle":{dt: false, gt: false, color: "#2E86C1"},
		"motorcycle":{dt: false, gt: false, color:"#76D7C4"},
		"truck":{dt: false, gt: false, color:"#F8C471"},
		"traffic sign":{dt: false, gt: false, color: "#F1C40F"},
		"traffic light":{dt: false, gt: false, color:"#CA6F1E"},
		"pedestrian":{dt: false, gt: false, color:"#1F618D"},
		"rider":{dt: false, gt: false, color:"#85C1E9"},
		"train":{dt: false, gt: false, color:"#F4ECF7"},
		"other vehicle":{dt: false, gt: false, color:"#28B463"},
		"other person":{dt: false, gt: false, color:"#85C1E9"},
		"trailer" :{dt: false, gt: false, color:"#F5B7B1"}
	};

	let detected_types = {
		"1":{name:"correctly classified", checked: false, color: "#F7F9F9"},
		"2":{name:"classification error", checked: false, color: "#A93226 "},
		"3":{name:"localization error", checked: false, color: "#2E86C1"},
		"4":{name:"cls + loc error", checked: false, color:"#2ECC71"},
		"5":{name:"duplicate error", checked: false, color: "#F1C40F"},
		"6":{name:"background error", checked: false, color:"#884EA0"},
		"7":{name:"missed GT error", checked: false, color:"#FEF5E7"},
		"8":{name:"incorrectly classified", checked: false, color:"#28B463"},
	};

  let cur_img_src;
  let cur_img_vals;
  let dt_bbox_val;
  let gt_bbox_val;
  let gt_cate_val;
  let cl_key = [];
  let gt_key = [];
  let whole_key = [];
  let dtype_key = [];
  let gt_dict = {};
  let actualWidth = 1280, actualHeight=720, givenWidth= 900, givenHeight=580;
  let boxHeight, boxWidth, box_area, X, Y, cur_gt_cate;

  function reset_selection(){
    let class_list_key = Object.keys(class_lists);
    for (var i=0; i < class_list_key.length; i++){
      class_lists[class_list_key[i]]['dt'] = false;
      class_lists[class_list_key[i]]['gt'] = false;
    }

    let dt_types_key = Object.keys(detected_types);
    for (var j=0; j < dt_types_key.length; j++){
      detected_types[dt_types_key[j]]['checked'] = false;
    }

  }

  export function get_instance_val(img_src, img_bbox_val, selected_class, selected_dtype){
    reset_selection();

    cur_img_src = img_src;
    cur_img_vals = img_bbox_val;
    dt_bbox_val = cur_img_vals['bbox_values']['box'];
    gt_bbox_val = cur_img_vals['bbox_values']['gt_bbox'];
    gt_cate_val = cur_img_vals['bbox_values']['gt_cate'];

    class_lists[selected_class]['dt'] = true;
    detected_types[selected_dtype]['checked'] = true;
    if (selected_dtype == 2 || selected_dtype == 4){
      let cor_class = gt_cate_val[selected_class][selected_dtype];
      for (var i =0; i < cor_class.length; i++){
        class_lists[cor_class[i]]['gt'] = true;
      }
    }else{
      class_lists[selected_class]['gt'] = true;
    }

    cl_key = Object.keys(cur_img_vals['bbox_values']['box']);

    whole_key = Object.keys(cur_img_vals['bbox_values']['box']);

    for (var i=0; i < cl_key.length; i++){
      let cur = Object.keys(dt_bbox_val[cl_key[i]]);
      for (var j=0; j<cur.length; j++){
        if (dtype_key.includes(cur[j]) == false){
          dtype_key.push(cur[j])
        }
      }
    }

    let k1 = Object.keys(gt_cate_val);
    for (var i =0; i < k1.length; i++){
      let k2 = Object.keys(gt_cate_val[k1[i]]);
      for (var j=0; j < k2.length; j++){
        let k3 = gt_cate_val[k1[i]][k2[j]];
        let k4 = gt_bbox_val[k1[i]][k2[j]];
        for(var l=0; l < k3.length; l++){
          if (whole_key.includes(k3[l]) == false){
            whole_key.push(k3[l]);
          }
          let kk = Object.keys(gt_dict);
          if (kk.includes(k3[l]) == false){
            gt_dict[k3[l]] = {};
          }
          if (Object.keys(gt_dict[k3[l]]).includes(k2[j]) == false){
            gt_dict[k3[l]][k2[j]] = [];
          }
          gt_dict[k3[l]][k2[j]].push(k4[l])
        }
      }
    }
    gt_key = Object.keys(gt_dict);
    gt_key = gt_key;
    whole_key = whole_key;
    cl_key = cl_key;
  }


</script>

<div id ="background" style="--display: {isOpenModal ? 'block' : 'none'}" on:click={closeModal}></div>
<div id = "modal" style = "--display : {isOpenModal ? 'block' : 'none'}">
  <div class="view-title">Image Detail View</div>
  <div id ="main-section">

    <div id = "image-view" class = "view-panel">

      <div id ="bbox-button-panel">
        <table class ="button-panel-table">
          <thead>
            <tr>
              <th></th>
              <th>GT</th>
              <th>DT</th>
            </tr>
          </thead>
          <tbody>
            {#each whole_key as cl}
              <tr>
                <td>{cl}</td>
                {#if gt_key.includes(cl) == true}
                <td><input type="checkbox" bind:checked={class_lists[cl]['gt']} id="checkbox-cl"></td>
                {/if}
                {#if gt_key.includes(cl) == false}
                <td></td>
                {/if}
                {#if cl_key.includes(cl) == true}
                <td><input type="checkbox" bind:checked={class_lists[cl]['dt']} id="checkbox-cl"></td>
                {/if}
                {#if cl_key.includes(cl) == false}
                <td></td>
                {/if}
              </tr>
            {/each}
          </tbody>
        </table>
        <table>
          <thead>
            <tr>
              <th>detection type</th>
            </tr>
          </thead>
          <tbody>
            {#each dtype_key as dt}
              <tr>
              <td><input type="checkbox" bind:checked={detected_types[dt]['checked']} name={dt} id="checkbox-dt"></td>
              <td>{detected_types[dt]['name']}</td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>

      <div id = "image-panel" class="show_image" width={givenWidth} height={givenHeight}>
        <img class="images" id = "selected_image" alt="" src={cur_img_src} width={givenWidth} height={givenHeight}>


        <svg class ="gt_bboxes" id="images_box" width={givenWidth} height={givenHeight}>
          {#each gt_key as cl}
            {#if class_lists[cl]['gt'] == true}
              {#each Object.keys(gt_dict[cl]) as dtype}
                {#if detected_types[dtype]['checked'] == true}
                  {#each gt_dict[cl][dtype] as cl_bbox}
                  {boxWidth = (Math.abs(cl_bbox['x2'] - cl_bbox['x1'])/actualWidth)*givenWidth}
                  {boxHeight = (Math.abs(cl_bbox['y2'] - cl_bbox['y1'])/actualHeight)*givenHeight}
                  {box_area = boxWidth * boxHeight}
                  {X = (cl_bbox['x1']/actualWidth)*givenWidth}
                  {Y = (cl_bbox['y1']/actualHeight)*givenHeight}

                  <rect x= {X} y = {Y} width = {boxWidth} height = {boxHeight} fill="transparent" stroke = {class_lists[cl]['color']}/>
                  <g>
                    {#if (boxWidth / 3 > 30)}
                      <text x = {X + boxWidth - 15} y={Y- 2} font-size={15} fill={class_lists[cl]['color']}>{cl}</text>
                    {/if}
                    {#if ((boxWidth / 3) <= 30 && (boxWidth /3 ) > 15)}
                      <text x = {X + boxWidth - 10} y={Y- 2} font-size={10} fill={class_lists[cl]['color']}>{cl}</text>
                    {/if}
                    {#if (boxWidth / 3 <= 15)}
                      <text x = {X + 0.67 * boxWidth} y={Y- 2} font-size={boxWidth / 3} fill={class_lists[cl]['color']}>{cl}</text>
                    {/if}
                  </g>
                  {/each}
                {/if}
              {/each}
            {/if}
          {/each}
        </svg>

        <svg class = "bboxes" id="images_box" width={givenWidth} height={givenHeight}>
          {#each cl_key as cl}
            {#if class_lists[cl]['dt'] == true}
              {#if dt_bbox_val[cl] != null}
              {#each Object.keys(dt_bbox_val[cl]) as dtype}
                {#if detected_types[dtype]['checked'] == true}
                  {#each dt_bbox_val[cl][dtype] as cl_bbox, i}
                  {boxWidth = (Math.abs(cl_bbox['x2'] - cl_bbox['x1'])/actualWidth)*givenWidth}
                  {boxHeight = (Math.abs(cl_bbox['y2'] - cl_bbox['y1'])/actualHeight)*givenHeight}
                  {box_area = boxWidth * boxHeight}
                  {X = (cl_bbox['x1']/actualWidth)*givenWidth}
                  {Y = (cl_bbox['y1']/actualHeight)*givenHeight}
                  <rect x= {X} y = {Y} width = {boxWidth} height = {boxHeight} fill="transparent" stroke = {class_lists[cl]['color']}/>
                  <g>
                    {#if (boxWidth / 3 > 30)}
											<text x = {X} y={Y- 2} font-size={15} fill={class_lists[cl]['color']}>{cl}</text>
										{/if}
										{#if ((boxWidth / 3 <= 30) && (boxWidth /3 ) > 15)}
										  <text x = {X} y={Y- 2} font-size={10} fill={class_lists[cl]['color']}>{cl}</text>
										{/if}
										{#if (boxWidth / 3 <= 15)}
											<text x = {X} y={Y- 2} font-size={boxWidth / 3} fill={class_lists[cl]['color']}>{cl}</text>
										{/if}
                  </g>
                  {/each}
                {/if}
              {/each}
              {/if}
            {/if}
          {/each}
        </svg>
      </div>

    </div>
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
    top: 3%;
    left: 10%;
    width: 1200px;
    height: 650px;
    padding: 15px;
    /*transform: translate(-50%, -50%);*/
    background: #fff;
    border: 2px solid;
  }
  #bbox-button-panel, #image-panel{
    display: flex;
    flex-direction: column;
  }
  #image-view{
    display: flex;
    height: 600px;
    padding: 5px;
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
  table, td, th{
    font-size: 0.85rem;
    margin-bottom: 5px;
  }

  #checkbox-cl, #checkbox-dt{
    transform: scale(1.5);
    background-color: #eee;
  }

  .show_image{
    text-align: center;
    padding: 10px;
  }
  .show_image .images{
    position: absolute;
    text-align: center;
    padding-left: 20px;
  }
  .show_image .bboxes{
    position: absolute;
    stroke-width: 2px;
    text-align: center;
    padding-left: 20px;
  }

  .show_image .gt_bboxes{
    position: absolute;
    stroke-width: 2px;
    stroke-dasharray: 7,3;
    text-align: center;
    padding-left: 20px;
  }

</style>