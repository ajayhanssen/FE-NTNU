import numpy as np

class NodalLoad:

    def __init__(self, node: Node, Fx=0, Fz=0, M=0):
        self.node = node
        self.Fx = Fx
        self.Fz = Fz
        self.M = M