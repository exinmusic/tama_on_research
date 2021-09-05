with open("tg19_bg50010.txt", "rb") as f:
	output = ""
	count1 = 0
	for line in f.readlines():
		n = 20
		chunks = [line[i:i+n] for i in range(0, len(line), n)]
		for chunk in chunks:
			hex_line = chunk.hex()
			output += (hex_line+'\n')
			count1 += 1

print(output)

with open("new_owned2.txt", "w") as f2:
	f2.write(output)

# with open("owned_bg.txt", "r") as f:
# 	count2 = 0
# 	for i in f.readlines():
# 		hex_line = i[:-1]
# 		#ln = bytes.fromhex(hex_line)
# 		print(hex_line)
# 		count2 += 1

# print(f"COUNT1: {count1}")
# print(f"COUNT2: {count2}")
# print(f"LINE DIFF: {count1-count2}")
