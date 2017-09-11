


def f(a,b):
 return sum((i*i for i in a))==sum((i*i for i in b)) \
    and sum((i*i*i for i in a))==sum((i*i*i for i in b))

def check(a,b):
 return sorted(a) == sorted(b)

if __name__=='__main__':
 n = 30
 for a1 in range(n):
   for a2 in range(n):
    for a3 in range(n):
     for b1 in range(n):
      for b2 in range(n):
       b3 = a1+a2+a3-b1-b2
       a,b = (a1,a2,a3),(b1,b2,b3)
       if check(a,b) != f(a,b):
        print('fail:', a, b)