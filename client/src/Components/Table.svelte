<script>
	export let style;
  export let table_heads;
  export let table_vals;
	export let detail = "False";

	console.log("detail ::: ", detail)
</script>

<table class={style}>
	<thead>
		<tr>
			{#each table_heads as head}
				<th>{head}</th>
			{/each}
			{#if detail == "True"}
				<th>details</th>
			{/if}
		<tr/>
	</thead>
	<tbody>
		{#each table_vals as rows}
			<tr>
				{#each rows as cell}
					<td>{cell}</td>
				{/each}
				{#if detail == "True"}
					<button>more detail</button>
				{/if}

			</tr>
		{/each}
	</tbody>
</table>

<style>
	table, th, td {
		border: 1px solid;
		border-collapse: collapse;
		margin-bottom: 10px;
	}

	table.redTable {
		border: 2px solid #A40808;
		background-color: #EEE7DB;
		width: 100%;
		text-align: center;
		border-collapse: collapse;
	}
	table.redTable td, table.redTable th {
		border: 1px solid #AAAAAA;
		padding: 3px 2px;
	}
	table.redTable tbody td {
		font-size: 13px;
	}
	table.redTable tr:nth-child(even) {
		background: #F5C8BF;
	}
	table.redTable thead {
		background: #A40808;
		background: -moz-linear-gradient(top, #bb4646 0%, #ad2020 66%, #A40808 100%);
		background: -webkit-linear-gradient(top, #bb4646 0%, #ad2020 66%, #A40808 100%);
		background: linear-gradient(to bottom, #bb4646 0%, #ad2020 66%, #A40808 100%);
	}
	table.redTable thead th {
		font-size: 19px;
		font-weight: bold;
		color: #FFFFFF;
		text-align: center;
		border-left: 2px solid #A40808;
	}
	table.redTable thead th:first-child {
		border-left: none;
	}

		table.blueTable {
		border: 1px solid #1C6EA4;
		background-color: #EEEEEE;
		width: 100%;
		text-align: center;
		border-collapse: collapse;
	}
	table.blueTable td, table.blueTable th {
		border: 1px solid #AAAAAA;
		padding: 3px 2px;
	}
	table.blueTable tbody td {
		font-size: 13px;
	}
	table.blueTable tr:nth-child(even) {
		background: #D0E4F5;
	}
	table.blueTable thead {
		background: #1C6EA4;
		background: -moz-linear-gradient(top, #5592bb 0%, #327cad 66%, #1C6EA4 100%);
		background: -webkit-linear-gradient(top, #5592bb 0%, #327cad 66%, #1C6EA4 100%);
		background: linear-gradient(to bottom, #5592bb 0%, #327cad 66%, #1C6EA4 100%);
		border-bottom: 2px solid #444444;
	}
	table.blueTable thead th {
		font-size: 15px;
		font-weight: bold;
		color: #FFFFFF;
		border-left: 2px solid #D0E4F5;
	}
	table.blueTable thead th:first-child {
		border-left: none;
	}
</style>