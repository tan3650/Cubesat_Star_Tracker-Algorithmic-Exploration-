
# File names
input_file = "C:/Users/Test/OneDrive/Documents/Tanvi/stars_below_8.csv"
output_file = "filtered_stars_38.csv"

# Read the file
with open(input_file, "r") as f:
    lines = f.readlines()

# Keep the header
header = lines[0]
filtered_lines = [header]

# Filter stars with Hpmag <= 4
for line in lines[1:]:
    if line.strip():  # skip empty lines
        mag = float(line.split(",")[3])
        if mag <= 4:
            filtered_lines.append(line)

# Write the filtered data
with open(output_file, "w") as f:
    f.writelines(filtered_lines)

print(f"Filtered data saved to {output_file}")
