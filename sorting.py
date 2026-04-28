import time
import random
import statistics
import json

# ══════════════════════════════════════════════════════════════════════════════
# Sorting Algorithms
# ══════════════════════════════════════════════════════════════════════════════

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left  = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
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
    pivot  = arr[len(arr) // 2]
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


# ── Custom Tim Sort ────────────────────────────────────────────────────────────
#
# Tim Sort is a hybrid algorithm that combines Insertion Sort for small runs
# and Merge Sort to combine those runs together.
#
# How it works:
#   1. Split the array into small "runs" of size MIN_RUN (32 here).
#   2. Sort each run in-place using Insertion Sort.
#   3. Merge adjacent runs together using the standard merge operation,
#      doubling the merge size each round until the whole array is sorted.
#
# The key insight is that Insertion Sort is very fast on small arrays
# (low overhead, good cache behaviour), and Merge Sort is efficient for
# combining already-sorted pieces. Together they give O(n) on sorted/nearly
# sorted data and O(n log n) in the worst case.

MIN_RUN = 32


def _insertion_sort_inplace(a, left, right):
    """Sort a[left:right+1] in place using Insertion Sort."""
    for i in range(left + 1, right + 1):
        key = a[i]
        j = i - 1
        while j >= left and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key


def _merge_inplace(a, left, mid, right):
    """Merge two sorted subarrays a[left:mid+1] and a[mid+1:right+1] in place."""
    left_part  = a[left : mid + 1]
    right_part = a[mid + 1 : right + 1]
    i, j, k = 0, 0, left
    while i < len(left_part) and j < len(right_part):
        if left_part[i] <= right_part[j]:
            a[k] = left_part[i];  i += 1
        else:
            a[k] = right_part[j]; j += 1
        k += 1
    while i < len(left_part):
        a[k] = left_part[i]; i += 1; k += 1
    while j < len(right_part):
        a[k] = right_part[j]; j += 1; k += 1


def tim_sort(arr):
    """
    Custom Tim Sort implementation.

    Step 1 – sort small runs with Insertion Sort.
    Step 2 – repeatedly merge adjacent runs, doubling size each round.
    """
    a = arr[:]
    n = len(a)

    # Step 1: sort every slice of size MIN_RUN with Insertion Sort
    for start in range(0, n, MIN_RUN):
        end = min(start + MIN_RUN - 1, n - 1)
        _insertion_sort_inplace(a, start, end)

    # Step 2: merge runs of increasing size
    size = MIN_RUN
    while size < n:
        for left in range(0, n, 2 * size):
            mid   = min(left + size - 1, n - 1)
            right = min(left + 2 * size - 1, n - 1)
            if mid < right:          # there is a right half to merge
                _merge_inplace(a, left, mid, right)
        size *= 2

    return a


# ══════════════════════════════════════════════════════════════════════════════
# Algorithm registry
# ══════════════════════════════════════════════════════════════════════════════

ALGORITHMS = {
    "Merge Sort":     merge_sort,
    "Insertion Sort": insertion_sort,
    "Bubble Sort":    bubble_sort,
    "Quick Sort":     quick_sort,
    "Heap Sort":      heap_sort,
    "Counting Sort":  counting_sort,
    "Shell Sort":     shell_sort,
    "Tim Sort":       tim_sort,   # <-- our own implementation now
}


# ══════════════════════════════════════════════════════════════════════════════
# Data generators
# ══════════════════════════════════════════════════════════════════════════════

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
    sorted_half = list(range(n // 2))
    random_half = [random.randint(0, n) for _ in range(n - n // 2)]
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


# ══════════════════════════════════════════════════════════════════════════════
# Benchmark configuration
# ══════════════════════════════════════════════════════════════════════════════

SIZES = [20, 50, 100, 500, 1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000]

REPS = {
    20:          2000,
    50:          1000,
    100:         500,
    500:         100,
    1_000:       50,
    5_000:       10,
    10_000:      5,
    50_000:      2,
    100_000:     1,
    500_000:     1,
    1_000_000:   1,
}

# Bubble Sort and Insertion Sort are O(n^2) and get skipped above this size
SLOW_ALGOS  = {"Insertion Sort", "Bubble Sort"}
SLOW_CUTOFF = 10_000


# ══════════════════════════════════════════════════════════════════════════════
# Benchmark runner
# ══════════════════════════════════════════════════════════════════════════════

def benchmark():
    results = []

    for struct_name, gen_fn in DATA_STRUCTURES.items():
        print(f"\n{'='*50}")
        print(f"  Input structure: {struct_name}")
        print(f"{'='*50}")

        for n in SIZES:
            reps = REPS[n]
            data = gen_fn(n)

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
                    times.append((time.perf_counter() - t0) * 1_000)

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


# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════

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

    print(f"\nBenchmark complete. {len(data)} measurements saved to '{out_file}'.")
    print("Run build_excel.py next to generate the Excel report.")