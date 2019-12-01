def has_unique_words(passwd):
    words = passwd.split()
    return len(set(words)) == len(words)

def has_unique_anagrams(passwd):
    words = [''.join(sorted(word)) for word in passwd.split()]
    return len(set(words)) == len(words)

with open('input-4.txt') as f:
    print(sum(has_unique_words(passwd) for passwd in f))
    f.seek(0)
    print(sum(has_unique_anagrams(passwd) for passwd in f))
