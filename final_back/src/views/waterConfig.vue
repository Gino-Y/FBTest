<template>
	<div>
		<el-form :inline="true" class="demo-form-inline" label-width="80px" label-position="right">
			<el-form-item label="户主电话:">
				<el-input placeholder="请输入电话号码" v-model="utele"></el-input>
			</el-form-item>
			<el-form-item label="交纳状态:">
				<el-select placeholder="交纳状态" v-model="value">
					<el-option label="全部" value=""></el-option>
					<el-option label="未催缴" value="0"></el-option>
					<el-option label="已催缴" value="2"></el-option>
					<el-option label="已缴纳" value="1"></el-option>
				</el-select>
			</el-form-item>
			<el-form-item label="用水月份:">
				<el-date-picker v-model="edate" type="month" placeholder="选择月份" format="yyyy 年 MM 月" value-format="yyyy-MM">
				</el-date-picker>
			</el-form-item>
			<el-form-item>
				<el-button type="primary" icon="el-icon-search" @click="search()" size="medium">查询</el-button>
				<el-button type="primary" @click="addEle()" size="medium" icon="el-icon-circle-plus-outline">新增</el-button>
			</el-form-item>
		</el-form>
		<el-table :data="tableData" border style="width: 100%">
			<el-table-column prop="tele" label="户主账号" align="center">
			</el-table-column>
			<el-table-column prop="name" label="户主姓名" align="center">
			</el-table-column>
			<el-table-column prop="num" label="用水量(吨)">
			</el-table-column>
			<el-table-column label="应缴水费(元)">
				<template scope="scope">
					<span v-if="scope.row.ispay!==1">{{scope.row.money}}</span>
					<span v-if="scope.row.ispay==1">{{scope.row.hadpay}}</span>
				</template>
			</el-table-column>
			<el-table-column prop="date" label="用水月份">
			</el-table-column>
			<el-table-column prop="ispay" label="缴纳状态" align="center">
				<template scope="scope">
					<span style="color: #67C23A;" v-if="scope.row.ispay==1">已缴纳</span>
					<el-button type="primary" size="mini" @click="pushFee(scope.row.id,scope.row.tele,scope.row.money)" round v-if="scope.row.ispay==0">催缴</el-button>
					<span style="color: #E6A23C;" v-if="scope.row.ispay==2">已催缴</span>
				</template>
			</el-table-column>
			<el-table-column prop="payday" label="交纳日期">
			</el-table-column>
			<el-table-column label="操作" align="center">
				<template scope="scope">
					<el-button v-if="scope.row.ispay!=1" type="primary" size="mini" icon="el-icon-edit" round @click="eleEdit(scope.row.id,scope.row.num)"></el-button>
					<el-button type="danger" icon="el-icon-delete" size="mini" round @click="eleDelete(scope.row.id)"></el-button>
				</template>
			</el-table-column>
		</el-table>
		<el-pagination style="text-align:center;margin: 30px;" background layout="prev, pager, next" :total="total"
		 @current-change="handleCurrentChange" :page-size="6" :current-page="pageIndex">
		</el-pagination>
		<el-dialog :title="digTitle" :visible.sync="centerDialogVisible" width="30%" center>
			<el-form :rules="rule" status-icon :model="fromname" class="demo-ruleForm" ref="fromname">
				<el-form-item label="户主账号:" prop="uptele" v-if="this.digTitle=='新增水费信息'">
					<el-input placeholder="请输入户主账号" v-model.number="fromname.uptele"></el-input>
				</el-form-item>
				<el-form-item label="用水量(吨):" prop="upnum">
					<el-input placeholder="请输入用水量" v-model.number="fromname.upnum" auto-complete="off"></el-input>
				</el-form-item>
				<el-form-item label="用水月份:" prop="update" v-if="this.digTitle=='新增水费信息'">
					<el-date-picker v-model="fromname.update" type="month" placeholder="选择月份" format="yyyy 年 MM 月" value-format="yyyy-MM"
					 style="width: 100%;">
					</el-date-picker>
				</el-form-item>
			</el-form>
			<span slot="footer" class="dialog-footer">
				<el-button @click="centerDialogVisible = false" size="small">取 消</el-button>
				<el-button type="primary" @click="updateConfirm('fromname')" size="small">确 定</el-button>
			</span>
		</el-dialog>
	</div>
</template>

<script>
	export default {
		data() {
			return {
				tableData: [],
				total: null,
				utele: null,
				edate: null,
				value: null,
				centerDialogVisible: false,
				digTitle: '',
				pageIndex: 1,
				fromname: {
					upid: '',
					uptele: '',
					update: '',
					upnum: ''
				},
				rule: {
					uptele: [{
						required: true,
						message: '请输入用户账号',
						trigger: 'blur'
					}, {
						required: true,
						type: 'number',
						message: '只能输入数字值',
						trigger: ['blur', 'change']
					}],
					upnum: [{
						required: true,
						message: '请输入本月用水',
						trigger: 'blur'
					}, {
						required: true,
						type: 'number',
						message: '只能输入数字值',
						trigger: ['blur', 'change']
					}],
					update: [{
						required: true,
						message: '请输入用水月份',
						trigger: 'blur',
					}]
				}
			}
		},
		mounted() {
			this.$axios.get(this.url + "/condwafee", {
				params: {
					page_index: 1,
				}
			}).then((res) => {
				this.tableData = res.data.rows
				this.total = res.data.count
			})

		},
		methods: {
			handleCurrentChange(val) {
				this.pageIndex = val
				this.$axios.get(this.url + "/condwafee", {
					params: {
						page_index: val,
						utele: this.utele,
						wdate: this.edate,
						wpay: this.value
					}
				}).then((res) => {
					this.tableData = res.data.rows
					this.total = res.data.count
				})
			},
			search() {
				console.log(this.utele, this.value, this.edate)
				this.$axios.get(this.url + "/condwafee", {
					params: {
						page_index: 1,
						utele: this.utele,
						wdate: this.edate,
						wpay: this.value
					}
				}).then((res) => {
					this.tableData = res.data.rows
					this.total = res.data.count
				})
			},
			eleEdit(id, num) {
				this.fromname.upid = id
				this.fromname.upnum = num
				this.centerDialogVisible = true
				this.digTitle = "修改水费信息"
			},
			pushFee(fid, tele, money) {
				this.$axios.get(this.url + "/pushfee", {
					params: {
						fid: fid,
						tele: tele,
						money: money,
						feekind: '水'
					}
				}).then((res) => {
					if (res.data.code == "0") {
						this.$message({
							duration: 1200,
							message: res.data.msg,
							type: 'success'
						});
						this.$axios.get(this.url + "/condwafee", {
							params: {
								page_index: this.pageIndex,
							}
						}).then((res) => {
							this.tableData = res.data.rows
							this.total = res.data.count
						})
					} else {
						this.$message({
							duration: 1200,
							message: res.data.msg,
							type: 'error'
						});
					}
				})
			},
			eleDelete(id) {
				this.$confirm('您确定要删除此条数据吗?', '提示', {
					confirmButtonText: '确定',
					cancelButtonText: '取消',
					type: 'warning'
				}).then(() => {
					this.$axios.post(this.url + "/delwafee", {
						wfid: id
					}).then((res) => {
						if(res.data.code=="0")
						{
							this.$message({
								duration: 1200,
								message: res.data.msg,
								type: 'success'
							});
							let totalPage = Math.ceil((this.total - 1) / 6); // 总页数
							let currentPage =this.pageIndex > totalPage ? totalPage : this.pageIndex;
							this.pageIndex = currentPage < 1 ? 1 : currentPage;
							this.$axios.get(this.url + "/condwafee", {
								params: {
									page_index: this.pageIndex,
								}
							}).then((res) => {
								this.tableData = res.data.rows
								this.total = res.data.count
							})
						}
					})

				}).catch(() => {
				})
			},
			addEle() {
				this.centerDialogVisible = true
				this.fromname.uptele = ''
				this.fromname.upnum = ''
				this.fromname.update = ''
				this.digTitle = "新增水费信息"
			},
			updateConfirm(formName) {
				this.$refs[formName].validate((valid) => {
					if (valid) {
						if (this.digTitle == "新增水费信息") {
							this.$axios.post(this.url + "/addwaterfee", {
								ard: {
									utele: this.fromname.uptele
								},
								args: {
									wfdate: this.fromname.update,
									wfnum: this.fromname.upnum
								}
							}).then((res) => {
								if (res.data.code == 1) {
									this.$message({
										duration: 1200,
										message: res.data.msg,
										type: 'error'
									});
								} else {
									this.$message({
										duration: 1200,
										message: res.data.msg,
										type: 'success'
									});
									this.$axios.get(this.url + "/condwafee", {
										params: {
											page_index: 1,
										}
									}).then((res) => {
										this.tableData = res.data.rows
										this.total = res.data.count
									})
									this.centerDialogVisible = false
								}
							})
						}
						if (this.digTitle == "修改水费信息") {
							this.$axios.post(this.url + "/updwafee", {
								wfid: this.fromname.upid,
								wfnum: this.fromname.upnum
							}).then((res) => {
								if (res.data.code == "0") {
									this.$message({
										duration: 1200,
										message: "修改成功",
										type: 'success'
									});
									this.centerDialogVisible = false
									this.$axios.get(this.url + "/condwafee", {
										params: {
											page_index: this.pageIndex,
										}
									}).then((res) => {
										this.tableData = res.data.rows
										this.total = res.data.count
									})
								}

							})
						}
					} else {
						console.log('error submit!!');
						return false;
					}
				});
			},
		}
	}
</script>

<style>
</style>
