<template>
	<div class="cover">
		<div class="cont">
			<el-form>
				<h3 style="text-align: center;color:#409eff;">后台登录</h3>
				<div class="space"></div>
				 <el-form-item>
				      <el-input placeholder="请输入用户名" v-model="username" @input="buttonChange()">
				       <i slot="prepend" class="el-icon-user"/>
				      </el-input>
				 </el-form-item>
				 <div class="space"></div>
				 <el-form-item>
				    <el-input placeholder="请输入密码" v-model="pwd" type="password" @input="buttonChange()">
						<i slot="prepend" class="el-icon-lock"/>
					</el-input>
				 </el-form-item>
				 <div class="space"></div>
				 <el-form-item>
				     <el-button type="primary" style="width: 100%;" icon="el-icon-monitor" :disabled="dis" @click="login()">登录</el-button>
				 </el-form-item>
			</el-form>
		</div>
	</div>
</template>

<script>
	export default{
		data(){
			return{
				username:'',
				pwd:'',
				dis:true
			}
		},
		methods:{
			buttonChange(){
				if(this.username==""||this.pwd=="")
				{
					this.dis=true
				}
				else
				{
					this.dis=false
				}
			},
			login(){
				this.$axios.get(this.url+"/pclogin",{params:{username:this.username,password:this.pwd}}).then((res)=>{
					if(res.data.code!==0)
					{
						this.$message({
						          duration:1200,
						          message: res.data.msg,
						          type: 'error'
						        });
					}
					else
					{
						this.$router.push({name:'main'})
					}
				})
			},
		}
	}
</script>

<style lang="scss" scoped="scoped">
	.cover{
		width: 100%;
		height: 100%;
		background: url(../assets/3c8a18065bd4a8331c4ed8189170dbf.jpg);
	}
	.cont{
		padding: 20px 30px;
		box-sizing: border-box;
		width: 27%;
		height: 52%;
		border-top-right-radius:40px ;
		border-bottom-left-radius: 40px;
		background-color: white;
		float: right;
		margin-right: 10%;
		margin-top: 10%;
		box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
	}
	.space{
		width: 100%;
		height: 11px;
	}
</style>
