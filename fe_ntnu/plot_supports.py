import numpy as np
from matplotlib import pyplot as plt

def plot_supports(nodes, nod_dof, fixed_dof):
    # plots the nodal supports
    # symbols for horizontal, vertical, and rotational support
    hsupx = np.array([0, -0.2, -0.2, 0])
    hsupy = np.array([0, 0.1, -0.1, 0])
    vsupx = np.array([0, 0.1, -0.1, 0])
    vsupy = np.array([0, -0.2, -0.2, 0])
    rsupx = np.array([0.1, -0.1, -0.1, 0.1, 0.1])
    rsupy = np.array([-0.1, -0.1, 0.1, 0.1, -0.1])

    fig = plt.figure(figsize=(7, 5), dpi=100)
    ax = fig.gca()

    for ibc in range(np.size(fixed_dof)):
        for inod in range(np.size(nod_dof, 0)):
            if fixed_dof[ibc] == nod_dof[inod, 0]:
                ax.plot(hsupx+nodes[inod, 0] , hsupy+nodes[inod, 1], c='k')
            if fixed_dof[ibc] == nod_dof[inod, 1]:
                ax.plot(vsupx+nodes[inod, 0] , vsupy+nodes[inod, 1], c='k')
            if fixed_dof[ibc] == nod_dof[inod, 2]:   
                ax.plot(rsupx+nodes[inod, 0] , rsupy+nodes[inod, 1], c='k')

    return fig