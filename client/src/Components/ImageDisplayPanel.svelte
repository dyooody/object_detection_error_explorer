<script>
	let image_idx_lists = [2,3,4,5,6,144];
	let image_idx_src = [];
	let img_lists_show = false;
  function get_file_bbox_vals(){
		image_idx_src = [];
		img_lists_show = !img_lists_show;
		console.log("get file bbox vals:::: ", img_lists_show);
		console.log("image_index_lists are:::: ", image_idx_lists);
		for (var i=0; i<image_idx_lists.length; i++){
			fetch('/get_image_src/'+image_idx_lists[i]).then(res=>res.json()).then(src=>{
				image_idx_src.push(src);
				image_idx_src = image_idx_src;
			});
		};
		console.log("image_idx_src::: ", image_idx_src);
  }

	export let image_panel = {clicked: false};
	export function image_panel_clicked(){
		image_panel.clicked = !image_panel.clicked;
		console.log("image panel click:::", image_panel.clicked);
	}

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

	let detected_types = {
		"1":{name:"correctly classified", checked: false, color: "#884EA0"},
		"2":{name:"classification error", checked: false, color: "#A93226 "},
		"3":{name:"localization error", checked: false, color: "#2E86C1"},
		"4":{name:"cls + loc error", checked: false, color:"#2ECC71"},
		"5":{name:"duplicate error", checked: false, color: "#F1C40F"},
		"6":{name:"background error", checked: false, color:"#F7F9F9"},
		"7":{name:"missed GT error", checked: false, color:"#FEF5E7"},
		"8":{name:"incorrectly classified", checked: false, color:"#F4ECF7"}
	};

</script>

<!--<button on:click={image_panel_clicked}>click!</button><br>
<button on:click={get_file_bbox_vals}>click for images</button><br>-->

<!--Image control panel
1) add class names and click = show bounding boxes of clicked images
2) detected labels and ground truth labels = clicked: bounding boxes of each labels
3) -->

{#if img_lists_show == true}
{#each image_idx_src as idx_scr}
	<!-- svelte-ignore a11y-missing-attribute -->
	<img class="images" id ="selected_image" src ={idx_scr} width = 500 height=350>
{/each}
{/if}
