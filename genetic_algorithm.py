import pandas as pd

df = pd.read_csv("d_l.tsv",sep="\t")
#print(df)
print("Heading")
#print(df.head())

parents_size = 2
parents = []
demo_size = 32
labs_size = 64
num = 0
for i in range(parents_size):
    parents.append(df.iloc[(i*demo_size):(i+1)*demo_size,:labs_size])
print(df.shape)
print(len(parents))
print(parents[0])
print(parents[1])

'''
      a     b     c     d
0     1     2     3     4
1   100   200   300   400
2  1000  2000  3000  4000
'''