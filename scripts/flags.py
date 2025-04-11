# Flagging Pipeline for Data Review
# Purpose: Identify and flag records that require attention based on specific criteria provided by domain experts
# Output: Flagged dataset + summary statistics by state, species, and month, useful for review

import pandas as pd

# Load dataset
df = pd.read_csv("Cleaned_Atlantic_Flyway_data2.csv")

# Clean relevant fields
df["Species"] = df["Species"].astype(str).str.strip()
df["Month"] = pd.to_numeric(df["Month"], errors="coerce")
df["UnitCounted"] = df["UnitCounted"].astype(str).str.strip()

# ---------------------------------------------
# FLAGGING CRITERIA
# ---------------------------------------------

# Criteria 1: Species codes for unknown birds (e.g., UNCO = Unknown Cormorants, etc.)
unknown_species_codes = ["UNCO", "UNGU", "UNHE", "UNTE", "UNTN"]
df["Flag_UnknownSpecies"] = df["4-digit_AOU_codes"].isin(unknown_species_codes)

# Criteria 2: Records collected between October and March (non-breeding season)
df["Flag_OffSeason"] = df["Month"].isin([10, 11, 12, 1, 2, 3])

# Criteria 3: UnitCounted = Unknown
df["Flag_UnitCounted_Unknown"] = df["UnitCounted"].str.lower() == "unknown"

# Criteria 4: UnitCounted field is blank or missing
df["Flag_UnitCounted_Blank"] = df["UnitCounted"].isin(["", "nan", "NaN"])

# Criteria 5: Missing PopulationEstimate
df["Flag_PopulationEstimate_Missing"] = pd.isnull(df["PopulationEstimate"])

# Criteria 6a-d: Specific flagged UnitCounted categories
df["Flag_UnitCounted_Adults"] = df["UnitCounted"].str.lower() == "adults"
df["Flag_UnitCounted_Individuals"] = df["UnitCounted"].str.lower() == "individuals"
df["Flag_UnitCounted_UnfledgedYoung"] = df["UnitCounted"].str.lower() == "unfledged young"
df["Flag_UnitCounted_FledgedYoung"] = df["UnitCounted"].str.lower() == "fledged young"

# ---------------------------------------------
# SUMMARIES FOR REVIEW
# ---------------------------------------------

# Summary 1: Unknown species records by state
unknown_species_summary = df[df["Flag_UnknownSpecies"]].groupby("State").size().reset_index(name="RecordCount")

# Summary 2: Off-season records by Month, State, and Species
off_season_summary = df[df["Flag_OffSeason"]].groupby(["Month", "State", "Species"]).size().reset_index(name="RecordCount")

# Summary 3: All flagged record counts by flag type
flag_columns = [col for col in df.columns if col.startswith("Flag_")]
flag_summary = df[flag_columns].sum().reset_index()
flag_summary.columns = ["FlagType", "RecordCount"]

# Save flagged dataset and summaries
df.to_csv("Flagged_Atlantic_Flyway_data.csv", index=False)

with pd.ExcelWriter("Flagging_Summary_Review.xlsx") as writer:
    unknown_species_summary.to_excel(writer, sheet_name="UnknownSpecies_ByState", index=False)
    off_season_summary.to_excel(writer, sheet_name="OffSeason_ByMonth", index=False)
    flag_summary.to_excel(writer, sheet_name="Flag_Counts", index=False)

print("✅ Flagging complete. Data saved as 'Flagged_Atlantic_Flyway_data.csv' and summary as 'Flagging_Summary_Review.xlsx'")
