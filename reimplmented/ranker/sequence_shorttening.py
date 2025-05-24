def shorttening(lst, window):
    arr = lst[:]
    i = 0
    while i + 2*window <= len(arr):
        chunk1 = arr[i : i + window]
        chunk2 = arr[i + window : i + 2*window]
        if chunk1 == chunk2:
            del arr[i + window : i + 2*window]
        else:
            i += 1

    return arr

def sequence_cleanser(io_sequence):
    w = 1
    current = io_sequence
    while len(io_sequence)//2 >= w:
        current = shorttening(current, w)
        w += 1
    return current