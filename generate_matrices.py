import random

f = open("d_l.tsv","w")
d_len = 32
l_len = 64
parents = 10
for i in range(parents):
    for j in range(d_len):
        for k in range(l_len):
            num = random.randint(0,1)
            if(k == l_len-1):
                f.write("%d\n"%(num) )
            else:
                f.write("%d\t"%(num) )
            #print(random.randint(0,1))
    f.write("\n\n")
