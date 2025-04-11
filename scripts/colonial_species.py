import pandas as pd

# Load the main dataset and reference dataset
main_df = pd.read_csv("updated_main_dataset.csv")  # Replace with actual filename
ref_df = pd.read_excel("Atlantic Flyway CWB species list_with_team_input.xlsx")  # Reference dataset with colonial waterbird species

# Get the list of valid species (common names) and AOU codes
valid_species = set(ref_df["COMMON NAME"])
valid_aou_codes = set(ref_df["AOU CODE"])


# Get the list of valid species (common names) and AOU codes
valid_species = set(ref_df["COMMON NAME"].dropna())  # Drop NaN values in reference list
valid_aou_codes = set(ref_df["AOU CODE"].dropna())  # Drop NaN values in reference list

# Apply filtering condition: Only remove rows where Species and AOU_codes are BOTH non-matching and NOT empty
filtered_df = main_df[
    (main_df["Species"].isna()) | (main_df["Species"].isin(valid_species)) |
    (main_df["AOU_codes"].isna()) | (main_df["AOU_codes"].isin(valid_aou_codes))
]

# Save the filtered dataset
filtered_df.to_csv("filtered_main_dataset.csv", index=False)

print("Filtered dataset saved as 'filtered_main_dataset.csv'.")