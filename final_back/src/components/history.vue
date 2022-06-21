<template>
	<div>
		<template>
			<el-table :data="tableData" border style="width: 100%">
				<el-table-column prop="pf_id" label="车位编号" align="center">
				</el-table-column>
				<el-table-column prop="pa_id" label="车位编号" align="center">
				</el-table-column>
				<el-table-column prop="pf_user_tele" label="使用人联系电话" align="center">
				</el-table-column>
				<el-table-column prop="pf_user_carnum" label="车牌号" align="center">
				</el-table-column>
				<el-table-column prop="pf_starttime" label="开始使用时间" align="center">
				</el-table-column>
				<el-table-column prop="pf_stoptime" label="结束使用时间" align="center">
				</el-table-column>
				<el-table-column prop="pf_hour" label="使用时间(h)" align="center">
				</el-table-column>
				<el-table-column prop="pf_money" label="费用(元)" align="center">
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
				tableData: [],
				total: null,
			}
		},
		mounted() {
			this.$axios.get(this.url + "/selecthistory", {
				params: {
					page_index: 1
				}
			}).then((res) => {
				this.tableData = res.data.datanum
				this.total = res.data.datacount
			})
		},
		methods:{
			handleCurrentChange(val) {
				this.current=val
				this.$axios.get(this.url + "/selecthistory", {
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
