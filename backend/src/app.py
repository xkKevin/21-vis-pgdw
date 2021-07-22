# -*- coding: UTF-8 -*-

from flask import Flask, jsonify, request, send_from_directory,json
# from flask_cors import CORS  # 前端已经通过代理处理CORS了，因此后端不需要再开启
import generate_transform_specs as gts
import python_adaptor
import os
import requests

# 当设置了某个路径为static_folder后，自动将最后一个文件夹设置为url的静态文件访问起始网址
# 如static_folder='../dist/static/data'，则 http://localhost/data/t.json 访问 ../dist/static/data/t.json文件
app = Flask(__name__, static_folder='../dist/static',
            template_folder='../dist')
# CORS(app, supports_credentials=True)  # 解决跨域问题，其实只有在开发时才有用

# app.jinja_env.variable_start_string = '[['
# app.jinja_env.variable_end_string = ']]'

data_path = os.environ.get("BACKEND_DATA_PATH", "backend/data/")
morpheus_url = os.environ.get("MORPHEUS_SERVICE_URL", "http://127.0.0.1:8890/useMorpheus")
script_file = "script_test.txt"

# 注意，以下两个输出结果不一样，此时程序中涉及到的路径皆以app.root_path为准
# print(os.getcwd()) # pgdw
# print(app.root_path)  # pgdw/backend

def cleanFolder():
    try:
        inputPath = os.path.join(data_path , 'morpheusUserData/input')
        outputPath = os.path.join(data_path , 'morpheusUserData/output')
        for root, dirs, files in os.walk(inputPath):
            for f in files:
                # print('33', os.path.join(root, f))
                delPath =os.path.join(root, f)
                os.remove(delPath)

        for root, dirs, files in os.walk(outputPath):
            for f in files:
                # print('39', os.path.join(root, f))
                delPath =os.path.join(root, f)
                os.remove(delPath)
        return 'success'
    except Exception as e:
        return str(e)  # 如果有异常的话，将异常信息返回给前端

def morpheusPost():
    try:
        filesList = []
        inputPath = os.path.join(data_path , 'morpheusUserData/input')
        outputPath = os.path.join(data_path , 'morpheusUserData/output')
        fp_list = []
        for root, dirs, files in os.walk(inputPath):
            for f in files:
                print('54', os.path.join(root, f))
                fp_list.append(open(os.path.join(root, f), "rb"))
                fileTup = ("inputlist" , (f, fp_list[-1]))
                filesList.append(fileTup)
                
        for root, dirs, files in os.walk(outputPath):
            for f in files:
                print('61', os.path.join(root, f))
                fp_list.append(open(os.path.join(root, f), "rb"))
                fileTup = ("output" , (f, fp_list[-1]))
                filesList.append(fileTup)

        result = requests.post(morpheus_url, files=filesList)
        respones = result.json()
        print('68', respones)
        return respones['scriptReturn']
    except Exception as e:
        return jsonify({'error_info': str(e)})
    finally:
        for fp in fp_list:
            fp.close()

@app.route('/healthy')
def healthy():
    return 'Backend Running'


# 前端向后端获取scripts、table name等信息
@app.route('/getScriptData', methods=['GET'])
def getData():
    if request.method == "GET":
        case_file = request.args.get("case_file", "")  # POST请求用 request.form.get
        if case_file:
            # print("%s%s/%s.txt" % (data_path, case_file[:-1], case_file))
            with open("%s%s/%s.txt" % (data_path, case_file[:-1], case_file), 'r', encoding='utf-8') as f:
                script_content = f.read() # 直接读取文件内容
        else:
            with open(data_path + 'r_case/r_case1.txt', 'r', encoding='utf-8') as f:
                script_content = f.read() # 直接读取文件内容
        return jsonify({'script_content': script_content})
    else:
        return jsonify({'error': "Not GET Request!"})

@app.route('/useMorpheus', methods=['GET'])
def getMorpheusData():
    if request.method == "GET":
        try:
            caseString = request.args.get("caseString")  # POST请求用 request.form.get
            if caseString:
                urlPath = morpheus_url
                paramas = {'caseString' : caseString}
                response = requests.get(urlPath, params=paramas)
                result = response.json()
                # now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                # baseDir = os.path.dirname(__file__)
                # outFile = 'out' + now_time + '.txt'
                # filePath = os.path.join(baseDir, './data/caseText/', outFile)
                # with open(filePath, "w", encoding='utf-8') as f:
                #     f.write(result['scriptReturn'])
                #     f.close()
                return jsonify({'scriptReturn': result['scriptReturn']})
        except Exception as e:
            return jsonify({'error_info': str(e)})
    #     if case_file:
    #         print("%s%s/%s.txt" % (data_path, case_file[:-1], case_file))
    #         with open("%s%s/%s.txt" % (data_path, case_file[:-1], case_file), 'r', encoding='utf-8') as f:
    #             script_content = f.read() # 直接读取文件内容
    #     else:
    #         with open(data_path + 'r_case/r_case1.txt', 'r', encoding='utf-8') as f:
    #             script_content = f.read() # 直接读取文件内容
    #     return jsonify({'script_content': script_content})
    # else:
    #     return jsonify({'error': "Not GET Request!"})


original_cwd = os.getcwd() # 查看当前工作目录

@app.route('/generate_transform_specs', methods=['GET'])
def generate_transform_specs():
    transform_specs = {}
    if request.method == "GET":
        script_content = request.args.get("script_content", "")  # POST请求用 request.form.get
        language = request.args.get("language", "r")
        data_path_lan = os.path.join(data_path, "user_data")
        if language == 'r':
            # data_path_lan = os.path.join(data_path, "r_case")
            adaptor = gts.generate_transform_specs
        elif language == 'python':
            # data_path_lan = os.path.join(data_path, "python_case") 
            adaptor = python_adaptor.generate_transform_specs

        # with open(os.path.join(data_path_lan, script_file), 'w', encoding='utf-8') as f:
        #     f.write(script_content)
        
        # -------- 以下代码是用来调试的 -------- # 
        # os.chdir(os.path.join(os.getcwd(), data_path_lan)) # 修改当前工作目录  os.path.join(os.getcwd(),script_name)
        # transform_specs = adaptor(script_content)  # transform_specs = gts.generate_transform_specs(script_file)
        # import json
        # with open("transform_specs.json", "w") as fp:
        #     json.dump(transform_specs, fp, indent=2)
        # ------------------------------------ # 
        # os.chdir(os.path.join(os.getcwd(), data_path_lan)) # 修改当前工作目录  os.path.join(os.getcwd(),script_name)
        # transform_specs = adaptor(script_content)  # 判断是否有异常发生
        try:
            os.chdir(os.path.join(os.getcwd(), data_path_lan)) # 修改当前工作目录  os.path.join(os.getcwd(),script_name)
            transform_specs = adaptor(script_content)  # 判断是否有异常发生
            return jsonify({'transform_specs': transform_specs})
            # return jsonify({'transform_specs': {}})
        except Exception as e:
            return jsonify({'error_info': str(e)})   # 如果有异常的话，将异常信息返回给前端
        finally:
            os.chdir(original_cwd) # 修改回原来的工作目录

@app.route('/morpheus_generate_transform_specs', methods=['GET'])
def morpheus_generate_transform_specs():
    transform_specs = {}
    if request.method == "GET":
        script_content = request.args.get("script_content", "")  # POST请求用 request.form.get
        language = request.args.get("language", "r")
        data_path_lan1 = os.path.join(data_path, "morpheusData/")
        if language == 'R':
            # data_path_lan = os.path.join(data_path, "r_case")
            adaptor = gts.generate_transform_specs
        elif language == 'python':
            # data_path_lan = os.path.join(data_path, "python_case") 
            adaptor = python_adaptor.generate_transform_specs

        # with open(os.path.join(data_path_lan, script_file), 'w', encoding='utf-8') as f:
        #     f.write(script_content)
        
        # -------- 以下代码是用来调试的 -------- # 
        # os.chdir(os.path.join(os.getcwd(), data_path_lan1)) # 修改当前工作目录  os.path.join(os.getcwd(),script_name)
        # transform_specs = adaptor(script_content)  # transform_specs = gts.generate_transform_specs(script_file)
        # import json
        # with open("transform_specs.json", "w") as fp:
        #     json.dump(transform_specs, fp, indent=2)
        # ------------------------------------ # 
        # os.chdir(os.path.join(os.getcwd(), data_path_lan)) # 修改当前工作目录  os.path.join(os.getcwd(),script_name)
        # transform_specs = adaptor(script_content)  # 判断是否有异常发生
        try:
            os.chdir(os.path.join(os.getcwd(), data_path_lan1)) # 修改当前工作目录  os.path.join(os.getcwd(),script_name)
            print(os.getcwd())
            transform_specs = adaptor(script_content)  # 判断是否有异常发生
            return jsonify({'transform_specs': transform_specs})
            # return jsonify({'transform_specs': {}})
        except Exception as e:
            return jsonify({'error_info': str(e)})   # 如果有异常的话，将异常信息返回给前端
        finally:
            os.chdir(original_cwd) # 修改回原来的工作目录

@app.route('/upload_morpheus_generate_transform_specs', methods=['GET'])
def upload_morpheus_generate_transform_specs():
    transform_specs = {}
    if request.method == "GET":
        script_content = request.args.get("script_content", "")  # POST请求用 request.form.get
        language = request.args.get("language", "r")
        data_path_lan1 = os.path.join(data_path, "morpheusData")
        if language == 'R':
            # data_path_lan = os.path.join(data_path, "r_case")
            adaptor = gts.generate_transform_specs
        elif language == 'python':
            # data_path_lan = os.path.join(data_path, "python_case") 
            adaptor = python_adaptor.generate_transform_specs

        # with open(os.path.join(data_path_lan, script_file), 'w', encoding='utf-8') as f:
        #     f.write(script_content)
        
        # -------- 以下代码是用来调试的 -------- # 
        # os.chdir(os.path.join(os.getcwd(), data_path_lan)) # 修改当前工作目录  os.path.join(os.getcwd(),script_name)
        # transform_specs = adaptor(script_file)  # transform_specs = gts.generate_transform_specs(script_file)
        # import json
        # with open("transform_specs.json", "w") as fp:
        #     json.dump(transform_specs, fp, indent=2)
        # ------------------------------------ # 
        # os.chdir(os.path.join(os.getcwd(), data_path_lan)) # 修改当前工作目录  os.path.join(os.getcwd(),script_name)
        # transform_specs = adaptor(script_content)  # 判断是否有异常发生
        try:
            os.chdir(os.path.join(os.getcwd(), data_path_lan1)) # 修改当前工作目录  os.path.join(os.getcwd(),script_name)
            print(os.getcwd())
            transform_specs = adaptor(script_content)  # 判断是否有异常发生
            return jsonify({'transform_specs': transform_specs})
            # return jsonify({'transform_specs': {}})
        except Exception as e:
            return jsonify({'error_info': str(e)})   # 如果有异常的话，将异常信息返回给前端
        finally:
            os.chdir(original_cwd) # 修改回原来的工作目录
            cleanFolder()


# 由于Flask只能开启一个static_folder，要想访问其他静态数据，则重新开启一个路由以专门访问数据
# Custom static data
@app.route('/data/<path:filename>')
def custom_static_folder(filename):
    # 因为当前flask运行的目录就在backend下，因此可以直接访问data/目录
    # print(os.getcwd(), filename)
    return send_from_directory(os.path.join(os.getcwd(), data_path), filename) # 这边的相对路径用的是root_path，也就是app.py目录地址，所以用绝对路径


@app.route('/api/getTablesAndParse', methods=['post'])
def getTablesAndParse():
    try:
        # print("request: ")
        # print(request.form.to_dict())
        tables = request.form.to_dict()
        if tables['type'] == "input":
            for tablename,tablecontent in tables.items():
                if tablename != 'type':
                    with open(data_path + "user_data/" + tablename,'w',newline='') as file_object:
                        file_object.write(tablecontent)
        elif tables['type'] == "output":
            for tablename,tablecontent in tables.items():
                if tablename != 'type':
                    with open(data_path + "user_data/" + tablename,'w',newline='') as file_object:
                        file_object.write(tablecontent)

        #使用io.StringIO和csv.reader解析从字符串中解析出csv
        #execute a cmd 
        script = '''library(tidyr)
library(dplyr)
p5_input1= read.table("benchmark5.txt", header = T, sep = ",")
TBL_3=gather(p5_input1,MORPH394,P,-`ID`,-`T`)
TBL_1=separate(TBL_3,`MORPH394`,into=c('MORPH469','Channel'))
morpheus=select(TBL_1,-`MORPH469`)
morpheus=as.data.frame(morpheus)
morpheus=select(morpheus,1,3,2,4)'''
        with open(data_path + 'code5.txt', 'w', encoding='utf-8') as f:
            f.write(script)
        return "True"
    except BaseException:
        return "False"

@app.route('/api/morpheusGetTablesAndParse', methods=['post'])
def morpheusGetTablesAndParse():
    try:
        # print("request: ")
        # print(request.form.to_dict())
        tables = request.form.to_dict()
        # print("306", tables)
        returnmsg = cleanFolder()
        print('356', returnmsg)
        for key, tablecontent in tables.items():
            if key.startswith("input"):
                tablename = key[6:-1]
                with open(data_path + "morpheusUserData/input/" + tablename,'w',newline='') as file_object:
                        file_object.write(tablecontent)
                with open(data_path + "morpheusData/" + tablename,'w',newline='') as file_object:
                    file_object.write(tablecontent)
            elif key.startswith("output"):
                tablename = key[7:-1]
                with open(data_path + "morpheusUserData/output/" + tablename,'w',newline='') as file_object:
                    file_object.write(tablecontent)
        # if tables['type'] == "input":
        #     for tablename,tablecontent in tables.items():
        #         if tablename != 'type':
        #             with open(data_path + "morpheusUserData/input/" + tablename,'w',newline='') as file_object:
        #                 file_object.write(tablecontent)
        #             with open(data_path + "morpheusData/" + tablename,'w',newline='') as file_object:
        #                 file_object.write(tablecontent)
        # elif tables['type'] == "output":
        #     for tablename,tablecontent in tables.items():
        #         if tablename != 'type':
        #             with open(data_path + "morpheusUserData/output/" + tablename,'w',newline='') as file_object:
        #                 file_object.write(tablecontent)
        #使用io.StringIO和csv.reader解析从字符串中解析出csv
        #execute a cmd 
        scriptReturn = morpheusPost()
        return jsonify({'scriptReturn': scriptReturn})
    except BaseException:
        return "False"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
