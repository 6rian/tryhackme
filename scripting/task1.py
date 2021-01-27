import base64

file = open("encoded_flag.txt","r")
flag = file.read()

for i in range(1,51):
	flag = base64.b64decode(flag)

print(flag.decode())
