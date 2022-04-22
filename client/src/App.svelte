<script>
	import DefaultImageView from './Components/DefaultImageView.svelte';
	import Distribution from './Components/Distribution.svelte';
	import { onMount } from 'svelte';
	import { scaleLinear } from "d3-scale";
	import Switch from "svelte-switch";
	import Modal from './Components/Modal.svelte';

	let switch_check = false;

	function handleChange(e){
		const {checked} = e.detail;
		switch_check = checked;
	}
	let show_default_chart = true;
	let show_default_images = true;
	let show_chart_images = false;

	let class_list = [];
  let ap = [];
  let nums = [];
  let gt_nums = [];
  let table_heads = [];
  let table_vals = [];
  let result_array = [];

  onMount(async ()=>{
    let dt_type_vals = {
		"bicycle": [],
		"bus": [],
		"car": [],
		"motorcycle": [],
		"other person": [],
		"other vehicle": [],
		"pedestrian": [],
		"rider": [],
		"traffic light": [],
		"traffic sign": [],
		"trailer": [],
		"train": [],
		"truck": []
	  };
    fetch('/class_values/').then(res =>res.json()).then(overall=>{
      result_array = overall;
      class_list = Object.keys(result_array);
      class_list = class_list;
      table_heads = ['class name', 'average precision', 'number', 'gt_number',
			'type 1', 'type 2', 'type 3', 'type 4', 'type 5', 'type 6', 'type 7', 'type 8'];
      table_heads = table_heads;

      for (var i=0; i < Object.keys(result_array).length; i++){
        nums.push(result_array[class_list[i]]['num']);
				nums = nums;
				ap.push(result_array[class_list[i]]['ap']);
				ap = ap;
				gt_nums.push(result_array[class_list[i]]['gt_num']);
				gt_nums = gt_nums;
        let dt_results = result_array[class_list[i]]['dt_result'];
				let dt_keys = Object.keys(dt_results);
				for (var j = 0; j < Object.keys(dt_results).length; j++){
					dt_type_vals[class_list[i]].push(dt_results[dt_keys[j]]['total_num'])
					dt_type_vals[class_list[i]] = dt_type_vals[class_list[i]];
				}
      }

      table_vals = [];
      for(var i = 0; i < class_list.length; i++){
        var row = [];
        row.push(class_list[i]);
				row.push(ap[i]);
				row.push(nums[i]);
				row.push(gt_nums[i]);
				for (var j=0; j<dt_type_vals[class_list[i]].length; j++){
					row.push(dt_type_vals[class_list[i]][j]);
				}
				table_vals.push(row);
      }
      table_vals = table_vals;
    });
  });

	// images
	let class_lists = {
		"car":{checked: false, color: "#884EA0"},
		"bus":{checked: false, color: "#A93226 "},
		"bicycle":{checked: false, color: "#2E86C1"},
		"motorcycle":{checked: false, color:"#17A589"},
		"truck":{checked: false, color:"#2ECC71"},
		"traffic sign":{checked: false, color: "#F1C40F"},
		"traffic light":{checked: false, color:"#CA6F1E"},
		"pedestrian":{checked: false, color:"#F7F9F9"},
		"rider":{checked: false, color:"#FEF5E7"},
		"train":{checked: false, color:"#F4ECF7"},
		"other vehicle":{checked: false, color:"#28B463"},
		"other person":{checked: false, color:"#85C1E9"},
		"trailer" :{checked: false, color:"#F5B7B1"}
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

	let current_selected_class;
	let current_selected_dtype;
	let selected_dtype;

	let image_source_val = [];
  let image_idx_src = [];
	let imageWidth = 1280, imageHeight=720, setWidth= 300, setHeight=168;
	let x1,x2,y1,y2,boxHeight, boxWidth, X, Y;
	let show_selected_images = false;
	let show_selected_chart = false;
	let image_val_lists = [];

	const padding = {top:20, right:15, bottom:20, left:25};
  let width = 500;
  let height = 200;

  let innerWidth = width - (padding.left + padding.right);

  let bbox_keys = [];
  let bbox_vals = [];
  let bbox_xScale;
  let bbox_yScale;
  let bbox_ticks = [];
  let bbox_barWidth;

  let score_keys = [];
  let score_vals = [];
  let score_xScale;
  let score_yScale;
  let score_ticks = [];
  let score_barWidth;

  let iou_keys = [];
  let iou_vals = [];
  let iou_xScale;
  let iou_yScale;
  let iou_ticks = [];
  let iou_barWidth;

	let classes_keys = [];
  let	classes_vals = [];
  let	classes_xScale;
  let classes_yScale;
  let classes_ticks = [];
  let classes_barWidth;

	function adjust_format(tick){
		return "'" + tick.toString().slice(-2);
	}



	function class_details_result(selected_class, selected_head){
		image_source_val = [];
		image_idx_src = [];
		image_val_lists = [];
		bbox_keys = [];
  	bbox_vals = [];
  	bbox_xScale;
  	bbox_yScale;
  	bbox_ticks = [];
  	bbox_barWidth;

  	score_keys = [];
  	score_vals = [];
  	score_xScale;
  	score_yScale;
  	score_ticks = [];
  	score_barWidth;

  	iou_keys = [];
  	iou_vals = [];
  	iou_xScale;
  	iou_yScale;
  	iou_ticks = [];
  	iou_barWidth;

		classes_keys = [];
  	classes_vals = [];
  	classes_xScale;
  	classes_yScale;
  	classes_ticks = [];
  	classes_barWidth;

		show_default_images = false;
		show_selected_images = true;
		show_default_chart = false;
		show_selected_chart = true;
		fetch("/detailed_class_info/"+selected_class+'/'+selected_head).then(res=>res.json()).then(data=>{
			image_val_lists = data['image_values'];
			selected_dtype = data['dtype'];
			current_selected_class = selected_class;
			current_selected_dtype = data['dtype'];
      for (var i =0; i< image_val_lists.length; i++){
        let image_path = "";
        let class_bbox = [];
        let dtype_bbox = [];
				let gt_bbox = [];
        let cl_key = [];
        let dt_key = [];
				let gt_key = [];
        let data = image_val_lists[i];
        dt_key = Object.keys(data['bbox_dtype']);
        dt_key = dt_key;
        cl_key = Object.keys(data['bbox_cate']);
        cl_key = cl_key;
				gt_key = Object.keys(data['gt_bbox']);
				gt_key = gt_key;
        image_path = data['image_dir'];
        image_idx_src.push(data['image_dir']);
        image_idx_src = image_idx_src;
        for (var j=0; j<Object.keys(data['bbox_cate']).length; j++){
          var cl_name = Object.keys(data['bbox_cate'])[j];
          class_bbox[cl_name] = data['bbox_cate'][cl_name];
        }
        for (var k=0; k<Object.keys(data['bbox_dtype']).length; k++){
          var dt_name = Object.keys(data['bbox_dtype'])[k];
          dtype_bbox[dt_name] = data['bbox_dtype'][dt_name];
        }
				for (var l=0; l<Object.keys(data['gt_bbox']).length; l++){
					var gt_name = Object.keys(data['gt_bbox'])[l];
					gt_bbox[gt_name] = data['gt_bbox'][gt_name];
				}
        class_bbox = class_bbox;
        dtype_bbox = dtype_bbox;
				gt_bbox = gt_bbox;
        image_source_val[image_path] = [];
        image_source_val[image_path]['cl_bbox'] = class_bbox;
        image_source_val[image_path]['dt_bbox'] = dtype_bbox;
				image_source_val[image_path]['gt_bbox'] = gt_bbox;

        //image_source_val[image_path] = class_bbox;
      }
			let total_bbox = data['bbox_size'];
			let bbox_lens = [];
			bbox_keys = Object.keys(total_bbox);
			for (var i=0; i< bbox_keys.length; i++){
        var each = {};
        each['key'] = bbox_keys[i];
        each['value'] = total_bbox[bbox_keys[i]].length;
        bbox_lens.push(total_bbox[bbox_keys[i]].length);
        bbox_vals.push(each);
      }
			let max_bbox_len = Math.max(...bbox_lens);
      bbox_xScale = scaleLinear()
        .domain([0, bbox_keys.length])
        .range([padding.left, width - padding.right]);

      bbox_yScale = scaleLinear()
        .domain([0, max_bbox_len])
        .range([height - padding.bottom, padding.top]);

      bbox_barWidth = innerWidth / bbox_keys.length;
      bbox_ticks = bbox_yScale.ticks(7);

			let total_score = data['detection_score'];
			let score_lens = [];
      score_keys = Object.keys(total_score);
      for (var i=0; i < score_keys.length; i++){
        var each = {};
        each['key'] = score_keys[i];
        each['value'] = total_score[score_keys[i]].length;
        score_lens.push(total_score[score_keys[i]].length);
        score_vals.push(each);
      }
      let max_score_len = Math.max(...score_lens);
      score_xScale = scaleLinear()
        .domain([0, score_keys.length])
        .range([padding.left, width - padding.right]);

      score_yScale = scaleLinear()
        .domain([0, max_score_len])
        .range([height - padding.bottom, padding.top]);

      score_barWidth = innerWidth / score_keys.length;
      score_ticks = score_yScale.ticks(7);

			let total_iou = data['iou'];
			let iou_lens = [];
      iou_keys = Object.keys(total_iou);
      for (var i=0; i < iou_keys.length; i++){
        var each = {};
        each['key'] = iou_keys[i];
        each['value'] = total_iou[iou_keys[i]].length;
        iou_lens.push(total_iou[iou_keys[i]].length);
        iou_vals.push(each);
      }
      let max_iou_len = Math.max(...iou_lens);
      iou_xScale = scaleLinear()
        .domain([0, iou_keys.length])
        .range([padding.left, width - padding.right]);

      iou_yScale = scaleLinear()
        .domain([0, max_iou_len])
        .range([height - padding.bottom, padding.top]);

        iou_barWidth = innerWidth / iou_keys.length;
        iou_ticks = iou_yScale.ticks(7);

			if(selected_dtype == 2){
				let total_classes = data['inc_classes'];
				let classes_len = [];
				classes_keys = Object.keys(total_classes);
				for (var i = 0; i < classes_keys.length; i++){
					var each = {};
					each['key'] = classes_keys[i];
					each['value'] = total_classes[classes_keys[i]];
					classes_len.push(total_classes[classes_keys[i]]);
					classes_vals.push(each);
				}
				let max_classes_len = Math.max(...classes_len);
				classes_xScale = scaleLinear()
					.domain([0, classes_keys.length])
					.range([padding.left, width - padding.right]);

				classes_yScale = scaleLinear()
					.domain([0, max_classes_len])
					.range([height - padding.bottom, padding.top]);

				classes_barWidth = innerWidth / classes_keys.length;
				classes_ticks = classes_yScale.ticks(5);
			}


		});
	}

	function td_doubleClicked(selected_class, event){
		//event.style.backgroundColor = "rgb(245, 244, 244)";
		event.style.backgroundColor = 'white';
		event.style.color = "black";
		show_default_images = true;
		show_selected_images = false;
		show_default_chart = true;
		show_selected_chart = false;
		show_chart_images = false;
	}

	function td_clicked(selected_class, selected_head, event){
		var j = document.getElementsByTagName("td");
		for (var i=0; i < j.length; i++){
			j[i].style.backgroundColor = 'white';
			j[i].style.color = "black";
		}
		event.style.backgroundColor = '#8a8787';
		event.style.color = "white";
		show_selected_images = true;
		show_default_images = false;
		show_default_chart = false;
		show_selected_chart = true;
		show_chart_images = false;
		class_details_result(selected_class, selected_head);

	}

	function chart_dblclick(chart_type, chart_key, event){
		console.log("event.style :: ", event.style);
		show_selected_images = true;
		show_chart_images = false;
		show_default_chart = false;
		show_selected_chart = true;
		show_default_images = false;
		event.style.fill = "#f5e0a8";
	}


	let chart_img_source_val = [];
	let chart_img_idx_src = [];
	let chart_image_val_lists = [];
	function chart_detail_info(chart_type, chart_key, event){
		console.log("event.style :: ", event.style);
		event.style.fill = "yellowgreen";
		chart_img_source_val = [];
		chart_img_idx_src = [];
		chart_image_val_lists = [];

		show_default_images = false;
		show_selected_images = false;
		show_default_chart = false;
		show_selected_chart = true;
		show_chart_images = true;
		fetch("/get_chart_detail_info/"+current_selected_class+'/'+current_selected_dtype+'/'+chart_key+'/'+chart_type).then(
			res=>res.json()).then(result=>{
				chart_image_val_lists = result;
				for (var i = 0; i < chart_image_val_lists.length; i++){
					let image_path = "";
					let class_bbox = [];
					let dtype_bbox = [];
					let gt_bbox = [];
					let cl_key = [];
					let dt_key = [];
					let gt_key = [];
					let data = chart_image_val_lists[i];
					dt_key = Object.keys(data['bbox_dtype']);
					dt_key = dt_key;
					cl_key = Object.keys(data['bbox_cate']);
					cl_key = cl_key;
					gt_key = Object.keys(data['gt_bbox']);
					gt_key = gt_key;
					image_path = data['image_dir'];
					chart_img_idx_src.push(data['image_dir']);
					chart_img_idx_src = chart_img_idx_src;
					for (var j=0; j<Object.keys(data['bbox_cate']).length; j++){
						var cl_name = Object.keys(data['bbox_cate'])[j];
						class_bbox[cl_name] = data['bbox_cate'][cl_name];
					}
					for (var k=0; k<Object.keys(data['bbox_dtype']).length; k++){
						var dt_name = Object.keys(data['bbox_dtype'])[k];
						dtype_bbox[dt_name] = data['bbox_dtype'][dt_name];
					}
					for (var l=0; l<Object.keys(data['gt_bbox']).length; l++){
						var gt_name = Object.keys(data['gt_bbox'])[l];
						gt_bbox[gt_name] = data['gt_bbox'][gt_name];
					}
					class_bbox = class_bbox;
					dtype_bbox = dtype_bbox;
					gt_bbox = gt_bbox;
					chart_img_source_val[image_path] = [];
					chart_img_source_val[image_path]['cl_bbox'] = class_bbox;
					chart_img_source_val[image_path]['dt_bbox'] = dtype_bbox;
					chart_img_source_val[image_path]['gt_bbox'] = gt_bbox;
				}
			})

	}

	function image_detail(img_src){
		console.log("img_src ::: ", img_src);

	}
	let isOpenModal = false;
	let modal_value;
	function openModal(){
		isOpenModal = true;
	}
	function closeModal(){
		isOpenModal = false;
	}


</script>

<main>
	<h1> Error Report</h1>
	<div id="container">
		<div id="sidebar" style="width: 550px;">
			<div id="summary-view" class="view-panel">
				<div class="view-title">Result Summary</div>
					<div id="table_size">
						<table class="summary-table">
							<thead>
								<tr>
									{#each table_heads as head}
										<th>{head}</th>
									{/each}
								<tr/>
							</thead>
							<tbody>
								{#each table_vals as rows}
									<tr>
										{#each rows as cell, i}
										<td on:click={td_clicked(rows[0], table_heads[i],this)} on:dblclick={td_doubleClicked(rows[0], this)}>{cell}</td>
										{/each}
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
			</div>
			<div id="score-distributions-view" class="view-panel">
				<div class="view-title">Score Distributions</div>
					<div id="score-distributions-view-content">
						{#if show_default_chart == true}
						<Distribution/>
						{/if}
						{#if show_selected_chart == true}
						<h3> bbox distribution </h3>
						<div class="chart" bind:clientWidth={width} bind:clientHeight={height}>
							<svg class = "chart-svg">
								<!-- y axis -->
								<g class="axis y-axis">
									{#each bbox_ticks as tick}
										<g class="tick tick-{tick}" transform="translate(0, {bbox_yScale(tick)})">
											<line x2="100%"></line>
											<text y ="-4">{tick} </text>
										</g>
									{/each}
								</g>

								<!-- x axis -->
								<g class = "axis x-axis">
									{#each bbox_vals as val, i}
										<g class="tick" transform="translate({bbox_xScale(i)}, {height})">
											<text x="{bbox_barWidth/2}" y="-4">{width > 380 ? val.key : adjust_format(val.value)}</text>
										</g>
									{/each}
								</g>

								<g class='bars'>
									{#each bbox_vals as val, i}
										<rect x="{bbox_xScale(i) + 10}" y="{bbox_yScale(val.value)}" width="{bbox_barWidth - 8}"
										height = "{bbox_yScale(0) - bbox_yScale(val.value)}"
										on:click={chart_detail_info('bbox', val.key, this)} on:dblclick={chart_dblclick('bbox', val.key, this)}/>
									{/each}
								</g>
							</svg>
						</div>

						<!-- score chart -->
						{#if selected_dtype != 7}
						<h3> score distribution </h3>
						<div class="chart" bind:clientWidth={width} bind:clientHeight={height}>
							<svg class = "chart-svg">
								<!-- y axis -->
								<g class="axis y-axis">
									{#each score_ticks as tick}
										<g class="tick tick-{tick}" transform="translate(0, {score_yScale(tick)})">
											<line x2="100%"></line>
											<text y ="-4">{tick} </text>
										</g>
									{/each}
								</g>

								<!-- x axis -->
								<g class = "axis x-axis">
									{#each score_vals as val, i}
										<g class="tick" transform="translate({score_xScale(i)}, {height})">
											<text x="{score_barWidth/2}" y="-4">{width > 380 ? val.key : adjust_format(val.value)}</text>
										</g>
									{/each}
								</g>

								<g class='bars'>
									{#each score_vals as val, i}
										<rect x="{score_xScale(i) + 10}" y="{score_yScale(val.value)}" width="{score_barWidth - 8}"
										height = "{score_yScale(0) - score_yScale(val.value)}"
										on:click={chart_detail_info('score', val.key, this)} on:dblclick={chart_dblclick('score', val.key, this)}/>
									{/each}
								</g>
							</svg>
						</div>
						{/if}

						<!-- iou chart -->
						{#if selected_dtype != 6 && selected_dtype != 7}
						<h3> iou distribution </h3>
						<div class="chart" bind:clientWidth={width} bind:clientHeight={height}>
							<svg class="chart-svg">
								<!-- y axis -->
								<g class="axis y-axis">
									{#each iou_ticks as tick}
										<g class="tick tick-{tick}" transform="translate(0, {iou_yScale(tick)})">
											<line x2="100%"></line>
											<text y ="-4">{tick} </text>
										</g>
									{/each}
								</g>

								<!-- x axis -->
								<g class = "axis x-axis">
									{#each iou_vals as val, i}
										<g class="tick" transform="translate({iou_xScale(i)}, {height})">
											<text x="{iou_barWidth/2}" y="-4">{width > 380 ? val.key : adjust_format(val.value)}</text>
										</g>
									{/each}
								</g>

								<g class='bars'>
									{#each iou_vals as val, i}
										<rect x="{iou_xScale(i) + 10}" y="{iou_yScale(val.value)}" width="{iou_barWidth - 8}"
										height = "{iou_yScale(0) - iou_yScale(val.value)}"
										on:click={chart_detail_info('iou', val.key, this)} on:dblclick={chart_dblclick('iou', val.key, this)}/>
									{/each}
								</g>
							</svg>
						</div>
						{/if}

						<!-- misdetected class chart-->
						{#if selected_dtype == 2}
						<h3> mis-detected distribution </h3>
						<div class = "chart" bind:clientWidth={width} bind:clientHeight={height}>
							<svg class = "chart-svg">
								<!-- y axis-->
								<g class="axis y-axis">
									{#each classes_ticks as tick}
										<g class="tick tick-{tick}" transform="translate(0, {classes_yScale(tick)})">
										<line x2="100%"></line>
										<text y ="-4">{tick} </text>
										</g>
									{/each}
								</g>

								<!-- x axis -->
								<g class = "axis x-axis">
									{#each classes_vals as val, i}
										<g class="tick" transform="translate({classes_xScale(i)}, {height})">
											<text x="{classes_barWidth/2}" y="-4">{width > 380 ? val.key : adjust_format(val.value)}</text>
										</g>
									{/each}
								</g>

								<g class='bars'>
									{#each classes_vals as val, i}
										<rect x="{classes_xScale(i) + 10}" y="{classes_yScale(val.value)}" width="{classes_barWidth - 8}"
										height = "{classes_yScale(0) - classes_yScale(val.value)}"
										on:click={chart_detail_info('type_class', val.key, this)} on:dblclick={chart_dblclick('type_class', val.key, this)}/>
									{/each}
								</g>

							</svg>
						</div>
						{/if}

					{/if}
					</div>
			</div>
		</div>

		<div id="main-section" style="width: 1000px;">
			<div id="selected-image-view" class="view-panel">
				<div class="view-title">Image View
					{#if show_selected_images == true || show_chart_images == true}
					<Switch on:change={handleChange} checked={switch_check} onColor="#7d8a91"
					onHandleColor="#fff" handleDiameter={20} unCheckedIcon={false}
					boxShadow="0px 1px 5px rgba(0, 0, 0, 0.6)"
					activeBoxShadow="0px 0px 1px 10px rgba(0, 0, 0, 0.2)"
					height={16} width={30} containerClass="react-switch"
					id="material-switch">
					<span slot="checkedIcon" />
					<span slot="unCheckedIcon"/>
					</Switch>

					{switch_check ? 'detection type' : 'class'}
					{/if}
				</div>
				<div id="selected-image-view-content">
					{#if show_default_images == true}
					<DefaultImageView/>
					{/if}

					{#if show_selected_images == true}
						{#if switch_check == false}
						<!-- svelte-ignore a11y-missing-attribute -->
						<div id ="images_view">
							{#each image_idx_src as img_src}
								<div class = "multiple_images" on:click={openModal} on:click={modal_value.get_instance_val(img_src, image_source_val[img_src])}>

									<!-- svelte-ignore a11y-missing-attribute -->
									<img class = "images" id="selected_image" src = {img_src} width = {setWidth} height={setHeight} >
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
								</div>
								<Modal isOpenModal={isOpenModal} on:closeModal={closeModal} bind:this={modal_value}/>
							{/each}
						</div>
						{/if}

						{#if switch_check == true}
						<!-- svelte-ignore a11y-missing-attribute -->
						<div id ="images_view">
							{#each image_idx_src as img_src}
								<div class = "multiple_images" on:click={openModal} on:click={modal_value.get_instance_val(img_src, image_source_val[img_src])}>
									<!-- svelte-ignore a11y-missing-attribute -->
									<img class = "images" id="selected_image" src = {img_src} width = {setWidth} height={setHeight}>
									<svg class = "bboxes" id="image_box" width={setWidth} height={setHeight}>
										{#each Object.keys(image_source_val[img_src]['dt_bbox']) as dt_name}
											{#each Object.keys(image_source_val[img_src]['dt_bbox'][dt_name]) as dt_key}
												{x1 = image_source_val[img_src]['dt_bbox'][dt_name][dt_key]['x1']}
												{x2 = image_source_val[img_src]['dt_bbox'][dt_name][dt_key]['x2']}
												{y1 = image_source_val[img_src]['dt_bbox'][dt_name][dt_key]['y1']}
												{y2 = image_source_val[img_src]['dt_bbox'][dt_name][dt_key]['y2']}
												{boxWidth = (Math.abs(x2-x1)/imageWidth)*setWidth}
												{boxHeight = (Math.abs(y2-y1)/imageHeight)*setHeight}
												{X = (x1/imageWidth)*setWidth}
												{Y = (y1/imageHeight)*setHeight}
												<rect x={X} y={Y} width={boxWidth} height={boxHeight} stroke={detected_types[dt_name]['color']}/>
											{/each}
										{/each}
									</svg>
								</div>
								<Modal isOpenModal={isOpenModal} on:closeModal={closeModal} bind:this={modal_value}/>
							{/each}
						</div>
						{/if}
					{/if}

					{#if show_chart_images == true}
						{#if switch_check == false}
						<!-- svelte-ignore a11y-missing-attribute -->
						<div id ="images_view">
							{#each chart_img_idx_src as img_src}
								<div class = "multiple_images" on:click={openModal} on:click={modal_value.get_instance_val(img_src, chart_img_source_val[img_src])}>
									<!-- svelte-ignore a11y-missing-attribute -->
									<img class = "images" id="selected_image" src = {img_src} width = {setWidth} height={setHeight} on:click={image_detail(img_src)}>
									<svg class = "bboxes" id="image_box" width={setWidth} height={setHeight}>
										{#each Object.keys(chart_img_source_val[img_src]['cl_bbox']) as cl_name}
											{#each Object.keys(chart_img_source_val[img_src]['cl_bbox'][cl_name]) as cl_key}
												{x1 = chart_img_source_val[img_src]['cl_bbox'][cl_name][cl_key]['x1']}
												{x2 = chart_img_source_val[img_src]['cl_bbox'][cl_name][cl_key]['x2']}
												{y1 = chart_img_source_val[img_src]['cl_bbox'][cl_name][cl_key]['y1']}
												{y2 = chart_img_source_val[img_src]['cl_bbox'][cl_name][cl_key]['y2']}
												{boxWidth = (Math.abs(x2-x1)/imageWidth)*setWidth}
												{boxHeight = (Math.abs(y2-y1)/imageHeight)*setHeight}
												{X = (x1/imageWidth)*setWidth}
												{Y = (y1/imageHeight)*setHeight}
												<rect x={X} y={Y} width={boxWidth} height={boxHeight} stroke={class_lists[cl_name]['color']}/>
											{/each}
										{/each}
									</svg>
								</div>
								<Modal isOpenModal={isOpenModal} on:closeModal={closeModal} bind:this={modal_value}/>
							{/each}
						</div>
						{/if}

						{#if switch_check == true}
						<!-- svelte-ignore a11y-missing-attribute -->
						<div id ="images_view">
							{#each chart_img_idx_src as img_src}
								<div class = "multiple_images" on:click={openModal} on:click={modal_value.get_instance_val(img_src, chart_img_source_val[img_src])}>
									<!-- svelte-ignore a11y-missing-attribute -->
									<img class = "images" id="selected_image" src = {img_src} width = {setWidth} height={setHeight}>
									<svg class = "bboxes" id="image_box" width={setWidth} height={setHeight}>
										{#each Object.keys(chart_img_source_val[img_src]['dt_bbox']) as dt_name}
											{#each Object.keys(chart_img_source_val[img_src]['dt_bbox'][dt_name]) as dt_key}
												{x1 = chart_img_source_val[img_src]['dt_bbox'][dt_name][dt_key]['x1']}
												{x2 = chart_img_source_val[img_src]['dt_bbox'][dt_name][dt_key]['x2']}
												{y1 = chart_img_source_val[img_src]['dt_bbox'][dt_name][dt_key]['y1']}
												{y2 = chart_img_source_val[img_src]['dt_bbox'][dt_name][dt_key]['y2']}
												{boxWidth = (Math.abs(x2-x1)/imageWidth)*setWidth}
												{boxHeight = (Math.abs(y2-y1)/imageHeight)*setHeight}
												{X = (x1/imageWidth)*setWidth}
												{Y = (y1/imageHeight)*setHeight}
												<rect x={X} y={Y} width={boxWidth} height={boxHeight} stroke={detected_types[dt_name]['color']}/>
											{/each}
										{/each}
									</svg>
								</div>
								<Modal isOpenModal={isOpenModal} on:closeModal={closeModal} bind:this={modal_value}/>
							{/each}
						</div>

						{/if}


					{/if}
				</div>
			</div>
		</div>
	</div>
</main>

<style>
	h1 {
		font-size: 1.3rem;
		font-weight: 500;
		margin-top: 0;
	}
	#container {
		display: flex;
	}
	#sidebar, #main-section {
		display: flex;
		flex-direction: column;
	}
	.view-panel {
		border: 2px solid #eee;
		margin-bottom: 15px;
		margin-right: 15px;
	}
	.view-title {
		background-color: #f3f3f3;
		font-size: 1.0rem;
		margin-bottom: 8px;
		padding: 3px 8px 5px 12px;
	}
	#selected-image-view-content {
		height: 600px;
		padding: 5px;
		overflow-y: auto;
	}
	#score-distributions-view-content {
		padding: 15px;
		height: 200px;
		overflow-y: auto;
	}
	table, th, td {
		border: 0.5px solid;
		border-collapse: collapse;
		margin-bottom: 2px;
	}
	.summary-table td:hover{
		font-weight: bold;
	}

	.summary-table {
		border: 1px solid #17202A;
		width: 100%;
		text-align: center;
		border-collapse: collapse;
	}
	.summary-table td, .summary-table th {
		border: 1px solid #808B96;
		padding: 4px 2px;
	}
	.summary-table tbody td {
		font-size: 10px;
	}
	/*.summary-table tr:nth-child(even) {
		background: #F5F4F4;
	}*/
	.summary-table thead {
		/*background: #e0e2e2;*/
		background: #F5F4F4;
	}
	.summary-table thead th {
		font-size: 10px;
		/*color: #FFFFFF;*/
		text-align: center;
	}
	.summary-table thead th:first-child {
		border-left: none;
	}

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

	h3{
    text-align: center;
  }
  .chart{
    width:100%;
    max-width: 500px;
    margin: 0 auto;
  }
  .chart-svg{
    position: relative;
    width: 100%;
    height: 200px;
  }
  .tick {
		font-family: Helvetica, Arial;
		font-size: .725em;
		font-weight: 200;
	}
  .tick line {
		stroke: #e2e2e2;
		stroke-dasharray: 2;
	}

	.tick text {
		fill: #ccc;
		text-anchor: start;
	}

	.tick.tick-0 line {
		stroke-dasharray: 0;
	}

	.x-axis .tick text {
		text-anchor: middle;
	}

	.bars rect {
		fill: #f5e0a8;
		stroke: none;
		opacity: 0.65;
	}



</style>