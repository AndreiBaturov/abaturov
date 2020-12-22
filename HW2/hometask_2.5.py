list = [7, 5, 3, 3, 2]
rating = int(input("Please enter a new rating: "))
list.append(rating)
list.sort(reverse=True)
print("Result: ",list)
