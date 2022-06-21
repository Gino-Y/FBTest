<template>
	<div>
		<template>
			<el-table :data="tableData" border style="width: 100%">
				<el-table-column prop="pa_id" label="车位编号" align="center">
				</el-table-column>
				<el-table-column prop="pa_floor" label="车位地址" align="center">
				</el-table-column>
				<el-table-column prop="tele" label="使用人联系电话" align="center">
				</el-table-column>
				<el-table-column prop="carnum" label="车牌号" align="center">
				</el-table-column>
				<el-table-column prop="starttime" label="开始使用时间" align="center">
				</el-table-column>
				<el-table-column label="操作" align="center">
					<template scope="scope">
						<el-button type="danger" size="mini" icon="el-icon-stopwatch" round @click="stopPaking(scope.row.pa_id,scope.row.pf_id,scope.row.starttime)">缴费停用</el-button>
					</template>
				</el-table-column>
			</el-table>
		</template>
		<el-pagination style="text-align:center;margin: 30px;" background layout="prev, pager, next" :total="total"
		 @current-change="handleCurrentChange" :page-size="6">
		</el-pagination>
	</div>
</template>

<script>
	export default{
		data(){
			return{
				current:1,
				pa_id: '',
				tableData: [],
				total: null,
				cs:''
			}
		},
		mounted() {
			this.$axios.get(this.url + "/selectaluse", {
				params: {
					page_index: 1
				}
			}).then((res) => {
				this.tableData = res.data.datanum
				this.total = res.data.datacount
			})
		},
		methods:{
			  getInervalHour(startDate, endDate) {
			            var ms = endDate.getTime() - startDate.getTime();
			            if (ms < 0) return 0;
			            return Math.floor(ms/1000/60/60);
			        },
			stopPaking(pa_id,pf_id,starttime)
			{
				this.$axios.get(this.url+"/selectchange").then((res)=>{
					this.cs=res.data[0][0]
					var date = new Date();
					console.log(date)
					var year = date.getFullYear();        //年 ,从 Date 对象以四位数字返回年份
					var month = date.getMonth() + 1;      //月 ,从 Date 对象返回月份 (0 ~ 11) ,date.getMonth()比实际月份少 1 个月
					var day = date.getDate();             //日 ,从 Date 对象返回一个月中的某一天 (1 ~ 31)
					var hours = date.getHours();          //小时 ,返回 Date 对象的小时 (0 ~ 23)
					var minutes = date.getMinutes();      //分钟 ,返回 Date 对象的分钟 (0 ~ 59)
					var seconds = date.getSeconds();      //秒 ,返回 Date 对象的秒数 (0 ~ 59)   
					var currentDate = year + "-" + month + "-" + day + " " + hours + ":" + minutes + ":" + seconds;
					let starttimeUse= new Date(starttime.replace(/-/g,"/"))
					this.$alert(`本次开始使用时间为：${starttime}，结束使用时间为:${currentDate}，共计使用：${this.getInervalHour(starttimeUse,date)}&nbsp;h，单价为：${this.cs}元/h，共需缴费：<span style='color:red'>${this.getInervalHour(starttimeUse,date)*this.cs}</span>元`, '缴费提示', {
					          confirmButtonText: '确定',
							  dangerouslyUseHTMLString:true
					        }).then(() => {
							this.$axios.post(this.url+"/stopparking",{paid:pa_id,pfid:pf_id,pfhour:this.getInervalHour(starttimeUse,date),pfmoney:this.getInervalHour(starttimeUse,date)*this.cs}).then((res)=>{
								this.$message({
									duration: 1200,
									message: res.data.msg,
									type: 'success'
								});
								let totalPage = Math.ceil((this.total - 1) / 6); // 总页数
								let currentPage =this.current > totalPage ? totalPage : this.current;
								this.current = currentPage < 1 ? 1 : currentPage;
								this.$axios.get(this.url + "/selectaluse", {
									params: {
										page_index: this.current
									}
								}).then((res) => {
									this.tableData = res.data.datanum
									this.total = res.data.datacount
								})
							})
					})
				})
				
			},
			handleCurrentChange(val) {
				this.current=val
				this.$axios.get(this.url + "/selectaluse", {
					params: {
						page_index: val
					}
				}).then((res) => {
					this.tableData = res.data.datanum
					this.total = res.data.datacount
				})
			}
		}
	}
</script>

<style>
</style>
