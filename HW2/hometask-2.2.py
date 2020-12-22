list = []

# number of elemetns as input
n = int(input("Enter number of elements : "))

# iterating till the range
for i in range(0, n):
    elem = int(input())
    list.append(elem)

i = 0
j = 0
while i < len(list)/2:
   list[j], list[j+1] = list[j+1], list[j]
   i = i+1
   j = j+2
   if len(list)%2 > 0 and i > len(list)/2-1: break

print(list)