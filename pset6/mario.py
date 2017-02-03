height = 0

while height < 1 or height > 23:
    print("Height (1-23):", end=" ")
    height = int(input())

for row in range(height):
    text = ""
    for i in range(height + 1):
        if i < height - 1 - row:
            text += " "
        else:
            text += "#"
    print(text)
    row += 1
