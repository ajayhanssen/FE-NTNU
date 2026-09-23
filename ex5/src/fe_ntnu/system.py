import numpy as np
from .distributedload import DistributedLoad
from .nodalload import NodalLoad

class System:

    def __init__(self, elements:list, loads:list=None, nodes:list=None):
        self.elements = elements
        self.loads = loads if loads is not None else []

        if nodes is not None:
            self.nodes = nodes
        else:
            self.nodes = []

            # find unique nodes
            for el in elements:
                for candidate in (el.n1, el.n2):
                    # only add candidate if not already in
                    if candidate not in self.nodes:
                        self.nodes.append(candidate)
        
        for idx, node in enumerate(self.nodes):
            node.dofs = [0+idx*3, 1+idx*3, 2+idx*3]
        
    
    def assemble(self):
        total_dofs = 3*len(self.nodes)

        # initn displacement vecg
        self.r = np.zeros(total_dofs)

        # stiffness mat
        K_glob = np.zeros((total_dofs, total_dofs))

        for el in self.elements:
            dofs = el.n1.dofs + el.n2.dofs
            K_glob[np.ix_(dofs, dofs)] += el.k_gl
            
        self.K_glob = K_glob
        
        # force vec
        self.R_glob = np.zeros(total_dofs)

        for load in self.loads:
            if isinstance(load, NodalLoad):
                dofs = load.node.dofs
                self.R_glob[dofs[0]] += load.Fx
                self.R_glob[dofs[1]] += load.Fz
                self.R_glob[dofs[2]] += load.M

            elif isinstance(load, DistributedLoad):
                R_eq = load.get_equivalent_nodal_forces()
                dofs = load.element.n1.dofs + load.element.n2.dofs
                self.R_glob[dofs] += R_eq


    def apply_bcs(self):
        fixed_dofs = []
        for node in self.nodes:
            for fixed_idx in node.fixed:
                fixed_dofs.append(node.dofs[fixed_idx])
        
        self.K_solve = np.copy(self.K_glob)
        self.R_solve = np.copy(self.R_glob)
        for dof in fixed_dofs:
            self.K_solve[dof, :] = 0.0  # zero in row
            self.K_solve[:, dof] = 0.0  # zero in col
            self.K_solve[dof, dof] = 1.0  # set diag to 1
            
            self.R_solve[dof] = 0.0 
            
        return self.K_solve, self.R_solve
    

    def solve(self):
        self.r = np.linalg.solve(self.K_solve, self.R_solve)
        return self.r

    def get_bandwidth(self):
        pass
    
    
    def __str__(self):
        elstr = ""
        for el in self.elements:
            elstr += el.__str__()

        return f"System containing {len(self.elements)} elements:\n{elstr}"
