import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


def E(q, r0, x, y):
    """Return the electric field vector E=(Ex,Ey) due to charge q at r0."""
    den = np.hypot(x - r0[0], y - r0[1]) ** 2
    return q * (x - r0[0]) / den, q * (y - r0[1]) / den


def main():
    # Grid of x, y points.
    nx, ny = 64, 64
    x = np.linspace(-2, 2, nx)
    y = np.linspace(-2, 2, ny)
    X, Y = np.meshgrid(x, y)

    # Create a multipole with nq charges of alternating sign, equally spaced
    # on the unit circle.
    nq = 64
    quart = nq / 4
    charges = []
    for i in range(nq):
        if i < quart:
            x_ = i / quart * 2 - 1
            y_ = 1
        elif i < 2 * quart:
            x_ = 1
            y_ = -(i - quart) / quart * 2 + 1
        elif i < 3 * quart:
            x_ = -(i - 2 * quart) / quart * 2 + 1
            y_ = -1
        else:
            x_ = -1
            y_ = (i - 3 * quart) / quart * 2 - 1
        q = -1
        charges.append((q, (x_, y_)))

    # Electric field vector, E=(Ex, Ey), as separate components.
    Ex, Ey = np.zeros((ny, nx)), np.zeros((ny, nx))
    for charge in charges:
        ex, ey = E(*charge, x=X, y=Y)
        Ex += ex
        Ey += ey

    fig = plt.figure()
    ax = fig.add_subplot(111)

    # Plot the streamlines with an appropriate colormap and arrow style.
    color = 2 * np.log(np.hypot(Ex, Ey))
    ax.streamplot(
        x,
        y,
        Ex,
        Ey,
        color=color,
        linewidth=1,
        cmap=plt.cm.inferno,
        density=2,
        arrowstyle='->',
        arrowsize=0.5,
    )

    # Add filled circles for the charges themselves.
    charge_colors = {True: '#aa0000', False: '#0000aa'}
    for q, pos in charges:
        ax.add_artist(Circle(pos, 0.05, color=charge_colors[q > 0]))

    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')

    plt.tight_layout()
    plt.savefig('square.png')
    # plt.show()


if __name__ == '__main__':
  main()
