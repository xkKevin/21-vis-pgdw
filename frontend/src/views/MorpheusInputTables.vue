<template>
  <div id="inputTables">
      <div id="upload" style="text-align:left;">
           <!-- style="border-bottom: 1px solid black" -->
         <el-row>
            <el-col style="margin-top:3%;height:13vh;border:none;width: 50%; background:#F6F8FB; display: flex; flex-direction: column;">
              <el-upload
              action=""
              ref="inputfiles"
              :on-remove="handleInputRemove"
              :on-change="handleInputChange"
              :auto-upload="false"
              :show-file-list="false"
              accept=".csv, .txt"
              multiple
              >
                  <el-button round slot="trigger" size="small" type="primary" style="border:1px solid #699E9D;background:white;margin-left:17px; height: 32px">
                    <div style="position:relative; top:-3px">
                        <img style="" src="@/assets/images/input.svg"/>
                        <span style="color: #666666;margin-left:9px;font-family: PingFangSC-Regular;font-weight: 400; font-size: 17px;">Source</span>
                    </div>
                  </el-button>
                  
              </el-upload>
              <div style="width:100%; overflow: auto; flex: 1;">
                <div v-for="(v,k) in inputfileList" :key="k" style="margin-left:17px;margin-top:1vh;">
                    <img src="@/assets/images/circle_input.svg"/>
                    {{v.name}}
                </div>
              </div>
          </el-col>
          <el-col style="margin-top:3%;height:13vh;border:none;width: 50%; background:#F6F8FB; display: flex; flex-direction: column;border-left:2px dashed #D9D9D9">
              <el-upload
              action=""
              ref="outputfiles"
              :on-remove="handleOutputRemove"
              :on-change="handleOutputChange"
              :auto-upload="false"
              :show-file-list="false"
              accept=".csv, .txt"
              multiple
              >
                  <el-button round slot="trigger" size="small" type="primary" style="border:1px solid #699E9D;background:white;margin-left:17px; height: 32px">
                    <div style="position:relative; top:-3px">
                        <img style="" src="@/assets/images/target.svg"/>
                        <span style="color: #666666;margin-left:9px;font-family: PingFangSC-Regular;font-weight: 400; font-size: 17px;">Target</span>
                    </div>
                  </el-button>
                  
              </el-upload>
              <div style="width:100%; overflow: auto; flex: 1;">
                <div v-for="(v,k) in outputfileList" :key="k" style="margin-left:17px;margin-top:1vh;">
                    <img src="@/assets/images/circle_output.svg"/>
                    {{v.name}}
                </div>
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
        
          <el-row style="background:white; padding: 1vh; text-align:center; border-bottom: 2px dashed #E6E6E6;">
              <!-- <el-button round @click="submitUpload" size="small" type="primary">upload and generate</el-button> -->
              <el-button round style="
                background:#6391D7;
                font-family: PingFangSC-Regular;
                font-size: 18px;
                color: #FFFFFF;
                letter-spacing: -0.7px;
                line-height: 17px;
                font-weight: 400;
                " 
                @click="submitUpload" size="small" type="primary"> <!-- v-loading.fullscreen.lock="fullscreenLoading" -->
                <!-- <i class="el-icon-upload2"></i> -->
                  Upload&nbsp;and&nbsp;Run
              </el-button>
          </el-row>
      </div>
  </div>
</template>

<script>
const request_api = "/backend"
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
    //   fullscreenLoading:false
    }
  },
    mounted() {
        window.myVue = this
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
            // console.log(this.$refs.inputfiles);
            // this.fullscreenLoading = true
            if(this.$refs.inputfiles.$children[0].fileList.length===0){  //  && this.$refs.outputfiles.$children[0].fileList.length===0
                this.$message({
                    showClose: true,
                    type:'error',
                    // showClose:true,
                    // duration:3000,
                    message:'Please select at least one file to upload'
                });
            }else{
                let flag1 = true,flag2 = true
                this.$emit("change-script-loading", true)
                let p1 = new Promise((resolve,reject)=>{
                    let data = {}
                    let output_file = {}
                    for(let key in this.outputFilesAsString){
                        output_file[key] = this.outputFilesAsString[key]
                    }
                    data['output'] = output_file

                    let input_file = {}
                    for(let key in this.inputFilesAsString){
                        input_file[key] = this.inputFilesAsString[key]
                    }
                    data['input'] = input_file
                    this.$axios({
                        url: `${request_api}/api/morpheusGetTablesAndParse`,
                        method: "post",
                        data: this.$qs.stringify(data),
                    }).then((response) => {
                        // this.fullscreenLoading = false
                        this.$emit("change-script-loading", false)
                        this.language = 'R';
                        this.$emit('getTableName',this.inputfileList[0].name)
                        this.$emit('updatechange',response.data.scriptReturn);

                        resolve();
                        
                    }).catch(err=>{
                        alert(err)
                        reject()
                    })     
                })
                /*
                let p2 = new Promise((resolve,reject)=>{
                    let data = {}
                    for(let key in this.inputFilesAsString){
                        data[key] = this.inputFilesAsString[key]
                    }
                    data['type'] = "input"
                    console.log(data)
                    this.$axios({
                        url: `${request_api}/api/morpheusGetTablesAndParse`,
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
                */
                // if(flag1 && flag2){
                //     // 调用接口上传数据
                //     const path = `${request_api}/useMorpheusPost`
                //     this.$axios.get(path)
                //     .then((response) => {
                //         this.fullscreenLoading = false
                //         this.language = 'R';
                //         this.$emit('getTableName',this.inputfileList[0].name)
                //         this.$emit('updatechange',response.data.scriptReturn);
                //     }).catch(err => {
                //         this.$message({
                //             message: err,
                //             type: "error", // success/warning/info/error
                //         });
                //     })
                // }
                Promise.all([p1]).then(()=>{
                    if(flag1 && flag2){
                        this.$refs.inputfiles.clearFiles();
                        this.$refs.outputfiles.clearFiles();
                        this.inputfileList = []
                        this.outputfileList = []
                        this.inputFilesAsString = {}
                        this.outputFilesAsString = {}
                        // this.$message({
                        //     message: "File(s) upload succeeded",
                        //     type: "success", // success/warning/info/error
                        // });
                        this.$emit("uploadSuccess");
                    }
                    else{
                        this.$message({
                            showClose: true,
                            message: "File(s) upload failed",
                            type: "error", // success/warning/info/error
                        });
                    }
                })
            };
        },
        handleOutputRemove(fileList){
            this.outputfileList = fileList
        },
        handleInputRemove(fileList){
            this.inputfileList = fileList
        }
    }
}
</script>
