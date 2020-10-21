def add(x, y):

    while (y != 0):
        carry = x & y
        x = x ^ y                       #sum = x ^ y
        y = carry << 1                  #carry = ( x & y ) << 1
                                        #x = sum
                                        #y = carry
    return x



print(add(7, 5))