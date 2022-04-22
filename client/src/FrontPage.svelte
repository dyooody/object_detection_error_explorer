<script>
	import { dataset_dev, each } from "svelte/internal";
	import { onMount } from 'svelte';
	import Table from './Components/Table.svelte';
	import DetailedSummary from './Components/DetailedSummary.svelte';
	import OverallSummary from './Components/OverallSummary.svelte';
	import TypeDesc from './Components/TypeDesc.svelte';
	import ImageDisplayPanel from "./Components/ImageDisplayPanel.svelte";
	import { Disclosure, DisclosureButton, DisclosurePanel } from "@rgossiaux/svelte-headlessui"
	import{ Listbox, ListboxButton, ListboxOptions, ListboxOption }from "@rgossiaux/svelte-headlessui";

	let img_path_valid = false;
	let img_list_show = false;
	let image_panel = {};
	let class_tab_click = {};
	let detection_tab_click = {};
	let show_class_bbox = true;
	let instance_level_click = {};
	let class_summary_display = false;
	let detection_summary_display = false;
	let cl_det_summary_display = false;
	let instance_display = false;
	let images_display = false;

	function reset_everything(){
		img_path_valid = false;
		img_list_show = false;
		image_panel.clicked = false;
		class_tab_click.clicked = false;
		detection_tab_click.clicked = false;
		instance_level_click.clicked = false;
		show_class_bbox = false;
		class_summary_display = false;
		detection_summary_display = false;
		cl_det_summary_display = false;
		instance_display = false;
		images_display = false;
	}

	let selected_image_id = 1;
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
		"train":{checked: false, color:"#F4ECF7"}
	};
	let selected = Object.keys(class_lists)[0];
	console.log("selected::: ", selected);

	let detected_types = {
		"1":{name:"correctly classified", checked: false, color: "#884EA0"},
		"2":{name:"classification error", checked: false, color: "#A93226 "},
		"3":{name:"localization error", checked: false, color: "#2E86C1"},
		"4":{name:"cls + loc error", checked: false, color:"#2ECC71"},
		"5":{name:"duplicate error", checked: false, color: "#F1C40F"},
		"6":{name:"background error", checked: false, color:"#F7F9F9"},
		"7":{name:"missed GT error", checked: false, color:"#FEF5E7"},
		"8":{name:"incorrectly classified", checked: false, color:"#F4ECF7"},
	};

	let img_path = "";
	let class_bbox = [];
	let detect_type_bbox = [];
	let cl_key = [];
	let dt_key = [];
	let actualWidth = 1280, actualHeight=720, givenWidth= 700, givenHeight=500;
	let smallImgWidth = 500, smallImageHeight = 350;
	let x1,x2,y1,y2,boxHeight, boxWidth, box_area, X, Y;

	function get_file_bbox_vals(selected_image_id){
		//console.log("get_file_bbox_vals:: ", selected_image_id);
		fetch('/get_file_bbox_vals/'+selected_image_id).then(res =>res.json()).then(data=>{

			dt_key = Object.keys(data['bbox_dtype']);
			dt_key = dt_key;
			cl_key = Object.keys(data['bbox_cate']);
			cl_key = cl_key;
			img_path = data['image_dir'];
			img_path = img_path;
			for (var i=0; i<Object.keys(data['bbox_cate']).length; i++){
				var cl_name = Object.keys(data['bbox_cate'])[i];
				class_bbox[cl_name] = data['bbox_cate'][cl_name];
			}
			for (var j=0; j<Object.keys(data['bbox_dtype']).length; j++){
				var dt_name = Object.keys(data['bbox_dtype'])[j];
				detect_type_bbox[dt_name] = data['bbox_dtype'][dt_name];
			}
			class_bbox = class_bbox;
			detect_type_bbox = detect_type_bbox;
		});
		return;
	}

	function image_id_submit(event){
		selected_image_id = event.target[0].value;
		selected_image_id = selected_image_id;
		img_path_valid = true;
		img_list_show = false;
		get_file_bbox_vals(selected_image_id)
	}


	let image_source_val = [];
	let img_idx_list = [];
	let image_idx_src = [];
	function get_image_src_bbox(image_idx_lists){
		img_idx_list = image_idx_lists;
		img_idx_list = img_idx_list;
		image_idx_src = [];
		image_source_val = [];
		img_list_show = true;
		img_path_valid = false;
		for (var i=0; i<image_idx_lists.length; i++){
			let class_bbox = [];
			let detect_type_bbox = [];
			let cl_key = [];
			let dt_key = [];
			fetch('/get_file_bbox_vals/'+image_idx_lists[i]).then(res=>res.json()).then(data =>{
				dt_key = Object.keys(data['bbox_dtype']);
				dt_key = dt_key;
				cl_key = Object.keys(data['bbox_cate']);
				cl_key = cl_key;
				img_path = data['image_dir'];
				img_path = img_path;
				image_idx_src.push(data['image_dir']);
				image_idx_src = image_idx_src;
				for (var i=0; i<Object.keys(data['bbox_cate']).length; i++){
					var cl_name = Object.keys(data['bbox_cate'])[i];
					class_bbox[cl_name] = data['bbox_cate'][cl_name];
				}
				for (var j=0; j<Object.keys(data['bbox_dtype']).length; j++){
					var dt_name = Object.keys(data['bbox_dtype'])[j];
					detect_type_bbox[dt_name] = data['bbox_dtype'][dt_name];
				}
				class_bbox = class_bbox;
				detect_type_bbox = detect_type_bbox;
				image_source_val[img_path] = [];
				image_source_val[img_path] = class_bbox;
				//image_source_val[img_path]['dt_bbox'] = detect_type_bbox;
				image_source_val = image_source_val;
			});
		}
		console.log("image_source_val :::: ", image_source_val);
		console.log("image_idx_src ::: ", image_idx_src);
	}

	function control_panel_values(event){
		const formData = new FormData(event.target);
		const data = {};
		for (let field of formData){
			const[key, value] = field;
			data[key] = value;
		}
		console.log("data :::::::::::::", data);
		let values = Object.values(data);
		console.log("values::: ", values);
		fetch('/images_with_conditions/'+values).then(res=>res.json()).then(result=>{
			console.log("result ::: ", result);
			console.log("calling the function get_file_bbox_vals");
			get_image_src_bbox(result);
			console.log("img_list_show ::: ", img_list_show);
		});
	}

	//click to change true and false
	function class_button_clicked(class_val){
		class_lists[class_val]['checked'] = !class_lists[class_val]['checked'];
	}

	function dtype_button_clicked(dtype_val){
		detected_types[dtype_val]['checked'] = !detected_types[dtype_val]['checked'];
	}

	function class_or_dtype(){
		show_class_bbox = !show_class_bbox;
	}

	function reset_images(){
		img_path_valid = false;
		img_list_show = false;
	}

	let detailed_value;

</script>

<div id="top-bar">
	<div id="title">
		Object Detection Results
	</div>
</div>

<div id="main">
	<div id ="left-side">
		<button on:click = {reset_everything}>RESET SETTING</button>
		{#if class_tab_click.clicked}
			<p>List of Class</p>
			<p>Click for detailed summary</p>
			<Listbox value={selected} on:change={(e)=>(selected = e.detail)} on:change ={detailed_value.get_class_detection_summary(selected)}>
				<ListboxButton>{selected}</ListboxButton>
				<ListboxOptions>
					{#each Object.keys(class_lists) as cl_name}
					<ListboxOption value = {cl_name}>
						{cl_name}
					</ListboxOption>
					{/each}
				</ListboxOptions>
			</Listbox>
		{/if}
		{#if detection_tab_click.clicked}
		<TypeDesc/>
		{/if}
		{#if instance_level_click.clicked}
		<Disclosure>
			<DisclosureButton>Individual Image</DisclosureButton>
			<DisclosurePanel>
				<form on:submit|preventDefault={image_id_submit}>
					<label for="image_id">Image ID</label>
					<input type="number" id="image_id" name="image_id" value="input_image_id"><br>
					<input type="submit" value="submit">
					<input on:click={reset_images} type="reset">
				</form>
			</DisclosurePanel>
		</Disclosure>
		<Disclosure>
			<DisclosureButton>Image Display Panel</DisclosureButton>
			<DisclosurePanel>
				<p>Image Panel</p>
				<form on:submit|preventDefault = {control_panel_values}>
					<label for="number of labels">Number of Labels</label>
					<input type="number" id="panel_input" name="labels" value=30><br>
					<label for="number of classes">Number of Classes</label>
					<input type="number" id="panel_input" name="classes" value=4><br>
					<label for="overall mAP">mAP score</label>
					<input type="text" id="panel_input" name="mAP" value="0.3"><br>
					<label for="number of images">Number of Images</label>
					<input type="number" id="panel_input" name="numbers" value=10><br>
					<input type="submit" value="submit">
					<input on:click={reset_images} type="reset">
				</form>
			</DisclosurePanel>
		</Disclosure>
		{/if}

	</div>

	<div id = "right-side">

		<OverallSummary bind:instance_level_click bind:detection_tab_click bind:class_tab_click
		bind:class_summary_display bind:detection_summary_display bind:cl_det_summary_display
		bind:instance_display bind:images_display bind:this={detailed_value}/>
		<ImageDisplayPanel bind:image_panel/>
		<!-- svelte-ignore a11y-missing-attribute -->
		<!-- Images with condition -->
		<div id = "images_view">
		{#if img_list_show == true}
		<div id="image_left">
			{#each image_idx_src as img_src}
			<div class="multiple_images" width ={smallImgWidth} height={smallImageHeight}>
			<img class='images' id='selected_image' src ={img_src} width ={smallImgWidth} height={smallImageHeight}>
				<svg class = "bboxes" id ="image_box" width ={smallImgWidth} height={smallImageHeight}>
					{#each Object.keys(image_source_val[img_src]) as cl_name}
						{#each Object.keys(image_source_val[img_src][cl_name]) as cl_key}
							{x1 = image_source_val[img_src][cl_name][cl_key]['x1']}
							{x2 = image_source_val[img_src][cl_name][cl_key]['x2']}
							{y1 = image_source_val[img_src][cl_name][cl_key]['y1']}
							{y2 = image_source_val[img_src][cl_name][cl_key]['y2']}
							{boxWidth = (Math.abs(x2-x1)/actualWidth)*smallImgWidth}
							{boxHeight = (Math.abs(y2-y1)/actualHeight)*smallImageHeight}
							{X = (x1/actualWidth)*smallImgWidth}
							{Y = (y1/actualHeight)*smallImageHeight}
							<rect x={X} y={Y} width={boxWidth} height ={boxHeight} stroke={class_lists[cl_name]['color']}/>
						{/each}
					{/each}
				</svg>
			</div>
		{/each}
	</div>
	<div class="images_summary" id="summary_right">
			{#each image_idx_src as img_src}
			<div class="each_summary" width ={smallImgWidth} height={smallImageHeight}>
				<p>{img_src}</p>
				<rect width={smallImgWidth} height={smallImageHeight}/>
			</div>
			{/each}
	</div>
	{/if} <!--img_list_show == true-->
	</div>

		<!-- showing one image-->
		<!-- svelte-ignore a11y-missing-attribute -->
		{#if img_path_valid == true}
		<button on:click={class_or_dtype}>class or dtype</button>
		{#if show_class_bbox}
		{#each cl_key as cl}
			<button on:click={class_button_clicked(cl)}>{cl}</button>
		{/each}
		<div class = "show_image" width = {givenWidth} height = {givenHeight}>
			<img class = "images" id = "selected_image" src={img_path} width = {givenWidth} height= {givenHeight}>
				<svg class = "bboxes" id = "image_box" width={givenWidth} height={givenHeight}>
				{#each cl_key as cl}
					{#if class_lists[cl]['checked'] == true}
						{#each class_bbox[cl] as cl_bbox}
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
		</div>
		{/if}
			<!-- detection type clicks-->
		{#if show_class_bbox == false}
		{#each dt_key as dt}
		<button on:click={dtype_button_clicked(dt)}>{dt}</button>
		{/each}
			<div class = "show_image" width = {givenWidth} height = {givenHeight}>
			<img class = "images" id = "selected_image" src={img_path} width = {givenWidth} height= {givenHeight}>
				<svg class = "bboxes" id = "image_box" width={givenWidth} height={givenHeight}>
				{#each dt_key as dt}
					{#if detected_types[dt]['checked'] == true}
						{#each detect_type_bbox[dt] as dt_bbox}
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
			</div>
		{/if}
		{/if} <!--image path valid-->
	</div>
</div>
<style>
	#main{
		display:flex;
	}
	#title {
		color: white;
		font-size: 20px;
		font-weight: 600;
		margin-left: 20px;
		margin-top: -4px;
		display: none;
	}
	#left-side {
		width: 300px;
		/*--width: 400px;
		width: var(--width);
		max-width: var(--width);
		min-width: var(--width);*/
	}
	#right-side{
		width: 900px;
	}
	#images_view{
		display: flex;
	}
	#image_left{
		width: 500px;
	}
	#summary_right{
		width:400px;
	}

	.show_image{
		display: flex;
    /*width: calc(var(--givenWidth) * 1px);
    height: calc(var(--givenHeight) * 1px);*/
	}
	.show_image .images{
		position: absolute;
    /*width: calc(var(--givenWidth) * 1px);
    height: calc(var(--givenHeight) * 1px);*/
	}
	.show_image .bboxes{
		position: absolute;
    /*stroke: var(--matchedBoxColor);
		width: calc(var(--givenWidth) * 1px);
    height: calc(var(--givenHeight) * 1px);*/
    stroke-width: 3px;
    fill: none;
	}
	.multiple_images{
		width: 60%;
		padding-top:10px;
	}
	.multiple_images .images{
		position: absolute;
	}
	.multiple_images .bboxes{
		position: relative;
		stroke-width: 3px;
		fill: none;
	}
	.each_summary{
		padding-left: 10px;

		height: var(smallImageHeight);
	}

	/*@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}*/
</style>