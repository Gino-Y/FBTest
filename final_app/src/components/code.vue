<template>
	<div>
		<van-field
		  label="手机号"
		  placeholder="请输入手机号"
					v-model="username"
					@input="change()"
					type="number"
		/>
		<van-field
		  label="验证码"
		  placeholder="请输入验证码"
					v-model="code"
					@input="change()"
		style="width: 70%;"
		/>
		<van-button type="info" :disabled="changeAble" size="small" style="float:right;margin-top:-36px;margin-right: 15px;width: 28%;" @click="getCode()">{{this.buttonText}}<span :style="{display:changeDisplay}">s后再次获取</span></van-button>
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
				code:"",
				dis:true,
				changeAble:true,
				buttonText:"获取验证码",
				changeDisplay:"none"
			}
		},
		methods:{
			change()
			{
				if(this.username==""||this.code=="")
				{
					this.dis=true
				}
				if(this.username!==""&&this.code!=="")
				{
					this.dis=false
				}
				if(this.username!=="")
				{
					this.changeAble=false
				}
				if(this.username=="")
				{
					this.changeAble=true
				}
			},
			getCode()
			{
				this.$axios.get(this.url+"/sendcode",{params:{tele:this.username}}).then((res)=>{
					if(res.data.code==0)
					{
						this.buttonText=60
						this.changeAble=true
						this.changeDisplay="inline"
						const timer=setInterval(()=>{this.buttonText--;if(this.buttonText==0){
							clearInterval(timer)
							this.buttonText="获取验证码"
							this.changeAble=false
							this.changeDisplay="none"
						}},1000)
					}
					else
					{
						Toast({
							message:res.data.data,
							position: 'top'
							})
					}
				})
				
			},
			loginTest()
			{
				this.$axios.get(this.url+"/codelogin",{params:{tele:parseInt(this.username),code:this.code}}).then((res)=>{
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
		}
	}
</script>

<style>
</style>
