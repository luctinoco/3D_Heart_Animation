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

def update(num, line, ax, pbar):
    pbar.update(1)  # Update the progress bar for each frame

    # Calculate elevation and azimuth for rotation
    elev = (num % 360) - 180 if num < total_frames // 2 else 180 - (num % 360)
    azim = num * 2

    # Update the viewing angle
    ax.view_init(elev=elev, azim=azim)
    ax.dist = 8 + 2 * np.sin(np.pi * num / total_frames)  # Change the distance for dynamic effect

    # Determine which phase of the animation we are in
    if num < formation_frames:
        # Heart formation phase
        factor = num / formation_frames
        current_x, current_y, current_z = x_heart * factor, y_heart * factor, z_heart * factor
    elif num < formation_frames + static_frames:
        # Static heart phase
        current_x, current_y, current_z = x_heart, y_heart, z_heart
    elif num < total_frames:
        # Collapse phase
        step = num - (formation_frames + static_frames)
        current_x, current_y, current_z = collapse_heart(x_heart, y_heart, z_heart, step, total_collapse_frames)
    else:
        # Growth phase
        growth_frames = num - (formation_frames + static_frames + total_collapse_frames)
        factor = growth_frames / growth_frames_total
        current_x, current_y, current_z = x_heart * factor, y_heart * factor, z_heart * factor

    # Update the line data for the animation
    line.set_data(current_x, current_y)
    line.set_3d_properties(current_z)
    return line,

# Total number of frames in the animation
total_frames = 720

# Frames for the heart formation phase
formation_frames = total_frames // 2

# Frames the heart remains static
static_frames = 0

# Total frames for the collapse phase
total_collapse_frames = total_frames // 2

# Total frames for the growth phase
growth_frames_total = total_frames

# Get the heart shape coordinates
x_heart, y_heart, z_heart = draw_3d_heart()

# Create a figure for plotting
fig = plt.figure(figsize=(6, 4))  # Resize figure for better rendering
ax = fig.add_subplot(111, projection='3d')
ax.axis('off')  # Remove the bounding box of the 3D axes

# Plot the initial heart shape
line, = ax.plot(x_heart, y_heart, z_heart, c='red')

# Use tqdm to show a progress bar during animation rendering
with tqdm(total=total_frames) as pbar:
    # Create the animation
    ani = animation.FuncAnimation(
        fig, update, fargs=(line, ax, pbar), frames=total_frames,
        interval=100, blit=False, repeat=True
    )

    # Save the animation as a GIF

# By: Lucas F. T. Leonardo
    ani.save('heart_animation.gif', writer='pillow', fps=20, dpi=120, savefig_kwargs={'facecolor': 'white'})
