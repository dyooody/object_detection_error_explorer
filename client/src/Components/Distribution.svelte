<script>
  import { onMount } from "svelte";
  import { scaleLinear } from "d3-scale";

  const padding = {top:20, right:15, bottom:20, left:25};
  let width = 500;
  let height = 200;

  let innerWidth = width - (padding.left + padding.right);

  let bbox_keys = [];
  let bbox_vals = [];
  let bbox_xScale;
  let bbox_yScale;
  let bbox_ticks = [];
  let bbox_barWidth;

  let score_keys = [];
  let score_vals = [];
  let score_xScale;
  let score_yScale;
  let score_ticks = [];
  let score_barWidth;

  let iou_keys = [];
  let iou_vals = [];
  let iou_xScale;
  let iou_yScale;
  let iou_ticks = [];
  let iou_barWidth;
  let show_default_chart = true;

  function adjust_format(tick){
    return "'" + tick.toString().slice(-2);
  }

  onMount(async() =>{
    fetch("/entire_distribution_chart/").then(res=>res.json()).then(result=>{
      show_default_chart = true;
      let total_bbox = result['bbox'];
      let bbox_lens = [];
      bbox_keys = Object.keys(total_bbox); // using keys as an xticks.
      for (var i=0; i< bbox_keys.length; i++){
        var each = {};
        each['key'] = bbox_keys[i];
        each['value'] = total_bbox[bbox_keys[i]].length;
        bbox_lens.push(total_bbox[bbox_keys[i]].length);
        bbox_vals.push(each);
      }
      let max_bbox_len = Math.max(...bbox_lens);
      bbox_xScale = scaleLinear()
        .domain([0, bbox_keys.length])
        .range([padding.left, width - padding.right]);

      bbox_yScale = scaleLinear()
        .domain([0, max_bbox_len])
        .range([height - padding.bottom, padding.top]);

      bbox_barWidth = innerWidth / bbox_keys.length;
      bbox_ticks = bbox_yScale.ticks(7);

      let total_score = result['score'];
      let score_lens = [];
      score_keys = Object.keys(total_score);
      for (var i=0; i < score_keys.length; i++){
        var each = {};
        each['key'] = score_keys[i];
        each['value'] = total_score[score_keys[i]].length;
        score_lens.push(total_score[score_keys[i]].length);
        score_vals.push(each);
      }
      let max_score_len = Math.max(...score_lens);
      score_xScale = scaleLinear()
        .domain([0, score_keys.length])
        .range([padding.left, width - padding.right]);

      score_yScale = scaleLinear()
        .domain([0, max_score_len])
        .range([height - padding.bottom, padding.top]);

      score_barWidth = innerWidth / score_keys.length;
      score_ticks = score_yScale.ticks(7);

      let total_iou = result['iou'];
      let iou_lens = [];
      iou_keys = Object.keys(total_iou);
      for (var i=0; i < iou_keys.length; i++){
        var each = {};
        each['key'] = iou_keys[i];
        each['value'] = total_iou[iou_keys[i]].length;
        iou_lens.push(total_iou[iou_keys[i]].length);
        iou_vals.push(each);
      }
      let max_iou_len = Math.max(...iou_lens);
      iou_xScale = scaleLinear()
        .domain([0, iou_keys.length])
        .range([padding.left, width - padding.right]);

      iou_yScale = scaleLinear()
        .domain([0, max_iou_len])
        .range([height - padding.bottom, padding.top]);

        iou_barWidth = innerWidth / iou_keys.length;
        iou_ticks = iou_yScale.ticks(7);
    });
  });

</script>

<!-- bbox chart -->
<h3> bbox distribution </h3>
<div class="chart" bind:clientWidth={width} bind:clientHeight={height}>
  <svg>
    <!-- y axis -->
    <g class="axis y-axis">
      {#each bbox_ticks as tick}
        <g class="tick tick-{tick}" transform="translate(0, {bbox_yScale(tick)})">
          <line x2="100%"></line>
          <text y ="-4">{tick} </text>
        </g>
      {/each}
    </g>

    <!-- x axis -->
    <g class = "axis x-axis">
      {#each bbox_vals as val, i}
        <g class="tick" transform="translate({bbox_xScale(i)}, {height})">
          <text x="{bbox_barWidth/2}" y="-4">{width > 380 ? val.key : adjust_format(val.value)}</text>
        </g>
      {/each}
    </g>

    <g class='bars'>
      {#each bbox_vals as val, i}
        <rect x="{bbox_xScale(i) + 10}" y="{bbox_yScale(val.value)}" width="{bbox_barWidth - 8}"
        height = "{bbox_yScale(0) - bbox_yScale(val.value)}"/>
      {/each}
    </g>
  </svg>
</div>

<!-- score chart -->
<h3> score distribution </h3>
<div class="chart" bind:clientWidth={width} bind:clientHeight={height}>
  <svg>
    <!-- y axis -->
    <g class="axis y-axis">
      {#each score_ticks as tick}
        <g class="tick tick-{tick}" transform="translate(0, {score_yScale(tick)})">
          <line x2="100%"></line>
          <text y ="-4">{tick} </text>
        </g>
      {/each}
    </g>

    <!-- x axis -->
    <g class = "axis x-axis">
      {#each score_vals as val, i}
        <g class="tick" transform="translate({score_xScale(i)}, {height})">
          <text x="{score_barWidth/2}" y="-4">{width > 380 ? val.key : adjust_format(val.value)}</text>
        </g>
      {/each}
    </g>

    <g class='bars'>
      {#each score_vals as val, i}
        <rect x="{score_xScale(i) + 10}" y="{score_yScale(val.value)}" width="{score_barWidth - 8}"
        height = "{score_yScale(0) - score_yScale(val.value)}"/>
      {/each}
    </g>
  </svg>
</div>

<!-- iou chart -->
<h3> iou distribution </h3>
<div class="chart" bind:clientWidth={width} bind:clientHeight={height}>
  <svg>
    <!-- y axis -->
    <g class="axis y-axis">
      {#each iou_ticks as tick}
        <g class="tick tick-{tick}" transform="translate(0, {iou_yScale(tick)})">
          <line x2="100%"></line>
          <text y ="-4">{tick} </text>
        </g>
      {/each}
    </g>

    <!-- x axis -->
    <g class = "axis x-axis">
      {#each iou_vals as val, i}
        <g class="tick" transform="translate({iou_xScale(i)}, {height})">
          <text x="{iou_barWidth/2}" y="-4">{width > 380 ? val.key : adjust_format(val.value)}</text>
        </g>
      {/each}
    </g>

    <g class='bars'>
      {#each iou_vals as val, i}
        <rect x="{iou_xScale(i) + 10}" y="{iou_yScale(val.value)}" width="{iou_barWidth - 8}"
        height = "{iou_yScale(0) - iou_yScale(val.value)}"/>
      {/each}
    </g>
  </svg>
</div>

<style>
  h3{
    text-align: center;
  }
  .chart{
    width:100%;
    max-width: 500px;
    margin: 0 auto;
  }
  svg{
    position: relative;
    width: 100%;
    height: 200px;
  }
  .tick {
		font-family: Helvetica, Arial;
		font-size: .725em;
		font-weight: 200;
	}
  .tick line {
		stroke: #e2e2e2;
		stroke-dasharray: 2;
	}

	.tick text {
		fill: #ccc;
		text-anchor: start;
	}

	.tick.tick-0 line {
		stroke-dasharray: 0;
	}

	.x-axis .tick text {
		text-anchor: middle;
	}

	.bars rect {
		fill: rgb(140, 163, 226);
		stroke: none;
		opacity: 0.65;
	}

</style>