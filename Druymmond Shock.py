import numpy as np
import matplotlib.pyplot as plt

filename = "data_15kpa.lvm"

# Read data while skipping header lines
with open(filename, "r") as file:
    lines = file.readlines()

# Detect where numeric data starts (ignoring LabVIEW headers)
data_start = 0
for i, line in enumerate(lines):
    if line.strip() and line[0].isdigit():
        data_start = i
        break

# Load numeric data using NumPy
data = np.loadtxt(filename, delimiter=",", skiprows=data_start)

# Extract columns
time = data[:, 0]  # Time column
pressure1 = data[:, 1]*832.11+15  # Sensor 1
pressure2 = data[:, 2]*832.11+15  # Sensor 2

# Plot Pressure vs. Time
plt.figure(figsize=(10, 5))
plt.plot(time, pressure1, label="Pressure Sensor 1", linestyle='-', linewidth=1.2, color ='b')
plt.plot(time, pressure2, label="Pressure Sensor 2", linestyle='--', linewidth=1.2, color ='r')

# Formatting the plot
plt.xlabel("Time (s)")
plt.ylabel("Pressure (KPa)")
plt.title("Shock Tube Pressure Sensor Data")
plt.legend()
plt.grid()

# Show the plot
plt.show()