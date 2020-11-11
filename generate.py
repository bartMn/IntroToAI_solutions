import sys
import copy
from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())


    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.domains:
            to_remove= set()
            for val in self.domains[var]: 
                if var.length != len(val):
                    to_remove.add(val)
            self.domains[var]= self.domains[var]- to_remove
   
                 
    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised= False
        overlap= self.crossword.overlaps[x, y]
        if not overlap:
            return revised

        to_remove= set()
        for val_x in self.domains[x]:
            #constraint
            count= 0
            for val_y in self.domains[y]:
                if val_x[overlap[0]] == val_y[overlap[1]]:
                    count+=1
                    break
            if count==0:
                to_remove.add(val_x)
                revised= True
        self.domains[x]= self.domains[x] - to_remove
        return revised
                    
            
    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        #creating arc queue if not given
        nghbrs={}
        for var in self.domains:
            nghbrs[var]= self.crossword.neighbors(var)
        
        if not arcs:
            arcs=[]
            for var in self.domains:
                for n_var in nghbrs[var]:
                    arcs.append((var, n_var))
            
        while arcs:
            x, y= arcs.pop(0)
            if self.revise(x, y):
                if len(self.domains[x])==0:
                    return False
                for var_n_v2 in nghbrs[x]:
                    if var_n_v2 != y:
                        arcs.append((var_n_v2, x))
        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var0 in self.domains:
            if var0 not in assignment:
                return False
        return True


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for var0 in self.domains:
            if var0 not in assignment:
                continue
            #checking if len is correct
            if len(assignment[var0]) != var0.length:
                return False
            
            #checking if overlap is the same
            nghbrs= self.crossword.neighbors(var0)
            for neighbor in nghbrs:
                if neighbor not in assignment:
                    continue
                overlap= self.crossword.overlaps[var0, neighbor]
                if assignment[var0][overlap[0]] != assignment[neighbor][overlap[1]]:
                    return False
                
            #checking if every var is distinct
            for var1 in assignment:
                if var0== var1 or not assignment[var1]:
                    continue
                elif assignment[var0]== assignment[var1]:
                    return False
        return True
    
    
    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        #return self.domains[var]
        domain={}
        neighbors= self.crossword.neighbors(var)
        for val in self.domains[var]:
            constraint_count=0
            for neighbor in neighbors:
                if neighbor in assignment:
                    continue
                for n_val in self.domains[neighbor]:
                    overlap= self.crossword.overlaps[var, neighbor]
                    if val[overlap[0]] != n_val[overlap[1]]:
                        constraint_count +=1
                        
            domain[val] =constraint_count
            
        sorted_dom= sorted(domain, key= lambda v: domain[v])
        
        return sorted_dom
                
    

    def select_unassigned_variable(self, assignment): 
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_vars= []
        for var in self.domains:
            if var not in assignment:
                unassigned_vars.append(var)
                
        #unassigned_vars.sort(key= lambda var: len(self.crossword.neighbors(var)), reverse= True)
        #unassigned_vars.sort(key= lambda var: len(self.domains[var]), reverse= False)
        unassigned_vars= self.multisort(list(unassigned_vars), ((lambda var: len(self.domains[var]), False), (lambda var: len(self.crossword.neighbors(var)), True)))
       
        return unassigned_vars[0]
        

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        if self.assignment_complete(assignment):
            return assignment
        virable= self.select_unassigned_variable(assignment)
                
        sorted_domain= self.order_domain_values(virable, assignment)
        for val in sorted_domain:
            assignment[virable]= val
            initial_domain= self.Inference(assignment, virable)
            if self.consistent(assignment):
                result= self.backtrack(assignment)
                if result and len(result)== len(self.domains):
                    return result
            assignment.pop(virable)
            self.domains= copy.copy(initial_domain)
        return None
    
    
    
    def Inference(self, assignment, var):
        new_arcs=[]
        initial_domain= copy.copy(self.domains)
        self.domains[var]= {assignment[var]}
        for neighbor in self.crossword.neighbors(var):
            new_arcs.append((neighbor, var))
        self.ac3(new_arcs)
        
        return initial_domain
            
    
    def multisort(self, to_sort, specs):
        for feature, reverse in reversed(specs):
            to_sort.sort(key= feature, reverse= reverse)
        return to_sort
    

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
