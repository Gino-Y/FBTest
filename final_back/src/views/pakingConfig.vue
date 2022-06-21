<template>
	  <el-tabs v-model="activeName" @tab-click="handleClick">
	    <el-tab-pane label="未使用" name="first"><nouse v-if="firstshow"></nouse></el-tab-pane>
	    <el-tab-pane label="正在使用" name="second"><aluse v-if="secondshow"></aluse></el-tab-pane>
	    <el-tab-pane label="历史订单" name="third"><history v-if="thirdshow"></history></el-tab-pane>
	  </el-tabs>
</template>

<script>
import nouse from "../components/NoUse.vue"
import aluse from "../components/AlUse.vue"
import history from "../components/history.vue"
	export default {
	    data() {
	      return {
	        activeName: 'first',
			firstshow:true,
			secondshow:false,
			thirdshow:false
	      };
	    },
	    methods: {
	      handleClick(tab) {
	      console.log(tab.name)
		  switch(tab.name){
			  case 'first':
			  this.firstshow=true;this.secondshow=false;this.thirdshow=false;break;
			  case 'second':
			  this.firstshow=false;this.secondshow=true;this.thirdshow=false;break;
			  case 'third':
			  this.firstshow=false;this.secondshow=false;this.thirdshow=true;break;
		  }
	    }
	  },
	  components:{
	  	nouse,
	  	aluse,
		history,
	  }
	}
</script>

<style scoped>
</style>
