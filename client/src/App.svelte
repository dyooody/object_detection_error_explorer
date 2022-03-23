<script>
	import { dataset_dev, each } from "svelte/internal";
	import { onMount } from 'svelte';
	import Table from './Components/Table.svelte';
	import Tab from './Components/Tab.svelte'
	import Listboxes from "./Components/Listbox.svelte";
	import Disclosure from './Components/Disclosure.svelte';


</script>



<div id="top-bar">
	<div id="title">
		Object Detection Results
	</div>
</div>

<div id="main">
	<div id ="left-side">
		<Disclosure/>
	</div>
	<div id = "right-side">
		<Tab/>
	</div>
</div>

<style>
	#main {
		display: flex;
	}
	#top-bar {
		width: 100%;
		height: 15px;
		background-color: var(--dark-grey);
		padding-top: 10px;
		padding-bottom: 10px;
		display: flex;
		align-items: center;
		border-bottom: 1.5px solid hsla(0, 0%, 0%, 0.1);
		display: none;
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
		--width: 450px;
		width: var(--width);
		max-width: var(--width);
		min-width: var(--width);
	}

	/*@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}*/
</style>