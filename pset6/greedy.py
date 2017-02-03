amount = -1
running = 0
change = {"Quarters": 0, "Dimes": 0, "Nickels": 0, "Pennies": 0}

while amount < 0:
    print("Amount of change:", end=" ")
    amount = float(input())

while running + 0.25 <= amount:
    running += 0.25
    change['Quarters'] += 1

while running + 0.1 <= amount:
    running += 0.1
    change['Dimes'] += 1

while running + 0.05 <= amount:
    running += 0.05
    change['Nickels'] += 1

while running + 0.01 <= amount:
    running += 0.01
    change['Pennies'] += 1

for key, value in change.items():
    print("{}: {}".format(key, value))
