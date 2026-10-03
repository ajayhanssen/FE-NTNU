import numpy as np

class DistributedLoad:

    def __init__(self, element: Element, qz=0):
        # qz is uniform load perpendicular to local element axis
        self.element = element
        self.qz = qz
        
    def get_equivalent_nodal_forces(self) -> np.array:
        L = self.element.L
        q = self.qz
        
        if not self.element.hinge_n1 and not self.element.hinge_n2:
            # all fixed
            R_loc = np.array([
                0,             # local x1
                -q * L / 2,     # local z1
                q * L**2 / 12, # local theta1
                0,             # local x2
                -q * L / 2,     # local z2
                -q * L**2 / 12 # local theta2
            ])
        elif not self.element.hinge_n1 and self.element.hinge_n2:
            # hinged at 2 (from lecture notes)
            R_loc = np.array([
                0,
                -5 * q * L / 8,
                q * L**2 / 8,
                0,
                -3 * q * L / 8,
                0
            ])
        elif self.element.hinge_n1 and not self.element.hinge_n2:
            # hinged at 1 (from ex 4 problem 2)
            R_loc = np.array([
                0,
                -3 * q * L / 8,
                0,
                0,
                -5 * q * L / 8,
                -q * L**2 / 8,
            ])
        
        elif self.element.hinge_n1 and self.element.hinge_n2:
            # both hinged
            R_loc = np.array([
                0,
                -q * L / 2,
                0,
                0,
                -q * L / 2,
                0,
            ])
        
        # transf local forces to global 
        R_glob = self.element.Tg.T @ R_loc
        return R_glob