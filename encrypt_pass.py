
def encrypt(data, shift):
    encrypted = ""
    for i in range(len(data)):
        char = data[i]
        if char.isupper():
            encrypted += chr((ord(char) + shift - 65) % 26 + 65)
        elif char.islower():
            encrypted += chr((ord(char) + shift - 97) % 26 + 97)
        elif char.isdigit():
            number = (int(char) + shift) % 10
            encrypted += str(number)
        else:
            encrypted += char
    return encrypted

def decrypt(data, shift):
    decrypted = ""
    for i in range(len(data)):
        char = data[i]
        if char.isupper():
            decrypted += chr((ord(char) - shift - 65) % 26 + 65)
        elif char.islower():
            decrypted += chr((ord(char) - shift - 97) % 26 + 97)
        elif char.isdigit():
            number = (int(char) - shift) % 10
            decrypted += str(number)
        else:
            decrypted += char
    return decrypted