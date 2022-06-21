<template>
	<div>
	<van-nav-bar
	  title="注  册"
	  left-arrow
	  @click-left="leftclick()"
	/>
	<van-notify v-model="success_show" type="success">
	  <van-icon name="passed" style="margin-right: 4px;" />
	  <span>注册成功，我们将尽快审核</span>
	</van-notify>
	<van-notify v-model="fail_show" type="warning">
	  <van-icon name="close" style="margin-right: 4px;" />
	  <span>此账号已被注册，请换一个账号</span>
	</van-notify>
	<div style="width: 100%;height: 50px;"></div>
	<van-form>
	  <van-field
	    label="手机号码"
	    placeholder="请输入手机号码"
		type="number"
		v-model="tele"
		:rules="[{ required: true, message: '请填写手机号' }]"
		@input="change()"
	  />
	  <van-field
	    label="姓名"
	    placeholder="请输入姓名"
		:rules="[{ required: true, message: '请填写姓名' }]"
		v-model="name"
		@input="change()"
	  />
	  <van-field
	    label="住房地址"
	    placeholder="例如:3栋"
		:rules="[{ required: true, message: '请填写栋数' }]"
		v-model="build"
		@input="change()"
	  />
	  <van-field
	    label="面积"
	    placeholder="例如:122,只需写数字"
		type="number"
		:rules="[{ required: true, message: '请填写面积数' }]"
		v-model="measure"
		@input="change()"
	  />
	  <van-field
	    label="密码"
	    placeholder=""
		type="password"
		v-model="pwd"
		:rules="[{ required: true, message: '请填写密码' }]"
		@input="change()"
	  />
	  <van-field
	    label="确认密码"
	    placeholder=""
		v-model="repwd"
		type="password"
		:rules="[{ required: true, message: '请再次填写密码' }]"
		@input="change()"
	  />
	  </van-form>
	   <div class="regButton">
	   <van-button block type="info" style="border-radius: 5px;" @click="sub()" :disabled="dis">提交审核</van-button>
	   </div>
	</div>
</template>

<script>
import { Toast } from 'vant';
	export default{
		data(){
			return{
				tele:"",
				name:"",
				build:"",
				measure:"",
				pwd:"",
				repwd:"",
				dis:true,
				success_show:false,
				fail_show:false
			}
		},
		methods:{
			change(){
				if(this.tele==""||this.name==""||this.build==""||this.measure==""||this.pwd==""||this.repwd=="")
				{
					this.dis=true
				}
				else
				{
					this.dis=false
				}
			},
			leftclick(){
				this.$router.push({name:"login"})
			},
			sub(){
				if(this.pwd!==this.repwd){
					Toast.fail({message:'请保证两次密码为正确的',position:"top"});
				}
				else{
					let date=new Date();
					this.$axios.post(this.url+"/addliver",{"uname":this.name,
					"utele":parseInt(this.tele),
					"ubuild":this.build,
					"upwd":this.$md5(this.pwd),
					"umeasure":parseInt(this.measure),
					"utime":date.toLocaleDateString().replace(/\//g, '-')}).then((res)=>{
						switch (res.data.code){
							case 1:
							this.success_show = true;
							      setTimeout(() => {
							        this.success_show = false;
									this.$router.push({name:"login"})
							      }, 1500);
							break;
							case 0:
							this.fail_show=true;
							setTimeout(() => {
							  this.fail_show = false;
							}, 1500)
						}
					})
				}
			}
		}
	}
</script>

<style lang="scss" scoped="scoped">
	.regButton{
		width: 90%;
		height: 40px;
		padding: 10px;
		margin-top:5px ;
	}
</style>
