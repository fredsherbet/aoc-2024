
def next_secret(n):
    n = prune(mix(n, n*64))
    n = prune(mix(n, n//32))
    n = prune(mix(n, n*2048))
    return n

def mix(a, b):
    return a^b

def prune(n):
    return n % 16777216

with open('input') as input:
    nums = [int(l.strip()) for l in input]

s = 0
for n in nums:
    secret = n
    for _ in range(2000):
        secret = next_secret(secret)
    print(f"{n}: {secret}")
    s += secret

print(s)

