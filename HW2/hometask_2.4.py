str = input(f"Please enter a string: ")
list = str.split(' ')
for index, value in enumerate(list):
    print(index, value[:10])

