<template>
	<div class="covertable">
		<div class="block">
		    <span class="demonstration">水费单价（元/吨）：</span>
			<div class="slider">
		    <el-slider v-model="value1" show-input :disabled="cslignt"></el-slider>
			</div>
		</div>
		<div class="block">
		    <span class="demonstration">电费单价（元/度）：</span>
			<div class="slider">
		    <el-slider v-model="value2" show-input :disabled="cslignt"></el-slider>
			</div>
		</div>
		<div class="block">
			<span class="demonstration">物业费单位（元/㎡）：</span>
			<div class="slider">
			<el-slider v-model="value3" show-input :disabled="cslignt"></el-slider>
			</div>
		</div>
		<div class="block">
			<span class="demonstration">停车费单价（元/h）：</span>
			<div class="slider">
			<el-slider v-model="value4" show-input :disabled="cslignt"></el-slider>
			</div>
		</div>
		<el-button type="primary" size="small" round style="float: right;margin-top: 25px;margin-right: 40px;" icon="el-icon-edit" v-if="editshow" @click="editshowFun()">修改单价</el-button>
		<el-button type="success" size="small" round style="float: right;margin-top: 25px;margin-right: 40px;" icon="el-icon-check" v-if="editconfirm" @click="editconfirmFun()">确认修改</el-button>
		<el-button type="info" size="small" round style="float: right;margin-top: 25px;margin-right: 40px;" icon="el-icon-close" v-if="editcancle" @click="editcancleFun()">取消修改</el-button>
	</div>
</template>

<script>
	export default{
		data(){
			return{
				value1:'',
				value2:'',
				value3:'',
				value4:'',
				tabledata:[],
				cslignt:true,
				editshow:true,
				editcancle:false,
				editconfirm:false
			}
		},
		methods:{
			editshowFun()
			{
				this.editshow=false
				this.editconfirm=true
				this.editcancle=true
				this.cslignt=false
			},
			editcancleFun()
			{
				this.value1=this.tabledata[0].cs_standard
				this.value2=this.tabledata[1].cs_standard
				this.value3=this.tabledata[2].cs_standard
				this.value4=this.tabledata[3].cs_standard
				this.editshow=true
				this.editconfirm=false
				this.editcancle=false
				this.cslignt=true
			},
			editconfirmFun()
			{
				this.$axios.get(this.url+"/updatecs",{params:{cswater:this.value1,csele:this.value2,cspr:this.value3,csparking:this.value4}}).then((res)=>{
					if(res.data.code==0)
					{
						this.$message({
						          duration:1200,
						          message: res.data.msg,
						          type: 'success'
						  });
						this.tabledata[0].cs_standard=this.value1
						this.tabledata[1].cs_standard=this.value2
						this.tabledata[2].cs_standard=this.value3
						this.tabledata[3].cs_standard=this.value4
						this.editshow=true
						this.editconfirm=false
						this.editcancle=false
						this.cslignt=true
					}
				})
			}
		},
		mounted(){
			this.$axios.get(this.url+"/selectcs").then((res)=>{
				if(res.data.length==0)
				{
					this.$axios.post(this.url+"/insertcs").then(()=>{
						this.value1=0
						this.value2=0
						this.value3=0
						this.value4=0
					})
				}
				else
				{
					this.tabledata=res.data
					this.value1=res.data[0].cs_standard
					this.value2=res.data[1].cs_standard
					this.value3=res.data[2].cs_standard
					this.value4=res.data[3].cs_standard
				}
			})
		}
	}
</script>

<style scoped="scoped">
	.covertable{
		width: 100%;
		height:480px;
		background-color: white;
		box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
	}
	.block{
		padding: 30px 24px;
		overflow: hidden;
		border-bottom: 1px solid #eff2f6;
	}
	.demonstration{
		display: block;
		float: left;
		color: #8492a6;
		line-height: 35px;
		width: 20%;
	}
	.slider{
		display: block;
		float: left;
		width: 78%;
	}
</style>
