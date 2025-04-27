import timeit

# Boyer-Moore
from collections import defaultdict

def boyer_moore(text, pattern):
    m, n = len(pattern), len(text)
    if m == 0: return 0
    char_table = defaultdict(lambda: m)
    for i in range(m - 1):
        char_table[pattern[i]] = m - 1 - i

    i = m - 1
    while i < n:
        j = m - 1
        k = i
        while j >= 0 and text[k] == pattern[j]:
            k -= 1
            j -= 1
        if j == -1:
            return k + 1
        i += char_table[text[i]]
    return -1

# Knuth-Morris-Pratt

def kmp_search(text, pattern):
    def compute_lps(pattern):
        lps = [0] * len(pattern)
        length, i = 0, 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    lps = compute_lps(pattern)
    i = j = 0
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
        if j == len(pattern):
            return i - j
        elif i < len(text) and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

# Rabin-Karp

def rabin_karp(text, pattern, d=256, q=101):
    m, n = len(pattern), len(text)
    if m == 0: return 0
    h = pow(d, m-1) % q
    p, t = 0, 0

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for i in range(n - m + 1):
        if p == t:
            if text[i:i+m] == pattern:
                return i
        if i < n - m:
            t = (t - h * ord(text[i])) % q
            t = (t * d + ord(text[i+m])) % q
            t = (t + q) % q
    return -1

# open files
with open('task3_files/story1.txt', 'r', encoding='utf-8-sig', errors='ignore') as f:
    story1 = f.read()

with open('task3_files/story2.txt', 'r', encoding='utf-8-sig', errors='ignore') as f:
    story2 = f.read()

real_substring1 = "алгоритм"
fake_substring1 = "паляниця"
real_substring2 = "метод"
fake_substring2 = "неіснуючий"

# run tests
algorithms = {"Boyer-Moore": boyer_moore, "Knuth-Morris-Pratt": kmp_search, "Rabin-Karp": rabin_karp}
stories = [("Story 1", story1, real_substring1, fake_substring1),
           ("Story 2", story2, real_substring2, fake_substring2)]

results = {}

for alg_name, alg_func in algorithms.items():
    for story_name, story, real_sub, fake_sub in stories:
        real_time = timeit.timeit(lambda: alg_func(story, real_sub), number=100)
        fake_time = timeit.timeit(lambda: alg_func(story, fake_sub), number=100)
        results[(alg_name, story_name, "Real")] = real_time
        results[(alg_name, story_name, "Fake")] = fake_time

# showw results
for key, value in results.items():
    alg, story, substr_type = key
    print(f"{alg} ({story}, {substr_type}): {value:.6f} seconds")

# compare
for story_name in ["Story 1", "Story 2"]:
    for substr_type in ["Real", "Fake"]:
        best_alg = min(algorithms, key=lambda alg: results[(alg, story_name, substr_type)])
        print(f"Fastest for {story_name} ({substr_type}): {best_alg}")

best_overall = min(algorithms, key=lambda alg: sum(results[(alg, story, substr)] for story, _, _, _ in stories for substr in ["Real", "Fake"]))
print(f"Overall fastest algorithm: {best_overall}")
