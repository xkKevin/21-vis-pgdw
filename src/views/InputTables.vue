<template>
  <div id="inputTables" >
      <el-row type="flex" justify="space-between">
        <!-- <div>Upload Tables</div>  -->
      </el-row>
      <div id="upload" style="text-align:left;">
         <el-row>
              <el-col style="margin-top:5%;height:20vh;border:none;width:8vw">
              <el-upload
              action=""
              ref="inputfiles"
              :on-remove="handleInputRemove"
              :on-change="handleInputChange"
              :auto-upload="false"
              :show-file-list="false"
              multiple
              >
                  <el-button round slot="trigger" size="small" type="primary" style="border:1px solid #699E9D;background:white;margin-left:17px">
                    <img style="" src="@/assets/images/input.svg"/>
                    <p style="display:inline;color: #666666;margin-left:9px;font-family: PingFangSC-Regular;font-weight: 400;">Source</p>
                  </el-button>
              </el-upload>
              <div v-for="(v,k) in inputfileList" :key="k" style="margin-left:2vw;margin-top:1vh;width:9vw">
                <img src="@/assets/images/circle_input.svg"/>
                {{v.name}}
              </div>
          </el-col>
          <!-- <el-col style="margin-top:5%;height:20vh;border:none;width:8vw">
              <el-upload   
              action=""
              ref="outputfiles"
              :on-remove="handleOutputRemove"
              multiple
              :on-change="handleOutputChange"
              :auto-upload="false"
              :show-file-list="false"
              >
                  <el-button round slot="trigger" size="small" type="primary" style="border:1px solid #699E9D;background:white;margin-left:17px">
                    <img style="" src="@/assets/images/output.svg"/>
                    <p style="display:inline;color: #666666;font-family: PingFangSC-Regular;font-weight: 400;">Target</p>
                  </el-button>
              </el-upload>
          </el-col> -->
         </el-row>
          
          <hr style=""> 
          <el-row style="background:white">
              <!-- <el-button round @click="submitUpload" size="small" type="primary">upload and generate</el-button> -->

              <el-button round style="
                background:#6391D7;
                font-family: PingFangSC-Regular;
                font-size: 14px;
                color: #FFFFFF;
                letter-spacing: -0.7px;
                line-height: 17px;
                font-weight: 400;
                display:flex;
                align-items: center;
                margin-left:7vw;
                " 
                @click="submitUpload" size="small" type="primary">
                  Upload
              </el-button>
          </el-row>
      </div>

  </div>
</template>

<script>
const request_api = ""
import Papa from 'papaparse'
export default {
  name: "uploadTables",
  data() {
    return {
      inputTableName: "",
      outputTableName:"",
      inputTableToShow:[],
      inputTableHead:[],
      outputTableToShow:[],
      outputTableHead:[],
      inputFilesAsString:{},
      outputFilesAsString:{},

      inputfileList:[],
      outputfileList:[],
    }
  },

  methods:{
        getInputTableData(filename){
            this.inputTableName = filename
      	   
            var data = Papa.parse(this.inputFilesAsString[filename]).data;
            this.inputTableHead = data[0]
            let objArr = []
            for(let row = 1;row < data.length;row++){
                let tempObj = {}
                for(let col = 0;col < data[0].length;col++){
                    tempObj[data[0][col]] = data[row][col]
                }
                objArr.push(tempObj)
            }
        },
        getOutputTableData(filename){
            this.outputTableName = filename
            var data = Papa.parse(this.outputFilesAsString[filename]).data;
            this.outputTableHead = data[0]
            let objArr = []
            for(let row = 1;row < data.length;row++){
                let tempObj = {}
                for(let col = 0;col < data[0].length;col++){
                    tempObj[data[0][col]] = data[row][col]
                }
                objArr.push(tempObj)
            }
        },
        handleInputChange(file, fileList) {
            this.inputfileList = fileList

            let reader = new FileReader()
            reader.readAsText(file.raw)
            reader.onload = (e) => {
                const fileString = e.target.result
                this.inputFilesAsString[file.name] = fileString
            }
        },
        handleOutputChange(file, fileList) {
            this.outputfileList = fileList
            
            let reader = new FileReader()
            reader.readAsText(file.raw)
            //这里用箭头函数主要是考虑到涉及到this时作用域的问题
            reader.onload = (e) => {
                const fileString = e.target.result
                this.outputFilesAsString[file.name] = fileString
            }
        },
        submitUpload(){
            // this.$emit("uploadSuccess");
            // return ;
            if(this.$refs.inputfiles.$children[0].fileList.length===0 && this.$refs.outputfiles.$children[0].fileList.length===0){
                this.$message({
                    type:'error',
                    showClose:true,
                    duration:3000,
                    message:'please choose at least a file!'
                });
            }else{
                let flag1 = true,flag2 = true
                let p1 = new Promise((resolve,reject)=>{
                    let data = {}
                    for(let key in this.outputFilesAsString){
                        data[key] = this.outputFilesAsString[key]
                    }
                    data['type'] = "output"
                    this.$axios({
                        url: "/api/getTablesAndParse",
                        method: "post",
                        data: this.$qs.stringify(data),
                    }).then(res => {
                        if(res.data === "False")flag1 = false
                        resolve()
                    }).catch(err=>{
                        alert(err)
                        reject()
                    })     
                })
                let p2 = new Promise((resolve,reject)=>{
                    let data = {}
                    for(let key in this.inputFilesAsString){
                        data[key] = this.inputFilesAsString[key]
                    }
                    data['type'] = "input"
                    this.$axios({
                        url: "/api/getTablesAndParse",
                        method: "post",
                        data: this.$qs.stringify(data),
                    }).then(res => {
                        if(res.data === "False")flag2 = false
                        resolve()
                    }).catch(err=>{
                        alert(err)
                        reject()
                    })     
                })

                Promise.all([p1,p2]).then(()=>{
                    if(flag1 && flag2){
                        alert("upload success")
                        this.$emit("uploadSuccess");
                    }
                    else{
                        alert("upload fail")
                    }
                })
            };
        },
        handleOutputRemove(file,fileList){
            this.outputfileList = fileList
        },
        handleInputRemove(file,fileList){
            this.inputfileList = fileList
        },
    }
}
</script>
