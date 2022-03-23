<script>
  import {
    Disclosure, DisclosureButton, DisclosurePanel
  } from "@rgossiaux/svelte-headlessui"

  let names = [];
  let descs = [];
  let des_data = [];
  fetch('/detect_type_description/').then(res =>res.json()).then(data=>{
    console.log("detect_type_description:::: ", data);
    console.log("any data ::: ", data.length);
    des_data = data;
    for (var i =0; i < data.length; i++){
      names.push(data[i]['name']);
      descs.push(data[i]['desc']);
    }
    names = names;
    descs = descs;
  })
</script>

<Disclosure>
  <DisclosureButton>Detection type description</DisclosureButton>
  <DisclosurePanel>
    {#each des_data as des}
    <Disclosure>
      <DisclosureButton>{des['name']}</DisclosureButton>
      <DisclosurePanel>{des['desc']}</DisclosurePanel>
    </Disclosure>
    {/each}
  </DisclosurePanel>
</Disclosure>

