def division(numerator, denominator):

    try:
       result = numerator / denominator
    except ZeroDivisionError:
       denominator = 0
       raise ValueError("Division by 0 is not allowed")

    return result

print(division(9, 3))