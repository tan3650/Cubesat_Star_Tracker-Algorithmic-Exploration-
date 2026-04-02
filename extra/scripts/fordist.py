import math
import csv

# Parameters
min_sep = 0.0017  # Minimum separation in radians

# Read input file
stars = []
with open("C:/Users/Test/OneDrive/Documents/Tanvi/StarTracker/hip_eci_new_38.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        stars.append({
            "HIP": int(row["HIP"]),
            "Hpmag": float(row["Hpmag"]),
            "x": float(row["x"]),
            "y": float(row["y"]),
            "z": float(row["z"])
        })

# Generate distance list for all star pairs
distance_list = []
N = len(stars)
for i in range(N-1):
    for j in range(i+1, N):
        xi, yi, zi = stars[i]["x"], stars[i]["y"], stars[i]["z"]
        xj, yj, zj = stars[j]["x"], stars[j]["y"], stars[j]["z"]

        # Compute angular distance
        dot_product = xi*xj + yi*yj + zi*zj
        dot_product = max(min(dot_product, 1.0), -1.0)  # avoid rounding errors
        Dij = math.acos(dot_product)

        # Only filter out extremely close stars
        if Dij >= min_sep:
            distance_list.append({
                "ID1": stars[i]["HIP"],
                "ID2": stars[j]["HIP"],
                "distance_rad": Dij
            })

# Sort by distance
distance_list.sort(key=lambda x: x["distance_rad"])

# Save to CSV
with open("distance_list_all_nofov.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["ID1", "ID2", "distance_rad"])
    writer.writeheader()
    writer.writerows(distance_list)

print(f"Generated {len(distance_list)} star pair distances.")
