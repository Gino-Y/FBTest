<template>
	<div class="main">
		<div class="main-content">
			<img src="../assets/ceced994f02feee8e6fb6f2632673e5.png" class="touxiang" />
			<span style="float: left;display: inline-block;margin: 43px 0 0 15px;color: #606266;">欢迎您，亲爱的用户</span>
		</div>
		<van-swipe class="my-swipe" :autoplay="5000" indicator-color="white" style="margin-top: 5px;">
		  <van-swipe-item>
			  <img src="../assets/图怪兽_40800cbc901d653cd3d3d5d5ae0d1714_22794.jpg" class="banner">
		  </van-swipe-item>
		  <van-swipe-item>
			  <img src="../assets/图司机-20210405-20531502.jpg" class="banner">
		  </van-swipe-item>
		  <van-swipe-item>
			  <img src="../assets/图怪兽_40800cbc901d653cd3d3d5d5ae0d1714_22794.jpg" class="banner">
		  </van-swipe-item>
		</van-swipe>
		<van-notice-bar
		  left-icon="volume-o"
		  text="请大家快点去缴费哦,不然就给你们停水停电了.请大家快点去缴费哦,不然就给你们停水停电了."
		  style="margin-top: 5px;"
		/>
		<van-grid :column-num="3" style="margin-top: 5px;color:#0086B3">
		  <van-grid-item @click="prsearchfee()">
		    <i class="iconfont icon-fang"></i><div style="height: 5px;"></div><span style="color: #909399;">物业费</span>
		  </van-grid-item>
		  <van-grid-item @click="wasearchfee()">
		    <i class="iconfont icon-shui"></i><div style="height: 5px;"></div><span style="color: #909399;">水费</span>
		  </van-grid-item>
		  <van-grid-item @click="elsearchfee()">
		    <i class="iconfont icon-dian"></i><div style="height: 5px;"></div><span style="color: #909399;">电费</span>
		  </van-grid-item>
		</van-grid>
		<div class="loginout" @click="outLogin()">退出登录</div>
	</div>
</template>

<script>
	export default{
		data(){
			return{
				
			}
		},
		methods:{
			outLogin(){
				this.$router.push({name:'login'})
			},
			wasearchfee(){
				this.$router.push({name:'detail',query: {feecode:'水费',tele:this.$route.query.tele}})
			},
			elsearchfee(){
				this.$router.push({name:'detail',query: {feecode:'电费',tele:this.$route.query.tele}})
			},
			prsearchfee(){
				this.$router.push({name:'detail',query: {feecode:'物业费',tele:this.$route.query.tele}})
			},
		}
	}
</script>

<style lang="scss" scoped="scoped">
	.main{
		width: 100%;
		height: 100%;
		background-color: #eeeeee;
		padding: 1%;
	}
	.main-content{
		height: 10%;
		border-radius: 10px;
		background-color: white;
		margin-top:3%;
	}
	.main-content:nth-last-of-type(1)
	{
		height: 13%;
		border-radius: 0;
	}
	 .my-swipe .van-swipe-item {
	    text-align: center;
	 }
	  table{
		  width: 100%;
		  border: none;
		  height: 100%;
		  text-align: center;
		  vertical-align: middle;
	  }
	  tr:nth-of-type(1)
	  {
		  vertical-align: bottom;
		  color: #0086B3;
	  }
	  tr:nth-of-type(2)
	  {  
	  	color: #c2c2c2;
	  }
	.touxiang
	  {
		  float: left;
		  width: 50px;
		  height: 50px;
		  border-radius: 100%;
		  margin: 17px 0 0 20px;
	  }
	.banner{
		width: 360px;
		height: 150px;
	}
	.loginout
	{
		border-top-left-radius: 25px;
		border-bottom-left-radius: 25px;
		height: 40px;
		width: 32%;
		float: right;
		background-color: #ee0a24;
		margin-top: 150px;
		color: white;
		text-align: center;
		line-height: 40px;
	}
	  @import "../assets/font_3sqperqths/iconfont.css"
</style>
