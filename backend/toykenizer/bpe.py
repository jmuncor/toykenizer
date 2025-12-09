
# Import and encode text into the UTF-8 byte representation
file = open ('text.txt', 'r')
content = file.read()
tokens = content.encode('utf-8')
tokens = list(map(int, tokens))

def most_common_pair( ids: list[int] ):
    freq_counts = {}
    for num in ids:
        if num not in freq_counts:
            freq_counts[num] = 0
        freq_counts[num] += 1
    freq_count_list = list(freq_counts.items())

    quicksort_tuples( freq_count_list, 0, len( freq_count_list ) - 1)

    return (freq_count_list)

def partition( tuples: list[tuple[int, int]], low: int, high: int) -> int:
    pivot = tuples[high]
    i = low -1

    for j in range(low, high):
        if tuples[j][1] >= pivot [1]:
            i += 1
            tuples[i], tuples[j] = tuples[j], tuples[i]

    tuples[i+1], tuples[high] = tuples[high], tuples[i+1]

    return i+1

def quicksort_tuples( tuples: list[tuple[int,int]], low:int, high:int):
    if low < high:
        initial_partition = partition( tuples, low, high )
        quicksort_tuples( tuples, low, initial_partition-1 )
        quicksort_tuples( tuples, initial_partition+1, high )

print (most_common_pair(tokens))
