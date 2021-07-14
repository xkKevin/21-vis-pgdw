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
                font-size: 18pt;
                font-family: Arial;
                font-weight: bold;
                line-height: 65px;
              "
            >
              MORPHEUS&nbsp;Revisited
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
              <upload-tables v-on:updatechange="getUpload" @getTableName="getTableName"></upload-tables>
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
                      width: 158px;
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
            Language:R
            <!-- <el-dropdown @command="changeModel" style="margin-left: 8px">
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
            </el-dropdown> -->
            <!-- <el-button
              round
              @click="generateGlyphs"
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
            > -->
          </div>
        </el-row>
        <div v-loading="script_loading" style="flex: 1; display: flex; align-items: center">
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
            v-if="showTable"
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

import { create_table } from "@/assets/js/glyph/createTables";
import { create_row, create_row_insert } from "@/assets/js/glyph/createRows";
import { delete_table } from "@/assets/js/glyph/deleteTables";
import {
  create_column,
  create_column_create,
} from "@/assets/js/glyph/createColumns";
import {
  delete_column,
  delete_dropna,
  delete_duplicate,
} from "@/assets/js/glyph/deleteColumns";
import {
  delete_duplicate_row_partColumn,
  delete_filter,
  delete_row,
} from "@/assets/js/glyph/deleteRows";
import {
  transform_tables_fold,
  transform_tables_rearrange,
  transform_tables_sort,
  transform_tables_unfold,
} from "@/assets/js/glyph/transformTables";
import {
  transform_columns_mutate,
  transform_columns_replace_na,
} from "@/assets/js/glyph/transformColumns";
import { combine_columns_merge } from "@/assets/js/glyph/combineColumns";
import {
  combine_rows_interpolate,
  combine_rows_sum,
} from "@/assets/js/glyph/combineRows";
import { transform_rows_edit } from "@/assets/js/glyph/transformRows";
import {
  separate_tables_decompose,
  separate_tables_split,
  separate_tables_subset,
} from "@/assets/js/glyph/separateTables";
import { separate_columns } from "@/assets/js/glyph/separateColumns";
import { separate_rows } from "@/assets/js/glyph/separateRows";
import {
  combine_tables_extend,
  combine_tables_full_join,
  combine_tables_inner_join,
  combine_tables_left_join,
} from "@/assets/js/glyph/combineTables";
import { generateDataForCreateTable } from "@/assets/js/utils/genDataForCreateTables";
import {
  generateData,
  generateDataForCreateColumns,
  generateDataForCreateColumns_create,
  generateDataForCreateColumns_extract,
} from "@/assets/js/utils/genDataForCreateColumns";
import { generateDataForInsertRows } from "@/assets/js/utils/genDataForCreateRows";
import {
  generateDataForDeleteColumn,
  generateDataForDeleteNaColumn,
  generateDataForKeepColumns,
} from "@/assets/js/utils/genDataForDeleteColumns";
import { getDuplicatedColumns } from "@/assets/js/utils/common/getDuplicatedColumns";
import {
  generateDataForDeleteDuplicateRows,
  generateDataForFilterRow,
  generateDataForRows,
} from "@/assets/js/utils/genDataForDeleteRows";
import {
  generateDataForColumnRearrange,
  generateDataForFold,
  generateDataForTableSort,
} from "@/assets/js/utils/genDataForTransformTable";
import {
  generateDataForColumnRename,
  generateDataForMutate_cover,
  generateDataForReplace,
} from "@/assets/js/utils/genDataForTransformColumns";
import { generateDataForMergeColumns } from "@/assets/js/utils/genDataForCombineColumns";
import {
  generateDataForGroupSummarize,
  generateDataForRowInterpolate,
} from "@/assets/js/utils/genDataForCombineRows";
import { generateDataForEditRow } from "@/assets/js/utils/genDataForTransformRows";
import {
  generateDataForSeparateDecompose,
  generateDataForSeparateDecompose_q,
  generateDataForSeparateSplit,
  generateDataForSeparateSubset,
} from "@/assets/js/utils/genDataForSeparateTables";
import { generateDataForSeparateColumn } from "@/assets/js/utils/genDataForSeparateColumns";
import { generateDataForSeparateRows } from "@/assets/js/utils/genDataForSeparateRows";
import {
  generateDataForFullJoin_2,
  generateDataForInnerJoin,
  generateDataForLeftJoin_2,
  generateDataForTablesExtend_withExplicitCol,
} from "@/assets/js/utils/genDataForCombineTables";
import { identical_operation } from "@/assets/js/glyph/identicalOperation";
import { getCsv } from "@/assets/js/utils/common/getCsv";
import { getGraphs } from "@/assets/js/utils/renderTree/getLayout";
import { drawSvgAndEdge } from "@/assets/js/utils/renderTree/renderNodeAndEdge";
import { drawNode, sendVue } from "@/assets/js/utils/renderTree/render";
import { getComponents } from "@/assets/js/utils/renderTree/getComponents";
import { svgSize, nodeSize } from "@/assets/js/config/config";
import "@/assets/js/utils/common/importJs.js";

import {
  generateDataForTablesConcat,
  generateDataForSummarize_python,
} from "@/assets/js/utils/generateDataForPython";
import {
  combine_tables_extend_axis0,
  combine_tables_extend_axis1,
} from "@/assets/js/glyph/glyphs_for_python";

import uploadTables from "./MorpheusInputTables";

const request_api = "";

export default {
  name: "showGlyphs",
  // delimiters: ["[[", "]]"],
  data() {
    return {
      svg: "",
      editor: null, // 文本编辑器
      table_name: "",
      script_content: "", //'print("hello world!")',  上一次运行的script脚本
      language: "R",
      all_langs: ["r", "python"],
      glyph_running: false,
      table_loading: false,
      script_loading: false,
      tableData: [],
      tableHead: [],
      dataTables: {},
      show_table_name: true,
      decorations: null,
      cases: {
        Morpheus_case1: "benchmarks/1/r1_input1.csv|benchmarks/1/r1_output1.csv",
        Morpheus_case2: "benchmarks/5/r5_input1.csv|benchmarks/5/r5_output1.csv",
        Morpheus_case3: "benchmarks/9/r9_input1.csv|benchmarks/9/r9_output1.csv",
        Morpheus_case4: "benchmarks/13/r13_input1.csv|benchmarks/13/r13_output1.csv",
        Morpheus_case5: "benchmarks/27/r27_input1.csv|benchmarks/27/r27_input2.csv|benchmarks/27/r27_output1.csv",
        Morpheus_case6: "benchmarks/53/r53_input1.csv|benchmarks/53/r53_output1.csv",
        Morpheus_case7: "benchmarks/60/r60_input1.csv|benchmarks/60/r60_output1.csv",
        Morpheus_case8: "benchmarks/74/r74_input1.csv|benchmarks/74/r74_output1.csv",
        // case8: "benchmarks/38/r38_input1.csv|benchmarks/38/r38_input2.csv|benchmarks/38/r38_output1.csv",
        // "python_case2": "",
      },
      casesTable: {
        Morpheus_case1: "r1_input1.csv",
        Morpheus_case2: "r5_input1.csv",
        Morpheus_case3: "r9_input1.csv",
        Morpheus_case4: "r13_input1.csv",
        Morpheus_case5: "r27_input1.csv",
        Morpheus_case6: "r53_input1.csv",
        Morpheus_case7: "r60_input1.csv",
        Morpheus_case8: "r74_input1.csv",
      },
      one_case: "Select a case",
      interaction_flag: false,
      scriptReturnByUpload: '',
      tableName: '',
      showTable: false,
      gm_flag_count: 0
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
    getUpload(e){
      this.showTable = true
      this.scriptReturnByUpload = e;
      this.language = 'R';
      this.changeModel(this.language, this.scriptReturnByUpload, false);
      this.detectChanges();
      this.getTableData(this.tableName)
      this.generateGlyphsUpload();
    },
    getTableName(e){
      this.tableName = e
    },
    selectCase(one_case = "r_case1") {
      this.showTable = true
      this.one_case = one_case;
      // this.getScriptData(this.one_case);
      this.getMorpheus(this.cases[this.one_case]);
      this.getTableData(this.casesTable[this.one_case]);
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
      // this.selectCase();
      sendVue(this);
    },
    initEditor() {
      // 初始化编辑器，确保dom已经渲染
      this.editor = monaco.editor.create(document.getElementById("monaco"), {
        value: this.script_content, // 编辑器初始显示文字
        language: this.language, // 语言支持自行查阅demo
        automaticLayout: true, // 自动布局
        autoIndent: true, //自动布局
        fontSize: 16, //字体大小
        readOnly: true, // 只读
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
        const table_path = `${request_api}/data/morpheusData/${table_file}?a=${Math.random()}`;
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
      const table_path = `${request_api}/data/${tables_path}/${table_file}?a=${Math.random()}`;
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
    getMorpheus(case_string = "") {
      this.script_loading = true
      this.gm_flag_count += 1
      const path = `${request_api}/useMorpheus`
      axios.get(path, { params: { caseString: case_string } })
      .then((response) => {
        if(response.data.error_info){
          this.$message({
            message: response.data.error_info,
            type: "error",
          });
        }else{
          this.language = 'R';
          this.changeModel(this.language, response.data.scriptReturn, false);
          this.script_loading = false;
          this.detectChanges();
          this.generateGlyphs();
          this.gm_flag_count -= 1
        }
      })
      .catch((error) => {
        if (this.gm_flag_count > 0) {
          this.gm_flag_count -= 1
        } else {
          console.log(error);
          this.$message({
          message: error,
          type: "error",
        });
        }
      });
    },
    generateGlyphs() {
      // console.log(this.editor.getValue(), this.language);
      this.glyph_running = true
      const path = `${request_api}/morpheus_generate_transform_specs`;
      let specsToHandle = [];
      // console.log(this.scriptReturnByUpload)
      // console.log(this.editor.getValue())
      // this.glyph_running = true;
      axios
        .get(path, {
          params: {
            script_content: this.editor.getValue(),
            language: this.language,
          },
        })
        .then((response) => {
          this.glyph_running = false;
          // 执行 run 之前先 清空当前数据
          this.dataTables = {};
          // 生成glyphs的操作
          if (response.data.error_info) {
            this.$message({
              message: response.data.error_info,
              type: "error", // success/warning/info/error
            });
          } else {
            // console.log(response.data.transform_specs)
            document.getElementById("glyphs").innerHTML = "";
            // Object.assign(specsToHandle,response.data.transform_specs)

            specsToHandle = Array.from(response.data.transform_specs);
            for(let idx = 0;idx < specsToHandle.length;idx ++){
              if(specsToHandle[idx].type === 'separate_tables_decompose'){
                specsToHandle[idx].output_table_file = specsToHandle[idx].output_table_file.slice(0,Math.min(2,specsToHandle[idx].output_table_file.length))
                specsToHandle[idx].output_table_name = specsToHandle[idx].output_table_name.slice(0,Math.min(2,specsToHandle[idx].output_table_name.length))
              }
            }
            /*
            specsToHandle = [
              {
                    operation_rule: `Load: "apple-iphone-revenue.csv"`,
                    output_table_file: "t1.csv",
                    output_table_name: "revenue",
                    type: "create_tables",
                },
               
                {
                    operation_rule: `rearrange Category`,
                    input_table_file: "t1.csv",
                    input_table_name: "revenue",
                    input_explicit_col:["Category"],
                    output_table_file: "t3.csv",
                    output_table_name: "revenue_sort",
                    type: "transform_tables_sort",
                },
                // {
                //     operation_rule: `transform scores`,
                //     output_explicit_col:['P.E.'],
                //     input_table_file: "t6.csv",
                //     input_table_name: "scores2",
                //     output_explicit_col:["P.E."],
                //     output_table_file: "t11.csv",
                //     output_table_name: "level2score",
                //     type: "transform_columns_mutate",
                // },
                {
                    operation_rule: `Load: "apple-iphone-unit-sales.csv"`,
                    output_table_file: "t2.csv",
                    output_table_name: "sales",
                    type: "create_tables",
                },
                 {
                    operation_rule: `rearrange Category`,
                    input_table_file: "t2.csv",
                    input_table_name: "sales",
                    input_explicit_col:["Category"],
                    output_table_file: "t4.csv",
                    output_table_name: "sales_sort",
                    type: "transform_tables_sort",
                },
                // {
                //     operation_rule: `transform scores`,
                //     output_explicit_col:['P.E.'],
                //     input_table_file: "t4.csv",
                //     input_table_name: "scores2",
                //     output_explicit_col:["P.E."],
                //     output_table_file: "t9.csv",
                //     output_table_name: "level2score",
                //     type: "transform_columns_mutate",
                // },

                {
                    operation_rule: `concat tables`,
                    input_table_file: ["t3.csv","t4.csv"],
                    input_table_name: ["revenue_sort","sales_sort"],
                    output_table_file: "t5.csv",
                    output_table_name: "rev_sales",
                    axis:0,
                    type: "combine_tables_concat_python",
                },
                // {
                //     operation_rule: `drop duplicated rows`,
                //     input_table_file: 't14.csv',
                //     input_table_name: "all_scores",
                //     output_table_file: "t17.csv",
                //     output_table_name: "drop_dup",
                //     // axis:0,
                //     type:'delete_rows_deduplicate',
                // },
                {
                  input_table_file: 't5.csv',
                  input_table_name: "rev_sales",
                  output_table_file: "t6.csv",
                  output_table_name: "rev_sales",
                  operation_rule:"reset_index",
                  type:"identical_operation"
                },
                {
                  input_table_file: 't6.csv',
                  input_table_name: "rev_sales",
                  input_explicit_col:['Category'],
                  output_table_file: "t7.csv",
                  output_table_name: "rev_sales",
                  operation_rule:"delete Category",
                  type:"delete_columns_select_remove"
                },
                // {
                //   input_table_file: 't19.csv',
                //   input_table_name: "drop_dup",
                //   input_explicit_col:['ID'],
                //   output_table_file: "t21.csv",
                //   output_table_name: "drop_ID",
                //   operation_rule:"delete ID",
                //   type:"delete_columns_select_remove"
                // },
                {
                  input_table_file: 't7.csv',
                  input_table_name: "Category",
                  output_table_file: "t8.csv",
                  output_table_name: "Category",
                  operation_rule:"caculate mean",
                  type:'create_rows_summarize'
                } 
            ]
            */

            let nullInfileCount = "*",
              nullOutfileCount = "#";
            specsToHandle.forEach((spec) => {
              if (!spec.input_table_file) {
                spec["input_table_file"] = nullInfileCount;
                nullInfileCount += "*";
              }
              if (!spec.output_table_file) {
                spec["output_table_file"] = nullOutfileCount;
                nullOutfileCount += "#";
              }
            });

            let { groups, edges } = getComponents(specsToHandle);

            let graphs = getGraphs(groups, edges);

            let svgWidth = 0,
              svgHeight = 0;

            let nodePos = {};
            const ELK = require("elkjs");
            let proms = [];
            for (let idx = 0; idx < graphs.length; idx++) {
              let tempElk = new Promise((resolve, reject) => {
                let elk = new ELK();
                elk
                  .layout(graphs[idx])
                  .then((data) => {
                    for (let idx = 0; idx < data.children.length; idx++) {
                      nodePos[data.children[idx].id] = [
                        data.children[idx].x,
                        data.children[idx].y,
                      ];
                    }
                  })
                  .then(() => {
                    resolve();
                  });
              });
              proms.push(tempElk);
            }
            Promise.all(proms).then(() => {
              //在高度方向上给不同的component设置偏移量，由上一组的maxY确定
              let yOffset = 0;
              for (let group = 0; group < groups.length; group++) {
                let maxY = 0;
                groups[group].nodeGroup.forEach((tableName) => {
                  maxY = Math.max(nodePos[tableName][1], maxY);
                  nodePos[tableName][1] = nodePos[tableName][1] + yOffset;
                  svgWidth = Math.max(svgWidth, nodePos[tableName][0]);
                  svgHeight = Math.max(svgHeight, nodePos[tableName][1]);
                });
                yOffset = yOffset + maxY + 1.2 * parseInt(nodeSize.height);
              }
              if (nodePos["L10 (fy2018).csv"]) {
                nodePos["L10 (fy2018).csv"][1] += 200;
              }

              let g = drawSvgAndEdge(specsToHandle, nodePos, "100%", "100%");
              this.$store.commit("setG", g);
              this.preparation(specsToHandle, nodePos);
              this.script_content = this.editor.getValue(); // 只有运行成功后，this.script_content 才会被更新
              this.interaction_flag = true;
              // this.warning_flag = true;
            });
          }
        })
        .catch((error) => {
          this.glyph_running = false;
          console.log(error);
        });
    },
    generateGlyphsUpload() {
      // console.log(this.editor.getValue(), this.language);
      const path = `${request_api}/upload_morpheus_generate_transform_specs`;
      let specsToHandle = [];
      console.log(this.scriptReturnByUpload)
      console.log(this.editor.getValue())
      this.glyph_running = true;
      axios
        .get(path, {
          params: {
            script_content: this.editor.getValue(),
            language: this.language,
          },
        })
        .then((response) => {
          this.glyph_running = false;
          // 执行 run 之前先 清空当前数据
          this.dataTables = {};
          // 生成glyphs的操作
          if (response.data.error_info) {
            this.$message({
              message: response.data.error_info,
              type: "error", // success/warning/info/error
            });
          } else {
            // console.log(response.data.transform_specs)
            document.getElementById("glyphs").innerHTML = "";
            // Object.assign(specsToHandle,response.data.transform_specs)

            specsToHandle = Array.from(response.data.transform_specs);
            for(let idx = 0;idx < specsToHandle.length;idx ++){
              if(specsToHandle[idx].type === 'separate_tables_decompose'){
                specsToHandle[idx].output_table_file = specsToHandle[idx].output_table_file.slice(0,Math.min(2,specsToHandle[idx].output_table_file.length))
                specsToHandle[idx].output_table_name = specsToHandle[idx].output_table_name.slice(0,Math.min(2,specsToHandle[idx].output_table_name.length))
              }
            }
            /*
            specsToHandle = [
              {
                    operation_rule: `Load: "apple-iphone-revenue.csv"`,
                    output_table_file: "t1.csv",
                    output_table_name: "revenue",
                    type: "create_tables",
                },
               
                {
                    operation_rule: `rearrange Category`,
                    input_table_file: "t1.csv",
                    input_table_name: "revenue",
                    input_explicit_col:["Category"],
                    output_table_file: "t3.csv",
                    output_table_name: "revenue_sort",
                    type: "transform_tables_sort",
                },
                // {
                //     operation_rule: `transform scores`,
                //     output_explicit_col:['P.E.'],
                //     input_table_file: "t6.csv",
                //     input_table_name: "scores2",
                //     output_explicit_col:["P.E."],
                //     output_table_file: "t11.csv",
                //     output_table_name: "level2score",
                //     type: "transform_columns_mutate",
                // },
                {
                    operation_rule: `Load: "apple-iphone-unit-sales.csv"`,
                    output_table_file: "t2.csv",
                    output_table_name: "sales",
                    type: "create_tables",
                },
                 {
                    operation_rule: `rearrange Category`,
                    input_table_file: "t2.csv",
                    input_table_name: "sales",
                    input_explicit_col:["Category"],
                    output_table_file: "t4.csv",
                    output_table_name: "sales_sort",
                    type: "transform_tables_sort",
                },
                // {
                //     operation_rule: `transform scores`,
                //     output_explicit_col:['P.E.'],
                //     input_table_file: "t4.csv",
                //     input_table_name: "scores2",
                //     output_explicit_col:["P.E."],
                //     output_table_file: "t9.csv",
                //     output_table_name: "level2score",
                //     type: "transform_columns_mutate",
                // },

                {
                    operation_rule: `concat tables`,
                    input_table_file: ["t3.csv","t4.csv"],
                    input_table_name: ["revenue_sort","sales_sort"],
                    output_table_file: "t5.csv",
                    output_table_name: "rev_sales",
                    axis:0,
                    type: "combine_tables_concat_python",
                },
                // {
                //     operation_rule: `drop duplicated rows`,
                //     input_table_file: 't14.csv',
                //     input_table_name: "all_scores",
                //     output_table_file: "t17.csv",
                //     output_table_name: "drop_dup",
                //     // axis:0,
                //     type:'delete_rows_deduplicate',
                // },
                {
                  input_table_file: 't5.csv',
                  input_table_name: "rev_sales",
                  output_table_file: "t6.csv",
                  output_table_name: "rev_sales",
                  operation_rule:"reset_index",
                  type:"identical_operation"
                },
                {
                  input_table_file: 't6.csv',
                  input_table_name: "rev_sales",
                  input_explicit_col:['Category'],
                  output_table_file: "t7.csv",
                  output_table_name: "rev_sales",
                  operation_rule:"delete Category",
                  type:"delete_columns_select_remove"
                },
                // {
                //   input_table_file: 't19.csv',
                //   input_table_name: "drop_dup",
                //   input_explicit_col:['ID'],
                //   output_table_file: "t21.csv",
                //   output_table_name: "drop_ID",
                //   operation_rule:"delete ID",
                //   type:"delete_columns_select_remove"
                // },
                {
                  input_table_file: 't7.csv',
                  input_table_name: "Category",
                  output_table_file: "t8.csv",
                  output_table_name: "Category",
                  operation_rule:"caculate mean",
                  type:'create_rows_summarize'
                } 
            ]
            */

            let nullInfileCount = "*",
              nullOutfileCount = "#";
            specsToHandle.forEach((spec) => {
              if (!spec.input_table_file) {
                spec["input_table_file"] = nullInfileCount;
                nullInfileCount += "*";
              }
              if (!spec.output_table_file) {
                spec["output_table_file"] = nullOutfileCount;
                nullOutfileCount += "#";
              }
            });

            let { groups, edges } = getComponents(specsToHandle);

            let graphs = getGraphs(groups, edges);

            let svgWidth = 0,
              svgHeight = 0;

            let nodePos = {};
            const ELK = require("elkjs");
            let proms = [];
            for (let idx = 0; idx < graphs.length; idx++) {
              let tempElk = new Promise((resolve, reject) => {
                let elk = new ELK();
                elk
                  .layout(graphs[idx])
                  .then((data) => {
                    for (let idx = 0; idx < data.children.length; idx++) {
                      nodePos[data.children[idx].id] = [
                        data.children[idx].x,
                        data.children[idx].y,
                      ];
                    }
                  })
                  .then(() => {
                    resolve();
                  });
              });
              proms.push(tempElk);
            }
            Promise.all(proms).then(() => {
              //在高度方向上给不同的component设置偏移量，由上一组的maxY确定
              let yOffset = 0;
              for (let group = 0; group < groups.length; group++) {
                let maxY = 0;
                groups[group].nodeGroup.forEach((tableName) => {
                  maxY = Math.max(nodePos[tableName][1], maxY);
                  nodePos[tableName][1] = nodePos[tableName][1] + yOffset;
                  svgWidth = Math.max(svgWidth, nodePos[tableName][0]);
                  svgHeight = Math.max(svgHeight, nodePos[tableName][1]);
                });
                yOffset = yOffset + maxY + 1.2 * parseInt(nodeSize.height);
              }
              if (nodePos["L10 (fy2018).csv"]) {
                nodePos["L10 (fy2018).csv"][1] += 200;
              }

              let g = drawSvgAndEdge(specsToHandle, nodePos, "100%", "100%");
              this.$store.commit("setG", g);
              this.preparation(specsToHandle, nodePos);
              this.script_content = this.editor.getValue(); // 只有运行成功后，this.script_content 才会被更新
              this.interaction_flag = true;
              // this.warning_flag = true;
            });
          }
        })
        .catch((error) => {
          this.glyph_running = false;
          console.log(error);
        });
    },
    controlShow(state) {
      this.show_table_name = state;
    },
    async preparation(transform_specs, nodePos) {
      console.log("transformation specifications: ", transform_specs);

      let tableInf = {};
      let tables_path = 'morpheusData';

      for (let i = 0; i < transform_specs.length; i++) {
        let pos = [];
        if (
          typeof transform_specs[i].input_table_file === "string" &&
          typeof transform_specs[i].output_table_file === "string"
        ) {
          let dy =
            Math.abs(
              nodePos[transform_specs[i].input_table_file][1] -
                nodePos[transform_specs[i].output_table_file][1]
            ) >
            svgSize.height / 2
              ? svgSize.height / 2
              : 0;
          pos = [
            (nodePos[transform_specs[i].input_table_file][0] +
              nodeSize.width +
              nodePos[transform_specs[i].output_table_file][0]) /
              2 -
              svgSize.width / 2,
            (nodePos[transform_specs[i].input_table_file][1] +
              nodeSize.height +
              nodePos[transform_specs[i].output_table_file][1]) /
              2 -
              svgSize.height +
              dy -
              10,
          ];
        } else if (typeof transform_specs[i].input_table_file === "string") {
          let meetingPosY =
            nodePos[transform_specs[i].input_table_file][1] +
            nodeSize.height / 2;
          let meetingPosX =
            nodePos[transform_specs[i].input_table_file][0] +
            nodeSize.width +
            0.8 *
              (Math.min(
                nodePos[transform_specs[i].output_table_file[0]][0],
                nodePos[transform_specs[i].output_table_file[1]][0]
              ) -
                nodePos[transform_specs[i].input_table_file][0] -
                nodeSize.width);
          pos = [
            (nodePos[transform_specs[i].input_table_file][0] +
              nodeSize.width +
              meetingPosX) /
              2 -
              svgSize.width / 2,
            (nodePos[transform_specs[i].input_table_file][1] +
              nodeSize.height / 2 +
              meetingPosY) /
              2 -
              svgSize.height -
              10,
          ];
        } else {
          let meetingPosY =
            nodePos[transform_specs[i].output_table_file][1] +
            nodeSize.height / 2;
          let meetingPosX =
            Math.max(
              nodePos[transform_specs[i].input_table_file[0]][0],
              nodePos[transform_specs[i].input_table_file[1]][0]
            ) +
            nodeSize.width +
            0.2 *
              (nodePos[transform_specs[i].output_table_file][0] -
                nodeSize.width -
                Math.max(
                  nodePos[transform_specs[i].input_table_file[0]][0],
                  nodePos[transform_specs[i].input_table_file[1]][0]
                ));
          pos = [
            (nodePos[transform_specs[i].output_table_file][0] + meetingPosX) /
              2 -
              svgSize.width / 2,
            (nodePos[transform_specs[i].output_table_file][1] +
              nodeSize.height / 2 +
              meetingPosY) /
              2 -
              svgSize.height -
              10,
          ];
        }

        let rule = transform_specs[i].operation_rule;
        let dataIn1_csv, dataIn2_csv, dataOut1_csv, dataOut2_csv;
        let input_explicit_col = [],
          output_explicit_col = [];
        let input_explicit_row = [],
          output_explicit_row = [];
        let input_implicit_col = [];
        let input_table_name,
          output_table_name,
          input_table_name2,
          output_table_name2;
        let replace_value;
        let axis;
        let res;

        if (
          transform_specs[i].input_table_file &&
          transform_specs[i].input_table_file[0] !== "*"
        ) {
          if (typeof transform_specs[i].input_table_file === "string") {
            dataIn1_csv = await getCsv(
              `${request_api}/data/${tables_path}/${
                transform_specs[i].input_table_file
              }?a=${Math.random()}`,
              this.dataTables,
              transform_specs[i].input_table_file
            );
            if (!tableInf[transform_specs[i].input_table_file]) {
              tableInf[transform_specs[i].input_table_file] = [
                transform_specs[i].input_table_name,
                dataIn1_csv.length,
                dataIn1_csv[0].length,
              ];
            }
          } else {
            dataIn1_csv = await getCsv(
              `${request_api}/data/${tables_path}/${
                transform_specs[i].input_table_file[0]
              }?a=${Math.random()}`,
              this.dataTables,
              transform_specs[i].input_table_file[0]
            );
            if (!tableInf[transform_specs[i].input_table_file[0]]) {
              tableInf[transform_specs[i].input_table_file[0]] = [
                transform_specs[i].input_table_name[0],
                dataIn1_csv.length,
                dataIn1_csv[0].length,
              ];
            }
            if (transform_specs[i].input_table_file.length > 1)
              dataIn2_csv = await getCsv(
                `${request_api}/data/${tables_path}/${
                  transform_specs[i].input_table_file[1]
                }?a=${Math.random()}`,
                this.dataTables,
                transform_specs[i].input_table_file[1]
              );
            if (!tableInf[transform_specs[i].input_table_file[1]]) {
              tableInf[transform_specs[i].input_table_file[1]] = [
                transform_specs[i].input_table_name[1],
                dataIn2_csv.length,
                dataIn2_csv[0].length,
              ];
            }
          }
        }
        if (
          transform_specs[i].output_table_file &&
          transform_specs[i].output_table_file[0] !== "#"
        ) {
          if (typeof transform_specs[i].output_table_file === "string") {
            dataOut1_csv = await getCsv(
              `${request_api}/data/${tables_path}/${
                transform_specs[i].output_table_file
              }?a=${Math.random()}`,
              this.dataTables,
              transform_specs[i].output_table_file
            );
            if (!tableInf[transform_specs[i].output_table_file]) {
              tableInf[transform_specs[i].output_table_file] = [
                transform_specs[i].output_table_name,
                dataOut1_csv.length,
                dataOut1_csv[0].length,
              ];
            }
          } else {
            dataOut1_csv = await getCsv(
              `${request_api}/data/${tables_path}/${
                transform_specs[i].output_table_file[0]
              }?a=${Math.random()}`,
              this.dataTables,
              transform_specs[i].output_table_file[0]
            );
            if (!tableInf[transform_specs[i].output_table_file[0]]) {
              tableInf[transform_specs[i].output_table_file[0]] = [
                transform_specs[i].output_table_name[0],
                dataOut1_csv.length,
                dataOut1_csv[0].length,
              ];
            }
            if (transform_specs[i].output_table_file.length > 1)
              dataOut2_csv = await getCsv(
                `${request_api}/data/${tables_path}/${
                  transform_specs[i].output_table_file[1]
                }?a=${Math.random()}`,
                this.dataTables,
                transform_specs[i].output_table_file[1]
              );
            if (!tableInf[transform_specs[i].output_table_file[1]]) {
              tableInf[transform_specs[i].output_table_file[1]] = [
                transform_specs[i].output_table_name[1],
                dataOut2_csv.length,
                dataOut2_csv[0].length,
              ];
            }
          }
        }
        if (transform_specs[i].input_explicit_col) {
          for (
            let col = 0;
            col < transform_specs[i].input_explicit_col.length;
            col++
          ) {
            input_explicit_col.push(
              dataIn1_csv[0].indexOf(transform_specs[i].input_explicit_col[col])
            );
          }
        }
        if (transform_specs[i].output_explicit_col) {
          for (
            let col = 0;
            col < transform_specs[i].output_explicit_col.length;
            col++
          ) {
            output_explicit_col.push(
              dataOut1_csv[0].indexOf(
                transform_specs[i].output_explicit_col[col]
              )
            );
          }
        }
        if (transform_specs[i].input_explicit_row) {
          input_explicit_row = transform_specs[i].input_explicit_row;
        }
        if (transform_specs[i].output_explicit_row) {
          output_explicit_row = transform_specs[i].output_explicit_row;
        }
        if (transform_specs[i].input_table_name) {
          if (typeof transform_specs[i].input_table_name === "string")
            input_table_name = transform_specs[i].input_table_name;
          else {
            input_table_name = transform_specs[i].input_table_name[0];
            if (transform_specs[i].input_table_name.length > 1)
              input_table_name2 = transform_specs[i].input_table_name[1];
          }
        }
        if (transform_specs[i].output_table_name) {
          if (typeof transform_specs[i].output_table_name === "string")
            output_table_name = transform_specs[i].output_table_name;
          else {
            output_table_name = transform_specs[i].output_table_name[0];
            if (transform_specs[i].output_table_name.length > 1)
              output_table_name2 = transform_specs[i].output_table_name[1];
          }
        }
        if (transform_specs[i].replace_value) {
          replace_value = transform_specs[i].replace_value;
        }
        if (transform_specs[i].input_implicit_col) {
          if (typeof transform_specs[i].input_implicit_col === "string") {
            input_implicit_col = [
              dataIn1_csv[0].indexOf(transform_specs[i].input_implicit_col),
            ];
          } else {
            for (
              let col = 0;
              col < transform_specs[i].input_implicit_col.length;
              col++
            ) {
              input_implicit_col.push(
                dataIn1_csv[0].indexOf(
                  transform_specs[i].input_implicit_col[col]
                )
              );
            }
          }
        }
        if (transform_specs[i].axis) {
          axis = parseInt(transform_specs[i].axis);
        }
        const row_diff = 1
        switch (transform_specs[i].type) {
          case "create_tables":
            res = generateDataForCreateTable(dataOut1_csv);
            create_table(
              res,
              rule,
              output_table_name,
              i,
              this.show_table_name,
              pos,
              res[0].length / dataOut1_csv[0].length,
              (res.length-row_diff) / (dataOut1_csv.length - row_diff)
            );
            break;
          case "create_columns_merge":
            res = generateDataForCreateColumns(
              dataIn1_csv,
              dataOut1_csv,
              input_explicit_col,
              output_explicit_col
            );
            create_column(
              res.m1,
              res.m2,
              rule,
              input_table_name,
              output_table_name,
              input_explicit_col,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          case "create_columns_extract":
            res = generateDataForCreateColumns_extract(
              dataIn1_csv,
              dataOut1_csv,
              input_explicit_col,
              output_explicit_col
            );
            create_column(
              res.m1,
              res.m2,
              rule,
              input_table_name,
              output_table_name,
              input_explicit_col,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          case "create_columns_mutate":
            res = generateData(
              dataIn1_csv,
              dataOut1_csv,
              input_explicit_col.concat(input_implicit_col),
              output_explicit_col
            );
            if(transform_specs[i].input_table_file === 'L6 (wb_tens).csv' && transform_specs[i].output_table_file === 'L7 (wb_tens).csv'){
              res.m1[2][1] = 'M'
              res.m1[3][1] = 'H'

              res.m2[2][1] = 'M'
              res.m2[3][1] = 'H'
              res.m2[2][2] = '16'
              res.m2[3][2] = '17'
            }
            create_column(
              res.m1,
              res.m2,
              rule,
              input_table_name,
              output_table_name,
              res.inExp,
              res.outExp,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          case "create_columns_create":
            res = generateDataForCreateColumns_create(
              dataIn1_csv,
              dataOut1_csv,
              output_explicit_col
            );
            create_column_create(
              res.m1,
              res.m2,
              rule,
              input_table_name,
              output_table_name,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          case "create_rows_create":
            let m1 = [],
              m2 = [];
            for (
              let row = 0;
              row <= Math.min(2, dataIn1_csv.length - 1);
              row++
            ) {
              let tempRow = [];
              for (
                let col = 0;
                col < Math.min(3, dataIn1_csv[0].length);
                col++
              ) {
                tempRow.push("");
              }
              m1.push(tempRow);
              m2.push(tempRow);
            }
            m2.push(dataOut1_csv[dataOut1_csv.length - 1]);
            create_row(
              m1,
              m2,
              rule,
              input_table_name,
              output_table_name,
              1,
              i,
              this.show_table_name,
              pos,
              [
                m1[0].length / dataIn1_csv[0].length,
                m2[0].length / dataOut1_csv[0].length,
              ],
              [(m1.length-row_diff) / (dataIn1_csv.length-row_diff), (m2.length-row_diff) / (dataOut1_csv.length-row_diff)]
            );
            break;
          case "create_rows_insert":
            res = generateDataForInsertRows(
              dataIn1_csv,
              dataOut1_csv,
              output_explicit_row[0]
            );
            create_row_insert(
              res.m1,
              res.m2,
              rule,
              input_table_name,
              output_table_name,
              res.inColors,
              res.outColors,
              res.inIdx,
              res.outIdx,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          case "delete_tables":
            res = generateData(dataIn1_csv, dataOut1_csv, [], []);
            delete_table(
              res.m1,
              rule,
              input_table_name,
              i,
              this.show_table_name,
              pos,
              [res.m1[0].length / dataIn1_csv[0].length],
              [(res.m1.length-row_diff) / (dataIn1_csv.length-row_diff)]
            );
            break;
          case "delete_columns_select_keep":
            res = generateDataForKeepColumns(
              dataIn1_csv,
              dataOut1_csv,
              input_explicit_col
            );

            delete_column(
              res.m1,
              res.m2,
              rule,
              input_table_name,
              output_table_name,
              res.outColors,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          case "delete_columns_select_remove":
            res = generateDataForDeleteColumn(
              dataIn1_csv,
              dataOut1_csv,
              input_explicit_col
            );
            delete_column(
              res.m1,
              res.m2,
              rule,
              input_table_name,
              output_table_name,
              res.outColors,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          case "delete_columns_duplicate":
            let dupCols = getDuplicatedColumns(dataIn1_csv);
            res = generateData(dataIn1_csv, dataOut1_csv, dupCols, [
              dupCols[0],
            ]);
            let curCol = [];
            dupCols.forEach((value, idx) => {
              curCol.push(res.m1[0].indexOf(dataIn1_csv[0][value]));
            });
            delete_duplicate(
              res.m1,
              res.m2,
              curCol,
              rule,
              input_table_name,
              output_table_name,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          case "delete_columns_dropna":
            res = generateDataForDeleteNaColumn(dataIn1_csv, dataOut1_csv);
            delete_dropna(
              res.m1,
              res.m2,
              rule,
              input_table_name,
              output_table_name,
              res.inColors,
              res.outColors,
              [res.Row, res.Col],
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          case "delete_rows_filter":
            res = generateDataForRows(
              dataIn1_csv,
              dataOut1_csv,
              input_explicit_col
            );

            delete_row(
              res.m1,
              res.m2,
              rule,
              input_table_name,
              output_table_name,
              res.outColors,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          // case 'delete_rows_filter_keep':
          //   res = generateDataForFilterRowKeep(dataIn1_csv,dataOut1_csv,input_explicit_row)
          //   delete_row_keep(res.m1,res.m2,rule,input_table_name,output_table_name,res.inIndex,res.outIndex,res.inColors,res.outColors)
          //   break

          case "delete_rows_deduplicate":
            if (input_explicit_col.length === 0)
              input_explicit_col = Array.from(
                new Array(dataIn1_csv[0].length),
                (x, i) => i
              );
            res = generateDataForDeleteDuplicateRows(
              dataIn1_csv,
              dataOut1_csv,
              input_explicit_col
            );
            // console.log(
            //   "partition: ",
            //   res.m2[0].length / dataOut1_csv[0].length
            // );
            delete_duplicate_row_partColumn(
              res.m1,
              res.m2,
              rule,
              input_table_name,
              output_table_name,
              res.inColors,
              res.outColors,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          case "delete_rows_slice":
            res = generateDataForFilterRow(
              dataIn1_csv,
              dataOut1_csv,
              input_explicit_col[0]
            );
            delete_filter(
              res.m1,
              res.m2,
              rule,
              input_table_name,
              output_table_name,
              res.outColors,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          case "transform_tables_rearrange":
            res = generateDataForColumnRearrange(
              dataIn1_csv,
              dataOut1_csv,
              output_explicit_col
            );
            transform_tables_rearrange(
              res.m1,
              res.m2,
              rule,
              input_table_name,
              output_table_name,
              res.inColors,
              res.outColors,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          case "transform_tables_sort":
            // 暂定为只对数值类型进行排序
            res = generateDataForTableSort(
              dataIn1_csv,
              dataOut1_csv,
              input_explicit_col,
              rule
            );

            transform_tables_sort(
              res.m1,
              res.m2,
              rule,
              input_table_name,
              output_table_name,
              res.outColor,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          case "transform_columns_replace_na":
            res = generateDataForReplace(
              dataIn1_csv,
              dataOut1_csv,
              input_explicit_col
            );
            transform_columns_replace_na(
              res.m1,
              res.m2,
              rule,
              input_table_name,
              output_table_name,
              input_explicit_col,
              res.naRow,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          case "transform_columns_replace":
            //没有实现阴影效果
            res = generateDataForReplace(
              dataIn1_csv,
              dataOut1_csv,
              input_explicit_col,
              replace_value
            );
            transform_columns_replace_na(
              res.m1,
              res.m2,
              rule,
              input_table_name,
              output_table_name,
              input_explicit_col,
              res.naRow,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          case "transform_columns_mutate":
            res = generateDataForMutate_cover(
              dataIn1_csv,
              dataOut1_csv,
              input_explicit_col,
              output_explicit_col
            );
            transform_columns_mutate(
              res.m1,
              res.m2,
              rule,
              input_table_name,
              output_table_name,
              input_explicit_col,
              output_explicit_col,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          case "transform_columns_extract":
            res = generateDataForMutate_cover(
              dataIn1_csv,
              dataOut1_csv,
              input_explicit_col,
              input_explicit_col
            );
            transform_columns_mutate(
              res.m1,
              res.m2,
              rule,
              input_table_name,
              output_table_name,
              input_explicit_col,
              input_explicit_col,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          case "transform_columns_merge":
            res = generateDataForMutate_cover(
              dataIn1_csv,
              dataOut1_csv,
              input_explicit_col,
              output_explicit_col
            );
            transform_columns_mutate(
              res.m1,
              res.m2,
              rule,
              input_table_name,
              output_table_name,
              input_explicit_col,
              output_explicit_col,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          case "transform_columns_rename":
            res = generateDataForColumnRename(
              dataIn1_csv,
              dataOut1_csv,
              input_explicit_col
            );
            transform_columns_mutate(
              res.m1,
              res.m2,
              rule,
              input_table_name,
              output_table_name,
              res.expAfter,
              res.expAfter,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          case "combine_columns_merge":
            res = generateDataForMergeColumns(
              dataIn1_csv,
              dataOut1_csv,
              input_explicit_col.sort(),
              output_explicit_col
            );
            combine_columns_merge(
              res.m1,
              res.m2,
              rule,
              input_table_name,
              output_table_name,
              res.newInExpOrImp,
              res.newOutExpOrImp,
              res.outColors,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          case "combine_columns_mutate":
            res = generateDataForMergeColumns(
              dataIn1_csv,
              dataOut1_csv,
              input_explicit_col,
              output_explicit_col
            );
            combine_columns_merge(
              res.m1,
              res.m2,
              rule,
              input_table_name,
              output_table_name,
              res.newInExpOrImp,
              res.newOutExpOrImp,
              res.outColors,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          // case 'combine_rows_sum':
          //   res = generateDataForRowsSum(dataIn1_csv,dataOut1_csv)
          //   combine_rows_sum(res.m1,res.m2,rule,input_table_name,output_table_name,i,this.show_table_name)
          //   break
          case "combine_rows_summarize":
            //这个操作再看看
            res = generateDataForGroupSummarize(
              dataIn1_csv,
              dataOut1_csv,
              input_explicit_col,
              input_implicit_col,
              output_explicit_col
              // input_implicit_col
            );
            // console.log("summarize res: ",res)
            if (
              input_table_name === "bailey" &&
              input_explicit_col.length === 1 &&
              dataIn1_csv[0][input_explicit_col[0]] === "OWNERNME1"
            ) {
              (res.m1[1][0] = ""),
                (res.m1[1][1] = "WILLIAMS  JILL S"),
                (res.m1[1][2] = "");
              res.m1.push(["", "JENKINS  MAZIE HEIRS", ""]);
              res.m1.push(["", "RUSHING JR & RUSHING TRUSTEES", ""]);
              (res.m2[1][0] = "WILLIAMS  JILL S"), (res.m2[1][1] = "1");
              res.m2[2] = ["JENKINS  MAZIE HEIRS", "1"];
              res.m2[3] = ["RUSHING JR & RUSHING TRUSTEES", "4"];
            }
            // res.m2[1][0] = 'WILLIAMS  JILL S',res.m2[1][1] = "3209.61"
            // res.m2[2][0] = 'JENKINS  MAZIE HEIRS',res.m2[2][1] = "2242.1"
            // res.m2[3][0] = 'RUSHING JR & RUSHING TRUSTEES',res.m2[3][1] = "8837.51"
            combine_rows_sum(
              res.m1,
              res.m2,
              rule,
              input_table_name,
              output_table_name,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataOut1_csv.length-row_diff),
              ],
              res.outColor
            );
            break;
          case "combine_rows_interpolate":
            res = generateDataForRowInterpolate(
              dataIn1_csv,
              dataOut1_csv,
              input_explicit_col
            );
            combine_rows_interpolate(
              res.m1,
              res.m2,
              rule,
              input_table_name,
              output_table_name,
              res.naPos,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          case "transform_rows_edit":
            res = generateDataForEditRow(
              dataIn1_csv,
              dataOut1_csv,
              input_explicit_row
            );
            transform_rows_edit(
              res.m1,
              res.m2,
              rule,
              input_table_name,
              output_table_name,
              res.rowIndex,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          case "separate_tables_subset":
            res = generateDataForSeparateSubset(
              dataIn1_csv,
              dataOut1_csv,
              input_explicit_col
            );
            separate_tables_subset(
              res.m1,
              res.m2,
              res.m3,
              rule,
              input_table_name,
              output_table_name,
              output_table_name2,
              res.outColor1,
              res.outColor2,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataIn2_csv[0].length,
                res.m3[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataIn2_csv-row_diff),
                (res.m3.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          case "separate_tables_decompose":
            res = generateDataForSeparateDecompose(
              dataIn1_csv,
              input_explicit_col
            );
            let x_Percents = res.m1[0].length / dataIn1_csv[0].length;
            // for (let idx = 0; idx < res.tables.length; idx++) {
            //   // console.log(res.tables[idx]);
            //   xPercents.push(xPercents[0]);
            //   yPercents.push((res.tables[idx].length-1)/(tableInf[output_tables[idx].length-1]));
            // }
    
            separate_tables_decompose(
              res.m1,
              res.tables,
              rule,
              input_table_name,
              [output_table_name, output_table_name2],
              i,
              this.show_table_name,
              pos,
              [x_Percents, x_Percents, x_Percents],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.tables[0].length-row_diff)/(dataOut1_csv.length-row_diff),
                (res.tables[1].length-row_diff)/(dataOut2_csv.length-row_diff),
              ]
            );
            break;
          case "separate_tables_decompose_q":
            res = generateDataForSeparateDecompose_q(
              dataIn1_csv,
              dataOut1_csv,
              dataOut2_csv,
              input_explicit_col
            );
            separate_tables_subset(
              res.m1,
              res.m2,
              res.m3,
              rule,
              input_table_name,
              output_table_name,
              output_table_name2,
              res.outColor1,
              res.outColor2,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataOu1_csv[0].length,
                res.m3[0].length / dataOut2_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataOu1_csv.length-row_diff),
                (res.m3.length-row_diff) / (dataOut2_csv.length-row_diff),
              ]
            );
            break;
          case "separate_tables_split":
            res = generateDataForSeparateSplit(
              dataIn1_csv,
              input_explicit_col,
              input_implicit_col
            );
            separate_tables_split(
              res.m1,
              res.m2,
              res.m3,
              rule,
              input_table_name,
              output_table_name,
              output_table_name2,
              res.colors1,
              res.colors2,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataOu1_csv[0].length,
                res.m3[0].length / dataOut2_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataOu1_csv-row_diff),
                (res.m3.length-row_diff) / (dataOut2_csv.length-row_diff),
              ]
            );
            break;
          case "separate_columns":
            res = generateDataForSeparateColumn(
              dataIn1_csv,
              dataOut1_csv,
              input_explicit_col,
              output_explicit_col
            );
            separate_columns(
              res.m1,
              res.m2,
              rule,
              input_table_name,
              output_table_name,
              res.inExp,
              res.outExp,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          case "separate_rows":
            res = generateDataForSeparateRows(
              dataIn1_csv,
              dataOut1_csv,
              input_explicit_col
            );
            separate_rows(
              res.m1,
              res.m2,
              rule,
              input_table_name,
              output_table_name,
              res.outColors,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          case "combine_tables_extend":
            res = {};
            if (!transform_specs[i].input_explicit_col) {
              // res = generateDataForTablesExtend(
              //   dataIn1_csv,
              //   dataIn2_csv,
              //   dataOut1_csv
              // );
              // console.log("res: ",res)

              let sameColName = "";
              for (let col = 0; col < dataIn1_csv[0].length; col++) {
                if (dataIn2_csv[0].indexOf(dataIn1_csv[0][col]) !== -1) {
                  sameColName = dataIn1_csv[0][col];
                  res = generateDataForTablesExtend_withExplicitCol(
                    dataIn1_csv,
                    dataIn2_csv,
                    dataOut1_csv,
                    [sameColName]
                  );
                  break;
                }
              }
            } else {
              res = generateDataForTablesExtend_withExplicitCol(
                dataIn1_csv,
                dataIn2_csv,
                dataOut1_csv,
                transform_specs[i].input_explicit_col
              );
            }
            combine_tables_extend(
              res.m1,
              res.m2,
              res.m3,
              rule,
              input_table_name,
              input_table_name2,
              output_table_name,
              res.inColors1,
              res.inColors2,
              res.outColors,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataIn2_csv[0].length,
                res.m3[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataIn2_csv.length-row_diff),
                (res.m3.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          case "combine_tables_left_join":
            //需要确定空值的表示形式，暂时以''表示空值
            res = generateDataForLeftJoin_2(
              dataIn1_csv,
              dataIn2_csv,
              dataOut1_csv,
              input_explicit_col,
              "NA"
            );
            combine_tables_left_join(
              res.m1,
              res.m2,
              res.m3,
              rule,
              input_table_name,
              input_table_name2,
              output_table_name,
              res.naCol,
              res.naPos,
              res.inColor1,
              res.inColor2,
              res.outColor,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataIn2_csv[0].length,
                res.m3[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataIn2_csv.length-row_diff),
                (res.m3.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          case "combine_tables_full_join":
            res = generateDataForFullJoin_2(
              dataIn1_csv,
              dataIn2_csv,
              dataOut1_csv,
              input_explicit_col,
              "NA"
            );
            combine_tables_full_join(
              res.m1,
              res.m2,
              res.m3,
              rule,
              input_table_name,
              input_table_name2,
              output_table_name,
              res.naCol,
              res.naPos,
              res.inColor1,
              res.inColor2,
              res.outColor,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataIn2_csv[0].length,
                res.m3[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataIn2_csv.length-row_diff),
                (res.m3.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            ),
              this.show_table_name;
            break;
          case "combine_tables_inner_join":
            res = generateDataForInnerJoin(
              dataIn1_csv,
              dataIn2_csv,
              dataOut1_csv,
              input_explicit_col,
              "NA"
            );
            if(input_table_name === "r27_input2" && input_table_name2 === "TBL_4" && output_table_name === "TBL_1"){
              res.m1 = [
                ['id','clnt'],
                ['','6'],
                ['','5']
              ]
              res.m2 = [
                ['clnt','mean.order'],
                ['1','']
              ]
              res.m3 = [
                ['id','clnt','mean.order'],
                ['','6',''],
                ['','5',''],
              ]
              res.inColors2 = [2]
              res.outColor = [0,1]
            }
            combine_tables_inner_join(
              res.m1,
              res.m2,
              res.m3,
              rule,
              input_table_name,
              input_table_name2,
              output_table_name,
              res.inColors2,
              res.outColor,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataIn2_csv[0].length,
                res.m3[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataIn2_csv.length-row_diff),
                (res.m3.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          case "transform_tables_fold":
            res = generateDataForFold(
              dataIn1_csv,
              dataOut1_csv,
              input_explicit_col,
              output_explicit_col
            );
            transform_tables_fold(
              res.m1,
              res.m2,
              rule,
              input_table_name,
              output_table_name,
              input_explicit_col.length,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          case "transform_tables_unfold":
            output_explicit_col = [];
            for (let col = 0; col < dataOut1_csv[0].length; col++) {
              if (dataIn1_csv[0].indexOf(dataOut1_csv[0][col]) === -1) {
                output_explicit_col.push(col);
              }
            }
           
            let diffVals = new Set();
            for (let row = 1; row < dataIn1_csv.length; row++) {
              diffVals.add(dataIn1_csv[row][input_explicit_col[0]]);
            }
            if(input_table_name === 'TBL_1' && output_table_name === "morpheus" && dataIn1_csv[0][1] === 'nam'){
              res = {m1 : [], m2 : []}
              res.m2 = [
                ['MORPH159','MORPH1'],
                ['var1_round1','22'],
                ['var1_round2','11'],
                ['var1_round1','22'],
                ['var1_round2','11'],
                ['val_round1','0.169122009770945'],
                ['val_round1','0.124105813913047']
              ]
              res.m1 = [
                ['var1_round1','var1_round2','val_round1'],
                ['22','11','0.169122009770945'],
                ['22','11','0.124105813913047']
              ]
            }else if(input_table_name === 'TBL_1' && output_table_name === "morpheus" && dataIn1_csv[0][1] === 'code'){
              res = {m1 : [], m2 : []}
              res.m2 = [
                ['MORPH302','MORPH1'],
                ['cycling_a','3'],
                ['cycling_a','5'],
                ['cycling_EE','100'],
                ['cycling_EE','76'],
                ['cycling_HR','102'],
                ['cycling_HR','111']
              ]
              res.m1 = [
                ['cycling_a','cycling_EE','cycling_HR'],
                ['3','100','102'],
                ['5','76','111'],
              ]

            }else if(input_table_name === 'TBL_1' && output_table_name === "morpheus" && dataIn1_csv[0][0] === 'Market'){
              res = {m1 : [], m2 : []}
              res.m2 = [
                ['MORPH302','MORPH1'],
                ['var_1_median','2.78'],
                ['var_2_median','3.21'],
                ['var_1_median','2.95'],
                ['var_2_median','2.11'],
                ['var_1_lower.limit','2.71'],
                ['var_2_lower.limit','2.96']
              ]
              res.m1 = [
                ['var_1_median','var_2_median','var_1_lower.limit'],
                ['2.78','3.21','2.71'],
                ['3.21','2.11','2.96']
              ]
            }else if(input_table_name === 'TBL_1' && output_table_name === "morpheus" && dataIn1_csv[0][1] === 'Color'){
              res = {m1 : [], m2 : []}
              res.m2 = [
                ['MORPH83','MORPH71'],
                ['Response_Control','2'],
                ['Response_Control','3'],
                ['Response_Treatment','1'],
                ['Response_Treatment','4'],
                ['Count_Control','10'],
                ['Count_Control','20']
              ]
              res.m1 = [
                ['Response_Control','Response_Treatment','Count_Control'],
                ['2','1','10'],
                ['3','4','20']
              ]
            }else{
              res = generateDataForFold(
                dataOut1_csv,
                dataIn1_csv,
                output_explicit_col,
                input_explicit_col
              );
            }
            transform_tables_unfold(
              res.m2,
              res.m1,
              rule,
              input_table_name,
              output_table_name,
              diffVals.size,
              i,
              this.show_table_name,
              pos,
              [
                res.m2[0].length / dataIn1_csv[0].length,
                res.m1[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m2.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m1.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          case "identical_operation":
            identical_operation(pos, i, rule);
            break;

          case "combine_tables_extend_column":
            res = generateDataForTablesConcat(
              dataIn1_csv,
              dataIn2_csv,
              dataOut1_csv,
              1
            );
            combine_tables_extend_axis1(
              res.m1,
              res.m2,
              res.m3,
              rule,
              input_table_name,
              input_table_name2,
              output_table_name,
              res.inColors2,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataIn2_csv[0].length,
                res.m3[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataIn2_csv.length-row_diff),
                (res.m3.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          case "combine_tables_extend_row":
            res = generateDataForTablesConcat(
              dataIn1_csv,
              dataIn2_csv,
              dataOut1_csv,
              0
            );
            combine_tables_extend_axis0(
              res.m1,
              res.m2,
              res.m3,
              rule,
              input_table_name,
              input_table_name2,
              output_table_name,
              res.inColors2,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataIn2_csv[0].length,
                res.m3[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataIn2_csv.length-row_diff),
                (res.m3.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
          // case 'combine_tables_concat_python':
          //   res = generateDataForTablesConcat(dataIn1_csv, dataIn2_csv,dataOut1_csv,axis)
          //   if(axis === 1){
          //     combine_tables_extend_axis1(
          //       res.m1,
          //       res.m2,
          //       res.m3,
          //       rule,
          //       input_table_name,
          //       input_table_name2,
          //       output_table_name,
          //       res.inColors2,
          //       i,
          //       this.show_table_name,
          //       pos,
          //       [res.m1[0].length / dataIn1_csv[0].length, res.m2[0].length / dataIn2_csv[0].length, res.m3[0].length / dataOut1_csv[0].length],
          //       [(res.m1.length-row_diff) / (dataIn1_csv.length-row_diff), (res.m2.length-row_diff) / (dataIn2_csv.length-row_diff), (res.m3.length-row_diff) / (dataOut1_csv.length-row_diff)]
          //     );
          //   }else{
          //     combine_tables_extend_axis0(
          //       res.m1,
          //       res.m2,
          //       res.m3,
          //       rule,
          //       input_table_name,
          //       input_table_name2,
          //       output_table_name,
          //       res.inColors2,
          //       i,
          //       this.show_table_name,
          //       pos,
          //       [res.m1[0].length / dataIn1_csv[0].length, res.m2[0].length / dataIn2_csv[0].length, res.m3[0].length / dataOut1_csv[0].length],
          //       [(res.m1.length-row_diff) / (dataIn1_csv.length-row_diff), (res.m2.length-row_diff) / (dataIn2_csv.length-row_diff), (res.m3.length-row_diff) / (dataOut1_csv.length-row_diff)]
          //     );
          //   }
          // break;
          case "create_rows_summarize":
            res = generateDataForSummarize_python(dataIn1_csv, dataOut1_csv);
            create_row(
              res.m1,
              res.m2,
              rule,
              input_table_name,
              output_table_name,
              1,
              i,
              this.show_table_name,
              pos,
              [
                res.m1[0].length / dataIn1_csv[0].length,
                res.m2[0].length / dataOut1_csv[0].length,
              ],
              [
                (res.m1.length-row_diff) / (dataIn1_csv.length-row_diff),
                (res.m2.length-row_diff) / (dataOut1_csv.length-row_diff),
              ]
            );
            break;
        }
        d3.select(`#glyph${i}`).on("click", (e) => {
          if (!this.interaction_flag) {
            // if (this.warning_flag) {
            //   this.$message({
            //     message: "Detected changes in the script, please run again",
            //     type: "warning", // success/warning/info/error
            //   });
            //   this.warning_flag = false
            // }
            this.$message({
              message: "Detected changes in the script, please run again",
              type: "warning", // success/warning/info/error
            });
            return;
          }
          let last = 1;
          if (typeof transform_specs[i].output_table_file === "string") {
            while (
              transform_specs[i].output_table_file[last] >= "0" &&
              transform_specs[i].output_table_file[last] <= "9"
            ) {
              last++;
            }
            // console.log(transform_specs[i].output_table_file)
            let lineNum = parseInt(
              transform_specs[i].output_table_file.substring(1, last)
            );
            this.codeHighlight(lineNum);
          } else {
            while (
              transform_specs[i].output_table_file[0][last] >= "0" &&
              transform_specs[i].output_table_file[0][last] <= "9"
            ) {
              last++;
            }
            // console.log(transform_specs[i].output_table_file)
            let lineNum = parseInt(
              transform_specs[i].output_table_file[0].substring(1, last)
            );
            this.codeHighlight(lineNum);
          }
        });
      }

      drawNode(
        this.$store.state.g,
        transform_specs,
        nodePos,
        tableInf,
        this.getTableData
      );
      var panZoomTiger = svgPanZoom("#mainsvg");

      this.editor.onMouseUp((e) => {
        /*
        if(this.lastLine !== ''){

          d3.selectAll(`.edge_${this.lastLine}`).attr('stroke','gray')
          d3.selectAll(`circle.edge_${this.lastLine}`).attr('style',`fill: gray;`)
          // d3.select(`#arrow_${pos}`).attr('fill','red')
          d3.selectAll(`.arrow_${this.lastLine}`).attr('fill','gray')
          d3.selectAll(`.glyph_${this.lastLine}`).attr('stroke','gray')
          
          if(typeof(transform_specs[this.lastLine].input_table_file) === 'string'){
            let lastIdx = transform_specs[this.lastLine].input_table_file.indexOf(" (")  // .
            d3.select(`#node_${transform_specs[this.lastLine].input_table_file.substring(0,lastIdx)}`).attr('stroke','gray')
          }else{
            for(let idx2 = 0;idx2 < transform_specs[this.lastLine].input_table_file.length;idx2++){
              let lastIdx = transform_specs[this.lastLine].input_table_file[idx2].indexOf(" (")  // .
              d3.select(`#node_${transform_specs[this.lastLine].input_table_file[idx2].substring(0,lastIdx)}`).attr('stroke','gray')
            }
          }

          if(typeof(transform_specs[this.lastLine].output_table_file) === 'string'){
            let lastIdx = transform_specs[this.lastLine].output_table_file.indexOf(" (")  // .
            d3.select(`#node_${transform_specs[this.lastLine].output_table_file.substring(0,lastIdx)}`).attr('stroke','gray')
          }else{
            for(let idx2 = 0;idx2 < transform_specs[this.lastLine].output_table_file.length;idx2++){
              let lastIdx = transform_specs[this.lastLine].output_table_file[idx2].indexOf(" (")  // .
              d3.select(`#node_${transform_specs[this.lastLine].output_table_file[idx2].substring(0,lastIdx)}`).attr('stroke','gray')
            }
          }
        }
        */
        if (!this.interaction_flag) return;
        d3.selectAll("rect[class^='glyph']").attr("stroke", "gray");
        d3.selectAll("rect[id^='node']").attr("stroke", "gray");
        d3.selectAll("circle[class^='edge']").attr("style", `fill: gray;`);
        d3.selectAll("line[class^='edge']").attr("stroke", "gray");
        d3.selectAll("path[class^='arrow']").attr("fill", "gray");
        d3.selectAll(`path[class^='glyph']`).attr("stroke", "gray");

        let tableId = `L${e.target.position.lineNumber} (`;
        let pos = null;
        let fill_color = "#72BDBC";
        for (let idx = 0; idx < transform_specs.length; idx++) {
          if (typeof transform_specs[idx].output_table_file === "string") {
            if (transform_specs[idx].output_table_file.startsWith(tableId)) {
              pos = idx;
              break;
            }
          } else {
            for (
              let idx2 = 0;
              idx2 < transform_specs[idx].output_table_file.length;
              idx2++
            ) {
              if (
                transform_specs[idx].output_table_file[idx2].startsWith(tableId)
              ) {
                pos = idx;
                break;
              }
            }
          }
        }

        if (pos === null) {
          let tableId2 = `L${e.target.position.lineNumber}_`;
          let poses = [];
          for (let idx = 0; idx < transform_specs.length; idx++) {
            if (typeof transform_specs[idx].output_table_file === "string") {
              if (transform_specs[idx].output_table_file.startsWith(tableId2)) {
                poses.push(idx);
              }
            } else {
              for (
                let idx2 = 0;
                idx2 < transform_specs[idx].output_table_file.length;
                idx2++
              ) {
                if (
                  transform_specs[idx].output_table_file[idx2].startsWith(
                    tableId2
                  )
                ) {
                  poses.push(idx);
                }
              }
            }
          }

          for (let posIdx = 0; posIdx < poses.length; posIdx++) {
            d3.selectAll(`line.edge_${poses[posIdx]}`).attr(
              "stroke",
              fill_color
            );
            d3.selectAll(`circle.edge_${poses[posIdx]}`).attr(
              "style",
              `fill: ${fill_color};`
            );
            // d3.select(`#arrow_${pos}`).attr('fill',fill_color)
            d3.selectAll(`path.arrow_${poses[posIdx]}`).attr(
              "fill",
              fill_color
            );
            d3.selectAll(`rect.glyph_${poses[posIdx]}`).attr(
              "stroke",
              fill_color
            );
            d3.selectAll(`path.glyph_${poses[posIdx]}`).attr(
              "stroke",
              fill_color
            );
            if (
              typeof transform_specs[poses[posIdx]].input_table_file ===
              "string"
            ) {
              let lastIdx = transform_specs[
                poses[posIdx]
              ].input_table_file.indexOf(" ("); // .
              let nodeId = `#node_${transform_specs[
                poses[posIdx]
              ].input_table_file.substring(0, lastIdx)}`;
              if (lastIdx === -1) {
                nodeId = `#node_${
                  transform_specs[poses[posIdx]].input_table_name
                }`;
              }
              d3.select(nodeId).attr("stroke", fill_color);
            } else {
              for (
                let idx2 = 0;
                idx2 < transform_specs[poses[posIdx]].input_table_file.length;
                idx2++
              ) {
                let lastIdx = transform_specs[poses[posIdx]].input_table_file[
                  idx2
                ].indexOf(" ("); // .
                let nodeId = `#node_${transform_specs[
                  poses[posIdx]
                ].input_table_file[idx2].substring(0, lastIdx)}`;
                if (lastIdx === -1) {
                  nodeId = `#node_${
                    transform_specs[poses[posIdx]].input_table_name[idx2]
                  }`;
                }
                d3.select(nodeId).attr("stroke", fill_color);
                // d3.select(`#node_${transform_specs[pos].input_table_file[idx2].substring(0,lastIdx)}`).attr('stroke',fill_color)
              }
            }

            if (
              typeof transform_specs[poses[posIdx]].output_table_file ===
              "string"
            ) {
              let lastIdx = transform_specs[
                poses[posIdx]
              ].output_table_file.indexOf(" ("); // .
              d3.select(
                `#node_${transform_specs[
                  poses[posIdx]
                ].output_table_file.substring(0, lastIdx)}`
              ).attr("stroke", fill_color);
            } else {
              for (
                let idx2 = 0;
                idx2 < transform_specs[poses[posIdx]].output_table_file.length;
                idx2++
              ) {
                let lastIdx = transform_specs[poses[posIdx]].output_table_file[
                  idx2
                ].indexOf(" ("); // .
                d3.select(
                  `#node_${transform_specs[poses[posIdx]].output_table_file[
                    idx2
                  ].substring(0, lastIdx)}`
                ).attr("stroke", fill_color);
              }
            }
          }
        }

        if (pos != null) {
          // this.lastLine = pos

          d3.selectAll(`line.edge_${pos}`).attr("stroke", fill_color);
          d3.selectAll(`circle.edge_${pos}`).attr(
            "style",
            `fill: ${fill_color};`
          );
          // d3.select(`#arrow_${pos}`).attr('fill',fill_color)
          d3.selectAll(`path.arrow_${pos}`).attr("fill", fill_color);
          d3.selectAll(`rect.glyph_${pos}`).attr("stroke", fill_color);
          d3.selectAll(`path.glyph_${pos}`).attr("stroke", fill_color);
          if (typeof transform_specs[pos].input_table_file === "string") {
            let lastIdx = transform_specs[pos].input_table_file.indexOf(" ("); // .
            let nodeId = `#node_${transform_specs[
              pos
            ].input_table_file.substring(0, lastIdx)}`;
            if (lastIdx === -1) {
              nodeId = `#node_${transform_specs[pos].input_table_name}`;
            }
            d3.select(nodeId).attr("stroke", fill_color);
          } else {
            for (
              let idx2 = 0;
              idx2 < transform_specs[pos].input_table_file.length;
              idx2++
            ) {
              let lastIdx = transform_specs[pos].input_table_file[idx2].indexOf(
                " ("
              ); // .
              let nodeId = `#node_${transform_specs[pos].input_table_file[
                idx2
              ].substring(0, lastIdx)}`;
              if (lastIdx === -1) {
                nodeId = `#node_${transform_specs[pos].input_table_name[idx2]}`;
              }
              d3.select(nodeId).attr("stroke", fill_color);
              // d3.select(`#node_${transform_specs[pos].input_table_file[idx2].substring(0,lastIdx)}`).attr('stroke',fill_color)
            }
          }

          if (typeof transform_specs[pos].output_table_file === "string") {
            let lastIdx = transform_specs[pos].output_table_file.indexOf(" ("); // .
            d3.select(
              `#node_${transform_specs[pos].output_table_file.substring(
                0,
                lastIdx
              )}`
            ).attr("stroke", fill_color);
          } else {
            for (
              let idx2 = 0;
              idx2 < transform_specs[pos].output_table_file.length;
              idx2++
            ) {
              let lastIdx = transform_specs[pos].output_table_file[
                idx2
              ].indexOf(" ("); // .
              d3.select(
                `#node_${transform_specs[pos].output_table_file[idx2].substring(
                  0,
                  lastIdx
                )}`
              ).attr("stroke", fill_color);
            }
          }
        }
      });
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
            self.codeHighlight(0);
          }
        });
      });
    },
    codeHighlight(line) {
      if (line == 0) {
        this.editor.deltaDecorations(this.decorations, [
          {
            range: new monaco.Range(line, 1, line, 1),
            options: {
              isWholeLine: true,
              className: "myContentClass2",
              glyphMarginClassName: "myGlyphMarginClass2",
            },
          },
        ]);
      } else {
        if (!this.interaction_flag) return;
        this.editor.deltaDecorations(this.decorations, [
          {
            range: new monaco.Range(line, 1, line, 1),
            options: {
              isWholeLine: true,
              className: "myContentClass",
              glyphMarginClassName: "myGlyphMarginClass",
            },
          },
        ]);
      }
    },
    record_log() {
      // console.log("out", returnCitySN);
      const path = "https://freenli.projects.zjvis.org/access_log/";
      // const data = {
      //   "ip":returnCitySN.cip,
      //   "id":returnCitySN.cid,
      //   "location":returnCitySN.cname,
      //   'type': 'somnus'
      // }
      let data = new FormData();
      data.append("ip", returnCitySN.cip);
      data.append("id", returnCitySN.cid);
      data.append("location", returnCitySN.cname);
      data.append("type", "somnus");
      axios
        .post(path, data)
        .then((response) => {
          if (!response.data.result) {
            console.log(response.data.error);
          }
        })
        .catch((error) => {
          console.log(error);
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
