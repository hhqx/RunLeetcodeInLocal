import inspect
import re
import sys
import time

# 巨好用的在线网站: https://regex101.com/
# 正则非获取匹配: https://www.cnblogs.com/whaozl/p/5462865.html,
# 正向反向, 肯定非获取:  (str?<=), (?=str)
# 正向反向, 否定非获取:  (str?<!), (?!str)
# 另外: str1|str2 的简洁形式:  str(?:1|2)

from typing import *

from rich.console import Console
from rich.table import Table

import re

def multiple_replacer(*key_values):
    replace_dict = dict(key_values)
    replacement_function = lambda match: replace_dict[match.group(0)]
    pattern = re.compile("|".join([re.escape(k) for k, v in key_values]), re.M)
    return lambda string: pattern.sub(replacement_function, string)

def multiple_replace(string, *key_values):
    return multiple_replacer(*key_values)(string)


class GetLeetCodeTestCase:
    def __init__(self, problem_content, regex=None):
        replace_map = (('null', 'None'), ('true', 'True'), ('false', 'False'), ('测试用例', 'Input'), ('期望结果', 'Output'))

        # for arg in (('null', 'None'), ('true', 'True'), ('false', 'False')):  # replace strings
        #     problem_content = problem_content.replace(*arg)
        problem_content = multiple_replacer(*replace_map)(problem_content)
        
        self.str = problem_content
        # self.regex = r"^(Input|Output): ?(.*)$"  # 以 换行符号 作为分割
        # self.regex = r"^(Input:|Output:)([\s\S]*?)(\n ?\n|(?=\n[A-Z]))"  # 以 双换行符号 或者 换行符加大写字母 作为分割
        self.regex = r"^(Input:|Output:|输入：|输出：|输入:|输出:)([\s\S]*?)(\n ?\n|(?=\n[A-Z])|(?=\n[\u4e00-\u9fa5]))"  # 以 双换行符号 或者 换行符加大写字母（或汉字） 作为分割
        self.regex = regex if regex else self.regex

        # input and output variable
        self.inout_leading = {'输入：': 'Input', '输出：': 'Output',
                              'Input:': 'Input', 'Output:': 'Output',
                              '输入:': 'Input', '输出:': 'Output'}
        self.inout_string = {'Input': [], 'Output': []}
        self.inout_dict = {'Input': [], 'Output': []}
        pass

    def get_test_case(self):
        # 正则表达式匹配
        matches = re.finditer(self.regex, self.str, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            # extract input output string
            inout_type = self.inout_leading[match.group(1)]
            inout_str = match.group(2)
            # save to dict
            self.inout_string[inout_type].append(inout_str)  # append input and output string
            key_value = self.extract_KeyValue_in_Input(inout_str) if inout_type == "Input" \
                else eval(inout_str)  # get dict
            self.inout_dict[inout_type].append(key_value)
        return self.inout_dict

    def extract_KeyValue_in_Input(self, str):
        def find_delimiter(s):
            char_in = ['[', '{', '(', '"', "'", ]
            char_out = [']', '}', ')', '"', "'", ]

            ans = []
            stack = []
            for i, c in enumerate(s):
                if c in char_in:
                    if stack and stack[-1] in ['"', ","]:
                        stack.pop()
                    else:
                        stack.append(c)
                elif c in char_out:
                    stack.pop()
                    if not stack:
                        ans.append(i + 1)
                
                # 如果栈空且遇到',', '\n'
                if not stack and c in [',', '\n']:
                    ans.append(i)
                elif not stack and i==len(s)-1:
                    ans.append(i+1)
            return ans

        dict_out = {}
        # remove space
        # str = str.replace(' ', '')

        # find ',' before '='
        if '=' in str:
            delimiter = []
            comma = -1
            for idx, c in enumerate(str):
                if c == ',':
                    comma = idx
                elif c == '=' and comma >= 0:
                    delimiter.append(comma)
            delimiter += [len(str)]
        else:
            delimiter = find_delimiter(str)

        # extract key-value string
        start_end_position = [-1] + delimiter + [len(str)]
        cnt = 0
        for i in range(len(start_end_position) - 1):
            start, end = start_end_position[i]+1, start_end_position[i + 1]
            
            # key-value string
            string = str[start:end]
            if not string or string.isspace():
                continue
            # print(string)

            # get key-value dict
            # key, value_string = re.findall(r'(.*)=(.*)', string)[0]
            if '=' in string:
                idx_equal = string.index('=')
                key, value_string = string[:idx_equal], string[idx_equal + 1:]
                key = key.replace(' ', '').replace('\n', '')
            else:
                key, value_string = f'input_{cnt+1}', string
            cnt += 1
            
            dict_out[key] = eval(value_string)
            # print((key, value_string))

        return dict_out

class StartTest:
    def __init__(self, question_content, solution_class, isDesignedClass=False, regex=None):
        # read config
        self.config = {'isDesignedClass': False, 'outputIsSet': False}  # set default
        for k, v in {'isDesignedClass': isDesignedClass}.items():  # set config according to the input config
            # if k in self.config:
            self.config[k] = v

        # initial variables
        self.question_content = question_content
        self.input_import_func = None
        self.solution_class = solution_class
        self.designed_class = solution_class
        self.designed_obj = None
        self.regex = regex

        # Get Test Case
        self.get_test_case()

        if not self.config['isDesignedClass']:
            # Get Solution Entry
            self.Solution = solution_class()
            entry_function_name = self.get_solution_entry_function_name()
            self.get_input_import_func(entry_function_name)
            SolutionEntryHandle = getattr(self.Solution, entry_function_name)
        else:
            def evaluate(**kargs):
            # def evaluate(op, args):
                out = []
                # out = [getattr(self, f)(*arg) for f, arg in zip(op, args)]
                op = kargs['op'] if 'op' in kargs else kargs['input_1']
                args = kargs['args'] if 'args' in kargs else kargs['input_2']
                op, args = list(kargs.values())[:2]
                for f, arg in zip(op, args):
                    # print(f, arg)
                    if f == self.designed_class.__name__:
                        self.designedObj = self.designed_class(*arg)
                        out.append(None)
                    else:
                        f = getattr(self.designedObj, f)
                        out.append(f(*arg))
                return out
            SolutionEntryHandle = evaluate
        # Get Test Entry
        self.SolutionEntryHandle = SolutionEntryHandle
        pass

    def get_solution_entry_function_name(self):
        # self.solution_class, self.kwargs_in_name
        name_obj = list(inspect.getmembers(self.solution_class, inspect.isfunction))
        # 根据函数定义行号排序
        name_obj.sort(key=lambda x: x[1].__code__.co_firstlineno)

        # 利用inspect包，筛选 Solution 中的 function
        name = None
        for (func_name, func_obj) in name_obj:
            # get function args
            full_args = inspect.getfullargspec(func_obj)
            args = full_args.args
            # {func_name for (func_name, func_obj) in inspect.getmembers(input_class, inspect.import_from)}

            # 找出类内参数和输入参数一致的函数, 返回其名称
            if args[1:] == self.kwargs_in_name:
                # print(f'Test function name: Solution.{func_name}, args: {args}')
                name = func_name
        # 如果根据输入输出参数未找到名称一致的, 返回最后一个
        if not name and name_obj:
            name = name_obj[-1][0]
        
        return name

    def get_input_import_func(self, func_name):
        """ 若定义了类内方法 import_from_$Data_Type, 在本地调试时会将$Data_Type表示的输入数据导入到类中. """
        f = getattr(self.solution_class, func_name)
        full_args = inspect.getfullargspec(f)
        args = full_args.args[1:]
        args_annotation = {k: v for k, v in full_args.annotations.items() if k in args}  # typing包的输入参数注释

        input_import_func = {}
        input_class_dict = {}
        for arg in args:
            # input_class = args_annotation[arg]
            if arg not in args_annotation.keys():
                input_import_func[arg] = lambda x: x
                continue
            elif args_annotation[arg].__module__ == 'builtins':
                # 如果是默认的数据类型, 则直接转化为该类型
                # input_class = args_annotation[arg]
                # input_import_func[arg] = lambda x: input_class(x)
                input_import_func[arg] = lambda x: x
                continue

            input_class = get_args(args_annotation[arg])[0]
            if str(input_class) in input_class_dict.keys():  # 如果类型和之前的某个参数一致, 则复制之前参数的转化函数作为当前参数的转化函数
                input_import_func[arg] = input_class_dict[str(input_class)]
                continue
            else:
                pass

            if input_class.__module__ == 'builtins':
                # 如果typing里面是默认的数据类型, 则不变
                func = lambda x: x
            else:
                # 若定义了转化函数导入, 否则赋值为None
                funcs_in_class = {func_name for (func_name, func_obj) in
                                  inspect.getmembers(input_class, inspect.isfunction)}
                if 'import_from' in funcs_in_class:
                    func = lambda x: input_class().import_from(x)
                else:
                    func = lambda x: x

            input_import_func[arg] = func
            input_class_dict[str(input_class)] = func  # 保存之前参数的转化函数
        self.input_import_func = input_import_func  # 强制类型转化函数, 导入

    def get_test_case(self):
        # Get Test Case
        TestCase = GetLeetCodeTestCase(self.question_content, self.regex)
        data = TestCase.get_test_case()
        self.kwargs_in, self.ground_truth = data['Input'], data['Output'],
        self.kwargs_in_name = list(self.kwargs_in[0].keys())

    def run_test(self):
        # Rich Print Table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Name")
        table.add_column("Your input")
        table.add_column("Output")
        table.add_column("Expected")
        table.add_column("Elapsed time", style='italic', justify='center')
        table.add_column("Status", style='bold', justify='center')
        console = Console(color_system='windows') if sys.platform.startswith('win') else Console()

        # print_flag
        print_flag = False

        # Run Test
        for i, kwargs, result_true in zip(range(len(self.kwargs_in)), self.kwargs_in, self.ground_truth):
            # If data_class has defined import function, convert the input to specified data type.
            for k, v in kwargs.items():
                if self.input_import_func and k in self.input_import_func:
                    import_func = self.input_import_func[k]
                else:
                    import_func = lambda x: x
                kwargs[k] = import_func(v)
            # kwargs = kwargs.copy()
            input_str = '\n'.join([f'{k}: {v}' for k, v in kwargs.items()])  # input_str
            getTime = lambda : time.perf_counter_ns()  # perf_counter_ns: 计算sleep时间, process_time_ns: 不计算sleep时间
            start_time = getTime()
            # Call the Entry Function Handle to Run the Test
            if 'input_1' not in kwargs or ('isDesignedClass' in self.config and self.config['isDesignedClass']):
                my_out = self.SolutionEntryHandle(**kwargs)
            else:
                my_out = self.SolutionEntryHandle(*list(kwargs.values()))
            elapsed_time = "{:.3f}".format((getTime()-start_time)/(10**6))

            if print_flag:
                print('\n' + '_'*10 + f' TEST{i+1} ' + '_'*15)
                # print('[bold][magenta]' + '\n' + '_'*10 + f' TEST{i+1} ' + '_'*15 + '[/magenta][/bold]')
                print(f'Your input:')
                # print('[bold][white]' + 'Your input:' + '[/white][/bold]')
                for k, v in kwargs.items():
                    print(f'\t{k}: {v}')
                print(f'Output:\n\t{my_out}')
                # print('[green][bold]' + 'Output:' + f'[/bold]\t{my_out}[/green]')
                print(f'Expected :\n\t{result_true}')
                print(f'Elapsed time: {elapsed_time} ms')

            err_style = ['bold underline red']
            # err_style = ['bold italic red']
            corr_style = ['#3EFF33', '#B6FF0E']
            # input_str = '\n'.join([f'{k}: {v}' for k, v in kwargs.items()])
            status = True
            status = False
            status = result_true == my_out
            style = corr_style[i % len(corr_style)] if status else err_style[0]
            table.add_row(
                f"Test {i+1}", f"{input_str}", f"{my_out}", f"{result_true}", f"{elapsed_time}ms",
                "Correct" if status else "Wrong",
                style=style
            )


        console.print(table)
        pass
