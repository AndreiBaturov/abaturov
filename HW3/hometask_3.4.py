# A function to set an extent without loop
def extent(x, y):

    x = x**y
    return x

print(extent(2, 10))

# A function to return an extent with loop

def extent2(x, y):
    num = x
    i = 1
    while i < y:
        x = x*num
        i += 1
    return x

print(extent2(2, 10))