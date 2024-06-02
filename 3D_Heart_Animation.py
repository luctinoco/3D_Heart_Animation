import numpy as np  # Library for numerical operations
import matplotlib.pyplot as plt  # Library for creating plots
from mpl_toolkits.mplot3d import Axes3D  # Toolkit for 3D plots
import matplotlib.animation as animation  # Library for creating animations
from tqdm import tqdm  # Library for displaying a progress bar


def draw_3d_heart():
    # Define the range of values for x (1000 points between -2 and 2)
    x = np.linspace(-2, 2, 1000)

    # Functions to calculate the y values for the heart shape
    y1 = np.sqrt(1 - (np.abs(x) - 1) ** 2)  # Upper part of the heart
    y2 = -3 * np.sqrt(1 - (np.abs(x) / 2) ** 0.5)  # Lower part of the heart

    # Concatenate points to form the 3D heart shape
    x = np.concatenate([x, x[::-1]])  # Join x with its reversed version
    y = np.concatenate([y1, y2[::-1]])  # Join y1 with reversed y2
    z = np.zeros_like(x)  # z remains zero for a 2D heart in 3D space

    return x, y, z


def collapse_heart(x, y, z, step, total_steps):
    # Calculate the collapse factor based on the current step
    collapse_factor = (total_steps - step) / total_steps
    return x * collapse_factor, y * collapse_factor, z * collapse_factor


def rotation_matrix(elev, azim, roll):
    # Combined rotation matrix for rotations around x, y, and z axes
    cos_a, sin_a = np.cos(np.radians(elev)), np.sin(np.radians(elev))
    cos_b, sin_b = np.cos(np.radians(azim)), np.sin(np.radians(azim))
    cos_c, sin_c = np.cos(np.radians(roll)), np.sin(np.radians(roll))

    # Rotation matrix for rotation around z-axis
    Rz = np.array([
        [cos_c, -sin_c, 0],
        [sin_c, cos_c, 0],
        [0, 0, 1]
    ])

    # Rotation matrix for rotation around y-axis
    Ry = np.array([
        [cos_b, 0, sin_b],
        [0, 1, 0],
        [-sin_b, 0, cos_b]
    ])

    # Rotation matrix for rotation around x-axis
    Rx = np.array([
        [1, 0, 0],
        [0, cos_a, -sin_a],
        [0, sin_a, cos_a]
    ])

    return Rz @ Ry @ Rx


def update(num, line, ax, text, pbar):
    pbar.update(1)  # Update the progress bar for each frame

    # Calculate the angles for rotation using a smooth function
    elev = 30 * np.sin(np.radians(num * 360 / total_frames))
    azim = num * 360 / total_frames
    roll = 15 * np.sin(np.radians(num * 360 / total_frames))

    # Determine which phase of the animation we are in
    if num < formation_frames:
        # Heart formation phase
        factor = num / formation_frames
        current_x, current_y, current_z = x_heart * factor, y_heart * factor, z_heart * factor
    elif num < formation_frames + static_frames:
        # Static heart phase
        current_x, current_y, current_z = x_heart, y_heart, z_heart
    else:
        # Collapse phase
        step = num - (formation_frames + static_frames)
        current_x, current_y, current_z = collapse_heart(x_heart, y_heart, z_heart, step, total_collapse_frames)

    # Rotate the heart shape in 3D space using combined rotation matrix
    coords = np.vstack((current_x, current_y, current_z))
    rotation_mat = rotation_matrix(elev, azim, roll)
    coords_rotated = rotation_mat @ coords

    current_x_rotated, current_y_rotated, current_z_rotated = coords_rotated

    # Update the line data for the animation
    line.set_data(current_x_rotated, current_y_rotated)
    line.set_3d_properties(current_z_rotated)

    # Update the text annotations with the current axes
    text.set_text(
        f'Axes:\nx = {current_x_rotated[0]:.2f}, y = {current_y_rotated[0]:.2f}, z = {current_z_rotated[0]:.2f}')

    # Ensure the heart stays within the visible bounds
    ax.set_xlim([-2, 2])
    ax.set_ylim([-3, 3])
    ax.set_zlim([-3, 3])

    return line, text


# Total number of frames in the animation
total_frames = 720

# Frames for the heart formation phase
formation_frames = total_frames // 3

# Frames the heart remains static
static_frames = total_frames // 3

# Total frames for the collapse phase
total_collapse_frames = total_frames // 3

# Get the heart shape coordinates
x_heart, y_heart, z_heart = draw_3d_heart()

# Create a figure for plotting
fig = plt.figure(figsize=(6, 6))  # Resize figure for better rendering
ax = fig.add_subplot(111, projection='3d')

# Add grid and axis labels
ax.grid(True)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Plot the initial heart shape
line, = ax.plot(x_heart, y_heart, z_heart, c='red')

# Add text annotations for the axes
text = ax.text2D(0.05, 0.95, '', transform=ax.transAxes)

# Ensure the grid and axes remain static
ax.view_init(elev=30, azim=30)
ax.dist = 10

# Use tqdm to show a progress bar during animation rendering
with tqdm(total=total_frames) as pbar:
    # Create the animation
    ani = animation.FuncAnimation(
        fig, update, fargs=(line, ax, text, pbar), frames=total_frames,
        interval=100, blit=False, repeat=True
    )

    # Save the animation as a GIF
    ani.save('heart_animation.gif', writer='pillow', fps=20, dpi=120, savefig_kwargs={'facecolor': 'white'})

