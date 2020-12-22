revenue = int(input("Enter an income value: "))
expenses = int(input("Enter a value of expenses: "))

if revenue > expenses:
   print(f"We are finishing this year with fantastic results. We have a pretty high income.")
   profitability =  (revenue - expenses)/revenue
   print(f"We earned a profit: ",profitability)
   workers = int(input("Enter a number of workers: "))
   income_for_1_employee = (revenue - expenses)/workers
   print("We earned "+str(income_for_1_employee)+" per 1 employee")
else: print(f"We are finishing this year with bad results. We are almost a bankrupt.")
