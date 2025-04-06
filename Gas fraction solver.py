import numpy as np
from scipy.optimize import fsolve
# Constants
Kp_N2 = 0.00618  # Equilibrium constant for N2 dissociation (atm)
Kp_O2 = 0.0083  # Equilibrium constant for O2 dissociation (atm)
P_total = 5.9  # Total pressure (kPa)
air_ratio = 78 / 22  # N2/O2 ratio in air
# Convert pressure to atm (since Kp is in atm)
P_total_atm = P_total / 101.325


def equations(vars):
    PN2, PO2 = vars  # Partial pressures in atm

    # Calculate atomic partial pressures from equilibrium
    PN = np.sqrt(Kp_N2 * PN2)
    PO = np.sqrt(Kp_O2 * PO2)

    # 1. Dalton's Law: Total pressure constraint
    eq1 = PN2 + PO2 + PN + PO - P_total_atm

    # 2. Nuclei conservation (N/O ratio = 3.545)
    total_N = 2 * PN2 + PN
    total_O = 2 * PO2 + PO
    eq2 = total_N / total_O - air_ratio

    return [eq1, eq2]


# Initial guesses (in atm)
guess = [0.025, 0.01]  # ~4 kPa N2, ~1 kPa O2

# Solve the system
solution = fsolve(equations, guess)

# Convert back to kPa
PN2_atm, PO2_atm = solution
PN_atm = np.sqrt(Kp_N2 * PN2_atm)
PO_atm = np.sqrt(Kp_O2 * PO2_atm)

# Convert all to kPa
PN2 = PN2_atm * 101.325
PO2 = PO2_atm * 101.325
PN = PN_atm * 101.325
PO = PO_atm * 101.325

# Calculate dissociation fractions
alpha_N2 = (PN / (2 * PN2 + PN))
alpha_O2 = (PO / (2 * PO2 + PO))

print(f"Solved Partial Pressures (kPa):")
print(f"N2: {PN2:.4f} kPa")
print(f"O2: {PO2:.4f} kPa")
print(f"N: {PN:.4f} kPa")
print(f"O: {PO:.4f} kPa")
print(f"\nDissociation Fractions:")
print(f"α_N2: {alpha_N2:.4f} ({alpha_N2 * 100:.2f}%)")
print(f"α_O2: {alpha_O2:.4f} ({alpha_O2 * 100:.2f}%)")
print(f"\nVerification:")
print(f"Total pressure: {PN2 + PO2 + PN + PO:.4f} kPa (target: {P_total} kPa)")
print(f"N/O ratio: {(2 * PN2 + PN) / (2 * PO2 + PO):.4f} (target: {air_ratio:.4f})")