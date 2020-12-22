def hometask_35():
    sum = 0
    finish = False

    while True:
         number = input("Enter sequence of numbers: ").split()
         for num in number:
             if num == "#":
                finish = True
                break
             if not num.isdigit():
                 print(f"This is not a number {num}")
                 break
             sum = sum + int(num)

         print(f"Total sum: {sum}")
         if finish:
             break

hometask_35()