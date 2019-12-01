def rand_seq(start, mult, multiples=1):
    prev = start
    while True:
        prev = (prev * mult) % 2147483647
        if prev % multiples == 0:
            yield prev

def matches(npairs, gen_a, gen_b):
    count = 0
    for i, (a, b) in enumerate(zip(gen_a, gen_b)):
        if i == npairs: break
        if (a & 65535) == (b & 65535): count += 1
    return count

gen_a_start = 783
gen_a_mult = 16807

gen_b_start = 325
gen_b_mult = 48271

print(matches(5000000, rand_seq(gen_a_start, gen_a_mult, 4), rand_seq(gen_b_start, gen_b_mult, 8)))
