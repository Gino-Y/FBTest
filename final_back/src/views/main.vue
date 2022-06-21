<template>
	<el-container style="width: 100%;height: 100%;">
	  <el-header style="height: 12%;background-color: #23262E">
		  <h1>小星星物业</h1>
		  <el-dropdown>
		  <h5>超级管理员<i class="el-icon-arrow-down el-icon--right"></i></h5>
		  <el-dropdown-menu slot="dropdown">
		          <el-dropdown-item icon="el-icon-user">我的信息</el-dropdown-item>
		          <el-dropdown-item icon="el-icon-switch-button" @click.native="loginout">退出登录</el-dropdown-item>
		        </el-dropdown-menu>
		  </el-dropdown>
		  <img src="../assets/ceced994f02feee8e6fb6f2632673e5.png">
	  </el-header>
	  <el-container>
	    <el-aside width="15%">
			 <el-menu
			      class="el-menu-vertical-demo"
			      background-color="#393D49"
			      text-color="#D2D6D4"
			      active-text-color="#FFFFFF"
				  style="height: 100%;"
				  router
				  >
				<el-menu-item index="/main/dataShow">
				        <i class="el-icon-pie-chart"></i>
				        <span slot="title">数据展示</span>
				</el-menu-item>
				<el-menu-item index="/main/userConfig">
				        <i class="el-icon-user"></i>
				        <span slot="title">用户管理</span>
				</el-menu-item>
				<el-submenu index="3">
				<template slot="title">
						<i class="el-icon-wallet"></i>
						<span>收费管理</span>
				</template>
				<el-menu-item index="/main/electriConfig">
				       <i class="iconfont icon-dianfei"></i>&nbsp;
				        <span slot="title">电费管理</span>
				</el-menu-item>
				<el-menu-item index="/main/waterConfig">
				        <i class="iconfont icon-shuifei"></i>&nbsp;
				        <span slot="title">水费管理</span>
				</el-menu-item>
				<el-menu-item index="/main/propertyConfig">
				        <i class="el-icon-office-building"></i>
				        <span slot="title">物业费管理</span>
				</el-menu-item>
				<el-menu-item index="/main/pakingConfig">
				        <i class="el-icon-truck"></i>
				        <span slot="title">停车费管理</span>
				</el-menu-item>
				</el-submenu>
				<el-menu-item index="/main/csConfig">
				        <i class="el-icon-setting"></i>
				        <span slot="title">系统设置</span>
				</el-menu-item>
				</el-menu>
		</el-aside>
	    <el-main style="background-color:whitesmoke">
			<router-view></router-view>
		</el-main>
	  </el-container>
	</el-container>
</template>

<script>
	export default{
		methods:{
			loginout()
			{
				this.$confirm('您确定要退出吗', '提示', {
				          confirmButtonText: '确定',
				          cancelButtonText: '取消',
				          type: 'warning'
				        }).then(() => {
				          this.$router.push({name:'login'})
				        }).catch(() => {
				                 
				        });
			}
		}
	}
</script>
<style lang="scss">
	h1{
		display: inline-block;
		color: #1989fa;
		margin-left: 40px;
		}
	img
	{
		float: right;
		border-radius: 50%;
		width: 50px;
		height: 50px;
		margin-top: 15px;
		margin-right: 15px;
	}
  .el-dropdown
	{
		display: inline-block;
		float: right;
		color: whitesmoke;
		margin-top: 12px;
		cursor: pointer;
	}
	h5{
		color:whitesmoke
	}
	@import "../assets/font_lqiddrohaxc/iconfont.css"
</style>
