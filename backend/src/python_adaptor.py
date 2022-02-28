# -*- coding: UTF-8 -*-

import os,re
import json,time
import subprocess

Python_path = 'python'

def execScript(script_content):
    '''
    执行数据清洗脚本，对于每一步清洗操作，都会保存这一个状态下的table，同时保存所有清洗过程的列在一个文件内
    Return:
        original_codes: 源脚本代码, 每个元素对应一行代码
        col_states：字典：key为行号，value为列；如果该行结果为table，则记录table的所有列
        group_states: 字典：key为行号，value为分组的列：如果该行结果存在分组，则记录分组的列
    '''
    str_time = str(time.time())
    script_exec_name = str_time + "_exec.txt"
    
    original_codes = []  # 源脚本代码, 每个元素对应一行代码，行号从1开始
    parser_info = {}  
    codes = ''
#     p_out_func_params = re.compile('''\s*(.+?)\s*=\s*([\w\.]+?)\s*[(](.*)[)]''')
#     p_out_cols = re.compile('''([\w]+)\[+\s*(.*?)\s*\]+''')
    p1 = re.compile('''^(\s*)(\w+)[\[\s\.]*(.*?)[\s\]]*=\s*([\w\.]+?)\s*[(](.*)[)]''') # 这里表示必须经过函数
    p2 = re.compile('''^(\s*)(\w+)[\[\s\.]*(.*?)[\s\]]*=\s*([\w\.]*)\s*''')  # 该匹配为赋值表达式，如： a["b"] = 23 能匹配得到 ('a', '"b"', '23')
    # space_index, output_table, columns, function, parameters
    p_pandas = re.compile("^(\s*)import\s*pandas\s*(as\s*(\w+))?\s*")
    
    # deleteMatchFiles("./", starts="table", ends=".csv")
    
    deleteMatchFiles("./", ends="_exec.txt")
    # deleteMatchFiles("./", starts="table", ends=".csv")
    deleteMatchFiles("./", starts="L", ends=").csv")
    deleteMatchFiles("./",  ends="_colnames.txt")
       

    pandas_abbr = 'pandas'  # 引入pandas库的名字
    space_index = ''
    flag = True
    
    # with open(script_name, "r") as fp:
    line_num = 0
    for line in script_content.split("\n"):
        line_num += 1
        codes += line
        original_codes.append(line.strip("\n"))
        match_r = p1.findall(line)
        match_r2 = p2.findall(line)
#             print(match_r)
        if len(match_r2) == 0:
            if codes[-1] != '\n':
                codes += '\n'
            pandas_r = p_pandas.findall(line)
            if len(pandas_r):
                if pandas_r[0][2]:
                    pandas_abbr = pandas_r[0][2]  # 获取代码中的pandas的别名
                if flag:
                    space_index = pandas_r[0][0]
                    codes += '''{space_index}import json
{space_index}col_states={{}}\n'''.format(space_index=space_index)
                    flag = False
        else:
            if len(match_r):
                parser_info[line_num] = match_r[0][1:]  # output_table, columns, function, parameters
            else:
                parser_info[line_num] = match_r2[0][1:]  # 这是赋值语句的情况（即没有函数） ('a', '"b"', '23')
            space_index = match_r2[0][0]
            if codes[-1] != '\n':
                codes += '\n'
            codes += \
'''{space_index}if (isinstance({value}, {pandas_abbr}.DataFrame)):
{space_index}    columns = list({value}.index.names)
{space_index}    if columns[0]:
{space_index}        columns.extend(list({value}.columns.values))
{space_index}        col_states[{line_num}] = columns
{space_index}        {value}.to_csv("L{line_num} ({value}).csv", index=True)
{space_index}    else:
{space_index}        col_states[{line_num}] = list({value}.columns.values)
{space_index}        {value}.to_csv("L{line_num} ({value}).csv", index=False)
\n'''.format(space_index=space_index, value=match_r2[0][1],line_num=line_num,pandas_abbr=pandas_abbr) 
                
    with open(script_exec_name, "w", encoding='utf-8') as fp:
        codes += '''{space_index}with open("{str_time}_colnames.txt","w",encoding='utf-8') as fp:
{space_index}    json.dump(col_states,fp,indent=2)'''.format(space_index=space_index, str_time=str_time)
        fp.write(codes)
        
    # if(os.system(Python_path + " " + script_exec_name)):
    exec_result = subprocess.getstatusoutput(Python_path + " " + script_exec_name) # 用以获取命令行输出的信息
    if exec_result[0]:  # 0表示执行成功，否则表示执行失败
        err_index = exec_result[1].find("Error")
        if err_index == -1:
            err_index = 0
        raise Exception("Failed to execute the current script!\n\n" + exec_result[1][err_index:])  # 如果执行失败，抛出异常
    
    with open(str_time+"_colnames.txt","r",encoding='utf-8') as fp:
        col_states = json.load(fp)
    
    return parser_info, convert_keys_to_int(col_states), pandas_abbr #, group_states


def deleteMatchFiles(directory, starts="", ends="", recursion = False, hour = 0.2):
    '''
    按特定要求删除某路径下的匹配文件，如果starts和ends都不填写，则默认删除该目录下所有文件
    recursion: 表示是否递归删除匹配的文件，默认为否，即值删除当前路径下的匹配文件
    hour: 表示删除大于hour个小时以前的文件
    '''
    now = time.time()
    for path, dir_list, file_list in os.walk(directory):
        if recursion: # 递归搜索并删除
            for fi in file_list:
                if fi.startswith(starts) and fi.endswith(ends): # "table9.csv".startswith("") 为 True
                    # print(directory, path, fi)
                    file_path = os.path.join(path, fi)
                    if (now - os.path.getctime(file_path))/3600 >= hour:
                        os.remove(file_path)
        else: # 非递归搜索
            if path == directory:  # 仅在当前文件下删除
                for fi in file_list:
                    if fi.startswith(starts) and fi.endswith(ends):
                        # print(directory, path, fi)
                        file_path = os.path.join(path, fi)
                        if (now - os.path.getctime(file_path))/3600 >= hour:
                            os.remove(file_path)
                break
                
    

def remove_quote(params, flag=False):
    '''
    先取出最外层的空格，然后去除参数列表中的最外层引号
    params 既可以是一个list，也可以是字符串
    若是list则返回一个list，若是字符串，也返回一个字符串
    '''

    if flag:
        if not params:
            return params
        if type(params) == str:
            params = params.strip()
            if params[0] in ('"', "'"):
                return params[1:-1]
            else:
                return params

        param_list_new = []
        for i in params:
            i = i.strip()
            if i[0] in ('"', "'"):
                param_list_new.append(i[1:-1])
            else:
                param_list_new.append(i)
        return param_list_new
    else:
        params = params.strip()
        if params[0] in ('"', "'"):
            if params[0] == params[-1]:
                return (True, params[1:-1])
        else:
            return (False, params)
    


def parseArgs(param_str):
    '''
    param_str: 原始参数字符串
    return：返回对应的参数列表，分为无名参数和有名参数
    '''
    args = {"none": []}  
    arg = ""
    arg_name = ""
    bracket_flag = 0  # 只有当flag为0时，表示括号匹配结束
    quote_flag = True  # 当quote_flag为True时，表示引号匹配结束
    quote_str = ""
    for i in param_str:
        if bracket_flag == 0 and quote_flag and i == ",":
            if arg_name:
                args[arg_name] = arg.strip()
                arg_name = ""
            else:
                args['none'].append(arg.strip())
            arg = ""
            continue
        elif i == "=":
            arg_name = arg.strip()
            arg = ""
            continue
        elif i == "(":
            bracket_flag += 1
        elif i == ")":
            bracket_flag -= 1
        elif i in ['"', "'", "`"]: 
            if quote_flag: # 表示目前没有匹配到引号
                quote_flag = False
                quote_str = i  # 此时最外层的引号是 i，在没有匹配到第二个i前，里面可以存放任何字符
            elif i == quote_str: # 表示当前的字符 i 匹配到了最外层的引号 quote_str
                quote_flag = True
                quote_str == ""
        arg += i
    if arg_name:
        args[arg_name] = arg.strip()
    else:
        args['none'].append(arg.strip())
    return args

def convert_keys_to_int(d: dict):
    new_dict = {}
    for k, v in d.items():
        try:
            new_key = int(k)
        except ValueError:
            new_key = k
        if type(v) == dict:
            v = _convert_keys_to_int(v)
        new_dict[new_key] = v
    return new_dict


def generate_transform_specs(script_content):
    # output_table, columns, function, parameters

    parser_info, col_states, pandas_abbr = execScript(script_content)
    transform_specs = []
    var2table = {} # 用来记录变量对应的table file名称
    # p_match_num = re.compile("table(.+)\.csv")  #  L{line_num} ({value})
    p_match_num = re.compile("L(.+) \(.+\).csv") 
    var2num = lambda var: int(p_match_num.findall(var2table[var])[0]) # 根据变量找到对应的行号
    
    p_loc = re.compile("loc\s*\[\s*(.+?)\s*$")
    p_brackets = re.compile("\[(.+)\]")
    
    for pi_key, pi_value in parser_info.items():
    
        # if len(pi_value) < 4 and var2table.get(pi_value[0]):
        #     var2table[pi_value[0]] = "L%d (%s).csv" % (pi_key, pi_value[0])
        #     continue

        line_num = pi_key

        if not col_states.get(line_num): # 如果该行输出不是表的话，直接跳过
            continue
            
        specs = {}
        output_tbl = pi_value[0]
        specs["output_table_name"] = output_tbl
        specs["output_table_file"] = "L%d (%s).csv" % (line_num, specs["output_table_name"])   # "table%d.csv" % line_num

        if len(pi_value) < 4: # 如果该行是赋值表达式
            if pi_value[1]: # 表示 有行/列参数
                specs["input_table_name"] = pi_value[0]
                specs["input_table_file"] = var2table[specs["input_table_name"]]
                if pi_value[1][0] in ['"', "'"]:
                    cols = pi_value[1].split(",")
                    specs["output_explicit_col"] = []
                    col_tmp = ""
                    for ci in cols:
                        if col_tmp:
                            ci = col_tmp + ci
                            col_tmp = ""
                        res = remove_quote(ci)
                        if res[0]:
                            specs["output_explicit_col"].append(res[1])
                        else:
                            col_tmp = ci
                    specs["type"] = 'create_columns_create'
                    specs["operation_rule"] = 'Create Columns: ' + ",".join(specs["output_explicit_col"])
                elif pi_value[1].startswith('loc') or pi_value[1].startswith('iloc'):
                    res = p_loc.findall(pi_value[1])[0].strip()
                    if res.startswith("len"):
                        specs["type"] = 'create_rows_create'
                        specs["operation_rule"] = "Create Row"
                    elif res.isdigit():
                        specs["type"] = 'transform_rows_edit'
                        specs["input_explicit_row"] = [int(res.isdigit())]
                        specs["operation_rule"] = "Edit row %s" % specs["input_explicit_row"][0]
            else: # 没有 行/列参数
                specs["type"] = 'create_tables'
                specs["operation_rule"] = 'Create Manually'
            
            var2table[output_tbl] = specs["output_table_file"]
            transform_specs.append(specs)
            continue

        # 以下代码为函数的情况
        funcs = pi_value[2].split(".")
        params = parseArgs(pi_value[3])
        
        if funcs[0] == pandas_abbr:
            func = funcs[1]
            if func in ["read_csv", "read_table", "read_json"]:
                specs["type"] = 'create_tables'
                if params.get('filepath_or_buffer'):
                    file = params.get('filepath_or_buffer')
                else:
                    file = params['none'][0] # 无名参数列表中的第一个值为加载的文件名
                specs["operation_rule"] = 'Load table from ' + file
                
            if func == "concat":
                str_tables = p_brackets.findall(pi_value[3])[0]

                specs["input_table_name"] = remove_quote(str_tables.split(","), flag=True)
                specs["input_table_file"] = [var2table[specs["input_table_name"][0]], var2table[specs["input_table_name"][1]]]
                if 'axis' in params.keys() and params.get('axis') == '1':
                    specs["type"] = "combine_tables_extend_column"
                    specs["operation_rule"] = "Extend tables along column axis"
                else:
                    specs["type"] = "combine_tables_extend_row"
                    specs["operation_rule"] = "Extend tables along row axis"
                    
            if func == "merge":
                specs["input_table_name"] = []
                pi = 0
                if params.get('left'):
                    specs["input_table_name"].append(params['left'])
                else:
                    specs["input_table_name"].append(params['none'][pi])
                    pi += 1
                if params.get('right'):
                    specs["input_table_name"].append(params['right'])
                else:
                    specs["input_table_name"].append(params['none'][pi])
                    pi += 1
                specs["input_table_file"] = [var2table[specs["input_table_name"][0]], var2table[specs["input_table_name"][1]]]
                join_type = "inner"
                if params.get('how'):
                    join_type = params.get('how')
                specs["type"] = "combine_tables_%s_join" % join_type
                specs["operation_rule"] = "%s join" % join_type.capitalize()
                if params.get('on'):
                    specs["input_explicit_col"] = [remove_quote(params.get('on'), flag=True)]
                    specs["operation_rule"] = "%s join on %s" % (join_type.capitalize(), specs["input_explicit_col"][0])
            
            if func == "unique":
                pass
        else:
            # input_tbl = funcs[0]
            specs["input_table_name"] = funcs[0]
            specs["input_table_file"] = var2table[specs["input_table_name"]]
            if len(funcs) >= 2:
                if funcs[1] in col_states[pi_key]:
                    specs["input_explicit_col"] = [funcs[1]]
            func = funcs[-1]
            
            if func == 'split':
                specs["type"] = "separate_columns"
                specs["operation_rule"] = "Split %s on %s" % (specs["input_explicit_col"][0], params['none'][0])
                
            if func == 'groupby':
                p_res = pi_value[3].split(".")
                specs["input_explicit_col"] = [i for i in col_states[line_num] if i in p_res[0]]
                specs["input_implicit_col"] = specs["input_explicit_col"]
                specs["input_explicit_col"] = list(set(col_states[line_num]) - set(specs["input_implicit_col"]))
                specs["output_explicit_col"] = specs["input_explicit_col"]
                func = p_res[-1][:-1]
                if  func in ['mean', 'max', 'mad', 'median', 'min','sum']:
                    specs["type"] = "combine_rows_summarize"
                    specs["operation_rule"] = "Group by %s, Summarize columns by %s" % (",".join(specs["input_implicit_col"]), func)  # Summarize rows
            
            if func == 'reset_index':
                if params.get('drop') and params.get('drop') == 'True':
                    rm_cols = set(col_states[var2num(specs["input_table_name"])]) - set(col_states[line_num])
                    if len(rm_cols):
                        specs["type"] = "delete_columns_select_remove"
                        specs["input_explicit_col"] = list(rm_cols)
                        specs["operation_rule"] = "Delete %s" % ",".join(rm_cols)
                    else:
                        specs["type"] = 'identical_operation'
                        specs["operation_rule"] = func
                else:
                    specs["type"] = 'identical_operation'
                    specs["operation_rule"] = func
                    
            if func == "merge":
                specs["input_table_name"] = [specs["input_table_name"], params['none'][0]]
                specs["input_table_file"] = [var2table[specs["input_table_name"][0]], var2table[specs["input_table_name"][1]]]
                join_type = "inner"
                if params.get('how'):
                    join_type = params.get('how')
                specs["type"] = "combine_tables_%s_join" % join_type
                specs["operation_rule"] = "%s join" % join_type.capitalize()
                if params.get('on'):
                    specs["input_explicit_col"] = [remove_quote(params.get('on'), flag=True)]
                    specs["operation_rule"] = "%s join on %s" % (join_type.capitalize(), specs["input_explicit_col"][0])
                

        if pi_value[1]:
            if pi_value[1][0] in ['"', "'"]:
                cols = pi_value[1].split(",")
                specs["output_explicit_col"] = []
                col_tmp = ""
                for ci in cols:
                    if col_tmp:
                        ci = col_tmp + ci
                        col_tmp = ""
                    res = remove_quote(ci)
                    if res[0]:
                        specs["output_explicit_col"].append(res[1])
                    else:
                        col_tmp = ci
            elif pi_value[1].startswith('loc') or pi_value[1].startswith('iloc'):
                res = p_loc.findall(pi_value[1])[0].strip()
                if res.startswith("len"):
                    specs["type"] = 'create_rows_create'
                    if  func in ['mean', 'max', 'mad', 'median', 'min','sum']:
                        specs["operation_rule"] = "Create Row, Summarize columns by %s" % (func)
                    else:
                        specs["operation_rule"] = "Create Row"
                elif res.isdigit():
                    specs["type"] = 'transform_rows_edit'
                    specs["input_explicit_row"] = [int(res.isdigit())]
                    specs["operation_rule"] = "Edit row %s" % specs["input_explicit_row"][0]
        
        
        var2table[output_tbl] = specs["output_table_file"]
        
        # print(func, specs)
        # if specs_before:
        #     transform_specs.append(specs_before)
        if specs:
            transform_specs.append(specs)
        # if specs_after:
        #     transform_specs.append(specs_after)

    return transform_specs