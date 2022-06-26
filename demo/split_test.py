
from os import remove


n = 5

lst = []
for i in range(125):
    lst.append(i)
    
length = len(lst)

def dumper():
    global n
    global lst
    intercept = len(lst) // n

    def foo(lst, intercept):
        sp_lst = []
        if len(lst) - intercept * n < intercept:
            for _ in range(n):
                sublist = lst[0:intercept]
                sp_lst.append(sublist)
                for item in sublist:
                    lst.remove(item)
            if lst != []:
                sp_lst.append(lst)
        else:
            intercept = intercept + 1
            sp_lst = foo(lst, intercept)
        return sp_lst
    sp_lst = foo(lst, intercept)
    if len(sp_lst) > n:
        m = sp_lst[-1]
        for n in range(len(m)):
            sp_lst[-1 - (n + 1)].append(m[0])
            m.remove(m[0])
    for p in sp_lst:
        if p == []:
            sp_lst.remove(p)

    return sp_lst

print(dumper())


    #for _ in range(n):
    #    sublist = lst[0:intercept]

    #    print(sublist)
    #    for item in sublist:
    #        lst.remove(item)

    


    


#thread_ = []
#for i in range(n):
#    thread = threading.Thread(target=starter).start()

