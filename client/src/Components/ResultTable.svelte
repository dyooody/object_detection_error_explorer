<script>
  import Table from './Table.svelte';
  import { onMount } from "svelte";

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

</script>

<Table table_heads = {table_heads} table_vals = {table_vals} style = "greyTable"/>