<script>
  import{
    Listbox, ListboxButton, ListboxOptions, ListboxOption,
    }from "@rgossiaux/svelte-headlessui";
  import Table from './Table.svelte';


  export const bdd_class = [
    {'id': 1, 'name': 'other vehicle'},
    {'id': 2, 'name': 'pedestrian'},
    {'id': 3, 'name': 'traffic light'},
    {'id': 4, 'name': 'traffic sign'},
    {'id': 5, 'name': 'truck'},
    {'id': 6, 'name': 'train'},
    {'id': 7, 'name': 'other person'},
    {'id': 8, 'name': 'bus'},
    {'id': 9, 'name': 'car'},
    {'id': 10, 'name': 'rider'},
    {'id': 11, 'name': 'motorcycle'},
    {'id': 12, 'name': 'bicycle'},
    {'id': 13, 'name': 'trailer'}];


  let table_heads = [];
  let detect_types = [];
  let detect_nums = [];
  let table_vals = [];
  export function get_class_detection_summary(class_name){
    console.log("selected class name : ", class_name)
		fetch('/class_detection_types/').then(res =>res.json()).then(data =>{
      let data_val = data[class_name]
      data_val = data_val
      table_heads = ['detection type', 'num'];
      table_heads = table_heads
      detect_types = Object.keys(data_val)
      detect_nums = Object.values(data_val)
      table_vals = []
      for (var i = 0; i < detect_nums.length; i++){
        var rows = []
        rows.push(detect_types[i])
        rows.push(detect_nums[i])

        table_vals.push(rows)
      }
      table_vals = table_vals
      console.log("table values:::: ", table_vals)
		})
	}
</script>

<Table table_heads = {table_heads} table_vals = {table_vals} style = "blueTable"/>
<!--
<div id = "main">
  <div id = "left">
    <Listbox value = {selected} on:change = {(e) => (selected = e.detail)} on:change = {get_class_detection_summary(selected.name)}>
      <ListboxButton>{selected.name}</ListboxButton>
      <ListboxOptions>
        {#each bdd_class as cl (cl.id)}
          <ListboxOption value = {cl}>
            {cl.name}
          </ListboxOption>
        {/each}
      </ListboxOptions>
    </Listbox>
  </div>
  <div id = "right">


  </div>
</div>
<style>
  #main{
    display: flex;
  }
  #left{
    width: 150px;
  }
  #right{
    width: 500px;
  }
</style>

-->
