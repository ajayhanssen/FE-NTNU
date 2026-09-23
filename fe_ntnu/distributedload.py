import numpy as np

class DistributedLoad:

    def __init__(self, element: Element, qz=0):
        # qz is the uniform load perpendicular to the local element axis (e.g., N/m)
        self.element = element
        self.qz = qz
        
    def get_equivalent_nodal_forces(self) -> np.array:
        L = self.element.L
        q = self.qz
        
        
        R_loc = np.array([
            0,             # local x1
            -q * L / 2,     # local z1
            q * L**2 / 12, # local theta1
            0,             # local x2
            -q * L / 2,     # local z2
            -q * L**2 / 12 # local theta2
        ])
        
        # transf local forces to global 
        R_glob = self.element.Tg.T @ R_loc
        return R_glob