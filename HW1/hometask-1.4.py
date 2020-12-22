import math
print("Enter the Number :")
num=int(input())
Largest=0;
while (num > 0):
    reminder=num%10
    if Largest<reminder:
        Largest = reminder
    num =int(num / 10)
print("The Largest Digit is :", Largest)