import numpy as np
from copy import deepcopy
import pdb

def N_choose_two(N):
    elements = [i for i in range(N)]
    projections = []
    while elements != []:
        for n in elements[1:]:
            projections.append(tuple([i for i in range(N) if i not in (elements[0], n)]) + (elements[0],n))
        elements.pop(0)
    return projections


class Sudoku:
    def __init__(self,N=2,digits=9, **kwargs):
        if N < 2: N = 2
        self.N = N
        self.digits = digits
        self.shape = tuple([digits]*N)
        self.grid = np.zeros(self.shape, dtype=np.int8)
        self.numbers = np.array([n+1 for n in range(digits)])
        self.xtra_rules = []
        if 'constraints' in kwargs.keys():
            self.xtra_rules = kwargs['constraints']
            
        self.fill()
    
   
    
    def find_indices(self, pos):
        """Find tuple of indices corresponding to integer positive in ndarray.
            
        Example:
            ```py
            >>> sudk = Sudoku(N=4)
            >>> grid = sudk.grid
            >>> sudk.find_indices(5420)
            (7,3,8,3) # gives slice position of 5420th element
            >>> grid[(7,3,8,3)] # how we access the element
            ```
            This allows us to loop on a range of `grid.size` and associate
            each element to a specific cell.

        """
        d = self.digits
        indices = []
        for i in range(self.N-1,-1,-1):
            index = pos//(d**i)
            pos -= index*d**i
            indices.append(index)
        return tuple(indices)
    
    def in_orthogonal(self, grid, indices, n):
        """Check if a number is already present on the lines of a cell, given its position.
        The word "lines" is used regardless of the axis considered, as the distinction 
        between line and column is meaningless in higher dimensions.

        Returns:
            _type_: _description_
        """
        on_line = False
        axes = [ax for ax in range(self.N)]
        for _ in range(self.N):
            if n in grid.transpose(axes)[indices[axes[0]]]:
                on_line = True
            axes.append(axes.pop(0))
        return on_line
    
    def in_square(self, grid, indices, n): # tN different projections (because N choose 2 dimensions to project on)
        in_any_square = False
        for projection in N_choose_two(self.N):
            # [[indices[i] for i in projection][:-2]]
            # permutation of indices using projection
            # [indices[:-2]]
            # otherwise
            subgrid = grid.transpose(projection)[tuple([indices[i] for i in projection][:-2])]
            line, column = [indices[i] for i in projection][-2:]
            subline = subgrid[:3] if line < 3 else subgrid[3:6] if line < 6 else subgrid[6:]
            square = subline[:,:3] if column < 3 else subline[:,3:6] if column < 6 else subline[:,6:]
            #pdb.set_trace()
            if n in square.reshape(1,self.digits):
                in_any_square = True
        return in_any_square
            
    def breaks_constraints(self, grid, indices, n):
        if self.xtra_rules == []: return False
        # check different rules per added constraint
        
    
    def fill(self):
        """Fill an empty grid conformly to how sudokus rules work.

        Returns:
            _type_: _description_
        """

        numbers = self.numbers
        for pos in range(self.grid.size):
            indices = self.find_indices(pos)
            if self.grid[indices] == 0:
                np.random.shuffle(numbers)
                for n in numbers:
                    if not self.in_orthogonal(self.grid,indices,n):
                        if not self.in_square(self.grid,indices,n):
                            if not self.breaks_constraints(self.grid,indices,n):
                                self.grid[indices] = n
                                if not (0 in self.grid): return True
                                elif self.fill(): return True
                break
        self.grid[indices] = 0 # resets current cell value to zero
        # allows for correcting complicated placements




if __name__ == '__main__':

    sudoku = Sudoku(N=2)
    print(sudoku.grid)
    print(not (0 in sudoku.grid))
