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
        if digits != int(np.sqrt(digits))**2 : raise ValueError('digits must be a perfect square')
        self.digits = digits
        self.shape = tuple([digits]*N)
        self.grid = np.zeros(self.shape, dtype=np.int8)
        self.numbers = np.array([n+1 for n in range(digits)])
        self.xtra_rules = []
        if 'constraints' in kwargs.keys():
            self.xtra_rules = kwargs['constraints']
        self.fill() # numbers ends up shuffled, so we redefine it here (faster than sort)
        self.numbers = np.array([n+1 for n in range(digits)])
        grid_copy = deepcopy(self.grid)
        self.solution = 1
        if 'difficulty' in kwargs: difficulty = kwargs['difficulty']
        else: difficulty=3
        while self.solution == 1 or difficulty > 0:
            self.solution = 0
            idx = tuple(np.random.randint(0,digits,N))
            while self.grid[idx] == 0: idx = tuple(np.random.randint(0,digits,N))
            value = self.grid[idx]
            self.grid[idx] = 0
            disposable_grid = deepcopy(self.grid)
            self.solve(disposable_grid)
            if self.solution != 1: self.grid[idx], difficulty = value, difficulty-1
        self.solution = grid_copy 
        # the "solution" variable's only reason to be a class property is so
        # 
    
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
            projected_idx = tuple([indices[i] for i in axes])
            if n in grid.transpose(tuple(axes))[projected_idx[:-1]]: return True
            axes.append(axes.pop(0))
        return on_line
    
    def in_square(self, grid, indices, n): # tN different projections (because N choose 2 dimensions to project on)
        in_any_square = False
        sq_size = int(np.sqrt(self.digits))
        for projection in N_choose_two(self.N):
            # [[indices[i] for i in projection][:-2]]
            # permutation of indices using projection
            # [indices[:-2]]
            # otherwise
            subgrid = grid.transpose(projection)[tuple([indices[i] for i in projection][:-2])]
            line, column = [indices[i] for i in projection][-2:]
            
            # subline = subgrid[:3] if line < 3 else subgrid[3:6] if line < 6 else subgrid[6:]
            # square = subline[:,:3] if column < 3 else subline[:,3:6] if column < 6 else subline[:,6:]
            # generalising lines above by using evaluation of reg string
            subline = eval(f'subgrid[:{sq_size}]'+\
                ''.join([f' if line < {k-sq_size} else subgrid[{k-sq_size}:{k}]' for k in range(sq_size*2, self.digits+1, sq_size)]))
            square = eval(f'subline[:,:{sq_size}]'+\
                ''.join([f' if column < {k-sq_size} else subline[:,{k-sq_size}:{k}]' for k in range(sq_size*2, self.digits+1, sq_size)]))            
            if n in square: return True
        return in_any_square
            
    def breaks_constraints(self, grid, indices, n):
        """Add constraints to the grid generation.

        Current constraints accepted are 'knight' and 'king', can't be used together and only work for N=2 and digits=9.
        """
        # constraints only for N = 2 and digits = 9 because of bad generalisations
        if self.xtra_rules == [] or self.N != 2 or self.digits != 9: return False
        breaks = False

        if 'king' in self.xtra_rules:
            line, column = indices
            T,B,L,R = line>0, line<grid.shape[0]-1, column>0, column<grid.shape[1]-1
            neighbours = [grid[idx] for idx in
                        [(line-1,column-1)]*T*L + [(line-1,column)]*T + [(line-1,column+1)]*T*R + \
                        [(line,column-1)]*L     +                             [(line,column+1)]*R + \
                        [(line+1,column-1)]*B*L + [(line+1,column)]*B + [(line+1,column+1)]*B*R]
            if n in neighbours: return True

        if 'knight' in self.xtra_rules:
            line, column = indices
            neighbour_positions = np.array([(line+m,column+n) for m in range(-2,3) for n in range(-2,3) if abs(m)+abs(n) == 3])
            nei_in_grid = (neighbour_positions.transpose(1,0)[0] > 0) * (neighbour_positions.transpose(1,0)[0] < grid.shape[0]-1) * \
                          (neighbour_positions.transpose(1,0)[1] > 0) * (neighbour_positions.transpose(1,0)[1] < grid.shape[1])
            # checks if knight positions are in grid
            neighbours = [grid[idx] for idx in 
                        [tuple(neighbour_positions[i]) for i in range(neighbour_positions.shape[0]) 
                            if nei_in_grid[i]]]
            if n in neighbours: return True
        
        return breaks

                
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
        self.grid[indices] = 0
         # resets current cell value to zero
        # allows for correcting complicated placements

    def solve(self, grid):
        """Fill an empty grid conformly to how sudokus rules work.

        Returns:
            _type_: _description_
        """
        numbers = self.numbers
        for pos in range(grid.size):
            indices = self.find_indices(pos)
            if grid[indices] == 0:
                for n in numbers:
                    if not self.in_orthogonal(grid,indices,n):
                        if not self.in_square(grid,indices,n):
                            if not self.breaks_constraints(grid,indices,n):
                                grid[indices] = n
                                if not (0 in grid): 
                                    self.solution += 1
                                    break
                                elif self.solve(grid): return True
                    grid[indices] = 0
                break
         # resets current cell value to zero
        # allows for correcting complicated placements


if __name__ == '__main__':

    sudoku = Sudoku(digits=4,N=3)
    print(sudoku.grid)
    print(sudoku.solution)
