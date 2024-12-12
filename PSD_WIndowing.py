import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import welch, windows


def apply_window(signal, window_type='hann'):
    """
    Apply a window function to the signal to reduce noise

    Parameters:
    signal (numpy.array): Input signal
    window_type (str): Type of window to apply

    Returns:
    numpy.array: Windowed signal
    """
    # Select window function
    if window_type == 'hann':
        window = windows.hann(len(signal))
    elif window_type == 'hamming':
        window = windows.hamming(len(signal))
    elif window_type == 'blackman':
        window = windows.blackman(len(signal))
    elif window_type == 'kaiser':
        window = windows.kaiser(len(signal), beta=14)
    else:
        raise ValueError("Invalid window type")

    return signal * window


# Parameters
WL = 532e-9  # Wavelength
v_max = [0.1056, 0.1101, 0.1296, 0.122]
v_min = [0.0129, 0.0168, 0.0152, 0.0155]

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
for i in range(4):
    dphi = np.arcsin(((voltage.iloc[:, i] - v_min[i]) / ((v_max[i] - v_min[i]) / 2)) - 1)
    delta_phi.append(dphi)

# Convert to numpy array
delta_phi = np.array(delta_phi)

# Compute PSD using Welch's method with different window types
plt.figure(figsize=(20, 15))

# Window types to compare
window_types = ['hann', 'hamming', 'blackman', 'kaiser']

for i in range(len(delta_phi)):
    plt.subplot(4, len(window_types), i * len(window_types) + 1)
    # Original signal PSD
    frequencies, psd = welch(delta_phi[i], fs, nfft=len(delta_phi[i]))
    plt.loglog(frequencies, psd, label="Original", linewidth=2)
    plt.title(f"Channel {i + 1} - Original PSD")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("PSD (rad²/Hz)")
    plt.grid(which="both", linestyle="--", linewidth=0.5)

    # Windowed signal PSD
    for j, window_type in enumerate(window_types):
        plt.subplot(4, len(window_types), i * len(window_types) + j + 1)

        # Apply window
        windowed_signal = apply_window(delta_phi[i], window_type)

        # Compute PSD
        frequencies, psd = welch(windowed_signal, fs, nfft=len(windowed_signal))

        plt.loglog(frequencies, psd, label=window_type.capitalize(), linewidth=2)
        plt.title(f"Channel {i + 1} - {window_type.capitalize()} Window")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("PSD (rad²/Hz)")
        plt.grid(which="both", linestyle="--", linewidth=0.5)
        plt.legend()


plt.savefig("PSD_plot_windowed_signals.png")
plt.show()


# Optional: Print some statistics about noise reduction
def calculate_noise_reduction(original_psd, windowed_psd):
    """
    Calculate noise reduction ratio
    """
    # Compare low-frequency components
    low_freq_original = np.mean(original_psd[:len(original_psd) // 10])
    low_freq_windowed = np.mean(windowed_psd[:len(windowed_psd) // 10])

    noise_reduction = (low_freq_original - low_freq_windowed) / low_freq_original * 100
    return noise_reduction


print("\nNoise Reduction Analysis:")
for i in range(4):
    print(f"\nChannel {i + 1}:")
    original_frequencies, original_psd = welch(delta_phi[i], fs, nfft=len(delta_phi[i]))

    for window_type in window_types:
        windowed_signal = apply_window(delta_phi[i], window_type)
        windowed_frequencies, windowed_psd = welch(windowed_signal, fs, nfft=len(windowed_signal))

        noise_reduction = calculate_noise_reduction(original_psd, windowed_psd)
        print(f"{window_type.capitalize()} Window Noise Reduction: {noise_reduction:.2f}%")