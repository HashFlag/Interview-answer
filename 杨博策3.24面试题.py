# 第一题
source_dict = {'key0': 'a', 'key1': 'b', 'key2': {'inner_key0': 'c', 'inner_key1': 'd'}}
update_dict = {'key1': 'x', 'key2': {'inner_key0': 'y'}}


def merge_dict(source_dict, update_dict):
    res = {}
    for k, v in source_dict.items():
        if k not in update_dict:
            res[k] = source_dict[k]
        else:
            if isinstance(source_dict[k], dict) and isinstance(update_dict[k], dict):
                res[k] = merge_dict(source_dict[k], update_dict[k])  # 递归
            else:
                res[k] = update_dict[k]

    return res


print(merge_dict(source_dict, update_dict))

# 第二题
conversion = {
    '0': '', '1': '', '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl', '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
}


def num_combination(digits):
    try:
        int(digits)  # 判断是否只含有数字
    except ValueError:
        return "请输入2-9之间的数字，不能包括字母"
    if len(digits) == 0:
        return []
    product = ['']
    for k in digits:
        product = [i + j for i in product for j in conversion[k]]
    return product


print(num_combination("345"))

# 第三题
"""
一. 内存泄露：

我认为内存泄露的根本原因就是因为：内存不是无限大的（有生之年应该看不到无限大的内存吧 哈哈）
每当程序创建一个新变量时，会分配一些内存来存储该变量的内容，也就是变量引用了一块内存空间。
每种编程语言都提供了要求内核分配和释放内存块，以供运行程序运行的方法，（python当然也有自己内存管理方法，垃圾回收机制就是其中的一种。）
当程序要求内核留出一块内存来使用时，但是某些时候由于错误，程序永远不会告诉内核它何时结束使用该内存。
这种情况下，内核会认为被这个内存块仍在被使用，而其他程序就无法访问这些内存块，相当于丢了一块内存。
一次内存泄露的危害几乎可以忽略，但是内存泄露堆积起来的后果就会很严重，因为被遗忘的内存的总大小可能会变得非常大，从而消耗计算机内存的很大一部分。
在这种情况下，如果客户端不停止，内存会一直涨，最后的结果就是把系统内存吃完，然后进程被系统杀掉了。
"""

# 内存泄露场景：
import objgraph  # pip install objgraph

list1 = []


class OBJ(object):
    pass


def func_to_leak():
    obj = OBJ()
    list1.append(obj)

    if True:
        return
    list1.remove(obj)


objgraph.show_growth()
func_to_leak()
print('after call func_to_leak')
objgraph.show_growth()

"""
结果：
after call func_to_leak
OBJ      1       +1

函数开始的时候把对象加入了列表list1中，期望是在函数退出之前从list1中删除，但是由于提前返回，并没有执行到最后的remove语句。从运行结果可以发现，
调用函数之后，增加了一个类OBJ的实例，然而理论上函数调用结束之后，所有在函数作用域中声明的对象都应被销毁，因此这里存在内存泄露。
"""
