outsideLoop = 0
insideLoop = 0
ifstate = 0

for i in range(17):
    outsideLoop += 1
    for j in range(17):
        insideLoop += 1
        if((j + 1) % 4 == 0):
            ifstate += 1
            print("hi")
            
print("{}, {}, {}".format(outsideLoop, insideLoop, ifstate))