import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import welch

# Parameters
WL = 532e-9  # Wavelength
v_max = [0.1056, 0.1101, 0.1296, 0.122]
v_min = [0.0129, 0.0168, 0.0152, 0.0155]
window_size = 22  # Adjust based on your data

# Read the CSV file
file_path = "scope.csv"
data = pd.read_csv(file_path)

# Extract time and voltage columns
time = data['second']
voltage = data[['Volt1', 'Volt2', 'Volt3', 'Volt4']]

# Sampling frequency
fs = 1 / (time[1] - time[0])
print(f"Sampling Frequency: {fs} Hz")

# Convert voltage to phase shift
delta_phi = []
for i in range(4):  # Process all 4 channels
    dphi = np.arcsin(((voltage.iloc[:, i] - v_min[i]) / ((v_max[i] - v_min[i]) / 2)) - 1)
    delta_phi.append(dphi)

# Convert to numpy array
delta_phi = np.array(delta_phi)

# Compute PSD using Welch's method for each phase shift signal
plt.figure(figsize=(15, 10))
for i in range(len(delta_phi)):
    frequencies, psd = welch(delta_phi[i], fs, nfft=len(delta_phi[i]))

    plt.subplot(2, 2, i + 1)
    plt.loglog(frequencies, psd, label=f"Channel {i + 1} Phase Shift PSD", linewidth=2)
    plt.grid(which="both", linestyle="--", linewidth=0.5)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("PSD of Phase Shift (rad²/Hz)")
    plt.title(f"PSD of Phase Shift Signal - Channel {i + 1}")
    plt.legend(fontsize=10)

plt.tight_layout()
plt.savefig('PSD_Phaseshift_4_channels')
plt.show()