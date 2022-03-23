<script>
  import{
    Tab, TabGroup, TabList, TabPanel, TabPanels
  }from "@rgossiaux/svelte-headlessui";
  import Table from './Table.svelte';
  import Listboxes from "./Listbox.svelte";

  let redStyle = "redTable";
	let blueStyle = "blueTable";

	let class_list = [];
	let ap = [];
	let result_array = [];
	let nums = [];
	let table_heads = [];
	let table_vals = [];
	let detail = "";
		function get_class_labels_summary(){
		fetch('/class_values/').then(res => res.json()).then(overall =>{
			console.log("overall class values:::: ",overall)
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
			console.log("ap:::: ", ap)
			console.log("nums :::: ", nums)

			table_vals = []
			for(var i = 0; i < class_list.length; i++){
			var row = []
			row.push(class_list[i])
			row.push(ap[i])
			row.push(nums[i])

			table_vals.push(row)
			}
			console.log("table_vals :::::", table_vals)
			table_vals = table_vals
		})
	}

	//let detection_heads = []
	let detect_types = []
	let detect_types_names = []
	let detect_types_vals = []
	let detection_results = []
	let detection_heads = []
	function get_detection_type_summary(){
		fetch('/detection_types/').then(res =>res.json()).then(summary =>{
			console.log("detection summary values:::: ", summary)
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
			console.log("detection table values :::: ", detection_results)
			detection_results = detection_results
		})
	}
</script>

<TabGroup>
  <TabList>
    <Tab on:click = {get_class_labels_summary}>Class summary</Tab>
    <Tab on:click = {get_detection_type_summary}>Detection Type summary</Tab>
    <Tab>Class-detection summary</Tab>
  </TabList>
  <TabPanels>
    <TabPanel><Table table_heads = {table_heads} table_vals = {table_vals} style = {blueStyle} detail = {detail}/></TabPanel>
    <TabPanel><Table table_heads = {detection_heads} table_vals = {detection_results} style = {redStyle}/></TabPanel>
    <TabPanel><Listboxes/></TabPanel>
  </TabPanels>
</TabGroup>