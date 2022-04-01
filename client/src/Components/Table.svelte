<script>
	export let style;
  export let table_heads;
  export let table_vals;
	//export let detail = "False";

	//console.log("detail ::: ", detail)

	function class_details_result(selected_class){
		console.log("selected_class :::: ", selected_class);
		fetch('/detailed_class_info/${selected_class}').then(res=>res.json()).then(data=>{
			console.log("class_detail_result:::: ", data);
		})
	}
</script>

<div id="table_size">
	<table class={style}>
		<thead>
			<tr>
				{#each table_heads as head}
					<th>{head}</th>
				{/each}
				<!--{#if detail == "True"}
					<th>details</th>
				{/if}-->
			<tr/>
		</thead>
		<tbody>
			{#each table_vals as rows}
				<tr>
					{#each rows as cell}
						<td on:click={class_details_result(cell)}>{cell}</td>
					{/each}
					<!--{#if detail == "True"}
						<td><button on:click={class_details_result(rows[0])}>more detail</button></td>
					{/if}-->


				</tr>
			{/each}
		</tbody>
	</table>
</div>

<style>
	#table_size{
		width: 700px;
	}
	table, th, td {
		border: 1px solid;
		border-collapse: collapse;
		margin-bottom: 10px;
	}

	table.greyTable {
		border: 2px solid #17202A;
		background-color: #ECEFF1;
		width: 100%;
		text-align: center;
		border-collapse: collapse;
	}
	table.greyTable td, table.greyTable th {
		border: 2px solid #808B96;
		padding: 5px 3px;
	}
	table.greyTable tbody td {
		font-size: 15px;
	}
	table.greyTable tr:nth-child(even) {
		background: #CCD1D1;
	}
	table.greyTable thead {
		background: #707B7C;
	}
	table.greyTable thead th {
		font-size: 18px;
		font-weight: bold;
		color: #FFFFFF;
		text-align: center;
		border-left: 2px solid #707B7C;
	}
	table.greyTable thead th:first-child {
		border-left: none;
	}
</style>