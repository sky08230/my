def reverse_list(l:list):
    '''
    get the mid position to reverse elements by pairs
    '''
    for i in range(len(l)//2): 
        l[i],l[len(l)-i-1]=l[len(l)-i-1],l[i]
    return l

'''
this function is to check the matrix meet the sudoku requirement 
'''
def  check_sudoku(matrix,n,m,num):
    # check the unqiuness by row
    if matrix[n].count(num)>=1:
        return False
    
    # check the unqiuness by column
    for i in range(9):
        if matrix[i][m]==num:
            return False
    
    # check the unqiuness by 3*3 matrix
    n_tri=n//3
    m_tri=m//3
    for ii in range(n_tri*3,n_tri*3+3):
        for jj in range(m_tri*3,m_tri*3+3):
            if matrix[ii][jj]==num:
                return False
    return True       

'''
use the recusive to fill in the 0 value from 1 to 9, 
if the check  check_sudoku is not satisfied then return original value fill the next value.
'''
def solve_sudoku(matrix,n,m):
    
    #if the loop reach the end of matrix ,then exit the recusive 
    if n==len(matrix)-1 and m==len(matrix):
        return True
    
    #if the column reach the maxium, then start from the next row and 0-column position 
    if m==len(matrix):
        n=n+1
        m=0
    if matrix[n][m]==0:
        for i in range(1,10):
            if check_sudoku(matrix,n,m,i):
                matrix[n][m]=i
                if solve_sudoku(matrix,n,m+1):
                    return True
                matrix[n][m]=0
    else:
        return solve_sudoku(matrix,n,m+1)
    return False    
                
'''
the main entry to call the function solve_sudoku
'''
def call_solve_sudoku(sudo):
    solve_sudoku(sudo,0,0)
    return sudo
    
sudo=\
[[3, 0, 6, 5, 0, 8, 4, 0, 0],
[5, 2, 0, 0, 0, 0, 0, 0, 0],
[0, 8, 7, 0, 0, 0, 0, 3, 1],
[0, 0, 3, 0, 1, 0, 0, 8, 0],
[9, 0, 0, 8, 6, 3, 0, 0, 5],
[0, 5, 0, 0, 9, 0, 6, 0, 0], 
[1, 3, 0, 0, 0, 0, 2, 5, 0],
[0, 0, 0, 0, 0, 0, 0, 7, 4],
[0, 0, 5, 2, 0, 6, 3, 0, 0]]
call_solve_sudoku(sudo)
print(sudo)
print(reverse_list([2,3,4]))
 