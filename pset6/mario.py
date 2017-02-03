print "Height: ",
height = input()

for row in range(height):
    text = ""
    for i in range(height + 1):
        if i < height - 1 - row:
            text = text + " "
        else:
            text = text + "#"
    print(text)
    row = row + 1
