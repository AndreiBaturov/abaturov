seasons = {'winter': [1, 2, 12], 'spring': [3, 4, 5], 'summer': [6, 7, 8], 'autumn': [9, 10, 11]}

flag = 0
month = int(input("Please enter a serial number of a month in a year: "))
for i in seasons:
   for i, j in seasons.items():
       if month in j:
         print(i)
         flag = 1
         break
       if flag == 1: break