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
volt1 = data[:, 1]  # Sensor 1
volt2 = data[:, 2]  # Sensor 2

# Filter Data Between 0.0194s and 0.02s
mask = (time > 0.0194) & (time < 0.02025)
filtered_time = time[mask]
filtered_volt1 = volt1[mask]
filtered_volt2 = volt2[mask]
filtered_p1 = volt1[mask]*832.11+15 # Scaling voltage to pressure
filtered_p2 =volt2[mask]*832.11+15  # scaling voltage to pressure
# Plot Pressure vs. Time (Filtered)
plt.figure(figsize=(10, 5))
plt.plot(filtered_time, filtered_volt1, label="Pressure Sensor 1", linestyle='-', linewidth=1.2, color='b')
plt.plot(filtered_time, filtered_volt2, label="Pressure Sensor 2", linestyle='--', linewidth=1.2, color='r')
plt.xlabel("Time (s)")
plt.ylabel("Volts")
plt.title("Primary Shock Tube Sensor readings in Volts ")
plt.legend()
plt.grid()
plt.figure()
plt.plot(filtered_time, filtered_p1, label="Pressure Sensor 1", linestyle='-', linewidth=1.2, color='b')
plt.plot(filtered_time, filtered_p2, label="Pressure Sensor 2", linestyle='-', linewidth=1.2, color='r')
# Formatting the plot
plt.xlabel("Time (s)")
plt.ylabel("Pressure (KPa)")
plt.title("Primary Shock Tube Pressure readings ")
plt.legend()
plt.grid()

# Show the plot
plt.show()