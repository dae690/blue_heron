
import pandas as pd
# Apply the business rule to fill missing PopulationEstimate values
df['PopulationEstimate'] = df.apply(
    lambda row: row['CorrectedCount'] 
    if pd.isna(row['PopulationEstimate']) and pd.notna(row['CorrectedCount'])
    else (row['UncorrectedCount'] 
          if pd.isna(row['PopulationEstimate']) and pd.notna(row['UncorrectedCount']) 
          else row['PopulationEstimate']),
    axis=1
)

# Save the updated dataset
df.to_excel("updated_population_estimate.xlsx", index=False)

# Count how many values were filled
filled_count = df['PopulationEstimate'].notna().sum()
print(f"PopulationEstimate values populated: {filled_count}")



