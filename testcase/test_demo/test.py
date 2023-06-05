import inspect

def func1():
    func2()

def func2():
    info = inspect.getframeinfo(inspect.currentframe().f_back)
    print(info.function, " was called from line ", info.lineno, " in ", info.filename)

func1()