<template>
	<div>
	<div class="top-app">
		<img style="margin-left: 25%;" src="../assets/图怪兽_0f4f9483842c1469ac384c9de9fcf822_58369.png" width="50%" height="50%"  />
	</div>
    <div id="nav">
		 <component :is="com"></component>
    </div>
	<span class="tab-left" @click="tabChange()">{{this.changetab}}</span>
	<span class="tab-right" @click="dian()">点击注册</span>
</div>
</template>
<script>
import compassword from "../components/password.vue"
import comcode from "../components/code.vue"
export default{
	data(){
		return{
			com:'compassword',
			changetab:'验证码登录'
		}
	},
	methods:{
		tabChange()
		{
			console.log(this.changetab)
			if(this.changetab=="验证码登录")
			{
				this.changetab="密码登录"
				this.com="comcode"
				return false;
			}
			if(this.changetab=="密码登录")
			{
				this.changetab="验证码登录"
				this.com="compassword"
			}
		},
		dian(){
			this.$router.push({name:'register'});
		},
	},
	components:{
		compassword,
		comcode
	}
}
</script>
<style lang="scss" scoped="scoped">
	.top-app{
		margin-top: 30px;
	}
	.tab-left{
	float: left;
	margin-left:15px ;
	margin-top: 20px;
	display: block;
	font-size: 13px;
	color: #1989fa;
	}
	.tab-right{
		float: right;
		margin-right:15px ;
		margin-top: 20px;
		display: block;
		font-size: 13px;
		color: #1989fa;
	}
</style>

