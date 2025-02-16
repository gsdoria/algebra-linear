def checkPrime(n):
    if n>1:
        for i in range(2, n//2+1):
            if n%i==0:
                return False
        return True
    return False

def primes(n): return [] if n<2 else [i for i in range(2, n+1) if checkPrime(i)]

def primeFactors(n):
    l = [1]
    p = primes(n//2)
    i = -1
    while n!=1 and i<len(p)-1:
        i += 1
        if n%p[i] == 0:
            n /= p[i]
            l.append(p[i])
            i = -1
    return l if len(l)>1 else [1,n]

def intersect(a,b):
    l = []
    l1 = a.copy()
    l2 = b.copy()
    i = 0
    while i<len(l1):
        n = l1[i]
        if n in l2:
            l.append(n)
            l1.remove(n)
            l2.remove(n)
            i-=1
        i+=1
    return l

def listProduct(l):
    i = 1
    for j in l: i*=j
    return i

# def mdc(a,b):
#     ma = max(a,b)
#     mi = min(a,b)
    
#     if ma % mi == 0:
#         return mi
#     else:
#         pa = primeFactors(a)
#         pb = primeFactors(b)
#         it = intersect( pa, pb )
#         it.remove(1)
#         return listProduct(it)

# def mmc(a,b):
#     ma = max(a,b)
#     mi = min(a,b)
    
#     if ma % mi == 0:
#         return ma
#     else:
#         pa = primeFactors(a)
#         pb = primeFactors(b)
#         it = intersect( pa, pb )

#         if len(it) == 1:
#             return a*b
#         else:
#             p = pa + pb
#             for i in it:
#                 p.remove(i)
#             return listProduct(p)

# mdc = lambda a,b: a if b==0 else mdc(b,a%b)
# mmc = lambda a,b: int(a*b/mdc(a,b))

def mdc(*args):
    if len(args)==2:
        return args[0] if args[1] == 0 else mdc(args[1], args[0] % args[1])
    else:
        n = args[0]
        for i in range(1, len(args)):
            n = mdc(n, args[i])
        return n


def mmc(*args):
    if len(args)==2:
        return int(args[0]*args[1] / mdc(args[0],args[1]))
    else:
        n = args[0]
        for i in range(1, len(args)):
            n = mmc(n, args[i])
        return n

# print(mdc(9,14))
# print(mmc(9,14))


def quad(a, b, c):
    d = (b**2 - 4*a*c)**(1/2)
    return ((-b + d)/(2*a) , (-b - d)/(2*a))