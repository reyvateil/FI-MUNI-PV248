from numpy import linalg
import numpy as np
from collections import defaultdict

# Load matrix
matrix = np.loadtxt(fname='numpy_data\\matrix.txt', delimiter=' ')
print(matrix)

# Solve equations
def solve_equation(matrix):
    left_side, right_side = np.hsplit(matrix, [len(matrix)])
    result = linalg.solve(left_side, right_side)
    print(result)

# Parse equation
equations = ['2 x + 3 y = 5', 'x - y = 0']
matrix = None

for equation in equations:
    coeffs = defaultdict(int)
    elems = equation.split(' ')
    coeff = 1

    for elem in elems:
        if elem.isdigit():
            coeff = int(elem)
        elif elem.isalpha():
            coeffs[elem] = coeff
        elif elem == '-':
            coeff *= -1
    coeffs['='] = coeff
    equa = [np.array([coeffs[key] for key in coeffs])]

    if matrix is not None:
        matrix = np.concatenate((matrix, equa), axis=0)
    else:
        matrix = equa

solve_equation(matrix)
