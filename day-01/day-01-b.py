from collections import Counter
list1 = []
list2 = Counter()
with open('input') as input:
	lines = input.readlines()
	for l in lines:
		try:
			a, b = l.split()
			list1.append(int(a))
			list2.update({int(b), 1})
		except:
			print(f"Error on line {l}")
			raise

d = 0
for a in list1:
	d += a * list2[a]

print(d)
	
