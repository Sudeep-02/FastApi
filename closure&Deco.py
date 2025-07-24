def decor(num):
    def wrapper(x):
        print(x)
        return x + num

    return wrapper


f = decor(2)
print(f)
x = f(5)
print(x)
