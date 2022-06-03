<script>
	import DefaultImageView from './Components/DefaultImageView.svelte';
	import Distribution from './Components/Distribution.svelte';
	import { onMount } from 'svelte';
	import { scaleLinear } from "d3-scale";
	import { line, curveStep, curveNatural, extent, svg, text } from 'd3';
	import Switch from "svelte-switch";
	import Modal from './Components/Modal.svelte';
	import { tooltip } from './Components/tooltip';
	let change_table_switch = false;
	let show_default_chart = true;
	let show_default_images = true;
	let show_chart_images = false;
	let show_gt_images = false;


	function tableChange(e){
		const {checked} = e.detail;
		change_table_switch = checked;
		show_chart_images = false;
		show_selected_chart = false;
		show_default_chart = true;
		show_default_images = true;
		console.log("chage_table_swtich :: ", change_table_switch);
	}


  let table_heads = [];
  let table_vals = [];
	let table_heads_desc;

	let gt_table_heads = [];
	let gt_table_vals = [];
	let gt_table_heads_desc;
	let other_heads_vals = ['class name', 'average precision', 'detected number', 'gt number', 'number'];

  onMount(async ()=>{
		fetch('/class_values/').then(res =>res.json()).then(overall=>{
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

			let result_array = overall;
			let class_list = Object.keys(result_array);
			class_list = class_list;
			table_heads = ['class name', 'average precision', 'detected number', 'gt number',
			'correct detection', 'classification error', 'localization error',
			'cls and loc error', 'duplication error', 'back detect error', 'other error'];
			//table_heads = ['class name', 'average precision', 'number', 'gt_number', 'type 1',
			//'type 2', 'type 3', 'type 4', 'type 5', 'type 6', 'type 8'];

			let nums = [];
			let ap = [];
			let gt_nums = [];

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
					if (dt_keys[j] != '7'){
						dt_type_vals[class_list[i]].push(dt_results[dt_keys[j]]['total_num'])
						dt_type_vals[class_list[i]] = dt_type_vals[class_list[i]];
					}
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
		fetch('/gt_values/').then(res => res.json()).then(overall =>{
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
			let result_array = overall;
			let class_list = Object.keys(result_array);
			//gt_table_heads = ['class name', 'number', 'type 1', 'type 2', 'type 3', 'type 4', 'type 5',
			//'type 6','type 7', 'type 8', 'type 9', 'type 10', 'type 11'];
			gt_table_heads = ['class name', 'number', 'match + correct', 'match + cls', 'match + loc',
			'match + cls and loc', 'match + incorrect', 'matches + cor, dup', 'matches + cor, cls', 'matches + cor, loc',
			'matches + with cor', 'matches + incor', 'missed detected']
			let nums = [];

			for (var i=0; i < Object.keys(result_array).length; i++){
				nums.push(result_array[class_list[i]]['num']);
				let gt_type = result_array[class_list[i]]['gt_type'];
				let gt_keys = Object.keys(gt_type);
				for (var j=0; j<Object.keys(gt_type).length; j++){
					dt_type_vals[class_list[i]].push(gt_type[gt_keys[j]]['num']);
				}
			}
			gt_table_vals = [];
			for (var i=0; i< class_list.length; i++){
				var row = [];
				row.push(class_list[i]);
				row.push(nums[i]);
				for (var j=0; j<dt_type_vals[class_list[i]].length; j++){
					row.push(dt_type_vals[class_list[i]][j]);
				}
				gt_table_vals.push(row);
			}
			gt_table_vals = gt_table_vals;
		});

		fetch('/dt_types/').then(res => res.json()).then(types=>{
			table_heads_desc = types;
			console.log("table_heads_desc ::: ", table_heads_desc);
		});
		fetch('/gt_types/').then(res => res.json()).then(types=>{
			gt_table_heads_desc = types;
			console.log("gt_table_head_desc ::: ", gt_table_heads_desc);
		});

  });

	// images
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
	let x1,x2,y1,y2,boxHeight, boxWidth, X, Y, gt_cate_name;
	let tooltip_val;
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

	let line_iou_xScale;
	let	line_iou_ySclae;
	let	line_bbox_xScale;
	let	line_bbox_yScale;
	let	line_score_xScale;
	let	line_score_yScale;
	let line_iou_xTicks = [];
	let line_iou_yTicks = [];
	let line_bbox_xTicks = [];
	let line_bbox_yTicks = [];
	let line_score_xTicks = [];
	let line_score_yTicks = [];

	let line_gen;
	let total_result;

	function adjust_format(tick){
		return "'" + tick.toString().slice(-2);
	}

	let gt_image_source_val = [];
	let gt_image_idx_src = [];
	let gt_image_val_lists = [];

	function gt_class_results(selected_class, selected_head){
		gt_image_source_val = [];
		gt_image_idx_src = [];
		gt_image_val_lists = [];

		show_default_images = false;
		show_selected_images = false;
		show_gt_images = true;
		fetch("/ground_truth_images/"+selected_class+'/'+selected_head).then(res=>res.json()).then(data=>{
			console.log("data ::: ", data);

			gt_image_val_lists = data['image_values'];
			current_selected_class = selected_class;
			current_selected_dtype = data['gtype'];

			for (var i = 0; i < gt_image_val_lists.length; i++){
				let cur_data = gt_image_val_lists[i];
				let image_path = cur_data['image_dir'];
				gt_image_idx_src.push(cur_data['image_dir']);
        gt_image_idx_src = gt_image_idx_src;
				let selected_bbox = cur_data['cate_dtype']['box'];

				gt_image_source_val[image_path] = [];
				gt_image_source_val[image_path]['cl_gt'] = selected_bbox;
			}

			console.log("gt_image_source_val :: ", gt_image_source_val);
		});
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

		line_iou_xScale;
		line_iou_ySclae;
		line_iou_xTicks = [];
		line_iou_yTicks = [];
		line_bbox_xScale;
		line_bbox_yScale;
		line_bbox_xTicks = [];
		line_bbox_yTicks = [];
		line_score_xScale;
		line_score_yScale;
		line_score_xTicks = [];
		line_score_yTicks = [];

		line_gen;

		show_default_images = false;
		show_selected_images = true;
		show_default_chart = false;
		show_selected_chart = true;
		show_gt_images = false;
		fetch("/detailed_class_info/"+selected_class+'/'+selected_head).then(res=>res.json()).then(data=>{
			total_result = data;
			image_val_lists = data['image_values'];
			selected_dtype = data['dtype'];
			current_selected_class = selected_class;
			current_selected_dtype = data['dtype'];

      for (var i =0; i< image_val_lists.length; i++){
        let image_path = "";

				let selected_gt_bbox = [];
				let selected_gt_cate = [];

        let data = image_val_lists[i];

        let bbox_values = data['bbox_cate'];
				let selected_bbox = data['cate_dtype']['box'];
				let selected_scores = data['cate_dtype']['score'];
				let selected_pred = data['cate_dtype']['pred'];
				let selected_gt = data['cate_dtype']['gt'];

        image_path = data['image_dir'];
        image_idx_src.push(data['image_dir']);
        image_idx_src = image_idx_src;
				for (var m=0; m<Object.keys(data['cate_dtype_gt']['gt_bbox']).length; m++){
					var gt_type = Object.keys(data['cate_dtype_gt']['gt_bbox'])[m];
					selected_gt_bbox[gt_type] = data['cate_dtype_gt']['gt_bbox'][gt_type];
				}
				for (var n=0; n<Object.keys(data['cate_dtype_gt']['gt_cate']).length; n++){
					var gt_type = Object.keys(data['cate_dtype_gt']['gt_cate'])[n];
					selected_gt_cate[gt_type] = data['cate_dtype_gt']['gt_cate'][gt_type];
				}
        image_source_val[image_path] = [];
				image_source_val[image_path]['cl_dt'] = selected_bbox;
				image_source_val[image_path]['cl_dt_gt'] = selected_gt_bbox;
				image_source_val[image_path]['cl_dt_gt_cate'] = selected_gt_cate;
				image_source_val[image_path]['cl_dt_score'] = selected_scores;
				image_source_val[image_path]['cl_dt_pred'] = selected_pred;
				image_source_val[image_path]['cl_dt_cate'] = selected_gt;
				image_source_val[image_path]['bbox_values'] = bbox_values;

				if (selected_bbox.length != selected_scores.length){
					console.log("INCORRECT!!!")
				}

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

			let total_chart_iou = data['chart_iou'];
			line_iou_xScale = scaleLinear()
				.domain([0, Math.max(...total_chart_iou)])
				.range([padding.left, width - padding.right]);

			line_iou_ySclae = scaleLinear()
				.domain([0, Math.max(...total_chart_iou)])
				.range([height - padding.bottom, padding.top]);

			line_iou_xTicks = line_iou_xScale.ticks(10);
			line_iou_yTicks = line_iou_ySclae.ticks(10);

			let total_chart_bbox = data['chart_bbox'];
			line_bbox_xScale = scaleLinear()
				.domain([0, Math.max(...total_chart_bbox)])
				.range([padding.left, width - padding.right]);

			line_bbox_yScale = scaleLinear()
				.domain([0, Math.max(...total_chart_bbox)])
				.range([height - padding.bottom, padding.top]);

			line_bbox_xTicks = line_bbox_xScale.ticks(10);
			line_bbox_yTicks = line_bbox_yScale.ticks(10);

			let total_chart_score = data['chart_score'];
			line_score_xScale = scaleLinear()
				.domain([0, Math.max(...total_chart_score)])
				.range([padding.left, width - padding.right]);

			line_score_yScale = scaleLinear()
				.domain([0, Math.max(...total_chart_score)])
				.range([height - padding.bottom, padding.top]);

			line_score_xTicks = line_score_xScale.ticks(10);
			line_score_yTicks = line_score_yScale.ticks(10);
			console.log("line_score_yTicks::: ", line_score_yTicks);

			line_gen = line()
				.curve(curveStep)
				.x((data) => line_bbox_xScale(data.chart_bbox))
				.y((data) => lines_score_yScale(data.chart_score));

			line_gen = line_gen;

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
		show_gt_images = false;
	}

	function td_clicked(selected_class, selected_head, event){
		console.log("selected td ::: ", selected_class + ", "+ selected_head);
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
		show_gt_images = false;
		class_details_result(selected_class, selected_head);

	}

	function td_gt_clicked(selected_class, selected_head, event){
		console.log("selected gt td ::: ", selected_class + ", " + selected_head);
		var j = document.getElementsByTagName("td");
		for (var i=0; i < j.length; i++){
			j[i].style.backgroundColor = 'white';
			j[i].style.color = "black";
		}
		event.style.backgroundColor = '#8a8787';
		event.style.color = "white";
		show_selected_images = false;
		show_default_images = false;
		show_gt_images = true;
		gt_class_results(selected_class, selected_head);
	}

	function chart_dblclick(chart_type, chart_key, event){
		console.log("event.style :: ", event.style);
		show_selected_images = true;
		show_chart_images = false;
		show_default_chart = false;
		show_selected_chart = true;
		show_default_images = false;
		show_gt_images = false;
		event.style.fill = "#f5e0a8";
	}


	let chart_img_source_val = [];
	let chart_img_idx_src = [];
	let chart_image_val_lists = [];
	function chart_detail_info(chart_type, chart_key, event){
		console.log("event.style :: ", event.style);
		var r = document.getElementsByClassName("chart_bars");
		for (var i=0; i < r.length; i++){
			r[i].style.fill = "#f5e0a8"
		}
		event.style.fill = "#f5bc1f";
		chart_img_source_val = [];
		chart_img_idx_src = [];
		chart_image_val_lists = [];

		show_default_images = false;
		show_selected_images = false;
		show_default_chart = false;
		show_selected_chart = true;
		show_chart_images = true;
		show_gt_images = false;
		fetch("/get_chart_detail_info/"+current_selected_class+'/'+current_selected_dtype+'/'+chart_key+'/'+chart_type).then(
			res=>res.json()).then(result=>{
				chart_image_val_lists = result;
				for (var i = 0; i < chart_image_val_lists.length; i++){
					let image_path = "";

					let selected_gt_bbox = [];
					let selected_gt_cate = [];

					let data = chart_image_val_lists[i];
					let bbox_values = data['bbox_cate'];
					let selected_bbox = data['cate_dtype']['box'];
					let selected_scores = data['cate_dtype']['score'];
					let selected_pred = data['cate_dtype']['pred'];
					let selected_gt = data['cate_dtype']['gt'];


					image_path = data['image_dir'];
					chart_img_idx_src.push(data['image_dir']);
					chart_img_idx_src = chart_img_idx_src;
					for (var m=0; m<Object.keys(data['cate_dtype_gt']['gt_bbox']).length; m++){
						var gt_type = Object.keys(data['cate_dtype_gt']['gt_bbox'])[m];
						selected_gt_bbox[gt_type] = data['cate_dtype_gt']['gt_bbox'][gt_type];
					}
					for (var n=0; n<Object.keys(data['cate_dtype_gt']['gt_cate']).length; n++){
						var gt_type = Object.keys(data['cate_dtype_gt']['gt_cate'])[n];
						selected_gt_cate[gt_type] = data['cate_dtype_gt']['gt_cate'][gt_type];
					}
					chart_img_source_val[image_path] = [];
					chart_img_source_val[image_path]['cl_dt'] = selected_bbox;
					chart_img_source_val[image_path]['cl_dt_gt'] = selected_gt_bbox;
					chart_img_source_val[image_path]['cl_dt_gt_cate'] = selected_gt_cate;
					chart_img_source_val[image_path]['cl_dt_score'] = selected_scores;
					chart_img_source_val[image_path]['cl_dt_pred'] = selected_pred;
					chart_img_source_val[image_path]['cl_dt_cate'] = selected_gt;
					chart_img_source_val[image_path]['bbox_values'] = bbox_values;
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
				<div class="view-title">Result Summary
					<Switch on:change={tableChange} checked={change_table_switch} onColor="#7d8a91"
					onHandleColor="#fff" handleDiameter={20} unCheckedIcon={false}
					boxShadow="0px 1px 5px rgba(0, 0, 0, 0.6)"
					activeBoxShadow="0px 0px 1px 10px rgba(0, 0, 0, 0.2)"
					height={16} width={30} containerClass="react-switch"
					id="material-switch">
					<span slot="checkedIcon" />
					<span slot="unCheckedIcon"/>
					</Switch>

					{change_table_switch  ? 'ground truth' : 'detection'}
				</div>
					{#if change_table_switch == false}
					<div id="table_size">
						<table class="summary-table">
							<!-- svelte-ignore component-name-lowercase
							<svg id="table_heads" transform="rotate(-90)"> -->
							<thead>
								<tr>
									{#each table_heads as head}
										{#if other_heads_vals.includes(head) == false}
										<th class="rotate"><div title={table_heads_desc[head]["desc"]} use:tooltip><span>{head}</span></div></th>
										{/if}
										{#if other_heads_vals.includes(head) == true}
										<th class="rotate"><div><span>{head}</span></div></th>
										{/if}
									{/each}
								<tr/>
							</thead>
							<tbody>
								{#each table_vals as rows}
									<tr>
										{#each rows as cell, i}
										<td on:click={td_clicked(rows[0], table_heads[i],this)} on:dblclick={td_doubleClicked(rows[0], this)}>
											{#if cell == 'bicycle'}
												<!-- svelte-ignore component-name-lowercase -->
												<svg class="color-block" width="8" height="10">
													<rect width="8" height="10" x="0" y="0" fill={class_lists[cell]['color']} stroke={class_lists[cell]['color']}/>
												</svg>
											{/if}
											{#if cell == 'bus'}
												<!-- svelte-ignore component-name-lowercase -->
												<svg class="color-block" x="0" width="8" height="10">
													<rect width="8" height="10" x="0" y="0" fill={class_lists[cell]['color']} stroke={class_lists[cell]['color']}/>
												</svg>
											{/if}
											{#if cell == 'car'}
												<!-- svelte-ignore component-name-lowercase -->
												<svg class="color-block" width="8" height="10">
													<rect width="8" height="10" fill={class_lists[cell]['color']} stroke={class_lists[cell]['color']}/>
												</svg>
											{/if}
											{#if cell == 'motorcycle'}
												<!-- svelte-ignore component-name-lowercase -->
												<svg class="color-block" width="8" height="10">
													<rect width="8" height="10" fill={class_lists[cell]['color']} stroke={class_lists[cell]['color']}/>
												</svg>
											{/if}
											{#if cell == 'other person'}
												<!-- svelte-ignore component-name-lowercase -->
												<svg class="color-block" width="8" height="10">
													<rect width="8" height="10" fill={class_lists[cell]['color']} stroke={class_lists[cell]['color']}/>
												</svg>
											{/if}
											{#if cell == 'other vehicle'}
												<!-- svelte-ignore component-name-lowercase -->
												<svg class="color-block" width="8" height="10">
													<rect width="8" height="10" fill={class_lists[cell]['color']} stroke={class_lists[cell]['color']}/>
												</svg>
											{/if}
											{#if cell == 'pedestrian'}
												<!-- svelte-ignore component-name-lowercase -->
												<svg class="color-block" width="8" height="10">
													<rect width="8" height="10" fill={class_lists[cell]['color']} stroke={class_lists[cell]['color']}/>
												</svg>
											{/if}
											{#if cell == 'rider'}
												<!-- svelte-ignore component-name-lowercase -->
												<svg class="color-block" width="8" height="10">
													<rect width="8" height="10" fill={class_lists[cell]['color']} stroke={class_lists[cell]['color']}/>
												</svg>
											{/if}
											{#if cell == 'traffic light'}
												<!-- svelte-ignore component-name-lowercase -->
												<svg class="color-block" width="8" height="10">
													<rect width="8" height="10" fill={class_lists[cell]['color']} stroke={class_lists[cell]['color']}/>
												</svg>
											{/if}
											{#if cell == 'traffic sign'}
												<!-- svelte-ignore component-name-lowercase -->
												<svg class="color-block" width="8" height="10">
													<rect width="8" height="10" fill={class_lists[cell]['color']} stroke={class_lists[cell]['color']}/>
												</svg>
											{/if}
											{#if cell == 'trailer'}
												<!-- svelte-ignore component-name-lowercase -->
												<svg class="color-block" width="8" height="10">
													<rect width="8" height="10" fill={class_lists[cell]['color']} stroke={class_lists[cell]['color']}/>
												</svg>
											{/if}
											{#if cell == 'train'}
												<!-- svelte-ignore component-name-lowercase -->
												<svg class="color-block" width="8" height="10">
													<rect width="8" height="10" fill={class_lists[cell]['color']} stroke={class_lists[cell]['color']}/>
												</svg>
											{/if}
											{#if cell == 'truck'}
												<!-- svelte-ignore component-name-lowercase -->
												<svg class="color-block" width="8" height="10">
													<rect width="8" height="10" fill={class_lists[cell]['color']} stroke={class_lists[cell]['color']}/>
												</svg>
											{/if}
											{cell}
										</td>
										{/each}
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
					{/if}
					{#if change_table_switch == true}
					<div id="table_size">
						<table class="summary-table">
							<thead>
								<tr>
									{#each gt_table_heads as head}
										{#if other_heads_vals.includes(head) == false}
										<th class="rotate"><div title={gt_table_heads_desc[head]["desc"]} use:tooltip><span>{head}</span></div></th>
										{/if}
										{#if other_heads_vals.includes(head) == true}
										<th class="rotate"><div><span>{head}</span></div></th>
										{/if}
									{/each}
								<tr/>
							</thead>
							<tbody>
								{#each gt_table_vals as rows}
									<tr>
										{#each rows as cell, i}
										<td on:click={td_gt_clicked(rows[0], gt_table_heads[i],this)} on:dblclick={td_doubleClicked(rows[0], this)}>
											{#if cell == 'bicycle'}
												<!-- svelte-ignore component-name-lowercase -->
												<svg class="color-block" width="8" height="10">
													<rect width="8" height="10" fill={class_lists[cell]['color']} stroke={class_lists[cell]['color']}/>
												</svg>
											{/if}
											{#if cell == 'bus'}
												<!-- svelte-ignore component-name-lowercase -->
												<svg class="color-block" width="8" height="10">
													<rect width="8" height="10" fill={class_lists[cell]['color']} stroke={class_lists[cell]['color']}/>
												</svg>
											{/if}
											{#if cell == 'car'}
												<!-- svelte-ignore component-name-lowercase -->
												<svg class="color-block" width="8" height="10">
													<rect width="8" height="10" fill={class_lists[cell]['color']} stroke={class_lists[cell]['color']}/>
												</svg>
											{/if}
											{#if cell == 'motorcycle'}
												<!-- svelte-ignore component-name-lowercase -->
												<svg class="color-block" width="8" height="10">
													<rect width="8" height="10" fill={class_lists[cell]['color']} stroke={class_lists[cell]['color']}/>
												</svg>
											{/if}
											{#if cell == 'other person'}
												<!-- svelte-ignore component-name-lowercase -->
												<svg class="color-block" width="8" height="10">
													<rect width="8" height="10" fill={class_lists[cell]['color']} stroke={class_lists[cell]['color']}/>
												</svg>
											{/if}
											{#if cell == 'other vehicle'}
												<!-- svelte-ignore component-name-lowercase -->
												<svg class="color-block" width="8" height="10">
													<rect width="8" height="10" fill={class_lists[cell]['color']} stroke={class_lists[cell]['color']}/>
												</svg>
											{/if}
											{#if cell == 'pedestrian'}
												<!-- svelte-ignore component-name-lowercase -->
												<svg class="color-block" width="8" height="10">
													<rect width="8" height="10" fill={class_lists[cell]['color']} stroke={class_lists[cell]['color']}/>
												</svg>
											{/if}
											{#if cell == 'rider'}
												<!-- svelte-ignore component-name-lowercase -->
												<svg class="color-block" width="8" height="10">
													<rect width="8" height="10" fill={class_lists[cell]['color']} stroke={class_lists[cell]['color']}/>
												</svg>
											{/if}
											{#if cell == 'traffic light'}
												<!-- svelte-ignore component-name-lowercase -->
												<svg class="color-block" width="8" height="10">
													<rect width="8" height="10" fill={class_lists[cell]['color']} stroke={class_lists[cell]['color']}/>
												</svg>
											{/if}
											{#if cell == 'traffic sign'}
												<!-- svelte-ignore component-name-lowercase -->
												<svg class="color-block" width="8" height="10">
													<rect width="8" height="10" fill={class_lists[cell]['color']} stroke={class_lists[cell]['color']}/>
												</svg>
											{/if}
											{#if cell == 'trailer'}
												<!-- svelte-ignore component-name-lowercase -->
												<svg class="color-block" width="8" height="10">
													<rect width="8" height="10" fill={class_lists[cell]['color']} stroke={class_lists[cell]['color']}/>
												</svg>
											{/if}
											{#if cell == 'train'}
												<!-- svelte-ignore component-name-lowercase -->
												<svg class="color-block" width="8" height="10">
													<rect width="8" height="10" fill={class_lists[cell]['color']} stroke={class_lists[cell]['color']}/>
												</svg>
											{/if}
											{#if cell == 'truck'}
												<!-- svelte-ignore component-name-lowercase -->
												<svg class="color-block" width="8" height="10">
													<rect width="8" height="10" fill={class_lists[cell]['color']} stroke={class_lists[cell]['color']}/>
												</svg>
											{/if}
											{cell}
										</td>
										{/each}
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
					{/if}
					<!--<InfoModal infoModalOpen={infoModalOpen} on:closeInfoModal={closeInfoModal}/>-->
			</div>

			<div id="score-distributions-view" class="view-panel">
				<div class="view-title">Score Distributions</div>
					<div id="score-distributions-view-content">
						{#if show_default_chart == true}
						<Distribution/>
						{/if}
						{#if show_selected_chart == true}
						<h4> bbox distribution </h4>
						<div class="chart" bind:clientWidth={width} bind:clientHeight={height}>
							<!-- svelte-ignore component-name-lowercase -->
							<svg class = "chart-svg">
								<!-- y axis -->
								<g class="axis y-axis">
									{#each bbox_ticks as tick}
										<g class="tick tick-{tick}" transform="translate(0, {bbox_yScale(tick)})">
											<!-- svelte-ignore component-name-lowercase -->
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
										<rect class = "chart_bars" x="{bbox_xScale(i) + 10}" y="{bbox_yScale(val.value)}" width="{bbox_barWidth - 8}"
										height = "{bbox_yScale(0) - bbox_yScale(val.value)}"
										on:click={chart_detail_info('bbox', val.key, this)} on:dblclick={chart_dblclick('bbox', val.key, this)}/>
									{/each}
								</g>
							</svg>
						</div>

						<!-- score chart -->
						{#if selected_dtype != 7}
						<h4> score distribution </h4>
						<div class="chart" bind:clientWidth={width} bind:clientHeight={height}>
							<!-- svelte-ignore component-name-lowercase -->
							<svg class = "chart-svg">
								<!-- y axis -->
								<g class="axis y-axis">
									{#each score_ticks as tick}
										<g class="tick tick-{tick}" transform="translate(0, {score_yScale(tick)})">
											<!-- svelte-ignore component-name-lowercase -->
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
										<rect class="chart_bars" x="{score_xScale(i) + 10}" y="{score_yScale(val.value)}" width="{score_barWidth - 8}"
										height = "{score_yScale(0) - score_yScale(val.value)}"
										on:click={chart_detail_info('score', val.key, this)} on:dblclick={chart_dblclick('score', val.key, this)}/>
									{/each}
								</g>
							</svg>
						</div>
						{/if}

						<!-- iou chart -->
						{#if selected_dtype != 6 && selected_dtype != 7}
						<h4> iou distribution </h4>
						<div class="chart" bind:clientWidth={width} bind:clientHeight={height}>
							<!-- svelte-ignore component-name-lowercase -->
							<svg class="chart-svg">
								<!-- y axis -->
								<g class="axis y-axis">
									{#each iou_ticks as tick}
										<g class="tick tick-{tick}" transform="translate(0, {iou_yScale(tick)})">
											<!-- svelte-ignore component-name-lowercase -->
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
										<rect class = "chart_bars" x="{iou_xScale(i) + 10}" y="{iou_yScale(val.value)}" width="{iou_barWidth - 8}"
										height = "{iou_yScale(0) - iou_yScale(val.value)}"
										on:click={chart_detail_info('iou', val.key, this)} on:dblclick={chart_dblclick('iou', val.key, this)}/>
									{/each}
								</g>
							</svg>
						</div>
						{/if}

						<!-- misdetected class chart-->
						{#if selected_dtype == 2}
						<h4> mis-detected distribution </h4>
						<div class = "chart" bind:clientWidth={width} bind:clientHeight={height}>
							<!-- svelte-ignore component-name-lowercase -->
							<svg class = "chart-svg">
								<!-- y axis-->
								<g class="axis y-axis">
									{#each classes_ticks as tick}
										<g class="tick tick-{tick}" transform="translate(0, {classes_yScale(tick)})">
										<!-- svelte-ignore component-name-lowercase -->
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
										<rect class = "chart_bars" x="{classes_xScale(i) + 10}" y="{classes_yScale(val.value)}" width="{classes_barWidth - 8}"
										height = "{classes_yScale(0) - classes_yScale(val.value)}"
										on:click={chart_detail_info('type_class', val.key, this)} on:dblclick={chart_dblclick('type_class', val.key, this)}/>
									{/each}
								</g>

							</svg>
						</div>
						{/if}


						<!-- bbox and score line chart-->
						<!--<h4> bbox and score</h4>
						<div class = "chart" bind:clientWidth= {width} bind:clientHeight={height}>-->
							<!-- svelte-ignore component-name-lowercase -->
							<!--<svg class = "chart-svg">-->
								<!-- y axis-->
								<!--<g class = "axis y-axis">
									{#each line_score_yTicks as tick}
										<g class ='tick tick-{tick}' transform='translate(0, {line_score_yScale(tick)})'>

											<line x2 = "100%"></line>
											<text y='-4'>{tick}</text>
										</g>
									{/each}
								</g>-->

								<!-- x axis
								<g class = "axis x-axis">
									{#each line_bbox_xTicks as tick}
										<g class = "tick" transform ='translate({line_bbox_xScale(tick)},0)'>

											<line y1="100%"/>
											<text y='{height - padding.bottom + 16}'>{tick}</text>
										</g>
									{/each}
								</g>




							</svg>
						</div>-->

					{/if}
					</div>
			</div>
		</div>

		<div id="main-section" style="width: 1000px;">
			<div id="selected-image-view" class="view-panel">
				<div class="view-title">Image View
					<!--
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
					{/if}-->
				</div>
				<div id="selected-image-view-content">
					{#if show_default_images == true}
					<DefaultImageView/>
					{/if}

					{#if show_selected_images == true}
						<!-- svelte-ignore a11y-missing-attribute -->
						<div id ="images_view">
							{#each image_idx_src as img_src}
								<div class = "multiple_images" on:click={openModal} on:click={modal_value.get_instance_val(img_src, image_source_val[img_src], current_selected_class, current_selected_dtype)}>
									<!-- svelte-ignore a11y-missing-attribute -->
									<img class = "images" id="selected_image" src = {img_src} width = {setWidth} height={setHeight} >
									<!-- svelte-ignore component-name-lowercase -->
									<svg class = "gt_bboxes" id="image_box" width={setWidth} height={setHeight}>
										{#each Object.keys(image_source_val[img_src]['cl_dt_gt']) as gt_type}
											{#each Object.keys(image_source_val[img_src]['cl_dt_gt'][gt_type]) as gt_key}
												{x1 = image_source_val[img_src]['cl_dt_gt'][gt_type][gt_key]['x1']}
												{x2 = image_source_val[img_src]['cl_dt_gt'][gt_type][gt_key]['x2']}
												{y1 = image_source_val[img_src]['cl_dt_gt'][gt_type][gt_key]['y1']}
												{y2 = image_source_val[img_src]['cl_dt_gt'][gt_type][gt_key]['y2']}
												{boxWidth = (Math.abs(x2-x1)/imageWidth)*setWidth}
												{boxHeight = (Math.abs(y2-y1)/imageHeight)*setHeight}
												{X = (x1/imageWidth)*setWidth}
												{Y = (y1/imageHeight)*setHeight}
												{gt_cate_name = image_source_val[img_src]['cl_dt_gt_cate'][gt_type][gt_key]}
												<rect x={X} y={Y} width={boxWidth} height={boxHeight} fill="transparent" stroke={class_lists[gt_cate_name]['color']}/> <!--stroke={gt_types[gt_type]['color']}/>-->
												<g>
													<!--<rect x={X + 0.67 * boxWidth} y = {Y - boxHeight/5} width ={boxWidth/3} height ={boxHeight/5} stroke={class_lists[current_selected_class]['color']} fill={class_lists[current_selected_class]['color']}/>-->
													{#if (boxWidth / 3) > 6}
														<text x = {X + boxWidth - 12} y={Y- 2} font-size={6} fill={class_lists[gt_cate_name]['color']}>{image_source_val[img_src]['cl_dt_gt_cate'][gt_type][gt_key]}</text>
													{/if}
													{#if (boxWidth / 3) <= 6 && (boxWidth /3 ) > 4}
														<text x = {X + boxWidth - 8} y={Y- 2} font-size={4} fill={class_lists[gt_cate_name]['color']}>{image_source_val[img_src]['cl_dt_gt_cate'][gt_type][gt_key]}</text>
													{/if}
													{#if (boxWidth / 3) <= 4}
														<text x = {X + 0.67 * boxWidth} y={Y- 2} font-size={boxWidth / 3} fill={class_lists[gt_cate_name]['color']}>{image_source_val[img_src]['cl_dt_gt_cate'][gt_type][gt_key]}</text>
													{/if}
												</g>
												{/each}
										{/each}
									</svg>
									<!-- svelte-ignore component-name-lowercase -->
									<svg class = "bboxes" id="image_box" width={setWidth} height={setHeight}>
										{#each Object.keys(image_source_val[img_src]['cl_dt']) as sel_bbox}
											{x1 = image_source_val[img_src]['cl_dt'][sel_bbox]['x1']}
											{x2 = image_source_val[img_src]['cl_dt'][sel_bbox]['x2']}
											{y1 = image_source_val[img_src]['cl_dt'][sel_bbox]['y1']}
											{y2 = image_source_val[img_src]['cl_dt'][sel_bbox]['y2']}
											{boxWidth = (Math.abs(x2-x1)/imageWidth)*setWidth}
											{boxHeight = (Math.abs(y2-y1)/imageHeight)*setHeight}
											{X = (x1/imageWidth)*setWidth}
											{Y = (y1/imageHeight)*setHeight}
											{tooltip_val = "predicted class : " + image_source_val[img_src]['cl_dt_pred'][sel_bbox] + "\n truth class : " + image_source_val[img_src]['cl_dt_cate'][sel_bbox] + "\n detection score : " + image_source_val[img_src]['cl_dt_score'][sel_bbox]}
											<rect title={tooltip_val} use:tooltip x={X} y={Y} width={boxWidth} height={boxHeight} fill="transparent" stroke={class_lists[current_selected_class]['color']}/>
											<g>
												<!--<rect x={X + 0.67 * boxWidth} y = {Y - boxHeight/5} width ={boxWidth/3} height ={boxHeight/5} stroke={class_lists[current_selected_class]['color']} fill={class_lists[current_selected_class]['color']}/>-->
												{#if (boxWidth / 3) > 6}
													<text x = {X} y={Y- 2} font-size={6} fill={class_lists[current_selected_class]['color']}>{image_source_val[img_src]['cl_dt_pred'][sel_bbox]}</text>
												{/if}
												{#if (boxWidth / 3) <= 6 && (boxWidth /3 ) > 4}
												<text x = {X} y={Y- 2} font-size={4} fill={class_lists[current_selected_class]['color']}>{image_source_val[img_src]['cl_dt_pred'][sel_bbox]}</text>
												{/if}
												{#if (boxWidth / 3) <= 4}
												<text x = {X} y={Y- 2} font-size={boxWidth / 3} fill={class_lists[current_selected_class]['color']}>{image_source_val[img_src]['cl_dt_pred'][sel_bbox]}</text>
												{/if}
											</g>
											{/each}
									</svg>
								</div>
								<Modal isOpenModal={isOpenModal} on:closeModal={closeModal} bind:this={modal_value}/>
							{/each}
						</div>

					{/if}

					{#if show_chart_images == true}
						<!-- svelte-ignore a11y-missing-attribute -->
						<div id ="images_view">
							{#each chart_img_idx_src as img_src}
								<div class = "multiple_images" on:click={openModal} on:click={modal_value.get_instance_val(img_src, chart_img_source_val[img_src], current_selected_class, current_selected_dtype)}>
									<!-- svelte-ignore a11y-missing-attribute -->
									<img class = "images" id="selected_image" src = {img_src} width = {setWidth} height={setHeight} on:click={image_detail(img_src)}>
									<!-- svelte-ignore component-name-lowercase -->
									<svg class = "gt_bboxes" id="image_box" width={setWidth} height={setHeight}>
										{#each Object.keys(chart_img_source_val[img_src]['cl_dt_gt']) as gt_type}
											{#each Object.keys(chart_img_source_val[img_src]['cl_dt_gt'][gt_type]) as gt_key}
												{x1 = chart_img_source_val[img_src]['cl_dt_gt'][gt_type][gt_key]['x1']}
												{x2 = chart_img_source_val[img_src]['cl_dt_gt'][gt_type][gt_key]['x2']}
												{y1 = chart_img_source_val[img_src]['cl_dt_gt'][gt_type][gt_key]['y1']}
												{y2 = chart_img_source_val[img_src]['cl_dt_gt'][gt_type][gt_key]['y2']}
												{boxWidth = (Math.abs(x2-x1)/imageWidth)*setWidth}
												{boxHeight = (Math.abs(y2-y1)/imageHeight)*setHeight}
												{X = (x1/imageWidth)*setWidth}
												{Y = (y1/imageHeight)*setHeight}
												{gt_cate_name = chart_img_source_val[img_src]['cl_dt_gt_cate'][gt_type][gt_key]}
												<rect x={X} y={Y} width={boxWidth} height={boxHeight} fill= "transparent" stroke={class_lists[gt_cate_name]['color']}/>
												<g>
													<!--<rect x={X + 0.67 * boxWidth} y = {Y - boxHeight/5} width ={boxWidth/3} height ={boxHeight/5} stroke={class_lists[current_selected_class]['color']} fill={class_lists[current_selected_class]['color']}/>-->
													{#if (boxWidth / 3) > 6}
														<text x = {X + boxWidth - 12} y={Y- 2} font-size={6} fill={class_lists[gt_cate_name]['color']}>{chart_img_source_val[img_src]['cl_dt_gt_cate'][gt_type][gt_key]}</text>
													{/if}
													{#if (boxWidth / 3) <= 6 && (boxWidth /3 ) > 4}
														<text x = {X + boxWidth - 8} y={Y- 2} font-size={4} fill={class_lists[gt_cate_name]['color']}>{chart_img_source_val[img_src]['cl_dt_gt_cate'][gt_type][gt_key]}</text>
													{/if}
													{#if (boxWidth / 3) <= 4}
														<text x = {X + 0.67 * boxWidth} y={Y- 2} font-size={boxWidth / 3} fill={class_lists[gt_cate_name]['color']}>{chart_img_source_val[img_src]['cl_dt_gt_cate'][gt_type][gt_key]}</text>
													{/if}
												</g>
											{/each}
										{/each}
									</svg>



									<!-- svelte-ignore component-name-lowercase -->
									<svg class = "bboxes" id="image_box" width={setWidth} height={setHeight}>
										{#each Object.keys(chart_img_source_val[img_src]['cl_dt']) as sel_bbox}
											{x1 = chart_img_source_val[img_src]['cl_dt'][sel_bbox]['x1']}
											{x2 = chart_img_source_val[img_src]['cl_dt'][sel_bbox]['x2']}
											{y1 = chart_img_source_val[img_src]['cl_dt'][sel_bbox]['y1']}
											{y2 = chart_img_source_val[img_src]['cl_dt'][sel_bbox]['y2']}
											{boxWidth = (Math.abs(x2-x1)/imageWidth)*setWidth}
											{boxHeight = (Math.abs(y2-y1)/imageHeight)*setHeight}
											{X = (x1/imageWidth)*setWidth}
											{Y = (y1/imageHeight)*setHeight}
											{tooltip_val = "predicted class : " + chart_img_source_val[img_src]['cl_dt_pred'][sel_bbox] + "\n truth class : " + chart_img_source_val[img_src]['cl_dt_cate'][sel_bbox] + "\n detection score : " + chart_img_source_val[img_src]['cl_dt_score'][sel_bbox]}
											<rect title={tooltip_val} use:tooltip x={X} y={Y} width={boxWidth} height={boxHeight} fill="transparent" stroke={class_lists[current_selected_class]['color']}/>
											<g>
												<!--<rect x={X + 0.67 * boxWidth} y = {Y - boxHeight/5} width ={boxWidth/3} height ={boxHeight/5} stroke={class_lists[current_selected_class]['color']} fill={class_lists[current_selected_class]['color']}/>-->
												{#if (boxWidth / 3) > 6}
													<text x = {X} y={Y- 2} font-size={6} fill={class_lists[current_selected_class]['color']}>{chart_img_source_val[img_src]['cl_dt_pred'][sel_bbox]}</text>
												{/if}
												{#if (boxWidth / 3) <= 6 && (boxWidth /3 ) > 4}
												<text x = {X} y={Y- 2} font-size={4} fill={class_lists[current_selected_class]['color']}>{chart_img_source_val[img_src]['cl_dt_pred'][sel_bbox]}</text>
												{/if}
												{#if (boxWidth / 3) <= 4}
												<text x = {X} y={Y- 2} font-size={boxWidth / 3} fill={class_lists[current_selected_class]['color']}>{chart_img_source_val[img_src]['cl_dt_pred'][sel_bbox]}</text>
												{/if}
											</g>
										{/each}
									</svg>
								</div>
								<Modal isOpenModal={isOpenModal} on:closeModal={closeModal} bind:this={modal_value}/>
							{/each}
						</div>
					{/if}

					{#if show_gt_images == true}
						<div id = "images_view">
							{#each gt_image_idx_src as img_src}
								<div class = "multiple_images">
									<img class = "images" id="selected_image" alt="" src = {img_src} width = {setWidth} height={setHeight} >
									<!-- svelte-ignore component-name-lowercase -->
									<svg class = "bboxes" id = "image_box" width={setWidth} height={setHeight}>
										{#each Object.keys(gt_image_source_val[img_src]['cl_gt']) as sel_bbox}
											{x1 = gt_image_source_val[img_src]['cl_gt'][sel_bbox]['x1']}
											{x2 = gt_image_source_val[img_src]['cl_gt'][sel_bbox]['x2']}
											{y1 = gt_image_source_val[img_src]['cl_gt'][sel_bbox]['y1']}
											{y2 = gt_image_source_val[img_src]['cl_gt'][sel_bbox]['y2']}
											{boxWidth = (Math.abs(x2-x1)/imageWidth)*setWidth}
											{boxHeight = (Math.abs(y2-y1)/imageHeight)*setHeight}
											{X = (x1/imageWidth)*setWidth}
											{Y = (y1/imageHeight)*setHeight}
											<rect x={X} y={Y} width={boxWidth} height={boxHeight} fill="transparent" stroke={class_lists[current_selected_class]['color']}/>
										{/each}
									</svg>
								</div>
							{/each}
						</div>
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
		margin-bottom: 10px;
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
	table, td ,th{
		border: 0.5px solid;
		border-collapse: collapse;
		margin-bottom: 2px;
	}

	th.rotate{
		height: 125px;
		white-space: nowrap;
		padding: 0 !important;
	}

	th.rotate > div {
		transform:
			translate(-1px, 45px)
			rotate(270deg);
		width: 30px;
	}

	th.rotate > div > span{
		border-bottom: 1px solid #e2e2e2;
		font-size: 13px;
	}


	.summary-table td:hover{
		font-weight: bold;
	}

	.summary-table {
		border: 1px solid #17202A;
		width: 100%;

		border-collapse: collapse;
	}
	.summary-table td summary-table th {
		border: 1px solid #808B96;
		padding: 4px 2px;
		text-align: center;
	}
	.summary-table tbody td {
		font-size: 10px;
		text-align: left;
	}

	.summary-table thead {
		background: #F5F4F4;
	}
	.summary-table thead th {
		font-size: 10px;
		text-align: center;
	}
	.summary-table thead th:first-child {
		border-left: none;
		text-align: center;
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
    stroke-width: 1px;
  }
	.multiple_images .gt_bboxes{
    position: absolute;
    top: 0;
    stroke-width: 1.5px;
    stroke-dasharray: 5,5;
  }

	h4{
    text-align: center;
    margin-top: 0;
    margin-bottom: 2px;
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