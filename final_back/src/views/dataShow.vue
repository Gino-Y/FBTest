<template>
	<div style="width: 100%;height: 100%;">
			<el-row :gutter="20" class="">
			<el-col :span="6" v-for="item in cardData" :key="item.$index">
				<div class="grid-content">
				  <div class="code"><span v-if="item.code!=='停车场'">费用缴纳情况</span><span v-if="item.code=='停车场'">车位使用情况</span><el-tag effect="dark" style="float: right;" size="mini">{{item.code}}</el-tag></div>
				  <hr>
				  <div class="data-pass">{{item.pass}}<span v-if="item.code!=='停车场'">（单）</span><span v-if="item.code=='停车场'">（处）</span></div>
				  <el-progress class="show" type="circle" :percentage="item.percent" width="90" height="90" style="margin-top: 20px;"></el-progress>
				  <div class="data-total">合计:{{item.total}}<span v-if="item.code!=='停车场'">（单）</span><span v-if="item.code=='停车场'">（处）</span></div>
				</div>
			</el-col>
			</el-row>
			<div class="chart">
				<div class="left-chart" id="thischart">
					<div style="height: 5px;"></div>
					<span>近六个月已交电费情况</span>
				</div>
				<div class="left-chart" id="thatchart">
					<div style="height: 5px;"></div>
					<span>已交费用统计</span>
				</div>
			</div>
	</div>
</template>

<script>
import { Chart } from '@antv/g2';
	export default{
		data(){
			return{
				cardData:[],
			}
		},
		mounted(){
			this.$axios.get(this.url+"/carddata").then((res)=>{
				this.cardData=res.data
			})
			this.$axios.get(this.url+"/thatchart").then((res)=>{
				const chart = new Chart({
				  container: 'thatchart',
				  autoFit: true,
				  height: 500,
				  padding: [30, 20, 50, 20],
				});
				chart.data(res.data);
				chart.scale('value', {
				  alias: '费用（元）',
				});
				
				chart.axis('type', {
				  tickLine: {
				    alignTick: false,
				  },
				});
				chart.axis('value', false);
				
				chart.tooltip({
				  showMarkers: false,
				});
				chart.interval().position('type*value');
				chart.interaction('element-active');
				
				// 添加文本标注
				res.data.forEach((item) => {
				  chart
				    .annotation()
				    .text({
				      position: [item.type, item.value],
				      content: item.value,
				      style: {
				        textAlign: 'center',
				      },
				      offsetY: -10,
				    })
				    .text({
				      position: [item.type, item.value],
				      style: {
				        textAlign: 'center',
				      },
				      offsetY: -12,
				    });
				});
				chart.theme({ "styleSheet": { "brandColor": "#5B8FF9", "paletteQualitative10": ["#5B8FF9", "#61DDAA", "#65789B", "#F6BD16", "#7262fd", "#78D3F8", "#9661BC", "#F6903D", "#008685", "#F08BB4"], "paletteQualitative20": ["#5B8FF9", "#CDDDFD", "#61DDAA", "#CDF3E4", "#65789B", "#CED4DE", "#F6BD16", "#FCEBB9", "#7262fd", "#D3CEFD", "#78D3F8", "#D3EEF9", "#9661BC", "#DECFEA", "#F6903D", "#FFE0C7", "#008685", "#BBDEDE", "#F08BB4", "#FFE0ED"] } });
				chart.render();
			})
			this.$axios.get(this.url+"/chartdata").then((res)=>{
				const chart = new Chart({
				  container:'thischart',
				  autoFit: true,
				  height: 200,
				  padding:[10,50,60,40]
				});
				chart.data(res.data);
				chart.scale({
				  month: {
				    range: [0, 1],
				  },
				  count: {
				    nice: true,
				  },
				});
				
				chart.tooltip({
				  showCrosshairs: true,
				  shared: true,
				});
				
				chart.axis('count', {
				  label: {
				    formatter: (val) => {
				      return val;
				    },
				  },
				});
				chart
				  .line()
				  .position('month*count')
				  .color('type')
				  .shape('smooth');
				chart
				  .point()
				  .position('month*count')
				  .color('type')
				  .shape('circle');
				chart.theme({ "styleSheet": { "brandColor": "#215B77", "paletteQualitative10": ["#215B77", "#1B9CD0", "#61C9FF", "#ABDFFF", "#EFF3DE", "#FFDE94", "#FFC741", "#D09C10", "#795B16"], "paletteQualitative20": ["#215B77", "#227BA2", "#1B9CD0", "#22BAED", "#61C9FF", "#8AD4FF", "#ABDFFF", "#C9E9FF", "#EFF3DE", "#FFE9B8", "#FFDE94", "#FFD470", "#FFC741", "#EDB40A", "#D09C10", "#A37B16", "#795B16"] } });
				chart.render();
			})
			
		}
	}
</script>

<style lang="scss" scoped="true">
	.el-col-6{
		height: 100%;
	}
	.show{
		float: right;
		
	}
	hr{
		 border: 0;
		 background-color: #d7dae2;
		 height: 1px;
	}
	.grid-content{
		height: 100%;
		background-color: white;
		border-radius: 10px;
		padding: 10px 10px 0 10px;
		box-sizing:border-box ;
		width: 100%;
	}
	.el-row{
		height: 36%;
	}
	.code{
		text-align: left;
		font-weight: 600;
		color: #666;
	}
	.data-pass{
		float: left;
		font-weight: 600;
		width: 60%;
		height: 65%;
		color: #606266;
		line-height: 120px;
		text-align: center;
	}
	.data-total{
		width: 100%;
		float: left;
		height: 25px;
		line-height: 25px;
		text-align: right;
		font-size: 13px;
		margin-top: 5px;
		border-top: 1px solid #d7dae2;
		color: #909399;
	}
	.chart{
		width: 100%;
		height:63%;
		padding-top: 1%;
	}
	.left-chart{
		text-align: center;
		width:50%;
		height: 94%;
		float: left;
		background-color: white;
		font-weight: 600;
		color: #666;
	}
</style>
