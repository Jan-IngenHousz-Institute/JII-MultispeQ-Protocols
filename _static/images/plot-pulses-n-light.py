# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.patches import ConnectionPatch

# # Create time array
# t = np.linspace(0, 10, 1000)

# # Create the pulse waveform
# def create_pulse(t, start, width, amplitude=1, color='red'):
#     return np.where((t >= start) & (t <= start + width), amplitude, 0), color

# # Generate pulses with different widths and colors
# pulse1, color1 = create_pulse(t, 1, 1)
# pulse2, color2 = create_pulse(t, 3.5, 0.5, amplitude=1, color='blue')
# pulse3, color3 = create_pulse(t, 5.5, 0.8, amplitude=1, color='red')
# pulse4, color4 = create_pulse(t, 7.5, 0.3, amplitude=1, color='blue')

# # Create the plot
# plt.figure(figsize=(12, 4))

# # Plot each pulse with its color
# plt.plot(t, pulse1, color1, linewidth=2)
# plt.plot(t, pulse2, color2, linewidth=2)
# plt.plot(t, pulse3, color3, linewidth=2)
# plt.plot(t, pulse4, color4, linewidth=2)

# # Add base line in blue
# plt.plot(t, np.zeros_like(t), 'b-', linewidth=1)

# # Set axis labels and limits
# plt.xlabel('time')
# plt.ylabel('Intensity')
# plt.ylim(-0.1, 1.2)
# plt.xlim(0, 10)

# # Add annotations
# plt.annotate('Pulse', xy=(1, 0.5), xytext=(0.5, 0.7),
#             arrowprops=dict(arrowstyle='<->'))
# plt.annotate('Pulse Length (μs) - variable', xy=(5.5, 1.1), xytext=(5.5, 1.1),
#             arrowprops=dict(arrowstyle='<->'))
# plt.annotate('Pulse Distance (μs) - fixed', xy=(6.3, 0.3), xytext=(6.3, 0.3),
#             arrowprops=dict(arrowstyle='<->'))

# # Customize grid and spines
# plt.grid(False)
# for spine in ['top', 'right']:
#     plt.gca().spines[spine].set_visible(False)

# plt.tight_layout()
# plt.show()


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch


# Create time array
t = np.linspace(0, 10, 1000)

# Create the pulse waveform
# def create_pulse(t, start, width, amplitude=1, color='red'):
#     return np.where((t >= start) & (t <= start + width), amplitude, 0), color

# # Generate pulses with different widths and colors
# pulse1, color1 = create_pulse(t, 1, 1)
# pulse2, color2 = create_pulse(t, 3.5, 0.5, amplitude=1, color='blue')
# pulse3, color3 = create_pulse(t, 5.5, 0.8, amplitude=1, color='red')
# pulse4, color4 = create_pulse(t, 7.5, 0.3, amplitude=1, color='blue')


# Create the pulse waveform
def create_pulse(t, start, width, amplitude=1, y=0):
    return np.where((t >= start) & (t <= start + width), amplitude, y)

# Generate pulses red trace
pulse1 = create_pulse(t, 1.5, 1)
pulse2 = create_pulse(t, 6, 1)

# Generate pulses blue trace
pulse3 = create_pulse(t, 4, 0.5, 0.7, 0.01)
pulse4 = create_pulse(t, 8.5, 0.5, 0.7, 0.01)

# Combine all pulses
waveform1 = pulse1 + pulse2
waveform2 = pulse3 + pulse4

fig, ax = plt.subplots(figsize=(12, 2.5))

ax.plot(t, waveform1, 'r-', linewidth=2)
ax.plot(t, waveform2, 'b-', linewidth=2)

# Set axis labels and limits
ax.set_xlabel('time', fontdict={"size": 15})
ax.set_ylabel('Intensity', fontdict={"size": 15})
ax.set_ylim(-0.1, 1.2)
ax.set_xlim(0, 11)


## Text Labels
ax.text(1.8, 1.2, "Pulse", fontdict={"size": 15} )
ax.text(5.95, 1.2, "Pulse Length (μs) - variable", fontdict={"size": 15} )
ax.text(9.2, .55, "Pulse Distance (μs) - fixed", fontdict={"size": 15} )

## Arrows
arrows = [
    [(0.01, 1.1),(4.51, 1.1)],  ## Indicate Pulse
    [(4.51, .6),(5.99, .6)],    ## Indicate Pulse Distance
    [(7.01, .6),(8.49, .6)],
    [(6, 1.1),(7, 1.1)],        ## Indicate Pulse Length
    [(8.5, 1.1),(9, 1.1)]
]

for arrow in arrows:
    con1 = ConnectionPatch(
        xyA=arrow[0], xyB=arrow[1],
        coordsA='data', coordsB='data',
        axesA=ax, axesB=ax,
        arrowstyle='|-|',
        mutation_scale=5,
        linewidth=2,
        linestyle='-',
        color='black'
    )
    ax.add_artist(con1)


ax.tick_params(axis='both', length=0)
ax.set_xticklabels([])  # Hide x-axis numbers
ax.set_yticklabels([])  # Hide y-axis numbers

# Customize grid and spines
ax.grid(False)
for spine in ['top', 'right']:
    plt.gca().spines[spine].set_visible(False)

# Display the plot
plt.tight_layout()
plt.show()