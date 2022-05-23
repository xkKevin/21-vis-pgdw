import re, os
import json, time

Rscript_path = "Rscript"  # Rscript执行路径
Python_path = 'python' # Python执行路径


def deleteMatchFiles(directory, starts="", ends="", recursion = False, hour = 100):
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


def execScript_R(script_content):
    '''
    执行数据清洗脚本，对于每一步清洗操作，都会保存这一个状态下的table，同时保存所有清洗过程的列在一个文件内
    Return:
        original_codes: 源脚本代码, 每个元素对应一行代码
        col_states：字典：key为行号，value为列；如果该行结果为table，则记录table的所有列
        group_states: 字典：key为行号，value为分组的列：如果该行结果存在分组，则记录分组的列
    '''
    str_time = str(time.time())
    script_exec_name = str_time + "_exec.txt"
    colnames_name = str_time+"_colnames.txt"
    
    original_codes = []  # 源脚本代码, 每个元素对应一行代码，行号从1开始
    codes = ""
    p = re.compile("^\s*([\w\.]+?)\s*(=|<-)\s*([\w\.:]+?)\s*[(]") # 设置函数名和outputname必须是以 A-Za-z0-9_. 这些符号组成的，其他符号将不会匹配，因此可以做到过滤注释
    # morpheus <- select(TBL_1,-`value`) → [('morpheus', '<-', 'select')]
    p2 = re.compile("^\s*([\w\.]+)[\(\s\$]*([\w\.]*?)[\s\)]*(=|<-)\s*([^#]+)") # 匹配一个赋值表达式
    # tbl1 $  b.2  = tbl1$d + 1  →  [('tbl1', 'b.2', '=', 'tbl1$d + 1')]
    
    # with open(script_name, "r") as fp:
    line_num = 0
    for line in script_content.split("\n"):
        line_num += 1
        codes += line
        if len(codes) and codes[-1] != '\n':
            codes += '\n'
        original_codes.append(line.strip("\n"))
        match_r = p.findall(line)
        if len(match_r) == 0:
            match_r2 = p2.findall(line)
            if len(match_r2):
                codes += \
    '''if (is.data.frame({value}) | is.matrix({value})) {{
        write(paste(append(colnames({value}), {line_num}, after = 0), collapse=','), "{colnames_name}", append=T)
        write.table({value}, file="L{line_num} ({value}).csv", sep=",", quote=FALSE, append=FALSE, na="NA", row.names=FALSE)
        if (is.grouped_df({value})) {{
            write(paste(append(group_vars({value}), "group{line_num}", after = 0), collapse=','), "{colnames_name}", append=T)
        }}
    }}\n'''.format(value=match_r2[0][0],line_num=line_num, colnames_name=colnames_name)  # matrix和dataframe是两种不一样的table结构
                
        else:
            if match_r[0][2] == "group_split":
                codes += \
'''index_i = 1
    for (ti in {value}){{
    if (is.data.frame(ti) | is.matrix(ti)) {{
        line_num = paste({line_num}, index_i, sep="_")
        write(paste(append(colnames(ti), line_num, after = 0), collapse=','), "{colnames_name}", append=T)
        write.table(ti, file=paste("L",line_num, " (", "{value}", "_", index_i, ").csv", sep=""), sep=",", quote=FALSE, append=FALSE, na="NA", row.names=FALSE)
        index_i = index_i + 1
    }}
}}'''.format(value=match_r[0][0],line_num=line_num, colnames_name=colnames_name)
            else:
                codes += \
    '''if (is.data.frame({value}) | is.matrix({value})) {{
        write(paste(append(colnames({value}), {line_num}, after = 0), collapse=','), "{colnames_name}", append=T)
        write.table({value}, file="L{line_num} ({value}).csv", sep=",", quote=FALSE, append=FALSE, na="NA", row.names=FALSE)
        if (is.grouped_df({value})) {{
            write(paste(append(group_vars({value}), "group{line_num}", after = 0), collapse=','), "{colnames_name}", append=T)
        }}
    }}\n'''.format(value=match_r[0][0],line_num=line_num, colnames_name=colnames_name)  # matrix和dataframe是两种不一样的table结构

    with open(script_exec_name, "w", encoding='utf-8') as fp:  # , newline='\r\n'
        fp.write(codes)
        
    if(os.system(Rscript_path + " " + script_exec_name)):
        # 0表示执行成功，否则表示执行失败
        raise Exception("Failed to execute the current script!")  # 如果执行失败，抛出异常
    
    col_states = {}  # key对应代码的行号，value对应此行代码执行完之后的table中的列
    group_states = {} # key为行号，value为分组的列
    if os.path.exists(colnames_name):  # 考虑执行script没有table输出的情况
        with open(colnames_name, "r", ) as fp:
            for line in fp.readlines():
                line = line.strip("\n")
                states = line.split(',')
                if states[0].startswith("group"):
                    group_states[int(states[0][5:])] = states[1:]
                else:
                    if "_" in states[0]:
                        col_states[states[0]] = states[1:]
                    else:
                        col_states[int(states[0])] = states[1:]
    
    return original_codes, col_states, group_states


def execScript_Python(script_content):
    '''
    执行数据清洗脚本，对于每一步清洗操作，都会保存这一个状态下的table，同时保存所有清洗过程的列在一个文件内
    Return:
        parser_info: 源脚本代码的解析
        col_states：字典：key为行号，value为列；如果该行结果为table，则记录table的所有列
        pandas_abbr: pandas的缩写，一般是 'pd'
    '''
    str_time = str(time.time())
    script_exec_name = str_time + "_exec.txt"
    
    original_codes = []  # 源脚本代码, 每个元素对应一行代码，行号从1开始
    parser_info = {}  
    codes = ''
#     p_out_func_params = re.compile('''\s*(.+?)\s*=\s*([\w\.]+?)\s*[(](.*)[)]''')
#     p_out_cols = re.compile('''([\w]+)\[+\s*(.*?)\s*\]+''')
    p1 = re.compile('''^(\s*)(\w+)[\[\s\.]*(.*?)[\s\]]*=\s*([\w\.]+?)\s*[(](.*)[)]''') # 这里表示必须经过函数
    p2 = re.compile('''^(\s*)(\w+)[\[\s\.]*(.*?)[\s\]]*=\s*([^#]+)''')  # 而这个匹配表示只需要一个赋值表达式就可以了
    # space_index, output_table, columns, function, parameters
    # 此种正则可以匹配多种形式的Wrangling格式（以下只是一些例子）：
    # 1. s_sum = s_sum.reset_index(drop=True) # 能够忽略注释  →  [('', 's_sum', '', 's_sum.reset_index', 'drop=True')] 这是最基础的
    # 2. s_sum.val = s_sum.reset_index(drop=True)  →  [('', 's_sum', 'val', 's_sum.reset_index', 'drop=True')] 第一个为缩进、第二个为output table name，第三个为 val 列（output column），第四个为函数名，第五个为函数参数
    # 3. s_sum['val'] = s_sum.reset_index(drop=True) → [('', 's_sum', "'val'", 's_sum.reset_index', 'drop=True')] 同上
    # 4. sales[['quarter', "year"]] = sales.Category.str.split("/",expand=True) → [('', 'sales', '\'quarter\', "year"',  'sales.Category.str.split', '"/",expand=True')]  第三个为 'quarter', "year" 列（output columns）
    p_pandas = re.compile("^(\s*)import\s*pandas\s*(as\s*(\w+))?\s*")

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
            if len(codes) and codes[-1] != '\n':
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
                parser_info[line_num] = match_r2[0][1:]  # 这是赋值语句的情况（即没有函数）
            space_index = match_r2[0][0]
            if len(codes) and codes[-1] != '\n':
                codes += '\n'
            codes += \
'''series_flag = False
{space_index}if (isinstance({value}, {pandas_abbr}.Series)):
{space_index}    series_flag = True
{space_index}    {value} = {value}.to_frame()
{space_index}if (isinstance({value}, {pandas_abbr}.DataFrame)):
{space_index}    columns = list({value}.index.names)
{space_index}    if columns[0]:
{space_index}        columns.extend(list({value}.columns.values))
{space_index}        col_states[{line_num}] = columns
{space_index}        {value}.to_csv("L{line_num} ({value}).csv", index=True)
{space_index}    else:
{space_index}        col_states[{line_num}] = list({value}.columns.values)
{space_index}        {value}.to_csv("L{line_num} ({value}).csv", index=False)
{space_index}if series_flag:
{space_index}    {value} = {value}[{value}.columns.values[0]]
\n'''.format(space_index=space_index, value=match_r2[0][1],line_num=line_num,pandas_abbr=pandas_abbr) 
                
    with open(script_exec_name, "w", encoding='utf-8') as fp:
        codes += '''{space_index}with open("{str_time}_colnames.txt","w",encoding='utf-8') as fp:
{space_index}    json.dump(col_states,fp,indent=2)'''.format(space_index=space_index, str_time=str_time)
        fp.write(codes)
        
    if(os.system(Python_path + " " + script_exec_name)):
        # 0表示执行成功，否则表示执行失败
        raise Exception("Failed to execute the current script!")  # 如果执行失败，抛出异常
    
    with open(str_time+"_colnames.txt","r",encoding='utf-8') as fp:
        col_states = json.load(fp)
    
    return parser_info, convert_keys_to_int(col_states), pandas_abbr #, group_states


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


def getTables(script_path, language="R"):
    wrangling_script = ""

    with open(script_path, 'r', encoding='utf-8') as fp:
        wrangling_script = fp.read()

    os.chdir(os.path.dirname(script_path))

    deleteMatchFiles("./", ends="_exec.txt")
    deleteMatchFiles("./", starts="L", ends=").csv")
    deleteMatchFiles("./",  ends="_colnames.txt")

    if language == "R":
        execScript_R(wrangling_script)
    else:
        execScript_Python(wrangling_script)


if __name__ == '__main__':
    # script_path 为脚本的绝对路径
    script_path = r"E:\other\notebook\transformers\DataWranglingTracer\table_generation\python_case1\python_script.txt"
    language = "Python"

    getTables(script_path, language)