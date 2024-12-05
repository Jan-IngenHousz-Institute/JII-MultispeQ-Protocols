import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch


# Create time array
t = np.linspace(0, 11, 1000)

# Create the pulse waveform
def create_pulse(t, start, width):
    return np.where((t >= start) & (t <= start + width), 1, 0)

# Generate pulses
pulse1 = create_pulse(t, 1.5, 1)
pulse2 = create_pulse(t, 4, 1)
pulse3 = create_pulse(t, 6.5, 1)
pulse4 = create_pulse(t, 9, 1)

# Combine all pulses
waveform = pulse1 + pulse2 + pulse3 + pulse4

fig, ax = plt.subplots(figsize=(12, 2.5))

ax.plot(t, waveform, 'r-', linewidth=2)

# Set axis labels and limits
ax.set_xlabel('time', fontdict={"size": 15})
ax.set_ylabel('Intensity', fontdict={"size": 15})
ax.set_ylim(-0.1, 1.2)
ax.set_xlim(0, 12)


## Indicate Pulse
ax.text(0.95, 1.2, "Pulse", fontdict={"size": 15} )
con1 = ConnectionPatch(
    xyA=(0.01, 1.1), xyB=(2.5, 1.1), 
    coordsA='data', coordsB='data',
    axesA=ax, axesB=ax,
    arrowstyle='|-|',
    mutation_scale=5,
    linewidth=2,
    linestyle='-',
    color='black'
)
ax.add_artist(con1)

## Indicate Pulse Distance
ax.text(4.8, 1.2, "Pulse Distance (μs)", fontdict={"size": 15} )
con2 = ConnectionPatch(
    xyA=(5, 1.1), xyB=(6.5, 1.1), 
    coordsA='data', coordsB='data',
    axesA=ax, axesB=ax,
    arrowstyle='|-|',
    mutation_scale=5,
    linewidth=2,
    linestyle='-',
    color='black'
)
ax.add_artist(con2)

## Indicate Pulse Length
ax.text(8.65, 1.2, "Pulse Length (μs)", fontdict={"size": 15} )
con3 = ConnectionPatch(
    xyA=(9, 1.1), xyB=(10, 1.1), 
    coordsA='data', coordsB='data',
    axesA=ax, axesB=ax,
    arrowstyle='|-|',
    mutation_scale=5,
    linewidth=2,
    linestyle='-',
    color='black'
)
ax.add_artist(con3)

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