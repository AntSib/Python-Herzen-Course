var = "per aspera ad astra"

def bar():
    var = "emptyness"

    def foo():
        global var
        return var+"!"

    return foo()


print(bar())
