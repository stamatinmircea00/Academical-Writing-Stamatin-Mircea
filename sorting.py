import time
import random
import statistics
import json

#Sorting Algorithms 

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left  = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    # Merge two sorted halves
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + left[i:] + right[j:]


def insertion_sort(arr):
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def bubble_sort(arr):
    a = arr[:]
    n = len(a)
    for i in range(n - 1):
        swapped = False
        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a


def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left   = [x for x in arr if x <  pivot]
    middle = [x for x in arr if x == pivot]
    right  = [x for x in arr if x >  pivot]
    return quick_sort(left) + middle + quick_sort(right)


def heap_sort(arr):
    a = arr[:]
    n = len(a)

    def heapify(size, root):
        largest = root
        left  = 2 * root + 1
        right = 2 * root + 2
        if left  < size and a[left]  > a[largest]: largest = left
        if right < size and a[right] > a[largest]: largest = right
        if largest != root:
            a[root], a[largest] = a[largest], a[root]
            heapify(size, largest)

    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    for i in range(n - 1, 0, -1):
        a[0], a[i] = a[i], a[0]
        heapify(i, 0)
    return a


def counting_sort(arr):
    if not arr:
        return arr
    mn, mx = min(arr), max(arr)
    count = [0] * (mx - mn + 1)
    for x in arr:
        count[x - mn] += 1
    result = []
    for i, cnt in enumerate(count):
        result.extend([i + mn] * cnt)
    return result


def shell_sort(arr):
    a = arr[:]
    n = len(a)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = a[i]
            j = i
            while j >= gap and a[j - gap] > temp:
                a[j] = a[j - gap]
                j -= gap
            a[j] = temp
        gap //= 2
    return a


def tim_sort(arr):
    a = arr[:]
    a.sort()
    return a



ALGORITHMS = {
    "Merge Sort":     merge_sort,
    "Insertion Sort": insertion_sort,
    "Bubble Sort":    bubble_sort,
    "Quick Sort":     quick_sort,
    "Heap Sort":      heap_sort,
    "Counting Sort":  counting_sort,
    "Shell Sort":     shell_sort,
    "Tim Sort":       tim_sort,
}


#Data generators

def gen_random(n):
    return [random.randint(0, 10 * n) for _ in range(n)]


def gen_sorted(n):
    return list(range(n))


def gen_reverse(n):
    return list(range(n, 0, -1))


def gen_almost_sorted(n):
    a = list(range(n))
    swaps = max(1, int(n * 0.02))
    positions = random.sample(range(n - 1), min(swaps, n - 1))
    for i in positions:
        a[i], a[i + 1] = a[i + 1], a[i]
    return a


def gen_half_sorted(n):
    sorted_half  = list(range(n // 2))
    random_half  = [random.randint(0, n) for _ in range(n - n // 2)]
    return sorted_half + random_half


def gen_flat(n):
    return [random.randint(0, 9) for _ in range(n)]


DATA_STRUCTURES = {
    "Random":          gen_random,
    "Sorted":          gen_sorted,
    "Reverse":         gen_reverse,
    "Almost Sorted":   gen_almost_sorted,
    "Half Sorted":     gen_half_sorted,
    "Flat (few vals)": gen_flat,
}


#Benchmarks

#Sizes
SIZES = [20, 50, 100, 500, 1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000]

#Repetitions per size
REPS = {
    20:      2000,
    50:      1000,
    100:     500,
    500:     100,
    1_000:   50,
    5_000:   10,
    10_000:  5,
    50_000:  2,
    100_000: 1,
    500_000: 1,
    1_000_000: 1,
}

#If it takes too much time, skip and mark as None.
SLOW_ALGOS = {"Insertion Sort", "Bubble Sort"}
SLOW_CUTOFF = 10_000   # skip if n > this


def benchmark():
    results = []

    for struct_name, gen_fn in DATA_STRUCTURES.items():
        print(f"\n{'='*50}")
        print(f"  Input structure: {struct_name}")
        print(f"{'='*50}")

        for n in SIZES:
            reps   = REPS[n]
            data   = gen_fn(n)

            for algo_name, sort_fn in ALGORITHMS.items():

                if algo_name in SLOW_ALGOS and n > SLOW_CUTOFF:
                    results.append({
                        "algo":      algo_name,
                        "structure": struct_name,
                        "n":         n,
                        "time_ms":   None,
                        "note":      "skipped (too slow)",
                    })
                    continue

                times = []
                for _ in range(reps):
                    d  = data[:]                          
                    t0 = time.perf_counter()
                    sort_fn(d)
                    times.append((time.perf_counter() - t0) * 1_000)   # → ms

                avg_ms = statistics.mean(times)

                results.append({
                    "algo":      algo_name,
                    "structure": struct_name,
                    "n":         n,
                    "time_ms":   round(avg_ms, 6),
                    "note":      "",
                })

            print(f"  n={n:>7,}  done  ({reps} reps each)")

    return results


#Main point

if __name__ == "__main__":
    print("Sorting Algorithm Benchmark")
    print("Algorithms :", ", ".join(ALGORITHMS.keys()))
    print("Structures :", ", ".join(DATA_STRUCTURES.keys()))
    print("Sizes      :", SIZES)
    print()

    data = benchmark()

    out_file = "results.json"
    with open(out_file, "w") as f:
        json.dump(data, f, indent=2)

    print(f"\n✓ Benchmark complete. {len(data)} measurements saved to '{out_file}'.")
    print("  Run build_excel.py next to generate the Excel report.")