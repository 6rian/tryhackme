import re
import requests
import time

host = "10.10.251.16"
port = 3010
throttle = 4
n = 0


def dump():
	global n, port
	print(f"[i] n={n}, port={port}")


def makeRequest():
	global throttle
	url = f"http://{host}:{port}/"
	print(f"Requesting: {url}")
	response = requests.get(url)
	time.sleep(throttle)
	return response


def handleResponse(r):
	global port, end
	global totalRequests

	if (r == "STOP" or port == 9765):
		print("STOP!")
		end = True

	print("[*] " + r)

	instructions = r.split(' ')  # ex: minus 212 35432
	dump()
	doOperation(instructions[0], instructions[1])
	dump()
	port = instructions[2]
	print(f"Moving to port: {port}")
	return ""


def doOperation(op, val):
	global n
	if op == "add":
		n += val
	elif op == "minus":
		n -= val
	elif op == "multiply":
		n *= val
	elif op == "divide":
		n /= val
	else:
		print(f"!! Unknown operator: {op}")
	return


# make initial request and parse out the next port
r = makeRequest()
match = re.search(r'onPort\"\>(\d+)\<', r.text)
port = match.group(1)

end = False
totalRequests = 0

while not end:
	try:
		totalRequests += 1
		print(totalRequests, end=' - ')
		handleResponse(makeRequest().text)
	except:
		print(f"{port} is closed.")
		end = True