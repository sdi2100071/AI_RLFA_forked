from csp import *

class NewCSP(CSP):
    def __init__(self, variables, domains, neighbors, constraints, constraint_dict):
        """Construct a CSP problem. If variables is empty, it becomes domains.keys()."""
        super().__init__(variables, domains, neighbors, constraints, constraint_dict)
        self.con_dict = constraint_dict
        self.cs = {}

        for var in variables:
            self.cs[var] = ()

        # print(self.cs[5])


def dom_wdeg(csp, assignment, var): 

    weight = 1
    for con in csp.con_dict[var]:
        if int(con[0][0]) not in assignment and int(con[0][1]) not in assignment:
            weight += con[1]

    return len(csp.curr_domains[var]) / weight    

    
def wdeg(assignment, csp):
    print(csp.nassigns)
    """Minimum-remaining-values heuristic."""
    if csp.curr_domains is None:
        return first_unassigned_variable(assignment, csp)
    
    min_value = float('inf')
    min_var = 0
    for v in csp.variables:
        if v not in assignment:
            curr_value = dom_wdeg(csp, assignment, v)
            if min_value >= curr_value:
                min_value = curr_value
                min_var = v

    return min_var
    
    
# ______________________________________________________________________________
# Constraint Propagation with AC3


def revise2(csp, Xi, Xj, removals, checks=0):
    """Return true if we remove a value."""
    revised = False
    for x in csp.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        # if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
        conflict = True
        for y in csp.curr_domains[Xj]:
            if csp.constraints(Xi, x, Xj, y, csp.con_dict):
                conflict = False
            checks += 1
            if not conflict:
                break
        if conflict:
            csp.prune(Xi, x, removals)
            revised = True

###################################
    if len(csp.curr_domains[Xi]) == 0:
        constraint = csp.con_dict[Xi]
        for i in range(len(constraint)):
            if int(constraint[i][0][0]) == int(Xi) and int(constraint[i][0][1]) == int(Xj) or \
            int(constraint[i][0][0]) == int(Xj) and int(constraint[i][0][1]) == int(Xi):
                constraint[i][1] += 1
        
        constraint = csp.con_dict[Xj]
        for i in range(len(constraint)):
            if int(constraint[i][0][0]) == int(Xi) and int(constraint[i][0][1]) == int(Xj) or \
            int(constraint[i][0][0]) == int(Xj) and int(constraint[i][0][1]) == int(Xi):
                constraint[i][1] += 1


    return revised
def AC3_2(csp, queue=None, removals=None, arc_heuristic=dom_j_up):
    """[Figure 6.3]"""
    if queue is None:
        queue = {(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]}
    csp.support_pruning()
    queue = arc_heuristic(csp, queue)
    checks = 0
    while queue:
        (Xi, Xj) = queue.pop()
        revised = revise2(csp, Xi, Xj, removals, checks)
        if revised:
            if not csp.curr_domains[Xi]:
                return False  # CSP is inconsistent
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.add((Xk, Xi))
    return True  # CSP is satisfiable
def mac2(csp, var, value, assignment, removals, constraint_propagation=AC3_2):
    """Maintain arc consistency."""
    return constraint_propagation(csp, {(X, var) for X in csp.neighbors[var]}, removals)

def forward_checking2(csp, var, value, assignment, removals):
    """Prune neighbor values inconsistent with var=value."""
    csp.support_pruning()

    for B in csp.neighbors[var]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                if not csp.constraints(var, value, B, b, csp.con_dict):
                    csp.prune(B, b, removals)
###########
###########
###########
            if len(csp.curr_domains[B]) == 0:
                constraint = csp.con_dict[var]
                for i in range(len(constraint)):
                    if int(constraint[i][0][0]) == int(var) and int(constraint[i][0][1]) == int(B) or \
                    int(constraint[i][0][0]) == int(B) and int(constraint[i][0][1]) == int(var):
                        constraint[i][1] += 1
                        break
                    
            if len(csp.curr_domains[B]) == 0:
                constraint = csp.con_dict[B]
                for i in range(len(constraint)):
                    if int(constraint[i][0][0]) == int(var) and int(constraint[i][0][1]) == int(B) or \
                    int(constraint[i][0][0]) == int(B) and int(constraint[i][0][1]) == int(var):
                        constraint[i][1] += 1
                        break

            if not csp.curr_domains[B]:
                return False
    return True


def cbj_search(csp, select_unassigned_variable = wdeg,
                order_domain_values = lcv, inference = forward_checking2):
    
    conflict_set = {}
    for var in csp.variables:
        conflict_set[var] = []

    
    def cbj(assignment):
        max_depth = 0
        if len(assignment) == len(csp.variables):
            return assignment
        
        var = select_unassigned_variable(assignment, csp)  
        for value in order_domain_values(var, assignment, csp): 
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                conflict_set[var].append(removals)

                # if not lenconflict_set[var][0]):
                    # conflict_set[var].append(value)
                    # conflict_set[var]

                print((conflict_set[var][-1]))
                print("NEXT LINE")

                # conflict_set[var] = [removals, depth]


        # print(conflict_set[variable])
                


            
                

    
    
    result = cbj({})
    assert result is None or csp.goal_test(result)
    return result

    