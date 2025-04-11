# Extracting Relevant Records from Two Large Colonial Waterbird Datasets

## Project Overview
This project aims to extract and refine historical colonial waterbird (CWB) data from the **Atlantic Flyway** datasets to improve conservation planning. The project is part of the **DAEN 690: Data Analytics Project** at George Mason University.

## Client Information
- **Client:** Atlantic Flyway Council (AFC) Nongame Migratory Bird Technical Section (NMBTS)
- **Primary Contacts:**
  - Ruth Boettcher, Chair, Waterbirds Committee
  - Angela Tringali, Conservation Delivery Specialist
- **Objective:** Identify and filter reliable historical records to support conservation decision-making.

## Development Approach
This project follows an **Agile Development** approach, divided into **5 sprints**:

![Project Management Mind Map](https://github.com/user-attachments/assets/a2d16571-3cbe-4f9e-86d7-0f0c718ad803) 


# Atlantic Flyway Colonial Waterbird Project

## 📌 Abstract
Monitoring colonial waterbirds across the Atlantic Flyway provides critical insight into ecosystem health. This project involved cleaning and standardizing historical survey data, updating species codes, and developing visualizations to support regional conservation planning. (See full abstract in `docs/abstract.md`.)

## 🧩 Project Structure
- **scripts/**: Python code for cleaning, updating AOU codes, and validation.
- **data/**: Raw and cleaned datasets, along with reference files.
- **tableau/**: Dashboards developed for species visualization and trend analysis.
- **docs/**: Methodology and findings.
- **utils/**: Optional helper functions for reuse.

## 📊 Dashboard
Interactive Tableau dashboards showing species distributions, colony trends, and survey metadata.

[🔗 View Tableau Dashboard](https://public.tableau.com/app/profile/...)

## ⚙️ Tools & Libraries
- Python: pandas, numpy, geopy, seaborn, etc.
- Tableau Public
- Ornithology Journal for AOU code reference

## 🚀 Getting Started
To reproduce the cleaning steps:

```bash
python scripts/data_cleaning.py
python scripts/species_code_update.py
