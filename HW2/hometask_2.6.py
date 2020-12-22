index = 1
result = []
spec = ["name", "price", "number", "color"]

while True:
    question = input("Should a new product be added yes or no ? ")
    if question.upper() == "NO":
        break
    item = {}

for spe in spec:
    user_data = input(f"Enter {spe} ")
    if user_data.isdigit():
        item[spe] = int(user_data)
    else:
        item[spe] = user_data

result.append(tuple([index, item]))
index += 1

print(result)

res_dict = {}

for item in spec:
    for param in result:
        if res_dict.get(item):
            res_dict[item].append(param[1].get(item))
        else:
            res_dict[item] = [param[1].get(item)]

print(res_dict)