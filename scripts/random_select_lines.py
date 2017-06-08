import random

f = open('./RC_2013-02', 'r')
output = open('./Reduced_RC_2013-02', 'w+')

for line in f:
    if random.randint(0, 9) == 0:
        output.write(line + '\n')
output.flush()

