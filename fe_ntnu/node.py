import numpy as np

class Node:

    def __init__(self, x: float, z: float, fixed=None):
        self.x = x
        self.z = z
        self.fixed = fixed if fixed is not None else [] # 0 -> x fixed, 1 -> z fixed, 2 -> theta fixed
        self.dofs = []
    
    def __str__(self) -> str:
        bcond = ""
        if self.fixed is not []:
            for i in self.fixed:
                match i:
                    case 0:
                        bcond += "x "
                    case 1:
                        bcond += "z "
                    case 2:
                        bcond += "theta"
            return f"Node at x={self.x} and z={self.z} with fixed {bcond}" 
        return f"Node at x={self.x} and z={self.z}"