import re, os
import time

Rscript_path = "Rscript"  # Rscript执行路径


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
    colnames_name = str_time+"_colnames.txt"
    
    original_codes = []  # 源脚本代码, 每个元素对应一行代码，行号从1开始
    codes = ""
    p = re.compile("^\s*([\w\.]+?)\s*(=|<-)\s*([\w\.:]+?)\s*[(]") # 设置函数名和outputname必须是以 A-Za-z0-9_. 这些符号组成的，其他符号将不会匹配，因此可以做到过滤注释
    
    # deleteMatchFiles("./", starts="table", ends=".csv")
    
    deleteMatchFiles("./", ends="_exec.txt")
    deleteMatchFiles("./", starts="L", ends=").csv")
    deleteMatchFiles("./",  ends="_colnames.txt")
    
    # with open(script_name, "r") as fp:
    line_num = 0
    for line in script_content.split("\n"):
        line_num += 1
        codes += line
        original_codes.append(line.strip("\n"))
        match_r = p.findall(line)
        if len(match_r) == 0:
            if codes[-1] != '\n':
                codes += '\n'
        else:
            if codes[-1] != '\n':
                codes += '\n'
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

    with open(script_exec_name, "w", encoding='utf-8') as fp:
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


def parseCondition(con_str):
    '''
    con_str: 原始条件字符串
    return：返回解析出包含各个名称的set
            如 "mass > mean(mass, na.rm = TRUE)" 解析成 ("mass", "mean", "na.rm", "TRUE")
    '''
    con_names = set()
    name = ''
    for i in con_str:
        if i in "()><=!&|,+-/*":
            if name:
                con_names.add(remove_quote(name))
            name = ''
        else:
            name += i
    if name:
        con_names.add(remove_quote(name))
    
    return con_names


def remove_quote(params):
    '''
    先取出最外层的空格，然后去除参数列表中的最外层引号
    params 既可以是一个list，也可以是字符串
    若是list则返回一个list，若是字符串，也返回一个字符串
    '''

    if not params:
        return params
    if type(params) == str:
        params = params.strip()
        if params[0] in ('"', "'", "`"):
            return params[1:-1]
        else:
            return params
        
    param_list_new = []
    for i in params:
        i = i.strip()
        if i[0] in ('"', "'", "`"):
            param_list_new.append(i[1:-1])
        else:
            param_list_new.append(i)
    return param_list_new


original_tables = {}

original_tables_file = "original_tables/"
# print(os.getcwd()) # pgdw
for path, dir_list, file_list in os.walk("./backend/data/user_data/original_tables/"):
    for fi in file_list:
        original_tables[fi[:-4]] = original_tables_file + fi


def generate_transform_specs(script_content):
    # 以下是测试：
    original_codes = [
        '''A = read.table(file = "sd.csv", "sdf.sss")''',
        '''B <- separate(data=  A, T, into=c('ha', 'G'))''',
        '''B = filter(B, P>'rT')''',
        '''C <- select(B, 4,1,2,3, 5)''',
#         '''D = gather(data=B, key="FF", `ssdf`, T, P)'''
#         '''D = spread(C, key="T", value=Channel)'''
#         '''D = summarise(C, ID=sum(ID), P=sd(P), .groups = NULL)'''
#         '''D = unite(B, "z", x,y, remove = FALSE)'''
#         '''D = left_join(x=A, B, by = c("first",`third`))'''
#         '''D = mutate(C, E=2*T+P, .keep="unused")'''
#         '''D = arrange(B, desc(`Channel`))'''
#         '''D = merge(x=A, B, by = c("first",`third`))'''
#         '''D = rbind(1:4, C)'''
#         '''D=subset(x= B, P> 2*T)'''
#         '''D = distinct(B, 'T', `MORPH394`)'''
        '''llll <- cbind(E  =  c(8:14), T = 1, B)'''
    ]
    col_states = {1: ['ID', 'T', 'P.1', 'P.2', 'Q.1'],
                 2: ['ID', 'T', 'MORPH394', 'P'],
                 3: ['ID', 'T', 'MORPH469', 'Channel', 'P'],
                 4: ['ID', 'T', 'Channel', 'P'],
                 5: ['ID', 'T', 'Channel', 'P'],
                 6: ['ID', 'Channel', 'T', 'P']}
    
    group_states = {4: 'T'}
    
    original_codes, col_states, group_states = execScript(script_content)

    # print(col_states)

    p = re.compile("^\s*([\w\.]+?)\s*(=|<-)\s*([\w\.:]+?)\s*[(](.+)[)]")  # 设置函数名和outputname必须是以 A-Za-z0-9_. 这些符号组成的
    p_match_num = re.compile("L(.+) \(.+\).csv") # p_match_num = re.compile("table(.+)\.csv")
    p_match_c = re.compile("c\s*\((.+)\)")

    result = []
    for ci in original_codes:
        tmp = p.findall(ci)
        if len(tmp):
            result.append(tmp[0])
        else:
            result.append([])

    transform_specs = []
    var2table = original_tables # 用来记录变量对应的table file名称
    var2num = lambda var: int(p_match_num.findall(var2table[var])[0]) # 根据变量找到对应的行号
    line_num = 0  # script的行号，从1开始
    

    # var2table = {"A": "table1.csv", "B": "table2.csv", "C": "table3.csv", "D": "table4.csv", "E": "table5.csv", "F": "table6.csv"}
    

    for r in result:
        line_num += 1
        if not (r and col_states.get(line_num) or col_states.get(str(line_num)+"_1")):
            continue
        
        output_tbl = r[0]
        func = r[2].split("::")[-1]  # 能够适配 dplyr:: 的情况
        params = parseArgs(r[3])  # 得到无名参数none和有名参数的dict

        specs_combine = {}
        specs = {}
        specs_after = {}

        # print(params)
        
        if func in ('read.table', 'read.csv', 'read.csv2', 'read.delim', 'read.delim2'):
            specs["type"] = 'create_tables'
            specs["output_table_name"] = output_tbl
            specs["output_table_file"] = "L%d (%s).csv" % (line_num, specs["output_table_name"])
            if params.get('file'):
                file = params.get('file')
            else:
                file = params['none'][0] # 无名参数列表中的第一个值为加载的文件名
            # specs["operation_rule"] = 'Load: ' + file
            specs["operation_rule"] = 'Load table from ' + file
            
            var2table[output_tbl] = specs["output_table_file"]

        elif func in ('data.frame', 'tibble'):
            specs["type"] = 'create_tables'
            specs["output_table_name"] = output_tbl
            specs["output_table_file"] = "L%d (%s).csv" % (line_num, specs["output_table_name"])
            specs["operation_rule"] = 'Create Manually'
            
            var2table[output_tbl] = specs["output_table_file"]
            
        elif func == 'separate_rows':
            specs["type"] = 'separate_rows'
            pi = 0
            if params.get('data'):
                specs["input_table_name"] = params.get('data')
            else:
                specs["input_table_name"] = params['none'][pi]
                pi += 1
            specs["input_table_file"] = var2table[specs["input_table_name"]]
            specs["output_table_name"] = output_tbl
            specs["output_table_file"] = "L%d (%s).csv" % (line_num, specs["output_table_name"])
            specs["input_explicit_col"] = remove_quote(params["none"][pi:])
            if params.get('sep'):
                specs["operation_rule"] = 'Split rows on %s by %s' % (','.join(specs["input_explicit_col"]), params["sep"])
            else:
                # specs["operation_rule"] = '''Separate Row: "[^[:alnum:].]+"'''
                specs["operation_rule"] = "Split rows"
            
            var2table[output_tbl] = specs["output_table_file"]
            
        elif func == 'filter':
            condition = r[3].replace(params['none'][0],"").strip().strip(",").strip()
            
            specs["type"] = 'delete_rows_filter'
            specs["input_table_name"] = params['none'][0]
            specs["input_table_file"] = var2table[specs["input_table_name"]]
            specs["output_table_name"] = output_tbl
            specs["output_table_file"] = "L%d (%s).csv" % (line_num, specs["output_table_name"])
            specs["input_explicit_col"] = [i for i in col_states[line_num] if i in parseCondition(condition)]
            specs["operation_rule"] = 'Keep rows where ' + condition
            
            var2table[output_tbl] = specs["output_table_file"]
            
        elif func == 'separate':
            specs["type"] = 'separate_columns'
            pi = 0
            if params.get('data'):
                specs["input_table_name"] = params.get('data')
            else:
                specs["input_table_name"] = params['none'][pi]
                pi += 1
            specs["input_table_file"] = var2table[specs["input_table_name"]]
            specs["output_table_name"] = output_tbl
            specs["output_table_file"] = "L%d (%s).csv" % (line_num, specs["output_table_name"])
            specs["input_explicit_col"] = []
            specs["output_explicit_col"] = []
            if params.get('col'):
                specs["input_explicit_col"].append(params.get('col'))
            else:
                specs["input_explicit_col"].append(params['none'][pi])
                pi += 1
            specs["input_explicit_col"] = remove_quote(specs["input_explicit_col"])
            if params.get('into'):
                if params.get('into').startswith("c("):
                    specs["output_explicit_col"] = remove_quote(p_match_c.findall(params.get('into'))[0].strip().split(','))
            else:
                if params['none'][pi].startswith("c("):
                    specs["output_explicit_col"] = remove_quote(p_match_c.findall(params['none'][pi])[0].strip().split(','))
                pi += 1
            if params.get('sep'):
                # specs["operation_rule"] = "Separate Columns: " + params.get('sep')
                specs["operation_rule"] = "Split %s on %s" % (specs["input_explicit_col"][0], params['sep'])
            else:
                # specs["operation_rule"] = '''Separate Columns: "[^[:alnum:]]+"'''
                specs["operation_rule"] = "Split " + specs["input_explicit_col"][0]
            
            var2table[output_tbl] = specs["output_table_file"]
        
        elif func == 'gather':
            specs["type"] = "transform_tables_fold"
            pi = 0
            if params.get('data'):
                specs["input_table_name"] = params.get('data')
            else:
                specs["input_table_name"] = params['none'][pi]
                pi += 1
            specs["input_table_file"] = var2table[specs["input_table_name"]]
            specs["output_table_name"] = output_tbl
            specs["output_table_file"] = "L%d (%s).csv" % (line_num, specs["output_table_name"])
            specs["output_explicit_col"] = []
            if params.get('key'):
                specs["output_explicit_col"].append(params.get('key'))
            else:
                specs["output_explicit_col"].append(params['none'][pi])
                pi += 1
            if params.get('value'):
                specs["output_explicit_col"].append(params.get('value'))
            else:
                specs["output_explicit_col"].append(params['none'][pi])
                pi += 1
            specs["output_explicit_col"] = remove_quote(specs["output_explicit_col"])
            remove_col = set()
            specs["input_explicit_col"] = []
            for i in range(pi, len(params['none'])):
                if params['none'][i].startswith('-'):
                    remove_col.add(params['none'][i][1:])
                else:
                    specs["input_explicit_col"].append(params['none'][i])
            if remove_col:
                remove_col = set(remove_quote(remove_col))
                specs["input_explicit_col"] = list(set(col_states[var2num(specs["input_table_name"])]) - remove_col)
            specs["input_explicit_col"] = remove_quote(specs["input_explicit_col"])
            specs["operation_rule"] = 'Fold'
            
            var2table[output_tbl] = specs["output_table_file"]
                 
        elif func == 'spread':
            specs["type"] = "transform_tables_unfold"
            pi = 0
            if params.get('data'):
                specs["input_table_name"] = params.get('data')
            else:
                specs["input_table_name"] = params['none'][pi]
                pi += 1
            specs["input_table_file"] = var2table[specs["input_table_name"]]
            specs["output_table_name"] = output_tbl
            specs["output_table_file"] = "L%d (%s).csv" % (line_num, specs["output_table_name"])
            specs["input_explicit_col"] = []
            if params.get('key'):
                specs["input_explicit_col"].append(params.get('key'))
            else:
                specs["input_explicit_col"].append(params['none'][pi])
                pi += 1
            if params.get('value'):
                specs["input_explicit_col"].append(params.get('value'))
            else:
                specs["input_explicit_col"].append(params['none'][pi])
                pi += 1
            specs["input_explicit_col"] = remove_quote(specs["input_explicit_col"])
            specs["operation_rule"] = 'Unfold'
            
            var2table[output_tbl] = specs["output_table_file"]
            
        elif func == "select":
            # 目前select可以支持数字，重命名，但不支持 1:3, A:C 这样的形式
            specs["input_table_name"] = params['none'][0]
            specs["input_table_file"] = var2table[specs["input_table_name"]]
            specs["output_table_name"] = output_tbl
            specs["output_table_file"] = "L%d (%s).csv" % (line_num, specs["output_table_name"])
            remove_col = []
            keep_col = []
            for i in range(1, len(params['none'])):
                if params['none'][i].startswith('-'):
                    col = params['none'][i][1:]
                    if str.isdigit(col):
                        col = col_states[var2num(specs["input_table_name"])][int(col)-1]
                    remove_col.append(col)
                else:
                    col = params['none'][i]
                    if str.isdigit(col):
                        col = col_states[var2num(specs["input_table_name"])][int(col)-1]
                    keep_col.append(col)
            remove_col = remove_quote(remove_col)
            keep_col = remove_quote(keep_col)
            var2table[output_tbl] = specs["output_table_file"]
            if remove_col:
                specs["type"] = 'delete_columns_select_remove'
                specs["input_explicit_col"] = remove_col
                specs["operation_rule"] = 'Delete ' + ','.join(remove_col)
            elif len(keep_col) < len(col_states[var2num(specs["input_table_name"])]):
                specs["type"] = 'delete_columns_select_keep'
                specs["input_explicit_col"] = keep_col
                # specs["operation_rule"] = 'Keep Columns: ' + ','.join(keep_col)
                specs["operation_rule"] = 'Keep ' + ','.join(specs["input_explicit_col"])

                rename_cols = []
                for pk, pv in params.items():
                    if pk in ('none'):
                        continue
                    pv = remove_quote(pv)
                    rename_cols.append(pv)
                if rename_cols:
                    pr_tmp = r[3].split(",")[1:]
                    specs["input_explicit_col"] = []
                    for i in pr_tmp:
                        specs["input_explicit_col"].append(remove_quote(i.split("=")[-1]))
                    specs["operation_rule"] = 'Keep ' + ','.join(specs["input_explicit_col"])
                    code1 = "%s=select(%s,%s)" % (specs["output_table_name"], specs["input_table_name"], '`%s`' % "`,`".join(specs["input_explicit_col"]))
                    script_code = original_codes[:line_num-1]
                    script_code.append(code1)  # 将原先的那一行代码替换掉
                    output_t1 = "L%d_1 (%s).csv" % (line_num, specs["output_table_name"])
                    script_code.append('''write.table({input_t}, file="{output_t1}", sep=",", quote=FALSE, append=FALSE, na="NA", row.names=FALSE)'''\
                        .format(input_t = specs["output_table_name"], output_t1=output_t1))
                    
                    script_exec_name = "rename_exec.txt"
                    with open(script_exec_name, "w", encoding='utf-8') as fp:
                        fp.write("\n".join(script_code))
                        
                    if(os.system(Rscript_path + " " + script_exec_name)):
                        # 0表示执行成功，否则表示执行失败
                        raise Exception("Failed to execute the %s script!" % script_exec_name)  # 如果执行失败，抛出异常
                    
                    new_tbl_file = "L%d_2 (%s).csv" % (line_num, specs["output_table_name"])
                    if os.path.exists(new_tbl_file):
                        os.remove(new_tbl_file)
                    os.rename(specs["output_table_file"], new_tbl_file) # 重命名文件

                    # os.rename(specs["output_table_file"], "L%d_2 (%s).csv" % (line_num, specs["output_table_name"])) # 重命名文件

                    specs["output_table_name"] = output_tbl  # + "_1"
                    specs["output_table_file"] = output_t1

                    specs_after = {
                        "type": 'transform_columns_rename',
                        "input_table_name": specs["output_table_name"],
                        "input_table_file": specs["output_table_file"],
                        "output_table_name": output_tbl,
                        "output_table_file": new_tbl_file,
                        "input_explicit_col": rename_cols,
                        "operation_rule": "Rename columns"
                    }
                    var2table[output_tbl] = specs_after["output_table_file"]

            else:
                specs["type"] = 'transform_tables_rearrange'
                specs["input_explicit_col"] = keep_col
                specs["operation_rule"] = 'Rearrange Columns'
                
        
        elif func in ("summarise", "summarize"):
            specs["type"] = "combine_rows_summarize"
            specs["input_table_name"] = params['none'][0]
            specs["input_table_file"] = var2table[specs["input_table_name"]]
            specs["output_table_name"] = output_tbl
            specs["output_table_file"] = "L%d (%s).csv" % (line_num, specs["output_table_name"])
            specs["output_explicit_col"] = []
            input_line_num = var2num(specs["input_table_name"])
            tmp = set()
            rule = []
            for pk, pv in params.items():
                pk = remove_quote(pk)
                if pk == 'none' or pk not in col_states[line_num]:
                    continue
                rule.append("%s=%s" % (pk, pv))
                specs["output_explicit_col"].append(pk)
                tmp = tmp.union(set([i for i in col_states[input_line_num] if i in parseCondition(pv)]))
            specs["input_explicit_col"] = list(tmp)
            if group_states.get(input_line_num):
                specs["input_implicit_col"] = [group_states[input_line_num][-1]]
                specs["operation_rule"] = "Group:%s, Summarize:%s" % (specs["input_implicit_col"][0], ",".join(rule))
            else:
                specs["operation_rule"] = "Summarize:" + ",".join(rule)
                 
            var2table[output_tbl] = specs["output_table_file"]

        elif func == 'count':
            specs["type"] = "combine_rows_summarize"
            specs["output_table_name"] = output_tbl
            specs["output_table_file"] = "L%d (%s).csv" % (line_num, specs["output_table_name"])
            if params.get('x'):
                specs["input_table_name"] = params['x']
                specs["input_explicit_col"] = remove_quote(params['none'])
            else:
                specs["input_table_name"] = params['none'][0]
                specs["input_explicit_col"] = remove_quote(params['none'][1:])
            specs["input_table_file"] = var2table[specs["input_table_name"]]
            if params.get('name'):
                specs["output_explicit_col"] = [remove_quote(params.get('name'))]
            else:
                specs["output_explicit_col"] = ['n']

            specs["operation_rule"] = "Group:%s, and Count" % (','.join(specs["input_explicit_col"]))
            var2table[output_tbl] = specs["output_table_file"]

            if params.get('sort') and params['sort'] in ('T', 'TRUE'):  # 涉及到排序，因此需要做separation，即拆成两步
                # print(original_codes[line_num-1])
                # 生成中间table
                p_sort = re.compile("sort\s*=\s*"+params['sort'])
                code1 = p_sort.sub('', original_codes[line_num-1])
                script_code = original_codes[:line_num-1]
                script_code.append(code1)  # 将原先的那一行代码替换掉
                output_t1 = "L%d_1 (%s).csv" % (line_num, specs["output_table_name"])   # "L%d_1 (%s).csv" % (line_num, specs["output_table_name"])
                script_code.append('''write.table({input_t}, file="{output_t1}", sep=",", quote=FALSE, append=FALSE, na="NA", row.names=FALSE)'''\
                    .format(input_t = specs["output_table_name"], output_t1=output_t1))
                
                script_exec_name = "sort_exec.txt"
                with open(script_exec_name, "w", encoding='utf-8') as fp:
                    fp.write("\n".join(script_code))
                    
                if(os.system(Rscript_path + " " + script_exec_name)):
                    # 0表示执行成功，否则表示执行失败
                    raise Exception("Failed to execute the %s script!" % script_exec_name)  # 如果执行失败，抛出异常
                
                new_tbl_file = "L%d_2 (%s).csv" % (line_num, specs["output_table_name"])
                if os.path.exists(new_tbl_file):
                    os.remove(new_tbl_file)
                os.rename(specs["output_table_file"], new_tbl_file) # 重命名文件

                specs["output_table_name"] = output_tbl  # + "_1"
                specs["output_table_file"] = output_t1

                specs_after = {
                    "type": 'transform_tables_sort',
                    "input_table_name": specs["output_table_name"],
                    "input_table_file": specs["output_table_file"],
                    "output_table_name": output_tbl,
                    "output_table_file": new_tbl_file,
                    "input_explicit_col": specs["output_explicit_col"],
                    # "operation_rule": "Sort: desc(%s)" % specs["output_explicit_col"][0]
                    "operation_rule": "Sort rows by desc(%s)" % specs["output_explicit_col"][0]
                }
                var2table[output_tbl] = specs_after["output_table_file"]

        
        elif func == "unite":
            specs["type"] = "combine_columns_merge"
            pi = 0
            if params.get('data'):
                specs["input_table_name"] = params.get('data')
            else:
                specs["input_table_name"] = params['none'][pi]
                pi += 1
            specs["input_table_file"] = var2table[specs["input_table_name"]]
            specs["output_table_name"] = output_tbl
            specs["output_table_file"] = "L%d (%s).csv" % (line_num, specs["output_table_name"])
            if params.get('col'):
                specs["output_explicit_col"] = [remove_quote(params.get('col'))]
            else:
                specs["output_explicit_col"] = [remove_quote(params['none'][pi])]
                pi += 1
            specs["input_explicit_col"] = []
            for i in range(pi, len(params['none'])):
                specs["input_explicit_col"].append(remove_quote(params['none'][i]))
            if params.get('sep'):
                specs["operation_rule"] = "Merge: '%s'" % params['sep']
            else:
                specs["operation_rule"] = "Merge: '_'"
                
            var2table[output_tbl] = specs["output_table_file"]
            
        elif func.endswith("_join"):
            specs["type"] = "combine_tables_" + func  
            specs["input_table_name"] = []
            pi = 0
            if params.get('x'):
                specs["input_table_name"].append(params['x'])
            else:
                specs["input_table_name"].append(params['none'][pi])
                pi += 1
            if params.get('y'):
                specs["input_table_name"].append(params['y'])
            else:
                specs["input_table_name"].append(params['none'][pi])
                pi += 1
            specs["input_table_file"] = [var2table[specs["input_table_name"][0]], var2table[specs["input_table_name"][1]]]
            specs["output_table_name"] = output_tbl
            specs["output_table_file"] = "L%d (%s).csv" % (line_num, specs["output_table_name"])
            # 暂时不支持 by=c("A"="B") 的这种情况
            if params.get('by'):
                if params['by'].startswith("c("):
                    specs["input_explicit_col"] = remove_quote(remove_quote(p_match_c.findall(params['by'])[0].strip().split(',')))
                else:
                    specs["input_explicit_col"] = [remove_quote(params['by'])]
            elif pi < len(params['none']):
                if params['none'][pi].startswith("c("):
                    specs["input_explicit_col"] = remove_quote(remove_quote(p_match_c.findall(params['none'][pi])[0].strip().split(',')))
                else:
                    specs["input_explicit_col"] = [remove_quote(params['none'][pi])]
            if not specs.get("input_explicit_col"):
                input1_cols = set(col_states[var2num(specs["input_table_name"][0])])
                input2_cols = set(col_states[var2num(specs["input_table_name"][1])])
                implicit_col = remove_quote(list(input1_cols & input2_cols))
                specs["input_explicit_col"] = implicit_col
            if len(specs["input_explicit_col"]) == 1:
                specs["operation_rule"] = "%s on %s" % (func.replace("_", " ").title(), specs["input_explicit_col"][0]) # .title 将各单词的首字母大写
            else:
                specs["operation_rule"] = "%s on %s" % (func.replace("_", " ").title(), ",".join(specs["input_explicit_col"])) # .title 将各单词的首字母大写
            
            var2table[output_tbl] = specs["output_table_file"]
            
        elif func == 'mutate':
            # 暂时仅支持单个操作，即一个等于号
            specs["input_table_name"] = params['none'][0]
            specs["input_table_file"] = var2table[specs["input_table_name"]]
            specs["output_table_name"] = output_tbl
            specs["output_table_file"] = "L%d (%s).csv" % (line_num, specs["output_table_name"])
            input_line_num = var2num(specs["input_table_name"])
            for pk, pv in params.items():
                pk = remove_quote(pk)
                if pk in ('none', ".keep", ".before", ".after"):
                    continue
                specs["output_explicit_col"] = [pk]
                specs["input_explicit_col"] = [i for i in col_states[input_line_num] if i in parseCondition(pv)]
                # rule = "%s=%s" % (pk, pv)
                # specs["operation_rule"] = "Mutate: " + rule
                specs["operation_rule"] = "Create %s from %s" % (pk, pv)
                if pk in col_states[input_line_num]:
                    if not params.get(".keep") or remove_quote(params.get(".keep")) == "all":
                        # 原来的列，且保留所有的列：transform
                        specs["type"] = 'transform_columns_mutate'
                    elif remove_quote(params.get(".keep")) == "unused":
                        # 原来的列，且删除使用的列：transform
                        if len(specs["input_explicit_col"]) > 1:
                            specs["type"] = 'combine_columns_mutate'
                        else:
                            specs["type"] = 'transform_columns_mutate'   
                else:
                    if not params.get(".keep") or remove_quote(params.get(".keep")) == "all":
                        # 新增的列，且保留所有的列：create
                        specs["type"] = 'create_columns_mutate'
                        if group_states.get(input_line_num):
                            specs["input_implicit_col"] = [group_states[input_line_num][-1]]
                            specs["operation_rule"] = "Group: %s, %s" % (specs["input_implicit_col"][0], specs["operation_rule"])
                    if remove_quote(params.get(".keep")) == "unused":
                        # 新增的列，且删除使用的列：transform
                        if len(specs["input_explicit_col"]) > 1:
                            specs["type"] = 'combine_columns_mutate'
                        elif len(specs["input_explicit_col"]) == 1:
                            specs["type"] = 'transform_columns_mutate'
                        else:
                            specs["type"] = 'create_columns_mutate'
                break
            
            var2table[output_tbl] = specs["output_table_file"]
            
        elif func == 'arrange':

            # 暂时先做单列排序
            specs["type"] = 'transform_tables_sort'
            specs["input_table_name"] = params['none'][0]
            specs["input_table_file"] = var2table[specs["input_table_name"]]
            specs["output_table_name"] = output_tbl
            specs["output_table_file"] = "L%d (%s).csv" % (line_num, specs["output_table_name"])
            if params['none'][1].startswith("desc"):
                specs["input_explicit_col"] = [remove_quote(params['none'][1][5:-1])]
                # specs["operation_rule"] = "Sort: desc(%s)" % specs["input_explicit_col"][0]
                specs["operation_rule"] = "Sort rows by desc(%s)" % specs["input_explicit_col"][0]
            elif params['none'][1].startswith("-"):
                specs["input_explicit_col"] = [remove_quote(params['none'][1][1:])]
                # specs["operation_rule"] = "Sort: desc(%s)" % specs["input_explicit_col"][0]
                specs["operation_rule"] = "Sort rows by desc(%s)" % specs["input_explicit_col"][0]
            else:
                specs["input_explicit_col"] = [remove_quote(params['none'][1])]
                # specs["operation_rule"] = "Sort: " + params['none'][1]
                specs["operation_rule"] = "Sort rows by asc(%s)" % params['none'][1]
            
            var2table[output_tbl] = specs["output_table_file"]

        elif func == 'merge':
            specs["type"] = "combine_tables_extend"
            specs["input_table_name"] = []
            pi = 0
            if params.get('x'):
                specs["input_table_name"].append(params['x'])
            else:
                specs["input_table_name"].append(params['none'][pi])
                pi += 1
            if params.get('y'):
                specs["input_table_name"].append(params['y'])
            else:
                specs["input_table_name"].append(params['none'][pi])
                pi += 1
            ######################################################
            specs["input_explicit_col"] = []
            if params.get("by"):
                specs["input_explicit_col"].extend(remove_quote([params["by"]]))
            else:
                if params.get("by.x"):
                    specs["input_explicit_col"].append(remove_quote(params["by.x"]))
                if params.get("by.y"):
                    specs["input_explicit_col"].append(remove_quote(params["by.y"]))
            ######################################################
            specs["input_table_file"] = [var2table[specs["input_table_name"][0]], var2table[specs["input_table_name"][1]]]
            specs["output_table_name"] = output_tbl
            specs["output_table_file"] = "L%d (%s).csv" % (line_num, specs["output_table_name"])
            if not params.get("all") or remove_quote(params.get("all")) in ("F", "FALSE"):
                specs["operation_rule"] = "Extend"
            elif params.get("all") in ("T", "TRUE"):
                specs["operation_rule"] = "Extend"
                
            var2table[output_tbl] = specs["output_table_file"]
            
        elif func == 'rbind':
            # 既可以连接两表，也可以Create Rows
            specs["output_table_name"] = output_tbl
            specs["output_table_file"] = "L%d (%s).csv" % (line_num, specs["output_table_name"])
            if var2table.get(params['none'][0]) and var2table.get(params['none'][1]):
                specs["type"] = "combine_tables_extend"
                specs["input_table_name"] = [params['none'][0], params['none'][1]]
                specs["input_table_file"] = [var2table[specs["input_table_name"][0]], var2table[specs["input_table_name"][1]]]
                specs["operation_rule"] = "Extend"
            else:
                if var2table.get(params['none'][0]):
                    specs["input_table_name"] = params['none'][0]
                elif var2table.get(params['none'][1]):
                    specs["input_table_name"] = params['none'][1]
                specs["type"] = "create_rows_create"
                specs["input_table_file"] = var2table[specs["input_table_name"]]
                specs["operation_rule"] = "Create Row"

            var2table[output_tbl] = specs["output_table_file"]
            
        elif func == "bind_rows":
            specs["type"] = "combine_tables_extend"
            specs["input_table_name"] = [params['none'][0], params['none'][1]]
            specs["input_table_file"] = [var2table[specs["input_table_name"][0]], var2table[specs["input_table_name"][1]]]
            specs["output_table_name"] = output_tbl
            specs["output_table_file"] = "L%d (%s).csv" % (line_num, specs["output_table_name"])
            specs["operation_rule"] = "Extend"
            
            var2table[output_tbl] = specs["output_table_file"]
            
        elif func == "subset":
            # 先不考虑subset和select，涉及到separate
            specs["type"] = 'delete_rows_filter'
            pi = 0
            if params.get('x'):
                specs["input_table_name"] = params['x']
            else:
                specs["input_table_name"] = params['none'][pi]
                pi += 1
            # print(var2table)
            specs["input_table_file"] = var2table[specs["input_table_name"]]
            specs["output_table_name"] = output_tbl
            specs["output_table_file"] = "L%d (%s).csv" % (line_num, specs["output_table_name"])
            # condition = r[3].replace(params['none'][0],"").strip().strip(",").strip()
            condition = ",".join(r[3].strip().split(",")[1:]).strip()
            specs["input_explicit_col"] = [i for i in col_states[line_num] if i in parseCondition(condition)]
            specs["operation_rule"] = 'Keep rows where ' + condition
            
            var2table[output_tbl] = specs["output_table_file"]
            
        elif func == 'unique':
            specs["type"] = 'delete_rows_deduplicate'
            pi = 0
            if params.get('.data'):
                specs["input_table_name"] = params['.data']
            else:
                specs["input_table_name"] = params['none'][pi]
                pi += 1
            specs["input_table_file"] = var2table[specs["input_table_name"]]
            specs["output_table_name"] = output_tbl
            specs["output_table_file"] = "L%d (%s).csv" % (line_num, specs["output_table_name"])
            specs["operation_rule"] = "Delete duplicate rows"
            
            var2table[output_tbl] = specs["output_table_file"]
            
        elif func == 'distinct':
            specs["type"] = 'delete_rows_deduplicate'
            pi = 0
            if params.get('x'):
                specs["input_table_name"] = params['x']
            else:
                specs["input_table_name"] = params['none'][pi]
                pi += 1
            specs["input_table_file"] = var2table[specs["input_table_name"]]
            specs["output_table_name"] = output_tbl
            specs["output_table_file"] = "L%d (%s).csv" % (line_num, specs["output_table_name"])
            specs["input_explicit_col"] = remove_quote(params['none'][pi:])
            specs["operation_rule"] = "Delete duplicate rows"
            
            var2table[output_tbl] = specs["output_table_file"]

        elif func == 'cbind':
            specs["output_table_name"] = output_tbl
            specs["output_table_file"] = "L%d (%s).csv" % (line_num, specs["output_table_name"]) 
            if len(params['none']) and var2table.get(params['none'][0]):
                specs["type"] = 'create_columns_create'
                specs["input_table_name"] = remove_quote(params['none'][0])
                specs["input_table_file"] = var2table[specs["input_table_name"]]
                specs["output_explicit_col"] = []
                for pk, pv in params.items():
                    pk = remove_quote(pk)
                    if pk in ('none', "deparse.level"):
                        continue
                    specs["output_explicit_col"].append(pk)

                specs["operation_rule"] = 'Create Columns: ' + ",".join(specs["output_explicit_col"])
            else:
                specs["type"] = 'create_tables'
                specs["operation_rule"] = 'Create Manually'
                var2table[output_tbl] = specs["output_table_file"]
            
            var2table[output_tbl] = specs["output_table_file"]

        elif func == 'as.data.frame':
            if not (len(params['none']) and var2table.get(params['none'][0])):
                specs["output_table_name"] = output_tbl
                specs["output_table_file"] = "L%d (%s).csv" % (line_num, specs["output_table_name"]) 
                specs["type"] = 'create_tables'
                specs["operation_rule"] = 'Create Manually'
                var2table[output_tbl] = specs["output_table_file"]
            else:  # 如果第一个无名参数本身就是table，那就不算是 create_tables
                specs["input_table_name"] = remove_quote(params['none'][0])
                specs["input_table_file"] = var2table[specs["input_table_name"]]
                specs["output_table_name"] = output_tbl
                specs["output_table_file"] = "L%d (%s).csv" % (line_num, specs["output_table_name"]) 
                specs["type"] = 'identical_operation'
                # specs["operation_rule"] = "%s(%s)" % (func, r[3])  # 函数名加参数
                specs["operation_rule"] = func
                var2table[output_tbl] = specs["output_table_file"]
        
        elif func == 'rename':
            specs["output_table_name"] = output_tbl
            specs["output_table_file"] = "L%d (%s).csv" % (line_num, specs["output_table_name"]) 
            specs["type"] = 'transform_columns_rename'
            specs["input_table_name"] = remove_quote(params['none'][0])
            specs["input_table_file"] = var2table[specs["input_table_name"]]
            specs["input_explicit_col"] = []
            specs["output_explicit_col"] = []
            for pk, pv in params.items():
                pv = remove_quote(pv)
                if pk in ('none'):
                    continue
                specs["input_explicit_col"].append(pv)
                specs["output_explicit_col"].append(remove_quote(pk))
            specs["operation_rule"] = 'Rename columns'
            
            var2table[output_tbl] = specs["output_table_file"]

        elif func in ("ungroup", "group_by"):
            specs["input_table_name"] = remove_quote(params['none'][0])
            specs["input_table_file"] = var2table[specs["input_table_name"]]
            specs["output_table_name"] = output_tbl
            specs["output_table_file"] = "L%d (%s).csv" % (line_num, specs["output_table_name"]) 
            specs["type"] = 'identical_operation'
            if len(params['none'])>1:
                specs["operation_rule"] = "%s: %s" % (func, ",".join(remove_quote(params['none'][1:])))
            else:
                specs["operation_rule"] = func  # 函数名加参数
            # specs["operation_rule"] = "%s(%s)" % (func, r[3])  # 函数名加参数
            var2table[output_tbl] = specs["output_table_file"]

        elif func == "group_split":
            # print(output_tbl, params, col_states)
            specs["type"] = 'separate_tables_decompose'
            specs["input_table_name"] = remove_quote(params['none'][0])
            specs["input_table_file"] = var2table[specs["input_table_name"]]
            specs["output_table_name"] = []
            specs["output_table_file"] = []
            for i in range(1,20):
                index_id = "%d_%d" % (line_num, i)
                if col_states.get(index_id):
                    specs["output_table_name"].append("%s_%d" % (output_tbl, i))
                    specs["output_table_file"].append("L%s (%s).csv" % (index_id, specs["output_table_name"][-1]))
                    var2table[specs["output_table_name"][-1]] = specs["output_table_file"][-1]
                else:
                    break
            specs["input_explicit_col"] = [remove_quote(params['none'][1])]
            specs["operation_rule"] = "Decompose by %s" % specs["input_explicit_col"][0]


        else: # default, could also just omit condition or 'if True'
            print("The function, %s, is not currently supported!" % func)
            specs["type"] = 'identical_operation'
            specs["input_table_name"] = remove_quote(params['none'][0])
            specs["input_table_file"] = var2table[specs["input_table_name"]]
            specs["output_table_name"] = output_tbl
            specs["output_table_file"] = "L%d (%s).csv" % (line_num, specs["output_table_name"]) 
            specs["operation_rule"] = func

            var2table[output_tbl] = "L%d (%s).csv" % (line_num, output_tbl)


        if len(transform_specs) >= 1 and specs["type"] in ("transform_columns_rename", "delete_columns_select_remove"):
            # 如果类型相同，而且此步的输入表是上一步的输出表，则遇到rename，delete可以合并
            if transform_specs[-1]["type"] == specs["type"] and specs["input_table_file"] == transform_specs[-1]["output_table_file"]:
                if specs["type"] == 'transform_columns_rename':
                    specs_combine["type"] = 'transform_columns_rename'
                    specs_combine["output_table_name"] = specs["output_table_name"]
                    specs_combine["output_table_file"] = specs["output_table_file"]
                    specs_combine["input_table_name"] = transform_specs[-1]["input_table_name"]
                    specs_combine["input_table_file"] = transform_specs[-1]["input_table_file"]
                    # using * operator to concat: [*test_list1, *test_list2]
                    specs_combine["input_explicit_col"] = [*transform_specs[-1]["input_explicit_col"], *specs["input_explicit_col"]]
                    specs_combine["output_explicit_col"] = [*transform_specs[-1]["input_explicit_col"], *specs["input_explicit_col"]]
                    specs_combine["operation_rule"] = 'Rename columns'
                elif specs["type"] == 'delete_columns_select_remove':
                    specs_combine["type"] = 'delete_columns_select_remove'
                    specs_combine["output_table_name"] = specs["output_table_name"]
                    specs_combine["output_table_file"] = specs["output_table_file"]
                    specs_combine["input_table_name"] = transform_specs[-1]["input_table_name"]
                    specs_combine["input_table_file"] = transform_specs[-1]["input_table_file"]
                    # using * operator to concat: [*test_list1, *test_list2]
                    specs_combine["input_explicit_col"] = [*transform_specs[-1]["input_explicit_col"], *specs["input_explicit_col"]]
                    # specs_combine["output_explicit_col"] = [*transform_specs[-1]["input_explicit_col"], *specs["input_explicit_col"]]
                    specs_combine["operation_rule"] = 'Delete ' + ','.join(specs_combine["input_explicit_col"])
                
            
        # print(func, specs)
        if specs_combine:
            # transform_specs.append(specs_combine)
            transform_specs[-1] = specs_combine
            continue
        if specs:
            transform_specs.append(specs)
        if specs_after:
            transform_specs.append(specs_after)
        
    return transform_specs
 