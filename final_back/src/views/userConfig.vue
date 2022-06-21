<template>
	<div>
	<el-form :inline="true"  class="demo-form-inline" label-width="80px" label-position="right">
	  <el-form-item label="户主电话:">
	    <el-input placeholder="电话" v-model="utele"></el-input>
	  </el-form-item>
	  <el-form-item label="户主姓名:">
	    <el-input placeholder="姓名" v-model="uname"></el-input>
	  </el-form-item>
	  <el-form-item label="审核状态:" >
	    <el-select placeholder="审核状态" v-model="value">
		  <el-option label="全部" value=""></el-option>
		  <el-option label="审核中" value="0"></el-option>
	      <el-option label="未通过" value="2"></el-option>
	      <el-option label="已通过" value="1"></el-option>
	    </el-select>
	  </el-form-item>
	  <el-form-item label="注册日期:">
	       <el-date-picker
	         v-model="utime"
	         type="date"
	         placeholder="选择日期"
			 format="yyyy 年 MM 月 dd 日"
			 value-format="yyyy-MM-dd">
	       </el-date-picker>
	  </el-form-item>
	  <el-form-item>
	    <el-button type="primary" icon="el-icon-search" @click="search()" size="medium">查询</el-button>
	  </el-form-item>
	</el-form>
	  <el-table
	    :data="tableData"
	    border
	    style="width: 100%"
		>
	    <el-table-column
	      prop="name"
	      label="姓名"
	      width="180" align="center">
	    </el-table-column>
	    <el-table-column
	      prop="tele"
	      label="账号"
	      width="180" align="center">
	    </el-table-column>
		<el-table-column
		  prop="date"
		  label="注册日期">
		</el-table-column>
	    <el-table-column
	      prop="build"
	      label="栋数"
		  align="center">
	    </el-table-column>
		<el-table-column
		  prop="measure"
		  label="房屋面积">
		</el-table-column>
		<el-table-column
		  prop="statue"
		  label="审核状态" align="center">
		  <template scope="scope">
			  <span v-if="scope.row.statue==0">
				  <el-button type="success" size="mini" icon="el-icon-check" round @click="userPass(scope.row.tele,scope.row.name,scope.row.measure,scope.row.date,scope.row.build,scope.$index)"></el-button>
				  <el-button type="warning" size="mini" icon="el-icon-close" round @click="userNot(scope.row.tele,scope.row.name,scope.row.measure,scope.row.date,scope.row.build,scope.$index)"></el-button>
			  </span>
			  <span style="color: #67C23A;" v-if="scope.row.statue==1">已通过</span>
			  <span style="color: #E6A23C;" v-if="scope.row.statue==2">未通过</span>
		  </template>
		</el-table-column>
		<el-table-column
		label="操作"
		align="center">
		<template scope="scope">
			<el-button type="primary" size="mini" icon="el-icon-edit" round @click="userEdit(scope.row.tele,scope.row.name,scope.row.measure,scope.row.date,scope.row.build,scope.row.statue,scope.$index)"></el-button>
			<el-button type="danger" icon="el-icon-delete" size="mini" round @click="userDelete(scope.row.tele,scope.$index)"></el-button>
		</template>
		</el-table-column>
	  </el-table>
	  <el-pagination style="text-align:center;margin: 30px;"
	    background
	    layout="prev, pager, next"
	    :total="total"
		@current-change="handleCurrentChange"
		:page-size="2"
		:current-page="pagecount">
	  </el-pagination>
	  <el-dialog
	    title="修改用户信息"
	    :visible.sync="centerDialogVisible"
	    width="30%"
	    center>
	    <el-form :rules="rule" status-icon :model="fromname" class="demo-ruleForm" ref="fromname">
			<el-form-item label="姓名:" prop="upname">
			  <el-input placeholder="请输入姓名" v-model="fromname.upname"></el-input>
			</el-form-item>
			<el-form-item label="住房面积:" prop="upmeasure">
			  <el-input placeholder="请输入住房面积" v-model.number="fromname.upmeasure" auto-complete="off"></el-input>
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
	export default{
		data(){
			return{
				tableData:[],
				total:null,
				uname:'',
				utele:'',
				utime:'',
				value:'',
				centerDialogVisible:false,
				pagecount:1,
				upindex:'',
				uptele:'',
				uptime:'',
				upstatue:'',
				upbuild:'',
				fromname:{
					upmeasure:'',
					upname:'',
				},
				rule:{
					upname:[{ required: true, message: '请输入姓名', trigger: 'blur'}],
					upmeasure:[{ required: true, message: '请输入住房面积', trigger: 'blur'},{required: true, type:'number', message: '只能输入数字值', trigger: ['blur', 'change']}]
				}
			}
		},
		mounted(){
			this.$axios.get(this.url+"/condliver",{params:{page_index:1,utele:this.utele,uname:this.uname,utime:this.utime,ustatue:this.value}}).then((res)=>{
				this.tableData=res.data.rows
				this.total=res.data.count
			})
		},
		methods:{
			search(){
				this.$axios.get(this.url+"/condliver",{params:{page_index:1,utele:this.utele,uname:this.uname,utime:this.utime,ustatue:this.value}}).then((res)=>{
					this.tableData=res.data.rows
					this.total=res.data.count
				})
			},
			userPass(tele,name,measure,date,build,index)
			{
				this.$axios.post(this.url+"/updliver",{utele:tele,uname:name,umeasure:measure,utime:date,ubuild:build,ustatue:1}).then(()=>{
					this.$message({
					          duration:1200,
					          message: "审核成功，已通过",
					          type: 'success'
					        });
					this.tableData[index].statue=1
				})
			},
			userNot(tele,name,measure,date,build,index)
			{
				this.$axios.post(this.url+"/updliver",{utele:tele,uname:name,umeasure:measure,utime:date,ubuild:build,ustatue:2}).then(()=>{
					this.$message({
					          duration:1200,
					          message: "审核成功，未通过",
					          type: 'warning'
					        });
					this.tableData[index].statue=2
				})
			},
			userEdit(tele,name,measure,date,build,statue,index)
			{
				this.centerDialogVisible=true
				this.uptele=tele
				this.fromname.upname=name
				this.fromname.upmeasure=measure
				this.uptime=date
				this.upbuild=build
				this.upstatue=statue
				this.upindex=index
			},
				 updateConfirm(formName) {
						this.$refs[formName].validate((valid) => {
						  if (valid) {
							this.$axios.post(this.url+"/updliver",{utele:this.uptele,uname:this.fromname.upname,umeasure:this.fromname.upmeasure,utime:this.uptime,ubuild:this.upbuild,ustatue:this.upstatue}).then((res)=>{
								if(res.data.code=="0")
								{
									this.tableData[this.upindex].name=this.fromname.upname
									this.tableData[this.upindex].measure=this.fromname.upmeasure
									this.centerDialogVisible=false
									this.$message({
								          duration:1200,
								          message: "修改成功",
								          type: 'success'
								      });
								}
								
							})
						  } else {
							console.log('error submit!!');
							return false;
						  }
						});
					  },
			userDelete(handleId)
			{
				 this.$confirm('您确定要删除此条数据吗?', '提示', {
				          confirmButtonText: '确定',
				          cancelButtonText: '取消',
				          type: 'warning'
				        }).then(()=>{
							this.$axios.post(this.url+"/delliver",{utele:handleId}).then((res)=>{
								if(res.data.code=="0")
								{
									let totalPage = Math.ceil((this.total - 1) / 6); // 总页数
								let currentPage =this.pagecount > totalPage ? totalPage : this.pagecount;
								this.pagecount = currentPage < 1 ? 1 : currentPage;
								this.$message({
								          duration:1200,
								          message: "删除成功",
								          type: 'success'
								        });
							this.$axios.get(this.url+"/condliver",{params:{page_index:this.pagecount,utele:this.utele,uname:this.uname,utime:this.utime,ustatue:this.value}}).then((res)=>{
								this.tableData=res.data.rows
								this.total=res.data.count
							})
								}
								
							})
							
						}).catch(()=>{
							
						})
			},
			handleCurrentChange(val)
			{
				this.pagecount=val
				this.$axios.get(this.url+"/condliver",{params:{page_index:val,utele:this.utele,uname:this.uname,utime:this.utime,ustatue:this.value}}).then((res)=>{
					this.tableData=res.data.rows
					this.total=res.data.count
				})
			}
		}
	}
</script>

<style>
</style>
