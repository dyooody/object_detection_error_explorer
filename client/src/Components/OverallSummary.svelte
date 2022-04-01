<script>
  import{
    Tab, TabGroup, TabList, TabPanel, TabPanels
  }from "@rgossiaux/svelte-headlessui";
  import Table from './Table.svelte';
  import DetailedSummary from "./DetailedSummary.svelte";
  //import I from "@rgossiaux/svelte-headlessui/internal/elements/I.svelte";

  let redStyle = "redTable";
	let blueStyle = "blueTable";

	export let class_summary_display = false;
	export let detection_summary_display = false;
	export let cl_det_summary_display = false;
	export let instance_display = false;
	export let images_display = false;
	export let class_detail_display = false;
	export let detection_detail_display = false;

	let class_list = [];
	let ap = [];
	let result_array = [];
	let nums = [];
	let table_heads = [];
	let table_vals = [];
	let detail = "";
	export let class_tab_click = {clicked : false};
	export function get_class_labels_summary(){
		class_detail_display = false;
		class_summary_display = true;
		detection_tab_click.clicked = false;
		instance_level_click.clicked = false;
		class_tab_click.clicked = !class_tab_click.clicked;
		console.log("class_summary_display :: ", class_summary_display);
		fetch('/class_values/').then(res => res.json()).then(overall =>{
			result_array = overall
			class_list = Object.keys(result_array)
			class_list = class_list
			// detail -> click -> more detail result tables (use if/else statement)
			// https://svelte.dev/tutorial/svelte-window
			table_heads = ['class name', 'average precision', 'number']
			table_heads = table_heads
			detail = "True"
			detail = detail
			for(var i = 0; i <Object.keys(result_array).length; i++){
				nums.push(result_array[class_list[i]]['num'])
				nums = nums
				ap.push(result_array[class_list[i]]['ap'])
				ap = ap
			}

			table_vals = []
			for(var i = 0; i < class_list.length; i++){
			var row = []
			row.push(class_list[i])
			row.push(ap[i])
			row.push(nums[i])

			table_vals.push(row)
			}
			table_vals = table_vals
		})
	}

	//let detection_heads = []
	let detect_types = []
	let detect_types_names = []
	let detect_types_vals = []
	let detection_results = []
	let detection_heads = []
	export let detection_tab_click = {clicked:false};
	export function get_detection_type_summary(){
		detection_summary_display = true;
		detection_detail_display = false;
		class_tab_click.clicked = false;
		instance_level_click.clicked = false;
		detection_tab_click.clicked = !detection_tab_click.clicked;
		console.log("detection_summary_display :: ", detection_summary_display);
		fetch('/detection_types/').then(res =>res.json()).then(summary =>{
			detection_heads = ['type', 'type name', 'number']
			detection_heads = detection_heads
			detect_types = Object.keys(summary)
			detect_types = detect_types
			for (var i =0; i < detect_types.length; i++){
				detect_types_names.push(summary[detect_types[i]]['type'])
				detect_types_names = detect_types_names
				detect_types_vals.push(summary[detect_types[i]]['num'])
				detect_types_vals = detect_types_vals
			}

			detection_results = []
			for (var i =0; i < detect_types.length; i++){
				var row = []
				row.push(detect_types[i])
				row.push(detect_types_names[i])
				row.push(detect_types_vals[i])

				detection_results.push(row)
			}
			detection_results = detection_results
		})
	}

	export function get_class_type_summary(){
		cl_det_summary_display = !cl_det_summary_display;
		console.log("cl_det_summary_display :: ", cl_det_summary_display);
	}

	export let instance_level_click = {clicked: false};
	export function get_instance_level(){
		instance_level_click.clicked = !instance_level_click.clicked;
		instance_display = !instance_display;
		class_tab_click.clicked = false;
		detection_tab_click.clicked = false;
		console.log("instance_display :: ", instance_display);
		console.log("instance_level_click::::", instance_level_click.clicked);
	}

	export let condition_images_click = {clicked: false};
	export function get_group_image_level(){
		condition_images_click.clicked = !condition_images_click.clicked;
		images_display = !images_display;
	}

	let class_detail_table_heads = [];
  let class_detail_detect_types = [];
  let class_detail_detect_nums = [];
  let class_detail_table_vals = [];
  export function get_class_detection_summary(class_name){
		class_detail_display = true;
		class_summary_display = false;
    console.log("selected class name : ", class_name)
		fetch('/class_detection_types/').then(res =>res.json()).then(data =>{
      let data_val = data[class_name]
      data_val = data_val
      class_detail_table_heads = ['detection type', 'num'];
      class_detail_table_heads = class_detail_table_heads
      class_detail_detect_types = Object.keys(data_val)
      class_detail_detect_nums = Object.values(data_val)
      class_detail_table_vals = []
      for (var i = 0; i < class_detail_detect_nums.length; i++){
        var rows = []
        rows.push(class_detail_detect_types[i])
        rows.push(class_detail_detect_nums[i])

        class_detail_table_vals.push(rows)
      }
      class_detail_table_vals = class_detail_table_vals
      console.log("table values:::: ", class_detail_table_vals)
		})
	}

	function back_to_main(){
		console.log("back_to_main");
		class_summary_display = true;
		console.log(class_summary_display);
		class_detail_display = false;
		console.log(class_detail_display);
		detection_summary_display = true;
		console.log(detection_summary_display);
		detection_detail_display = false;
		console.log(detection_detail_display);
	}
</script>

<TabGroup>
  <TabList>
    <Tab on:click = {get_class_labels_summary}>Class summary</Tab>
    <Tab on:click = {get_detection_type_summary}>Detection Type summary</Tab>
		<Tab on:click = {get_instance_level}>Instance level summary</Tab>
		<Tab on:click = {get_group_image_level}>Images with Conditions</Tab>
  </TabList>
  <TabPanels>
    <TabPanel>
			{#if class_tab_click.clicked == true}
			{#if class_summary_display == true}
				<Table table_heads = {table_heads} table_vals = {table_vals} style = "greyTable" detail = {detail}/>
    	{/if}
			{#if class_detail_display == true}
				<button on:click={back_to_main}>back to main</button>
				<Table table_heads = {class_detail_table_heads} table_vals = {class_detail_table_vals} style = "greyTable"/>
			{/if}
			{/if}
		</TabPanel>
		<TabPanel>
			{#if detection_tab_click.clicked == true}
			{#if detection_summary_display == true}
				<Table table_heads = {detection_heads} table_vals = {detection_results} style = "greyTable"/>
    	{/if}
			{/if}
		</TabPanel>
		<!--
		<TabPanel>
			{#if cl_det_summary_display == true}
			<DetailedSummary/>
			{/if}
		</TabPanel>-->
		<TabPanel>
			{#if instance_display == true}
				Instance level
			{/if}
		</TabPanel>
		<TabPanel>
			{#if images_display == true}
				Images level display
			{/if}
		</TabPanel>
  </TabPanels>
</TabGroup>