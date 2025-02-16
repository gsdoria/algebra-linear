from matrix import Matrix

from utils import mmc, mdc

class Sistema(Matrix):
    def __init__(self, rows=0, columns=0, isIdentity=False, fromValues=[], xs=[]):
        super().__init__(rows=rows, columns=columns, isIdentity=isIdentity, fromValues=fromValues)
        self.xs = xs if len(xs) else [0]*self.rows
    

    def __str__(self):
        s = ""
        for y in range(self.rows):
            for x in range(self.columns):
                s += f'{str(self.values[y][x])+" ":>4}'
            s += f"|{str(self.xs[y]):>2}\n"
        return s
    
    def solve1(self):
        # print(self.values[self.rows-1][0])
        # print(self.values[self.rows-2][0])
        # print(self.values[self.rows-1][1])

        c = Sistema(fromValues=self.values, xs=self.xs)


        for i in range(c.rows):
            mr = mdc(*c.values[i], c.xs[i])
            if mr != 1:
                c.values[i] = c.mul_row(i, 1/mr)
                c.xs[i] /= mr
        
        # print("c")
        # print(c)

        passo = 1


        r = c.rows

        for y in range( int(c.rows*(c.rows-1)/2)-c.rows+1 ):
            for x in range(0,y+1):
                print(c.values[c.rows-(y-x)-1][x])
        

        solved = [0 for i in range(r)]

        for y in range(c.rows*2):
            # xi = 0
            # yi = c.rows-1
            # print('r', r)

            print("passo: ", passo)
            if 0 <= y and y < r*(r-1)/2:
                for x in range(y):
                    yi = r-y+x
                    xi = x

                    print("1-------", yi, xi, c.values[yi][xi])


                    cv = c.values[yi][xi]
                    n = [float('inf'), -1] # [valor, indice]


                    for j in range(c.rows-1):
                        mr = mmc(cv, self.values[j][xi])
                        if mr<n[0] and j != yi:
                            n = [ mr, j ]

                    c.values[yi] = c.mul_row(yi, n[0])
                    c.xs[yi] = c.xs[yi]*n[0]
                    print(f"l{yi+1} * {n[0]}")


                    c.values[yi] = c.sum_row(yi, n[1], 0)
                    c.xs[yi] =  c.xs[yi] - c.xs[n[1]]
                    print(f"l{yi+1} - l{n[1]+1}")

                    print(c)

                    
                    if c.values[yi].count(0) == r-1:
                        mul = 1/c.values[yi][yi]
                        c.values[yi] = list(map(int, c.mul_row(yi, mul)))
                        c.xs[yi] = c.xs[yi]* mul
                        print(f"l{yi+1} * {mul}")
                        solved[yi] = 1
                    
                    
                    print(c)



            elif y<r**2-r:
                for x in range(2*r - y - 1):
                    yi = r+r-y-2-x
                    xi = r-x-1

                    print("2-------", yi, xi, c.values[yi][xi])

                    cv = c.values[yi][xi]
                    n = [float('inf'), -1] # [valor, indice]


                    for j in range(c.rows-1):

                        if not any(solved):
                            mr = mmc(cv, self.values[j][xi])
                            if mr<n[0] and j != yi and mr!=0:
                                n = [ mr, j ]
                        else:
                            ind = solved.index(1)
                            n = [mmc(cv, self.values[ind][xi]), ind]

                    
                    print("xi", xi)


                    c.values[yi] = c.mul_row(yi, n[0])
                    c.xs[yi] = c.xs[yi]*n[0]
                    print(f"l{yi+1} * {n[0]:.2f} --1")


                    c.values[yi] = c.sum_row(yi, n[1], 0)
                    c.xs[yi] =  c.xs[yi] - c.xs[n[1]]
                    print(f"l{yi+1} - l{n[1]+1}")

                    print(c)

                    
                    if c.values[yi].count(0) == r-1 and c.values[yi].count(1) != 1 and c.values[yi][yi]!=0:
                        mul = 1/c.values[yi][yi]
                        c.values[yi] = list(map(int, c.mul_row(yi, mul)))
                        c.xs[yi] = c.xs[yi]* mul
                        print(f"l{yi+1} * {mul:.2f}")
                    
                    
                    print(c)
            
            # else:
            #     for x in range(r):
            #         print("3-------", x, x, c.values[x][x])
                    

            # print(c)

            passo+=1
    
    def solve(self):
        d = self.determinante()
        
        if d==0:
            return -1
        
        r = self.rows
        
        lx = [
            Matrix(fromValues=[
                [
                    self.xs[y] if i==x else self.values[y][x]
                    for x in range(r)
                ]
                for y in range(r)
            ]) for i in range(r)
        ]

        return {i:lx[i].determinante()/d for i in range(self.rows)}



s = Sistema(fromValues=[
    # [2,1,1],
    # [3,6,3],
    # [4,4,8],

    # [2,1,1,1],
    # [2,4,2,2],
    # [3,3,6,3],
    # [4,4,4,8],

    [2,1,1],
    [1,2,1],
    [1,1,2],
],
# xs = [7,24,36]
# xs = [11,24,39,56]
# xs = [4,5]
xs = [7,8,9]
)

# print(s)

print(s.solve())