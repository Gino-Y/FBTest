<template>
	<div>
	<van-field
	  label="手机号"
	  placeholder="请输入手机号码"
				v-model="username"
				@input="change()"
				type="number"
	/>
	<van-field
	  type="password"
	  label="密码"
	  placeholder="请输入密码"
				v-model="password"
				@input="change()"
	/>
	<div style="margin: 0 auto;margin-top: 20px;width: 95%;">
	  <van-button :disabled="dis" @click="loginTest()" block type="info" style="letter-spacing: 20px;vertical-align: middle;height: 40px;border-radius: 5px;">登录</van-button>
	</div>
	</div>
</template>

<script>
	import { Toast } from 'vant';
	export default{
		data(){
			return{
				username:"",
				password:"",
				dis:true
			}
		},
		methods:{
			loginTest(){
				this.$axios.get(this.url+"/liverlogin",{params:{username:parseInt(this.username),pwd:this.$md5(this.password)}}).then((res)=>{
					if(res.data.msg=="登陆成功")
					{
						this.$router.push({name:'entrance',query:{tele:this.username}});
					}
					else{
				Toast({
					message:res.data.msg,
					position: 'top'
					})
				}
			   })
			},
			change()
			{
				if(this.username==""||this.password=="")
				{
					this.dis=true
				}
				else
				{
					this.dis=false
				}
			},
		}
	}
</script>

<style lang="scss" scoped="scoped">
</style>
