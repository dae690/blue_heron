# 📁 Project Folder Structure – Atlantic Flyway Waterbird Data Cleaning Project

This document explains the purpose of each folder in the repository to help navigate the project structure efficiently.

---

## 🔹 `data/`
Contains all datasets and reference files used in the project.

- `raw/` – Original, unprocessed datasets (e.g., historical CWB data, AOU species lists).
- `cleaned/` – Cleaned and structured datasets ready for analysis or visualization.
- `reference/` – Supporting files like AOU code mappings, metadata documentation, or flyway state lists.

---

## 🔹 `scripts/`
All Python scripts used in data cleaning, transformation, and validation.

- `data_cleaning.py` 
- `species_code_update.py` 
- `geolocation_check.py`
- `automate_updates.py` 

---

## 🔹 `tableau/`
Dashboards and supporting materials built using Tableau.

- `dashboards/` – Exported `.twbx` or `.hyper` files from Tableau Public.
- `descriptions/` – Writeups explaining dashboard layout, filters, and logic.

---
## 🔹 `docs/`
All project documentation, findings, and planning notes.

- `abstract.md` – Full abstract summarizing project purpose and scope.
- `methodology.md` – Step-by-step explanation of the data cleaning process.
- `findings.md` – Key results, visualizations, and insights from the analysis.
- `sprint_plan.md` – Agile sprint tasks and timeline breakdown (optional).

---

## 🔹 Root Files
- `README.md` – Overview of the project, tools used, and dashboard access.
- `.gitignore` – Files and folders excluded from version control.
- `INFO.md` – This file.

---