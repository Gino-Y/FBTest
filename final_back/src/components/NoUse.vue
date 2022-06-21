<template>
	<div>
		<template>
			<el-table :data="tableData" border style="width: 100%">
				<el-table-column prop="pa_id" label="车位编号" align="center">
				</el-table-column>
				<el-table-column prop="pa_fooler" label="车位地址" align="center">
				</el-table-column>
				<el-table-column label="操作" align="center">
					<template scope="scope">
						<el-button type="success" size="mini" icon="el-icon-mouse" round @click="usePaking(scope.row.pa_id)">使用</el-button>
					</template>
				</el-table-column>
			</el-table>
		</template>
		<el-pagination style="text-align:center;margin: 30px;" background layout="prev, pager, next" :total="total"
		 @current-change="handleCurrentChange" :page-size="6">
		</el-pagination>
		<el-dialog title="填写使用信息" :visible.sync="centerDialogVisible" width="30%" center>
			<el-form :rules="rule" status-icon :model="fromname" class="demo-ruleForm" ref="fromname">
				<el-form-item label="联系电话:" prop="uptele">
					<el-input placeholder="请输入联系电话" v-model.number="fromname.uptele"></el-input>
				</el-form-item>
				<el-form-item label="车牌号:" prop="upcarnum">
					<el-input placeholder="请输入车牌号" v-model="fromname.upcarnum"></el-input>
				</el-form-item>
			</el-form>
			<span slot="footer" class="dialog-footer">
				<el-button @click="centerDialogVisible = false" size="small">取 消</el-button>
				<el-button type="primary" @click="updateConfirm('fromname')" size="small">确 定</el-button>
			</span>
		</el-dialog>
		<el-dialog title="填写停车位信息" :visible.sync="addressDialogVisible" width="30%" center>
			<el-form :rules="rule" status-icon :model="fromname2" class="demo-ruleForm" ref="fromname2">
				<el-form-item label="地址" prop="address">
					<el-input placeholder="请输入地址" v-model="fromname2.address"></el-input>
				</el-form-item>
			</el-form>
			<span slot="footer" class="dialog-footer">
				<el-button @click="addressDialogVisible = false" size="small">取 消</el-button>
				<el-button type="primary" @click="insertConfirm('fromname2')" size="small">确 定</el-button>
			</span>
		</el-dialog>
		<div class="add-parking" @click="addressDialogVisible=true"><i class="el-icon-circle-plus-outline"></i></div>
	</div>
</template>
<script>
	export default {
		data() {
			return {
				current:1,
				pa_id: '',
				tableData: [],
				total: null,
				centerDialogVisible: false,
				addressDialogVisible:false,
				fromname: {
					upcarnum: '',
					uptele: '',
				},
				fromname2:{
					address:'',
				},
				rule: {
					upcarnum: [{
						required: true,
						message: '请输入车牌号',
						trigger: 'blur'
					}],
					address: [{
						required: true,
						message: '请输入地址',
						trigger: 'blur'
					}],
					uptele: [{
						required: true,
						message: '请输入手机号码',
						trigger: 'blur'
					}, {
						required: true,
						type: 'number',
						message: '只能输入数字值',
						trigger: ['blur', 'change']
					}]
				}
			};
		},
		mounted() {
			this.$axios.get(this.url + "/selectnouse", {
				params: {
					page_index: 1
				}
			}).then((res) => {
				this.tableData = res.data.num
				this.total = res.data.datacount
			})
		},
		methods: {
			usePaking(pa_id) {
				this.pa_id = pa_id
				this.centerDialogVisible = true
			},
			insertConfirm(formName){
				this.$refs[formName].validate((valid) => {
					if (valid) {
						this.$axios.post(this.url+"/addpaking",{pa_fooler:this.fromname2.address}).then((res)=>{
							if(res.data.code=="0")
							{
								this.addressDialogVisible=false
								this.$message({
									duration: 1200,
									message: res.data.msg,
									type: 'success'
								});
								this.$axios.get(this.url + "/selectnouse", {
									params: {
										page_index: 1
									}
								}).then((res) => {
									this.tableData = res.data.num
									this.total = res.data.datacount
								})
							}
						})
					}
				})
			},
			updateConfirm(formName) {
				this.$refs[formName].validate((valid) => {
					if (valid) {
						this.$axios.post(this.url+"/usepaking",{paid:this.pa_id,pftele:this.fromname.uptele,pfcarnum:this.fromname.upcarnum}).then((res)=>{
							if(res.data.code=="0")
							{
								this.$message({
									duration: 1200,
									message: res.data.msg,
									type: 'success'
								});
								let totalPage = Math.ceil((this.total - 1) / 6); // 总页数
								let currentPage =this.current > totalPage ? totalPage : this.current;
								this.current = currentPage < 1 ? 1 : currentPage;
								this.$axios.get(this.url + "/selectnouse", {
									params: {
										page_index: this.current
									}
								}).then((res) => {
									this.tableData = res.data.num
									this.total = res.data.datacount
								})
								this.fromname.uptele=''
								this.fromname.upcarnum=''
								this.centerDialogVisible=false
							}
						})
					} else {
						console.log('error submit!!');
						return false;
					}
				});
			},
			handleCurrentChange(val) {
				this.current=val
				this.$axios.get(this.url + "/selectnouse", {
					params: {
						page_index: val
					}
				}).then((res) => {
					this.tableData = res.data.num
					this.total = res.data.datacount
				})
			}
		}
	}
</script>

<style scoped="scoped">
	.add-parking{
		width: 50px;
		height: 50px;
		font-size: 40px;
		text-align: center;
		line-height: 50px;
		color: #409EFF;
		box-shadow: rgb(0 0 0 / 12%) 0px 0px 6px;
		background-color: white; 
		cursor: pointer;
		border-radius: 5px;
		position: absolute;
		top: 85%;
		left: 95%;
		z-index: 2;
	}
</style>
