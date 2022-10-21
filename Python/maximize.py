# f(X) = X^2
# S = ( f(X1) + f(X2) + ... + f(XK) ) % M
# The Code maximizes S taking the values of f(X) from each of K lines
# Example input:
# 3 1000
# 2 5 4
# 3 7 8 9
# 5 5 7 8 9 10
# output : 206
# Source : Hackerrank > Prepare > PythonItertools > Maximize It!
# url : https://www.hackerrank.com/challenges/maximize-it/problem?isFullScreen=true


from itertools import product
K, M = map(int, input("Input K & M : ").split())
List = [[int(i)**2 for i in input().split()[1:]] for _ in range(K)]
print("The maximum value is :", max([sum(r) % M for r in product(*List)]))
