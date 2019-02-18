import random

f = open("d_l.tsv","w")
d_len = 32
l_len = 64
parents = 1
rows = 0

f.write("\t")
for i in range(l_len):
    if(i == l_len-1):
        f.write("%d\n"%(i))
    else:
        f.write("%d\t"%(i))

for parent in range(parents):
    for row in range(d_len):
        f.write("%d\t"%(rows))
        for k in range(l_len):
            num = random.randint(0,1)
            if(k == l_len-1):
                f.write("%d\n"%(num) )
            else:
                f.write("%d\t"%(num) )
            #print(random.randint(0,1))
        rows+=1
