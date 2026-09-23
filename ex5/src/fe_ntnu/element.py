import numpy as np
from .eucl_dist import eucl_dist

class Element:

    def __init__(self, n1, n2, E, I, A, hinge_n1=False, hinge_n2=False):
        self.n1 = n1
        self.n2 = n2
        self.E = E
        self.I = I
        self.A = A
        self.hinge_n1 = hinge_n1
        self.hinge_n2 = hinge_n2
        self.L = eucl_dist([n1.x, n1.z], [n2.x, n2.z]) # calc length
        self.psi = np.atan2(self.n2.z-self.n1.z, self.n2.x-self.n1.x) # calc angle

        Tgs = np.array([[np.cos(self.psi), np.sin(self.psi), 0],
                        [-np.sin(self.psi), np.cos(self.psi), 0],
                        [0, 0, 1]])

        self.Tg = np.zeros((6, 6)) # global transformation mat
        self.Tg[0:3, 0:3] = Tgs
        self.Tg[3:6, 3:6] = Tgs

        k_loc = self.get_k_local()
        self.k_gl = self.Tg.T @ k_loc @ self.Tg
    
    def get_k_local(self) -> np.array:
        L, A, I, E = self.L, self.A, self.I, self.E
        mu = A*L**2/I

        if not self.hinge_n1 and not self.hinge_n2:
            # all fixed
            k_loc = E * I / L**3 * np.array([
                [ mu,    0,       0,     -mu,    0,       0     ],
                [  0,   12,     -6*L,      0,  -12,     -6*L   ],
                [  0,  -6*L,     4*L**2,   0,   6*L,     2*L**2],
                [-mu,    0,       0,      mu,    0,       0     ],
                [  0,  -12,      6*L,      0,   12,      6*L   ],
                [  0,  -6*L,     2*L**2,   0,   6*L,     4*L**2]
            ])
        elif not self.hinge_n1 and self.hinge_n2:
            # hinged at 2
            k_loc = E * I / L**3 * np.array([
                [ mu,    0,       0,     -mu,    0,       0],
                [  0,    3,     -3*L,      0,   -3,       0],
                [  0,   -3*L,    3*L**2,   0,    3*L,     0],
                [-mu,    0,       0,      mu,    0,       0],
                [  0,   -3,      3*L,      0,    3,       0],
                [  0,    0,       0,       0,    0,       0]
            ])
        elif self.hinge_n1 and not self.hinge_n2:
            # hinged at 1
            k_loc = E * I / L**3 * np.array([
                [ mu,    0,       0,     -mu,    0,       0],
                [  0,    3,       0,       0,   -3,    -3*L],
                [  0,    0,       0,       0,    0,       0],
                [-mu,    0,       0,      mu,    0,       0],
                [  0,   -3,       0,       0,    3,     3*L],
                [  0,  -3*L,      0,       0,    3*L, 3*L**2]
            ])
        else:
            # both hinged
            k_loc = E * I / L**3 * np.array([
                [ mu,    0,       0,     -mu,    0,       0],
                [  0,    0,       0,       0,    0,       0],
                [  0,    0,       0,       0,    0,       0],
                [-mu,    0,       0,      mu,    0,       0],
                [  0,    0,       0,       0,    0,       0],
                [  0,    0,       0,       0,    0,       0]
            ])
        
        return k_loc
    
    def __str__(self):
        return f"Element with L={self.L}, E={self.E}, I={self.I} and A={self.A} and Nodes:\n\t{self.n1.__str__()}\n\t{self.n2.__str__()}\nangle={self.psi}\n"
