<script>
	export let style;
  export let table_heads;
  export let table_vals;

	function class_details_result(selected_class, selected_head){
		console.log("selected_class :::: ", selected_class);
		console.log("selected_head :::: ", selected_head);
		fetch('/detailed_class_info/'+selected_class+'/'+selected_head).then(res=>res.json()).then(data=>{
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
			<tr/>
		</thead>
		<tbody>
			{#each table_vals as rows}
				<tr>
					{#each rows as cell, i}
						<td on:click={class_details_result(rows[0], table_heads[i])}>{cell}</td>
					{/each}
				</tr>
			{/each}
		</tbody>
	</table>
</div>

<style>
	/*#table_size{
		padding: 5px;
		width: 700px;
	}*/
	table, th, td {
		border: 0.5px solid;
		border-collapse: collapse;
		margin-bottom: 2px;
	}

	table.greyTable {
		border: 1px solid #17202A;
		width: 100%;
		text-align: center;
		border-collapse: collapse;
	}
	table.greyTable td, table.greyTable th {
		border: 1px solid #808B96;
		padding: 4px 2px;
	}
	table.greyTable tbody td {
		font-size: 10px;
	}
	table.greyTable tr:nth-child(even) {
		background: rgb(245, 244, 244);
	}
	table.greyTable thead {
		background: #e0e2e2;
	}
	table.greyTable thead th {
		font-size: 10px;
		/*color: #FFFFFF;*/
		text-align: center;
	}
	table.greyTable thead th:first-child {
		border-left: none;
	}
</style>