def count2s(x):

    count = 0
    for i in range(x + 1):
        for c in str(i):
            if (c == '2'):
                count += 1
    return count


print(count2s(23))