import itertools as it
from utils import mmc, mdc, quad

class Matrix:
    def __init__(self, fromValues: list[list[int]]=[], rows: int=0, columns: int=0, isIdentity: bool=False):

        if len(fromValues):
            for i in fromValues:
                if len(i) != len(fromValues[0]):
                    raise Exception('Todas as linhas e colunas da matriz devem ser congruentes.')

        self.rows = rows if not len(fromValues) else len(fromValues)
        self.columns = (
            columns 
                if columns != 0 else rows
            ) if not len(fromValues) else len(fromValues[0])
        self.isSquare = self.rows == self.columns
        self.isIdentity = self.isSquare and isIdentity
        self.values = ([ 
                        [ 0 
                            for _ in range(self.columns)
                        ] for _ in range(self.rows)
                    ] if not self.isIdentity else [
                        [ 1 if x==y else 0 
                            for x in range(self.columns)
                        ] for y in range(self.rows)
                    ]) if not len(fromValues) else fromValues
        
        # self.isOrtho = (self * self.transposta()) == Matrix(rows=self.rows, isIdentity=True)

    def __str__(self):
        s = ""
        
        for y in range(self.rows):
            for x in range(self.columns):
                v = round(self.values[y][x], 14)
                if int(v) == v:
                    s += f'{int(v):>4} '
                else:
                    s += f'{v:>4.3f} '

            s += "\n"
        
        return s

    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return False
        for ir in range(len(self.values)):
            for ic in range(len(self.values[0])):
                if self.values[ir][ic] != other.values[ir][ic]:
                    return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):

        if not 'Matrix' in str(type(other)):
            raise Exception('Somas só podem ser feitas entre 2 matrizes.')
        
        if not (self.rows == other.rows and self.columns == other.columns):
            raise Exception("As matrizes devem ter o mesmo número de linhas e colunas.")

        return Matrix(fromValues=[ 
            [ self.values[y][x]+other.values[y][x] for x in range(self.columns) ] 
                for y in range(self.rows) 
            ])
    __radd__ = __add__

    def __mul__(self, other):
        tOther = type(other).__name__

        # if 'int' in tOther or 'float' in tOther:
        if tOther in ['int', 'float', 'complex']:
            return Matrix(fromValues=[ [ x*other for x in y ] for y in self.values ])
        
        elif 'Matrix' in tOther:
            if len(self.values[0]) == len(other.values):

                Arows = len(self.values)
                Acolumns = len(self.values[0])
                Bcolumns = len(other.values[0])
                
                m = []
                for i in range(Arows):
                    m.append([])
                    for j in range(Bcolumns):
                        m[i].append(
                            round(sum(
                                self.values[i][x] * other.values[x][j] 
                                    for x in range(Acolumns)
                                )
                            ,14))
                return Matrix(fromValues=m)
            else:
                raise Exception('O número de linhas da primeira matrix e o número de colunas da segunda matrix devem ser o mesmo.')
        
        raise Exception('Matrizes só podem ser multiplicadas por número reais.')
    __rmul__ = __mul__

    def __truediv__(self,other):
        tOther = type(other).__name__

        # if 'int' in tOther or 'float' in tOther:
        if tOther in ['int', 'float', 'complex']:
            return Matrix(fromValues=[ [ x/other for x in y ] for y in self.values ])
    __rtruediv__ = __truediv__


    def __erroQ(self):
        raise Exception("Matriz deve ser quadrada.")


    def switch_row(self, row1: int, row2: int):
        self.values[row1], self.values[row2] = self.values[row2], self.values[row1]
    
    def sum_row(self, row1: list[list[int]] | int, row2: list[list[int]] | int, sum: bool = True):
        if type(row1) == list and type(row2) == list:
            if len(row1) == len(row2):
                return [ row1[i] + row2[i] * (1 if sum else -1) for i in range(len(row1)) ]
        
        elif type(row1) == list and type(row2) == int:
            if len(row1) == len(self.values[row2]):
                self.values[row2] = [ row1[i] + self.values[row2][i] * (1 if sum else -1) for i in range(len(row1)) ]

        elif type(row1) == int and type(row2) == list:
            if len(row2) == len(self.values[row1]):
                self.values[row1] = [ self.values[row1][i] + row2[i] * (1 if sum else -1) for i in range(len(row2)) ]
        else:
            self.values[row1] = [
                self.values[row1][i] + self.values[row2][i] * (1 if sum else -1) 
                for i in range(len(self.values[row1]))
            ]
            
        # return [ self.values[row1][i] + self.values[row2][i] * (1 if sum else -1) for i in range(len(self.values[0])) ]
    
    def mul_row(self, row: list[list[int]] | int, n: float):
        if type(row) == list:
            return [ i*n for i in row ]
        else:
            self.values[row] = [ i*n for i in self.values[row] ]
    
    # nao terminado
    def sistema(self, valores: list[int] = []):
        if len(valores)==0:
            valores = [0]*self.rows
        elif len(valores)!=self.rows:
            raise Exception("Número errado de variáveis.")
        
        if self.columns < self.rows:
            return Matrix(fromValues=self.values[:self.columns]).sistema(valores[:self.columns])
        
        v = self.values


        def zeros(row: list):
            return row.count(0) == len(row)-1

        respostas = valores.copy()
        certos = [0]*len(respostas)
        for vx in range(self.columns):

            # vx = 0
            if 1:
                linhaAtual = self.rows-1
                mx = float("inf")
                variavelAtual = v[linhaAtual][vx]
                for vy in range(1, linhaAtual+1):
                    
                    variavelIteracao = v[linhaAtual-vy][vx]
                    
                    mx = min(mx, mmc(variavelAtual, variavelIteracao))
                    
                    print(f"(vx,vy):{(vx,vy)}\tva:{variavelAtual}\tvi: {variavelIteracao}\tmx:{mx}")
                    
                    # if mx == variavelAtual:

                    print("indice escolhido:", linhaAtual-vy)
                    valorMultiplicacao = v[linhaAtual][vx]
                    
                    # linhaAtual <- linhaAtual - vm*(linhaAtual-vy)
                    self.sum_row(
                        linhaAtual,
                        self.mul_row(v[linhaAtual-vy], valorMultiplicacao),
                        False
                    )
                    
                        # print('-------------------------------------')
                        # print(respostas[linhaAtual])
                        # print(valorMultiplicacao)
                    

                    # linhaAtual <- linhaAtual - vm*(linhaAtual-vy)
                    respostas[linhaAtual] -= respostas[linhaAtual-vy]*valorMultiplicacao


                    if zeros(v[linhaAtual]):
                        valorDivisao = v[linhaAtual][self.columns-vx-1]
                        self.mul_row(linhaAtual, 1/valorDivisao)
                        respostas[linhaAtual] /= valorDivisao
                        certos[linhaAtual] = 1
                    
                    print("repostas:", respostas)
                    print("certos:", certos)
                    


                    print()
                    print(self)
                    print(respostas)
                    print()
                    break 
                linhaAtual-=1

        
        print(self)


    def determinante(self):
        if not self.isSquare:
            self.__erroQ()
        
        if self.isIdentity:
            return 1
        
        s = self.values

        if self.rows == 1:
            return s[0][0]
        
        elif self.rows == 2:
            return s[0][0]*s[1][1] - s[0][1]*s[1][0]
        
        else:
            perm = [i for i in it.permutations(range(self.rows))]

            def cc(s1,s2):
                count = 0
                s1 = list(s1)
                s2 = list(s2)
                i=0
                while s2 != s1 and i<len(s1):
                    if s2[i] != s1[i]:
                        a, b = s2[i], s2[s2[i]]
                        s2[i], s2[a] = b, a
                        count += 1
                        i = 0
                    i+=1
                return count

            det = 0
            for i in perm:
                prod = 1
                for j in range(len(i)):
                    prod *= self.values[j][ i[j] ]

                sign = (-1) ** cc(range(0, self.rows), i)
                det += sign * prod
            return det
    
    def traco(self):
        if not self.isSquare:
            self.__erroQ()
        return sum(self.values[i][i] for i in range(self.rows))

    def transposta(self):
        return Matrix(fromValues=list(zip(*self.values)))
    
    def cofator(self, x: int, y: int):
        if not self.isSquare:
            self.__erroQ()
        if self.rows == 1:
            return self.values[0][0]
        return (
                ( (-1) ** (x+y+2) ) 
                * 
                Matrix(fromValues=
                    [
                        [v for iv, v in enumerate(row) if iv != x ]
                            for ir, row in enumerate(self.values) if ir != y
                    ] 
                ).determinante()
            )

    def adj(self):
        if not self.isSquare:
            self.__erroQ()
        else:
            return Matrix(fromValues=
                [
                    [self.cofator(x, y) for x in range(len(self.values[0]))]
                    for y in range(len(self.values))
                ]
            ).transposta()

    def inversa(self):
        if self.determinante()==0:
            raise Exception("Determinante deve ser diferente a zero para ter inversa.")
        elif not self.isSquare:
            self.__erroQ()
        elif self.rows == 1:
            return 1/self.values[0][0]*Matrix(fromValues=[[1]])
        else:
            return 1/self.determinante() * self.adj()
    
    def pseudoinversa(self):
        if self.columns < self.rows:
            return (self.transposta()*self).inversa()*self.transposta()
        else:
            return self.transposta()*(self*self.transposta()).inversa()
    
    def autovalores(self):
        if not self.isSquare:
            raise Exception("Matriz deve ser quadrada para ter autovalores.")
        else:
            if self.rows == 2:
                s = self.values
                
                l = []
                for lamb in range(self.rows):
                    b = -s[0][0]-s[1][1]
                    c = self.determinante()
                    ls = quad(1, b, c)

                    m0 = Matrix(fromValues=[
                        [v-ls[lamb] if j == i else v for j,v in enumerate(row)]
                        for i,row in enumerate(self.values)
                    ])

                    mv = m0.values
                    x = mv[0][1]/mv[0][0]
                    y = -x*mv[1][0]/mv[1][1]

                    l.append({
                        "autovalor": ls[lamb], 
                        "autovetor": (x,y)
                    })
                return l

    # def kernel(self):
    #     print(self)
        
    #     if self.rows != 2:
    #         self.__erroQ()
        
        


    # def svd(self):
    #     a

            

        

# SOMA E MULTIPLICAÇÃO --------
# m = Matrix(1,2)

# print(m.rows, m.columns, m.isSquare)
# print(m)

# m = Matrix(3,2)
# print(m.rows, m.columns, m.isSquare)
# print(m)

# m = Matrix(6, isIdentity=True)
# print(m)

# m1 = Matrix(6, isIdentity=True)
# m = 9*m

# m1 *= 4

# print(m)
# print(m1*8)

# print(type(1+1j).__name__)

# print(m*(1+1j))

# print(m1+m)


# OPERAÇÃOES DE LINHA ---------
# a = Matrix(fromValues=[[1,2,3],[4,5,6],[7,8,90]])
# b = Matrix(fromValues=[[7,8], [9,10],])

# # a,b = a*b, b*a
# # print(a)
# # print(a.determinante())
# # print(a)
# # print(b)
# # a.switch_row(0,1)

# print(a)

# print(a.sum_row(0,1))
# print(a.mul_row(0,7))


# DETERMINANTE -------------
# c = Matrix(fromValues=[
#     [1,1,1,2],
#     [1,1,2,1],
#     [1,2,1,1],
#     [2,1,1,1],
# ])

# print(c)
# print(c.traco())
# print("ccccccc", c.determinante())


# TRANSPOSTA ---------------
# d = Matrix(fromValues=[
#     [1,2],
#     [3,4],
#     [5,6]
# ])

# e = d.transposta()

# print(d)
# print(e)


# COFATOR, ADJUNTA E INVERSA -------
# a = Matrix(fromValues=[[1,2,3],[4,5,6],[7,8,90]])
# a = Matrix(fromValues=[[1,2,3,4],[4,5,6,7],[7,8,90,10],[10,11,12,193]])
# print(a)
# print("determinante: ", a.determinante())
# print("cofator(2,0): ", a.cofator(0,2))
# print("adjunta:\n", a.adj())
# print("inversa:\n", a.inversa())
# print("I:")
# print("inv(a) * a")
# print(a.inversa() * a)
# print("a * inv(a)")
# print(a * a.inversa())


# AUTOVALORES, AUTOVETORES ------
# a = Matrix(fromValues=[[1,2,3],[4,5,6],[7,8,90]])
# a = Matrix(fromValues=[[1,2],[3,4]])
# print(a.autovalores())




# PSEUDOINVERSA
# a = Matrix(fromValues=[[5,10]])
# print(a)
# am = a.pseudoinversa()
# print("A+")
# print(am)

# print("A * A+ * A")
# print(a*am*a)
# print("A * A+")
# print(a*am)

# print("A+ * A * A+")
# print(am*a*am)
# print("A+ * A")
# print(am*a)




# KERNEL
# a = Matrix(fromValues=[[1,4],[4,16]])
# print(a.kernel())