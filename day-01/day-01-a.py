
list1 = []
list2 = []
with open('input') as input:
	lines = input.readlines()
	for l in lines:
		try:
			a, b = l.split()
			list1.append(int(a))
			list2.append(int(b))
		except:
			print(f"Error on line {l}")
			raise

list1.sort()
list2.sort()
d = 0
for a, b in zip(list1, list2):
	d += abs(a-b)

print(d)
	
