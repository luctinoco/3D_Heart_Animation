import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from tqdm import tqdm

def draw_3d_heart():
    # Defining the range of values for x
    x = np.linspace(-2, 2, 1000)

    # Function to calculate the values of y and z
    y1 = np.sqrt(1 - (np.abs(x) - 1) ** 2)
    y2 = -3 * np.sqrt(1 - (np.abs(x) / 2) ** 0.5)

    # Concatenating points to form the 3D heart
    x = np.concatenate([x, x[::-1]])
    y = np.concatenate([y1, y2[::-1]])
    z = np.zeros_like(x)

    return x, y, z

def collapse_heart(x, y, z, step, total_steps):
    collapse_factor = (total_steps - step) / total_steps
    return x * collapse_factor, y * collapse_factor, z * collapse_factor

def update(num, line, ax, pbar):
    pbar.update(1)  # Update progress bar

    elev = (num % 360) - 180 if num < total_frames // 2 else 180 - (num % 360)
    azim = num * 2

    ax.view_init(elev=elev, azim=azim)
    ax.dist = 8 + 2 * np.sin(np.pi * num / total_frames)

    if num < formation_frames:
        factor = num / formation_frames
        current_x, current_y, current_z = x_heart * factor, y_heart * factor, z_heart * factor
    elif num < formation_frames + static_frames:
        current_x, current_y, current_z = x_heart, y_heart, z_heart
    elif num < total_frames:
        step = num - (formation_frames + static_frames)
        current_x, current_y, current_z = collapse_heart(x_heart, y_heart, z_heart, step, total_collapse_frames)
    else:
        growth_frames = num - (formation_frames + static_frames + total_collapse_frames)
        factor = growth_frames / growth_frames_total
        current_x, current_y, current_z = x_heart * factor, y_heart * factor, z_heart * factor

    line.set_data(current_x, current_y)
    line.set_3d_properties(current_z)
    return line,

total_frames = 720  # Total number of frames in the animation
formation_frames = total_frames // 2  # Frames for heart formation
static_frames = 0  # Frames the heart remains static
total_collapse_frames = total_frames // 2  # Total frames for collapse
growth_frames_total = total_frames  # Total frames for growth

x_heart, y_heart, z_heart = draw_3d_heart()

fig = plt.figure(figsize=(6, 4))  # Resize figure for better rendering
ax = fig.add_subplot(111, projection='3d')
ax.axis('off')  # Remove bounding box of 3D axes

line, = ax.plot(x_heart, y_heart, z_heart, c='red')

with tqdm(total=total_frames) as pbar:
    ani = animation.FuncAnimation(fig, update, fargs=(line, ax, pbar), frames=total_frames,
                                  interval=100, blit=False,
                                  repeat=True)

    ani.save('heart_animation.gif', writer='pillow', fps=20, dpi=120, savefig_kwargs={'facecolor': 'white'})
# Lucas F. T. Leonardo

