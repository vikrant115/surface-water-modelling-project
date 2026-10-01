import numpy as np
from scipy.optimize import fsolve

q_lake = 17000        # m3/day (Main river inflow)
n = 0.030             # Manning's roughness
s = 0.00015           # Bed slope
d = 0.4               # Constant depth (m)


def manning_residual(B):
    area = B * d
    perimeter = B + (2 * d)
    r = area / perimeter

    # Manning's: Q = (1/n) * A * R^(2/3) * S^(1/2)
    return ((1/n) * area * (r**(2/3)) * (s**0.5)) - q_lake/86400


new_width = fsolve(manning_residual, 2.0)[0]
velocity_m_day = q_lake / (new_width * d)

print(f" {new_width:<10.3f} |{velocity_m_day:<15.2f}")


def calculate_monthly_hydraulics():

    # --- 1. Constant Parameters ---
    q_lake = 17000       # m3/day (Main river inflow)
    n = 0.030            # Manning's roughness
    s = 0.0001           # Bed slope
    d = 0.6              # Constant depth (m)

    # --- 2. Monthly Meenachil Discharge (m3/day) ---
    meenachil_data = {
        "January": 6000,
        "February": 5500,
        "March": 5000,
        "April": 4500,
        "May": 4000,
        "June": 8000,
        "July": 12000,
        "August": 15000,
        "September": 13000,
        "October": 10000,
        "November": 8000,
        "December": 7000
    }

    print(
        f"{'Month':<12} | {'Total Q (m3/d)':<15} | "
        f"{'Width (m)':<10} | {'Velocity (m/d)':<15}"
    )
    print("-" * 60)

    for month, q_meenachil in meenachil_data.items():

        q_total_day = q_lake + q_meenachil
        q_total_sec = q_total_day / 86400  # Convert to m3/s for Manning's

        # Solver for Width (B)
        def manning_residual(B):
            area = B * d
            perimeter = B + (2 * d)
            r = area / perimeter

            # Manning's: Q = (1/n) * A * R^(2/3) * S^(1/2)
            return ((1/n) * area * (r**(2/3)) * (s**0.5)) - q_total_sec

        new_width = fsolve(manning_residual, 2.0)[0]
        velocity_m_day = q_total_day / (new_width * d)

        print(
            f"{month:<12} | {q_total_day:<15.0f} | "
            f"{new_width:<10.3f} |{velocity_m_day:<15.2f}"
        )


calculate_monthly_hydraulics()
