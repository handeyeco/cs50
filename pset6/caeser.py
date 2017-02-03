import sys

if len(sys.argv) < 2:
    print("No argument")
    exit(1)

key = int(sys.argv[1])

if key < 0:
    print("Non-positive")
    exit(1)

print("Unencrypted:", end=" ")
unencrypted = input()
encrypted = ""

for char in unencrypted:
    if char.isalpha():
        char = ord(char)
        if char >= 65 and char <= 90:
            gap = 65
            char -= gap
        else:
            gap = 97
            char -= gap
        char = chr((((char + key) % 26) + gap))
        encrypted += char
    else:
        encrypted += char

print("Encrypted: {}".format(encrypted))
exit(0)
