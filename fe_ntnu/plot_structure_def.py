import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import CubicSpline
from .plot_supports import plot_supports

def plot_structure_def(sys, scale, supports=True, numbers=True):
    #plot the beam structure defined by nodes and elements
    #the flag supports (1/0) decides if supports are plotted or not
    nodes = np.zeros((len(sys.nodes), 2))
    for i, node in enumerate(sys.nodes):
        nodes[i, :] = [node.x, node.z]
    
    nod_dof = np.array([node.dofs for node in sys.nodes]) + 1
    
    fixed_dof = []
    for idx, node in enumerate(sys.nodes):
        for fdof in node.fixed:
            fixed_dof.append(idx * 3 + fdof + 1)
    fixed_dof = np.array(fixed_dof)

    node_map = {node: idx + 1 for idx, node in enumerate(sys.nodes)}
    el_nod = np.array([[node_map[el.n1], node_map[el.n2]] for el in sys.elements])

    r = sys.r * scale

    if supports:
        fig = plot_supports(nodes, nod_dof, fixed_dof)
        ax = fig.gca()
    else:
        fig, ax = plt.subplots()
    
    # undeformed
    for el in sys.elements:
        ax.plot([el.n1.x, el.n2.x], [el.n1.z, el.n2.z], linestyle="--", color="c", linewidth=2, zorder=1)
        
        # plot hinges on undeformed structure
        if getattr(el, 'hinge_n1', False):
            ax.plot(el.n1.x, el.n1.z, marker='o', markerfacecolor='white', markeredgecolor='c', markersize=5, zorder=2)
        if getattr(el, 'hinge_n2', False):
            ax.plot(el.n2.x, el.n2.z, marker='o', markerfacecolor='white', markeredgecolor='c', markersize=5, zorder=2)


    # Compute new coordinates
    nodes_def = np.array(nodes, copy = 1, dtype = float)
    for inod in range(0, nodes.shape[0]):
        for ixz in range(0, 2):
            if nod_dof[inod, ixz] != 0:
                nodes_def[inod, ixz] = nodes[inod, ixz] + r[nod_dof[inod, ixz] - 1]
    nodes2 = np.copy(nodes_def)

    if numbers == 1:
        # Plot node number
        for inod in range(0, nodes2.shape[0]):
            ax.text(nodes2[inod, 0], nodes2[inod, 1], str(inod + 1), color = 'red', fontsize = 16)

    for iel in range(0, el_nod.shape[0]):
        el = sys.elements[iel]  # Access the element directly
        
        delta_x = nodes[el_nod[iel, 1] - 1, 0] - nodes[el_nod[iel, 0] - 1, 0]
        delta_z = nodes[el_nod[iel, 1] - 1, 1] - nodes[el_nod[iel, 0] - 1, 1]
        L = np.sqrt(delta_x ** 2 + delta_z ** 2)
        if delta_z >= 0:
            psi = np.arccos(delta_x / L)
        else:
            psi = -np.arccos(delta_x / L)

        delta_x2 = nodes2[el_nod[iel, 1] - 1, 0] - nodes2[el_nod[iel, 0] - 1, 0]
        delta_z2 = nodes2[el_nod[iel, 1] - 1, 1] - nodes2[el_nod[iel, 0] - 1, 1]
        L2 = np.sqrt(delta_x2 ** 2 + delta_z2 ** 2)
        if delta_z2 >= 0:
            psi2 = np.arccos(delta_x2 / L2)
        else:
            psi2 = -np.arccos(delta_x2 / L2)

        alf = psi - psi2
        dx = np.zeros((2, 1))
        dz = np.zeros((2, 1))
        phi = np.zeros((2, 1))
        for inod in range(0, 2):
            if nod_dof[el_nod[iel, inod] - 1, 0] > 0:
                dx[inod] = r[nod_dof[el_nod[iel, inod] - 1, 0] - 1]
            if nod_dof[el_nod[iel, inod] - 1, 1] > 0:
                dz[inod] = r[nod_dof[el_nod[iel, inod] - 1, 1] - 1]
            if nod_dof[el_nod[iel, inod] - 1, 2] > 0:
                phi[inod] = r[nod_dof[el_nod[iel, inod] - 1, 2] - 1]
        phi = phi - alf
        x = np.array([0, L2])
        z = np.array([0, 0])
        xx = np.arange(0, 1.01, 0.01)*L2
        
        # hinge?
        # 1 means fixed first derivative, 2 means fixed second derivative
        bc_start = (2, 0.0) if getattr(el, 'hinge_n1', False) else (1, -phi[0, 0])
        bc_end   = (2, 0.0) if getattr(el, 'hinge_n2', False) else (1, -phi[1, 0])
        
        cs = CubicSpline(x, z, bc_type = (bc_start, bc_end))
        zz = cs(xx)

        # Rotate
        xxzz = np.array([[np.cos(psi2), -np.sin(psi2)], [np.sin(psi2), np.cos(psi2)]]) @ np.vstack([xx, zz])

        # Displace
        xx2 = xxzz[0, :] + nodes2[el_nod[iel, 0] - 1, 0]
        zz2 = xxzz[1, :] + nodes2[el_nod[iel, 0] - 1, 1]
        ax.plot(xx2, zz2, 'k', linewidth = 2, zorder=2)
        
        # Plot hinges on deformed structure
        if getattr(el, 'hinge_n1', False):
            ax.plot(xx2[0], zz2[0], marker='o', markerfacecolor='none', markeredgecolor='black', markersize=6, zorder=3)
        if getattr(el, 'hinge_n2', False):
            ax.plot(xx2[-1], zz2[-1], marker='o', markerfacecolor='none', markeredgecolor='black', markersize=6, zorder=3)

        if numbers == 1:
            # Plot element numbers. These are not plotted in the midpoint to
            # avoid number superposition when elements cross in the middle
            ax.text(xx2[round(xx2.size / 2.5)], zz2[round(xx2.size / 2.5)], str(iel + 1), color = 'blue', fontsize = 16)


    ax.axis('equal')
    plt.grid()
    plt.xlabel(r"x in m")
    plt.ylabel(r"z in m")
    plt.show()

    return fig

if __name__ == "__main__":
    nodes = np.array([[0,4], [4,4], [4,0], [8,0]]) #[m]
    print(nodes)
    print(nodes[:,0])