lst = [1,2,3]
def GetFirstElementInList(lst):
    if type(lst) != list:
        print('[main(warn)]: 变量类型错误, 类型: {}'.format(type(lst)))
    else:
        element = lst[0]
        lst.remove(element)
        return element

print(GetFirstElementInList(lst))
print(lst)

