import numpy as np
import matplotlib.pyplot as plt

# Set random seed for reproducible results
np.random.seed(42)

# Generate x-axis data points (pulses)
x = np.linspace(0, 120, 1000)

# Create the piecewise function
def pulse_signal(x, noise_level=0.02):
    y = np.zeros_like(x)
    
    # Initial baseline (0-20)
    mask1 = x < 20
    y[mask1] = 6000
    
    # Plateau region (20-70)
    mask2 = (x >= 20) & (x < 70)
    y[mask2] = 12500
    
    # Decay region (70-120)
    mask3 = x >= 70
    y[mask3] = 6000 + 6500 * np.exp(-(x[mask3]-70)/20)
    
    # Add noise components
    noise = np.random.normal(0, noise_level * np.mean(y), len(x))

    y += noise

    # Prevent negative values
    y = np.maximum(y, 0)

    return y

# Calculate y values
y = pulse_signal(x)

# Create the plot
plt.figure(figsize=(10, 5))
plt.plot(x, y, 'b-', linewidth=2)

plt.text(3, 6500, "Fs", fontdict={"size": 15})
plt.text(63, 13200, "Fm'", fontdict={"size": 15})

# Customize the plot
plt.grid(True, linestyle='-', axis='y', alpha=0.3)
plt.xlabel('Pulses', fontdict={"size": 15})
plt.ylabel('Intensity a.u.', fontdict={"size": 15})
for spine in ['top', 'right']:
    plt.gca().spines[spine].set_visible(False)

# Set axis limits
plt.xlim(0, 120)
plt.ylim(4000, 14000)

# Use a tight layout
plt.tight_layout()

# Show the plot
plt.show()