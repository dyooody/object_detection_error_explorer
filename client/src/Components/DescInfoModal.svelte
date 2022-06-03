<script>
  import { createEventDispatcher } from 'svelte';
  import Switch from "svelte-switch";

  export let infoModalOpen;

  const dispatch = createEventDispatcher();
  function closeInfoModal(){
    infoModalOpen = false;
    dispatch('closeInfoModal', {infoModalOpen});
  }

  let switch_check = false; //detection type and ground truth type

  function handleChange(e){
    const {checked} = e.detail;
    switch_check = checked;
  }

</script>

<div id="background" style="--display: {infoModalOpen ? 'block' : 'none'}" on:click={closeInfoModal}></div>
<div id="modal" style="--display : {infoModalOpen ? 'block' : 'none'}">
  <div id = "desc-view" class = "view-panel">
    <div class = 'view-title'>Type Description
      <Switch on:change={handleChange} checked={switch_check} onColor="#7d8a91"
      onHandleColor="#fff" handleDiameter={20} unCheckedIcon={false}
      boxShadow="0px 1px 5px rgba(0, 0, 0, 0.6)"
			activeBoxShadow="0px 0px 1px 10px rgba(0, 0, 0, 0.2)"
			height={16} width={30} containerClass="react-switch"
			id="material-switch">
			<span slot="checkedIcon" />
			<span slot="unCheckedIcon"/>
			</Switch>
    </div>

  </div>
</div>0

<style>
  #background{
    display: var(--display);
    position: fixed;
    z-index: 1;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(245, 243, 243, 0.01);
  }

  #modal{
    display: var(--display);
    position:fixed;
    z-index: 2;
    top: 5%;
    left: 25%;
    width: 800px;
    height: 600px;
    padding: 15px;
    /*transform: translate(-50%, -50%);*/
    background: #fff;
    border: 2px solid;
  }
  .view-panel{
    border: 2px solid #eee;
    margin-bottom: 15px;
    margin-right:15px;
  }
  .view-title{
    background-color: #f3f3f3;
    font-size: 1.0rem;
    margin-bottom: 8px;
    padding: 3px 8px 5px 12px;
  }
</style>