import os
import datetime
from flask import Flask, jsonify, globals
from flask.globals import request
from werkzeug.utils import secure_filename
 
app = Flask(__name__)

globals.isRun = False

@app.route('/')
def hello():
    return 'hello docker&flask'

@app.route('/useMorpheus', methods = ['post', 'GET'])
def useMorpheus():
    if globals.isRun == True:
        os.system('killall Morpheus &> /dev/null')
        os.system('killall run-morpheus.sh')
        print('kill morpheus')
    globals.isRun = True
    now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    outFileName = 'out' + now_time + '.txt'
    shString = './run-morpheus.sh \"'
    shInputPathList = []
    writeSignal = False
    scriptReturn = 'library(tidyr)\rlibrary(dplyr)\r\r'
    temp = ''
    tempList = []
    cleanInputTable = ''
    cleanOutputTable = ''
    if request.method == 'POST':
        inputlist = request.files.getlist('inputlist')
        output = request.files['output']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        for input in inputlist:
            inputUpload_path = os.path.join(basepath, 'uploads',secure_filename(input.filename))  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
            shInputPath = os.path.join('uploads',secure_filename(input.filename))
            shInputPathList.append(shInputPath)
            input.save(inputUpload_path)
        outputUpload_path = os.path.join(basepath, 'uploads',secure_filename(output.filename))
        shOutputPath = os.path.join('uploads',secure_filename(output.filename))
        output.save(outputUpload_path)
        for path in shInputPathList:
            shString += path + '|'
        shString += shOutputPath + '\" specs/spec2/ ' + outFileName
        os.system(shString)
        filepath = './uploads'
        del_list = os.listdir(filepath)
        for f in del_list:
            file_path = os.path.join(filepath, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
    if request.method == "GET":
        caseString = request.args.get('caseString')
        # for c in caseString:
        #     if c == '|':
        #         tempList.append(temp)
        #         temp = ''
        #     temp += c
        #     if c == '/':
        #         temp =''
        shString += caseString
        shString += '\" specs/spec2/ ' + outFileName
        os.system(shString)
    for c in shString:
        if c == '|':
            tempList.append(temp)
            temp = ''
        temp += c
        if c == '/':
            temp =''
    for input in tempList:
        scriptReturn = scriptReturn + input[:-4] + ' = read.csv(\"' + input + '\")\r'
    scriptReturn += '\r'
    with open(outFileName) as fp:
        for line in fp.readlines():
            if line.startswith("There were"):
                writeSignal = False
            if line.startswith("Warning messages"):
                writeSignal = False
            if writeSignal:
                scriptReturn += line
            if line.startswith("R program"):
                writeSignal = True
    os.remove('./' + outFileName)
    globals.isRun = False
    return jsonify({'scriptReturn': scriptReturn})
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080',debug=True)