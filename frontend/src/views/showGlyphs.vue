<template>
  <div id="showGlyphs">
    <!-- <remote-script src="https://github.com/bumbu/svg-pan-zoom/blob/master/dist/svg-pan-zoom.min.js"></remote-script> -->
    <!-- <remote-script src="http://ariutta.github.io/svg-pan-zoom/dist/svg-pan-zoom.min.js"></remote-script> -->
    <remote-script
      src="https://somnus.projects.zjvis.org/data/static/svg-pan-zoom.js"
    ></remote-script>
    <!-- <remote-script src="https://pv.sohu.com/cityjson?ie=utf-8"></remote-script> -->
    <el-row type="flex" justify="center" style="height: 45vh">
      <el-col style="width: 20vw; margin-right: 7px">
        <el-row style="height: 100%; display: flex; flex-direction: column">
          <el-header height="65px" style="background: black">
            <div
              style="
                text-align: center;
                color: white;
                font-size: 21pt;
                font-family: Arial;
                font-weight: bold;
                line-height: 65px;
              "
            >
              Somnus
            </div>
          </el-header>
          <div
            style="
              background: #f6f8fb;
              flex: 1;
              display: flex;
              flex-direction: column;
            "
          >
            <div id="tag0" class="tag" style="height: 50px"></div>
            <el-row
              style="
                flex: 1;
                height: 100%;
                display: flex;
                flex-direction: column;
              "
            >
              <upload-tables></upload-tables>
              <el-row
                style="
                  background: white;
                  padding-top: 15px;
                  flex: 1;
                  padding-left: 1vh;
                "
              >
                <span style="font-family: Arial; font-size: 20px">Case:</span>
                <el-dropdown @command="selectCase" style="margin-left: 8px">
                  <span
                    class="el-dropdown-link"
                    style="
                      width: 138px;
                      display: inline-block;
                      text-align: center;
                      padding: 4px 0;
                    "
                  >
                    {{ one_case }}
                  </span>
                  <i class="el-icon-arrow-down el-icon--right" style="position: relative; left: -6px;"></i>
                  <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item
                      v-for="key in Object.keys(cases)"
                      :key="key"
                      :value="key"
                      :command="key"
                    >
                      {{ key }}
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </el-dropdown>
              </el-row>
            </el-row>
          </div>
        </el-row>
      </el-col>

      <el-col
        style="
          width: 40vw;
          padding: 0 0 0 0;
          height: 100%;
          display: flex;
          flex-direction: column;
        "
      >
        <el-row
          type="flex"
          justify="space-between"
          style="height: 50px; background: #f5f5f5"
        >
          <div id="tag1"></div>
          <div class="title_right">
            Language:
            <el-dropdown @command="changeModel" style="margin-left: 8px">
              <span
                class="el-dropdown-link"
                style="width: 69px; display: inline-block; text-align: center; padding: 2px 0;"
              >
                {{ language }}
              </span>
              <i class="el-icon-arrow-down el-icon--right" style="position: relative; left: -4px;"></i>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item
                  v-for="item in all_langs"
                  :key="item"
                  :value="item"
                  :command="item"
                >
                  {{ item }}
                </el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
            <el-button
              round
              @click="generateSomnusGlyphs"
              style="
                background: #6391d7;
                font-family: PingFangSC-Regular;
                font-size: 18px;
                color: #ffffff;
                letter-spacing: -0.7px;
                line-height: 17px;
                font-weight: 400;
                display: flex;
                align-items: center;
                height: 38px;
                margin-top: 3px;
                margin-left: 8px;
              "
              >Run</el-button
            >
          </div>
        </el-row>
        <div style="flex: 1; display: flex; align-items: center">
          <div id="monaco" style="height: 38vh; width: 98%"></div>
        </div>
        <!-- style="width:40vw; height:100%; padding:0 0 0 0; display: grid; grid-template-columns: [c1] 100%; grid-template-rows: [r1] 50px [r2] auto;" -->
      </el-col>
      <el-col
        class="table_panel"
        style="width: 40vw; display: flex; flex-direction: column; height: 100%"
      >
        <el-row
          type="flex"
          justify="space-between"
          style="height: 50px; background: #f5f5f5"
        >
          <div id="tag2"></div>
          <div class="title_right">
            {{ table_name }}
            <!--
            Select Table:
            <el-dropdown @command="getTableData">
              <span
                class="el-dropdown-link"
                style="
                  width: 135px;
                  display: inline-block;
                  text-align: right;
                "
              >
                {{ table_name }}
                <i class="el-icon-arrow-down el-icon--right"></i>
              </span>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item
                  v-for="item in all_tables"
                  :key="item"
                  :value="item"
                  :command="item"
                >
                  {{ item }}
                </el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
            -->
          </div>
        </el-row>
        <div
          style="
            border-left: 2px solid #e6e6e6;
            padding: 0px 20px;
            flex: 1;
            display: flex;
            align-items: center;
          "
        >
          <el-table
            v-loading="table_loading"
            element-loading-spinner="el-icon-loading"
            element-loading-text="Loading"
            stripe
            :data="tableData"
            height="38vh"
            style="border: 2px solid #e6e6e6"
          >
            <el-table-column type="index"> </el-table-column>
            <!-- label 为 显示在table上的名字 -->
            <el-table-column
              v-for="item in tableHead"
              :key="item[1]"
              :label="item[0]"
            >
              <template scope="scope">
                {{ scope.row[item[1]] }}
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-col>
    </el-row>
    <el-row style="margin-top: 9px">
      <el-col style="height: 52.6vh; display: flex; flex-direction: column;">
        <el-row
          type="flex"
          justify="space-between"
          style="height: 50px; background: #f5f5f5"
        >
          <div id="tag3"></div>
        </el-row>
        <div
          id="glyphs"
          style="flex: 1; padding: 3px 1px"
          v-loading="glyph_running"
          element-loading-spinner="el-icon-loading"
          element-loading-text="Running"
        ></div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import axios from "axios";
import * as d3 from "d3";
import * as monaco from "monaco-editor"; // https://www.cnblogs.com/xuhaoliang/p/13803230.html
import { getCsv } from "@/assets/js/utils/common/getCsv";
import uploadTables from "./InputTables";
import {generateGlyphs, sendVue_gp, codeHighlight, record_log} from "@/assets/js/glyph/generate_provenance";

const request_api = "/backend";

export default {
  name: "showGlyphs",
  // delimiters: ["[[", "]]"],
  data() {
    return {
      svg: "",
      editor: null, // 文本编辑器
      table_name: "",
      script_content: "", //'print("hello world!")',  上一次运行的script脚本
      language: "r",
      all_langs: ["r", "python"],
      glyph_running: false,
      table_loading: false,
      tableData: [],
      tableHead: [],
      dataTables: {},
      show_table_name: true,
      decorations: null,
      cases: {
        r_case1: "input1.csv",
        r_case2: "warpbreaks.csv",
        r_case3: "Energy-Poverty 32641 homes.csv",
        r_case4: "fy2018.csv",
        r_case5: "benchmark5.txt",
        r_case6: "benchmark19.txt",
        r_case7: "original_tables/table1.csv",
        python_case1: "apple-iphone-revenue.csv",
        // "python_case2": "",
      },
      one_case: "Select a case",
      interaction_flag: false,
      // warning_flag: true, // 只在第一次警告用户
    };
  },
  components: {
    uploadTables,
  },
  // watch: {
  //   one_case: function () {
  //     this.getScriptData(this.one_case);
  //     this.getTableData(this.cases[this.one_case]);
  //   },
  // },
  methods: {
    selectCase(one_case = "r_case1") {
      this.one_case = one_case;
      this.getScriptData(this.one_case);
      this.getTableData(this.cases[this.one_case]);
    },
    drawTag(id, text) {
      let svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      svg.setAttribute("id", `${id}svg`);
      svg.setAttribute("width", "230px");
      svg.setAttribute("height", "40px");
      svg.setAttributeNS(
        "http://www.w3.org/2000/xmlns/",
        "xmlns:xlink",
        "http://www.w3.org/1999/xlink"
      );

      // document.getElementById("glyphs").appendChild(svg)
      // let svg = d3.append("svg")
      //           .attr('id',`${id}svg`)

      document.getElementById(id).appendChild(svg);
      let g = d3.select(`#${id}svg`).append("g");
      g.append("path")
        .attr("d", "M0,0 L0,40 L200,40 L230,0 L0,0")
        .attr("fill", "#62ADB2");

      // g.append("rect")
      // .attr('x',0)
      // .attr('y',0)
      // .attr("height",10)
      // .attr("width",60)
      // .attr("fill","red")

      g.append("text")
        .attr("x", 0)
        .attr("y", 0)
        .attr("dy", 26)
        .attr("dx", 18)
        .attr("text-anchor", "start")
        .attr("fill", "white")
        .attr("font-size", `19px`)
        .attr("font-weight", "bold")
        .attr("font-family", "Arial")
        .text(text);
    },
    initData() {
      this.initEditor();
      // this.getTableData(this.cases["r_case1"]);
      // this.getScriptData();
      this.selectCase();
      sendVue_gp(this);
      record_log("somnus", returnCitySN);
    },
    initEditor() {
      // 初始化编辑器，确保dom已经渲染
      this.editor = monaco.editor.create(document.getElementById("monaco"), {
        value: this.script_content, // 编辑器初始显示文字
        language: this.language, // 语言支持自行查阅demo
        automaticLayout: true, // 自动布局
        autoIndent: true, //自动布局
        fontSize: 16, //字体大小
        readOnly: false, // 只读
        theme: "vs", // 官方自带三种主题vs, hc-black, or vs-dark,
        glyphMargin: true,
      });

      this.editor.onKeyUp((e) => {
        this.detectChanges();
      });
    },
    detectChanges() {
      if (this.script_content == this.editor.getValue()) {
        // console.log("no changes");
        this.interaction_flag = true;
      } else {
        // console.log("changes");
        this.interaction_flag = false;
        this.fireKeyEvent(document.getElementById("tag3"), "keyup", 27);  // Escape code is 27
      }
    },
    changeModel(lang = "r", script_content = "", flag = true) {
      //创建新模型，value为旧文本，lang 为语言
      var oldModel = this.editor.getModel(); //获取旧模型
      if (flag) {
        // flag 为 true，说明是界面传来的，注意不能用 script_content === "" 来判断，因为 第二个参数传进来的是 VueComponent
        if (lang === this.language) return;
        // console.log("script_content:", script_content);
        script_content = this.editor.getValue();
        this.language = lang;
      }
      // modesIds即为支持语言
      // var modesIds = monaco.languages.getLanguages().map(function (lang) {
      //   return lang.id;
      // });
      var newModel = monaco.editor.createModel(script_content, lang);

      //将旧模型销毁
      if (oldModel) {
        oldModel.dispose();
      }
      //设置新模型
      this.editor.setModel(newModel);
      this.decorations = this.editor.deltaDecorations(
        [],
        [
          {
            range: new monaco.Range(1, 1, 1, 1),
            options: {
              isWholeLine: true,
              className: "myContentClass2",
              glyphMarginClassName: "myGlyphMarginClass2",
            },
          },
        ]
      );

      // console.log(this.decorations);
    },
    async getTableData(table_file) {
      this.table_loading = true;
      // 降低网络带宽，减少请求次数，同时避免
      if (this.dataTables[table_file] == undefined) {
        const table_path = `${request_api}/data/user_data/${table_file}?a=${Math.random()}`;
        await getCsv(table_path, this.dataTables, table_file);
      }
      this.table_name = table_file.startsWith("original_tables/")
        ? table_file.slice(16)
        : table_file;
      // console.log(this.dataTables);
      this.tableData = this.dataTables[table_file].tableData;
      this.tableHead = this.dataTables[table_file].tableHead;
      this.table_loading = false;
      /*
      const table_path = `${request_api}/data/user_data/${table_file}?a=${Math.random()}`;
      // dataIn1_csv = await getCsv(table_path);
      d3.text(table_path).then(data => {
        // console.log("text", d3.csvParseRows(data))
        this.table_name = table_file
        data = d3.csvParseRows(data)
        this.tableData = data.splice(1)
        let id = 0
        this.tableHead = data[0].map(value => [value, id++])
      })
      */
      /*
      d3.csv(table_path).then((data) => {
        this.table_name = table_file;
        this.tableData = data;
        this.tableHead = data.columns;
        // this.tableData = [{"iPhone": 3.7039999999999997, "YOY growth": 0.0, "iPhone1": 1.666, "YOY growt2h": 13}];
        // this.tableHead = [["iPhone",1], ["YOY growth",2], ["iPhone1",3], ["YOY growt2h",4]]; //data.columns;
        console.log(data.columns);
        console.log(data);
      });
      */
    },
    getScriptData(case_file = "") {
      const path = `${request_api}/getScriptData`;
      axios
        .get(path, { params: { case_file } })
        .then((response) => {
          this.language = case_file.split("_")[0];
          this.changeModel(this.language, response.data.script_content, false);
          this.detectChanges();
        })
        .catch((error) => {
          console.log(error);
          this.$message({
            message: error,
            type: "error", // success/warning/info/error
          });
        });
    },
    generateSomnusGlyphs() {
      generateGlyphs('generate_transform_specs', 'user_data');
    },
    controlShow(state) {
      this.show_table_name = state;
    },
    initEvent() {
      let self = this;
      this.$nextTick(function () {
        document.addEventListener("keyup", function (e) {
          // console.log(e);
          if (e.key == "Escape" || e.keyCodeVal == 27) {
            d3.selectAll("rect[class^='glyph']").attr("stroke", "gray");
            d3.selectAll("rect[id^='node']").attr("stroke", "gray");
            d3.selectAll("circle[class^='edge']").attr("style", `fill: gray;`);
            d3.selectAll("line[class^='edge']").attr("stroke", "gray");
            d3.selectAll("path[class^='arrow']").attr("fill", "gray");
            d3.selectAll(`path[class^='glyph']`).attr("stroke", "gray");
            codeHighlight(0);
          }
        });
      });
    },
    fireKeyEvent(el, evtType, keyCode) {
      var doc = el.ownerDocument,
        win = doc.defaultView || doc.parentWindow,
        evtObj;
      if (doc.createEvent) {
        if (win.KeyEvent) {
          evtObj = doc.createEvent("KeyEvents");
          evtObj.initKeyEvent(
            evtType,
            true,
            true,
            win,
            false,
            false,
            false,
            false,
            keyCode,
            0
          );
        } else {
          evtObj = doc.createEvent("UIEvents");
          Object.defineProperty(evtObj, "keyCode", {
            get: function () {
              return this.keyCodeVal;
            },
          });
          Object.defineProperty(evtObj, "which", {
            get: function () {
              return this.keyCodeVal;
            },
          });
          evtObj.initUIEvent(evtType, true, true, win, 1);
          evtObj.keyCodeVal = keyCode;
        }
        el.dispatchEvent(evtObj);
      } else if (doc.createEventObject) {
        evtObj = doc.createEventObject();
        evtObj.keyCode = keyCode;
        el.fireEvent("on" + evtType, evtObj);
      }
    },
  },
  mounted() {
    this.initData();
    this.initEvent();
    this.drawTag("tag0", "Data Panel");
    this.drawTag("tag1", "Script Panel");
    this.drawTag("tag2", "Table Panel");
    this.drawTag("tag3", "Graph Panel");
    // this.record_log();
  },
};
</script>

<style>
#showGlyphs {
  border: 2px solid #e3e6f0;
  background-color: #e3e6f0;
}

tr {
  color: black;
}
/* thead tr   !important*/
.el-table th {
  background-color: #f5f5f5;
  color: black;
}

/* .el-table__row--striped td{
  background-color: #F6F8FB !important;
} */

.title_right {
  display: flex;
  align-items: center;
  margin-right: 20px;
  font-family: Arial;
  font-size: 20px;
}
.el-col,
.el-header,
.el-aside,
.el-main,
.el-footer {
  /* border: 1px solid grey; */
  background-color: white;
}
footer.el-footer {
  padding: 10px;
}
.el-dropdown {
  border-radius: 8px;
  border: 1px solid grey;
  background-color: white;
  /* background-color: lightblue; */
  font-size: 20px;
}
.el-dropdown-link {
  cursor: pointer;
  color: #409eff;
  font-family: Arial;
  font-size: 20px;
}
.el-icon-arrow-down {
  font-size: 12px;
}

.myGlyphMarginClass {
  background: #6391d7;
  margin-left: 35px !important;
  width: 6px !important;
}

.myContentClass {
  background: lightblue;
}

.myContentClass2,
.myGlyphMarginClass2 {
}
</style>
