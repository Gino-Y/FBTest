<template>
  <div class="main">
	<van-sticky>
	 <van-nav-bar
	  :title="this.feecode+'详情'"
	  left-arrow
	  @click-left="leftclick()"
	/>
	 <van-tabs sticky title-inactive-color="#58727e" title-active-color="#1989fa" color="#1989fa" @click="tabchange" >
	   <van-tab title="未交费"></van-tab>
	   <van-tab title="已交费"></van-tab>
	   <van-tab title="全  部"></van-tab>
	 </van-tabs>
	</van-sticky>
	<van-pull-refresh v-model="isLoading" @refresh="onRefresh()" success-text="刷新成功" loading-text="刷新中....">
	<div class="content">
		<van-empty :description="'未查到相应的'+this.feecode+'单'" v-if="this.listdata.length==0" />
		<div v-if="this.feecode=='水费'">
		<div class="list" v-for="item in listdata" :key="item.id">
			<span>订单编号:{{item.id}}<span v-if="item.ispay==0||item.ispay==2" style="color: #F56C6C;display: inline;margin-left: 160px;">未交费</span><span v-if="item.ispay==1" style="display: inline;color: #07c160;;margin-left: 160px;">已交费</span></span>
			<span>本月用水:{{item.num}}吨</span>
			<span v-if="item.ispay==0||item.ispay==2">单价:{{item.money/item.num}}元/吨</span>
			<span v-if="item.ispay==1">单价:{{item.hadpay/item.num}}元/吨</span>
			<span v-if="item.ispay==1">已交水费:{{item.hadpay}}元</span>
			<span v-if="item.ispay==0||item.ispay==2">应交水费:{{item.money}}元</span>
			<span>抄表月份:{{item.date}}</span>
			<span v-if="item.ispay==1">交费日期:{{item.payday}}</span>
			<van-button @click="payfee(item.id,item.money)" v-if="item.ispay==0||item.ispay==2" round  type="info" size="mini" style="letter-spacing: 10px;text-indent: 10px;margin-left: 75%;">交费</van-button>
		</div>
		</div>
		<div v-if="this.feecode=='电费'">
		<div class="list" v-for="item in listdata" :key="item.id">
			<span>电费单号:{{item.id}}<span v-if="item.ispay==0||item.ispay==2" style="color: #F56C6C;display: inline;margin-left: 160px;">未交费</span><span v-if="item.ispay==1" style="display: inline;color: #07c160;;margin-left: 160px;">已交费</span></span>
			<span>本月用电:{{item.num}} 度</span>
			<span v-if="item.ispay==0||item.ispay==2">单价:{{item.money/item.num}}元/度</span>
			<span v-if="item.ispay==1">单价:{{item.hadpay/item.num}}元/度</span>
			<span v-if="item.ispay==1">已交电费:{{item.hadpay}}元</span>
			<span v-if="item.ispay==0||item.ispay==2">应交电费:{{item.money}}元</span>
			<span>抄表月份:{{item.date}}</span>
			<span v-if="item.ispay==1">交费日期:{{item.payday}}</span>
			<van-button @click="payfee(item.id,item.money)" v-if="item.ispay==0||item.ispay==2" round  type="info" size="mini" style="letter-spacing: 10px;text-indent: 10px;margin-left: 75%;">交费</van-button>
		</div>
		</div>
		<div v-if="this.feecode=='物业费'">
		<div class="list" v-for="item in listdata" :key="item.id">
			<span>物业费单号:{{item.id}}<span v-if="item.ispay==0||item.ispay==2" style="color: #F56C6C;display: inline;margin-left: 160px;">未交费</span><span v-if="item.ispay==1" style="display: inline;color: #07c160;;margin-left: 160px;">已交费</span></span>
			<span v-if="item.ispay==1">已交物业费:{{item.hadpay}} 元</span>
			<span v-if="item.ispay==0||item.ispay==2">应交物业费:{{item.money}} 元</span>
			<span>抄表月份:{{item.date}}</span>
			<span v-if="item.ispay==1">交费日期:{{item.payday}}</span>
			<van-button @click="payfee(item.id,item.money)" v-if="item.ispay==0||item.ispay==2" round  type="info" size="mini" style="letter-spacing: 10px;text-indent: 10px;margin-left: 75%;">交费</van-button>
		</div>
		</div>
	</div>
	</van-pull-refresh>
	</div>
</template>

<script>
import { Dialog } from 'vant';
import { Notify} from 'vant';
	export default{
		data(){
			return{
				feecode:this.$route.query.feecode,
				tele:this.$route.query.tele,
				listdata:[],
				titlecode:0,
				isLoading:false
			}
		},
		mounted(){
			if(this.feecode=="水费")
			{
				this.$axios.get(this.url+"/appcondwafee",{params:{utele:this.tele,wpay:'0,2'}}).then((res)=>{
					this.listdata=res.data.rows;
					this.allPage=res.data.count;
				})
			}
			if(this.feecode=="电费")
			{
				this.$axios.get(this.url+"/appcondelfee",{params:{utele:this.tele,wpay:'0,2'}}).then((res)=>{
					this.listdata=res.data.rows;
					this.allPage=res.data.count;
				})
			}
			if(this.feecode=="物业费")
			{
				this.$axios.get(this.url+"/appcondprfee",{params:{utele:this.tele,wpay:'0,2'}}).then((res)=>{
					this.listdata=res.data.rows;
					this.allPage=res.data.count;
				})
			}
		},
		methods:{
			onRefresh() {
				 setTimeout(()=>{
					 if(this.feecode=="水费")
					 {
					 	switch (this.titlecode)
					 	{
					 		case 0:
					 		this.dataGet("/appcondwafee",'0,2');break;
					 		case 1:
					 		this.dataGet("/appcondwafee",1);break;
					 		case 2:
					 		this.dataGet("/appcondwafee");break;
					 	}
					 }
					 if(this.feecode=="电费")
					 {
					 	switch (this.titlecode)
					 	{
					 		case 0:
					 		this.dataGet("/appcondelfee",'0,2');break;
					 		case 1:
					 		this.dataGet("/appcondelfee",1);break;
					 		case 2:
					 		this.dataGet("/appcondelfee");break;
					 	}
					 }
					 if(this.feecode=="物业费")
					 {
					 	switch (this.titlecode)
					 	{
					 		case 0:
					 		this.dataGet("/appcondprfee",'0,2');break;
					 		case 1:
					 		this.dataGet("/appcondprfee",1);break;
					 		case 2:
					 		this.dataGet("/appcondprfee");break;
					 	}
					 }
					 this.isLoading=false
				 },600)
			    },
			dataGet(inurl,statue)//封装的获取各个订单参数的方法
			{
				this.$axios.get(this.url+inurl,{params:{utele:this.tele,wpay:statue}}).then((res)=>{
					this.listdata=res.data.rows;
					this.allPage=res.data.count;
				})
			},
			tabchange(title){
				if(this.feecode=="水费")
				{
					switch (title)
					{
						case 0:
						this.dataGet("/appcondwafee",'0,2');break;
						case 1:
						this.dataGet("/appcondwafee",1);break;
						case 2:
						this.dataGet("/appcondwafee");break;
					}
				}
				if(this.feecode=="电费")
				{
					switch (title)
					{
						case 0:
						this.dataGet("/appcondelfee",'0,2');break;
						case 1:
						this.dataGet("/appcondelfee",1);break;
						case 2:
						this.dataGet("/appcondelfee");break;
					}
				}
				if(this.feecode=="物业费")
				{
					switch (title)
					{
						case 0:
						this.dataGet("/appcondprfee",'0,2');break;
						case 1:
						this.dataGet("/appcondprfee",1);break;
						case 2:
						this.dataGet("/appcondprfee");break;
					}
				}
				this.titlecode=title
			},
			payfee(pid,money){
				Dialog.confirm({
				  title: '提示',
				  message: `您确定要支付${money} 元的${this.feecode}吗`,
				})
				  .then(() => {
				    if(this.feecode=="水费")
					{
						if(this.titlecode==0)
						{
							this.$axios.post(this.url+"/paywafee",{wfid:pid,wfhadpay:money}).then((res)=>{
								Notify({ type: 'success', message: res.data.msg });
								this.dataGet("/appcondwafee",'0,2')
							})
						}
						if(this.titlecode==2)
						{
							this.$axios.post(this.url+"/paywafee",{wfid:pid,wfhadpay:money}).then((res)=>{
								Notify({ type: 'success', message: res.data.msg });
								this.dataGet("/appcondwafee")
							})
						}
					}
					if(this.feecode=="电费")
					{
						if(this.titlecode==0)
						{
							this.$axios.post(this.url+"/payelfee",{efid:pid,efhadpay:money}).then((res)=>{
							Notify({ type: 'success', message: res.data.msg });
							this.dataGet("/appcondelfee",'0,2')
							})
						}
						if(this.titlecode==2)
						{
							this.$axios.post(this.url+"/payelfee",{efid:pid,efhadpay:money}).then((res)=>{
							Notify({ type: 'success', message: res.data.msg });
							this.dataGet("/appcondelfee")
							})
						}
					}
					if(this.feecode=="物业费")
					{
						if(this.titlecode==0)
						{
							this.$axios.post(this.url+"/payprfee",{pfid:pid,pfhadpay:money}).then((res)=>{
								Notify({ type: 'success', message: res.data.msg });
								this.dataGet("/appcondprfee",'0,2')
							})
						}
						if(this.titlecode==2)
						{
							this.$axios.post(this.url+"/payprfee",{pfid:pid,pfhadpay:money}).then((res)=>{
								Notify({ type: 'success', message: res.data.msg });
								this.dataGet("/appcondprfee")
							})
						}
					}
				  })
				  .catch(() => {
				    // on cancel
				  });
			},
			leftclick(){
				this.$router.push({name:'entrance',query: {tele:this.$route.query.tele}})
			}
		}
	}
</script>

<style lang="scss" scoped="scoped">
	.main{
		padding-top: 10px;
		height: 800px;
	}
	.content{
		width: 98%;
		background: #F9F9F9;
		margin: 0 auto;
		margin-top: 2px;
	}
	.list{
	    width: 100%;
		margin-top: 3px;
		background-color: white;
		padding: 4px 0 4px 20px;
	}
	.list>span{
		color: #969799;
		display: block;
		font-size: 13px;
		padding: 3px 0;
	}
	.list>span:nth-of-type(1){
		color:#646566;
		font-size: 14px;
	}
</style>
