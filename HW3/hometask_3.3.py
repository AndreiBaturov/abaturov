def sum_maxvalues(*args):
    first_maxval = args[0]
    second_maxval = args[0]
    for arg in args:
        if arg > first_maxval:
           second_maxval = first_maxval
           first_maxval = arg
        elif arg < first_maxval and arg > second_maxval:
           second_maxval = arg

    return first_maxval + second_maxval

print(sum_maxvalues(4, 11, 5, 14, 3, 10, 19, 6))