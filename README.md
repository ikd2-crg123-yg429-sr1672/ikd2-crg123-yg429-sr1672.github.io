# Overdosed: Mapping the U.S. Overdose Crisis Through County-Level Data and Demographic Indicators

## Group 4 Team Members
* [Isak Dai](https://github.com/idai26)
* [Courtney Green](https://github.com/courtneyrgreen)
* [Jen Guo](https://github.com/JenYanni)
* [Sophia Rutman](https://github.com/sophiarutman)


## Executive Summary
In 2021, 106,699 Americans died from a drug overdose. Drug deaths plateaued in 2022 after rising during the pandemic, but the crisis is far from over. People of all ages, races, and backgrounds have died or lost loved ones to addiction, but the crisis has been most dire in certain communities. Rural Appalachia, impoverished urban centers, and Native American reservations have seen the highest rates of overdose deaths. Other areas with high rates of overdose deaths tend to have lower household incomes, lower rates of college education, and higher unemployment rates.


Young adults have the highest rates of drug use. In states with higher rates of college education, drug use is concentrated among young adults. There are also differences in the type of drug used by age and racial group that policymakers should consider when designing addiction prevention and treatment programs. For instance, tranquilizer and inhalant use is most prevalent among White Americans, and marijuana use is more common among younger Americans.


## Instructions for Running Code

Render index.qmd, finding.qmd, and references.qmd. Opening index.html will then allow you to view the website in your browser. Ignore any rendering errors unrelated to these three files - they are irrelevant. 


## Repository Structure
Code used to create the visualizations on the website are available in code/visualizations. All data used in the project can be found in the data folder, with raw_data containing the unmodified data and clean_data containing tidy data cleaned using the code found in code/Data Cleaning. The outputs folder contains html widgets that are embedded in the website. The renv folder and requirements.txt allow for reproducibility of the R and Python environments used to create the website. The website folder contains the final rendered html files and other support files for references and the search function.

```
├── .quarto.yml                # Quarto configuration
├── requirements.txt           # Python package dependencies
├── renv.lock                  # R environment lock file
├── references.bib             # Reference list (BibTeX)
├── README.md                  # Project overview and usage
├── index.qmd                  # Main dashboard page
├── data.qmd                   # Describes data sources
├── findings.qmd              # Summary of key findings
├── references.qmd             # References section
├── about.qmd                  # Project background
├── instructions.md            # Setup or collaboration notes
├── outputs/                   # HTML visualizations for embedding
│   └── [*.html]               # Saved Plotly/Vega/Folium charts
├── website/                   # Website output folder (for publishing)
├── img/                       # Images used in site or markdown
├── data/                      # Raw and processed data files (ignored in Git if listed in .gitignore)
├── code/
│   ├── Data Cleaning/
│   │   ├── addiction cleaning.qmd
│   │   ├── Joining-Datasets.qmd
│   │   └── [*.ipynb, *.R]     # Cleaning scripts
│   ├── EDA/
│   │   ├── IsakEDA.qmd
│   │   ├── Jen addition eda.qmd
│   │   ├── state_level_EDA.ipynb
│   │   └── USDA_EDA_Courtney.qmd
│   └── visualizations/
│       ├── county_metrics_plotly.py
│       ├── folium_county_metrics.py
│       ├── Line Plot.ipynb
│       ├── LinkedPlots.ipynb
│       ├── demographics.ipynb
│       ├── overdose_deaths.qmd
│       └── revised_overdose_deaths.py
├── renv/                      # R environment metadata (used by renv)
```