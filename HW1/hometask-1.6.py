first_result = int(input("Please enter a result for the first training day: "))
final_result = int(input("Please enter a result for the last training day: "))
result = int(first_result)
day = 1

while result <= final_result:
    result += result*0.1
    day += 1

print("You have reached the final result by the day: ", day)
