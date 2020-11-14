import math

left = 3
right = 32
if((right & (right-1) == 0) and right != 0):
    print("power of 2")
    times = math.sqrt(right)
    print("Times: {}".format(times))
    shifted = left << int(times)
    print("Result = {}".format(shifted))