# Full Cleaning Pipeline for Atlantic Flyway Dataset
# Purpose: Standardize and clean species names, units, survey methods, AOU codes, and related fields

import pandas as pd
import re

# STEP 1: Load the original dataset
df = pd.read_csv("filtered_States.csv")  # Replace with your actual dataset file path

# STEP 2: Standardize categorical values using mapping dictionaries
# These mappings fix inconsistent text labels across fields

# 2a: Data Quality Mapping
data_quality_mapping = {
    "Unknown": "Unknown", "Precise Estimate": "Precise Estimate", "Good Estimate": "Good Estimate",
    "good": "Good Estimate", "Good": "Good Estimate", "Rough Estimate": "Rough Estimate",
    "Precise": "Precise Estimate", "precise": "Precise Estimate", "Rough": "Rough Estimate",
    "rough": "Rough Estimate", "nown": "Unknown", "Unreliable": "Unreliable"
}

# 2b: Count Type Mapping
count_type_mapping = {
    "Aerial": "Aerial", "Actual Count": "Actual", "Estimate": "Estimate", "Unknown": "Unknown",
    "Actual": "Actual", "estimate": "Estimate", "actual": "Actual", "Flush Count": "Flush Count",
    "Incomplete": "Incomplete", "Flush": "Flush Count", "flush": "Flush Count",
    "Part Count/Part Estimate": "Partial", "Sample": "Partial", "Other": "Other",
    "nown": "Unknown", "Partial": "Partial"
}

# 2c: Unit Counted Mapping
unit_counted_mapping = {
    "Nests": "Nests", "Individuals": "Individuals", "Pairs": "Pairs", "nests": "Nests",
    "Unknown": "Unknown", "pairs": "Pairs", "Yg Fledged": "Fledged Young", "Adults": "Adults",
    "Nest": "Nests", "incubating adults": "Adults, incubating", "Individual": "Individuals",
    "Incubating Adults": "Adults, incubating", "Adult": "Adults", "adults": "Adults",
    "Chick": "Unfledged Young", "Pair": "Pairs", "adults, nests": "Adults, breeding",
    "nown": "Unknown", "Sample": "Unknown", "Banded chicks": "Unfledged Young"
}

# Apply the mappings to their respective columns
df["DataQuality"] = df["DataQuality"].map(data_quality_mapping)
df["CountType"] = df["CountType"].map(count_type_mapping)
df["UnitCounted"] = df["UnitCounted"].map(unit_counted_mapping)

# STEP 3: Normalize Species and AOU Codes using reference list
ref_df = pd.read_csv("IBP-AOS-LIST24.csv")
spec_to_common = dict(zip(ref_df["SPEC"], ref_df["COMMONNAME"]))
common_to_spec = dict(zip(ref_df["COMMONNAME"], ref_df["SPEC"]))

# Replace AOU codes with species names where applicable
df["AOU_codes"] = df["Species"].map(common_to_spec)  # Convert species to AOU
# Also convert AOU to species (in case some are in code form)
df["Species"] = df["Species"].replace(spec_to_common)

# STEP 4: Reconfirm AOU mapping again for consistency
species_to_aou = dict(zip(ref_df["COMMONNAME"], ref_df["SPEC"]))
df["AOU_codes"] = df["Species"].map(species_to_aou)

# STEP 5: Filter out non-matching species and AOU codes based on reference list
valid_species = set(ref_df["COMMONNAME"].dropna())
valid_aou = set(ref_df["SPEC"].dropna())
df = df[
    (df["Species"].isna()) | (df["Species"].isin(valid_species)) |
    (df["AOU_codes"].isna()) | (df["AOU_codes"].isin(valid_aou))
]

# STEP 6: Special AOU 4-letter code cleanup for unknown groups
special_4code_map = {
    "UNCO": "Unknown Cormorants",
    "UNGU": "Unknown Gulls",
    "UNHE": "Unknown Herons",
    "UNTE": "Unknown Terns",
    "UNTN": "Unknown Terns"
}
df["4-digit_AOU_codes"] = df["4-digit_AOU_codes"].astype(str).str.strip()
df["Species"] = df.apply(
    lambda row: special_4code_map.get(row["4-digit_AOU_codes"], row["Species"]), axis=1
)

# STEP 7: Estimate population values based on available count columns
df["CorrectedCount"] = pd.to_numeric(df["CorrectedCount"], errors="coerce")
df["UncorrectedCount"] = pd.to_numeric(df["UncorrectedCount"], errors="coerce")
df["PopulationEstimate"] = df["CorrectedCount"].combine_first(df["UncorrectedCount"])

# STEP 8: Move Observer values into 'Landmass' column based on provided external observer list
observer_df = pd.read_csv("unique_observers.csv")
landmass_values = set(observer_df["Observer"].dropna())
df["Landmass"] = df["Observer"].where(df["Observer"].isin(landmass_values))
df.loc[df["Observer"].isin(landmass_values), "Observer"] = pd.NA

# STEP 9: Clean and classify SurveyMethod into categories
# 9a: Remove encoding noise from SurveyMethod values
def fix_encoding_issues(value):
    value = str(value).encode('utf-8', 'ignore').decode('utf-8', 'ignore')
    value = value.replace('\xa0', ' ')
    value = re.sub(r'[–—‑]', '-', value)
    value = re.sub(r'Ã|Â|,', ' ', value)
    value = re.sub(r'\s+', ' ', value)
    return value.strip()

df["SurveyMethod"] = df["SurveyMethod"].fillna("Unknown").astype(str).str.strip()
df["SurveyMethod_Cleaned"] = df["SurveyMethod"].apply(fix_encoding_issues)

# 9b: Assign categories to SurveyMethod values
def classify_method(value):
    lower = value.lower()
    if lower.startswith("other -"): return value
    if "aerial" in lower: return "Aerial"
    if "ground" in lower and "boat" in lower: return "Boat"
    if "boat" in lower: return "Boat"
    if "drone" in lower: return "Drone"
    if "photo" in lower: return "Photographic"
    if "foot" in lower: return "Foot"
    if "ground" in lower: return "Ground"
    if "nest retention" in lower: return "Nest Retention"
    if "perimeter count" in lower: return "Perimeter Count"
    if "total ground count" in lower: return "Total Ground Count"
    if "visual estimate" in lower: return "Visual Estimate"
    if "partial count and projection" in lower: return "Partial Projection"
    if "unknown" in lower or "not recorded" in lower: return "Unknown"
    return "Other"

df["SurveyMethod_Category"] = df["SurveyMethod_Cleaned"].apply(classify_method)

# STEP 10: Save the final cleaned version
# You can change the output filename as needed
df.to_csv("Cleaned_Atlantic_Flyway_Final.csv", index=False)
print("✅ Data cleaning completed and saved as 'Cleaned_Atlantic_Flyway_Final.csv'")
