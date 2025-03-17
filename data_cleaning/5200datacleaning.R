## 
library(tidyverse)
library(readxl)

## load in data

data <- read_excel("../data/raw_data/est21all.xls",
                   skip = 3)

## filter to state level

state_raw <- data |> 
  filter(`County FIPS Code` == '000') |> 
  select(c(3,4,8,14,23))

state <- data.frame(
  code = state_raw$`Postal Code`,
  name = state_raw$Name,
  total_pov = as.numeric(state_raw$`Poverty Percent, All Ages`),
  child_pov = as.numeric(state_raw$`Poverty Percent, Age 0-17`),
  mhi = as.numeric(state_raw$`Median Household Income`)
)

## filter to county level

county_raw <- data |> 
  filter(`County FIPS Code` != '000') |> 
  select(c(1,2,4,8,14,23))

county <- data.frame(
  code = paste(county_raw$`State FIPS Code`,
               county_raw$`County FIPS Code`,
               sep = ""),
  name = county_raw$Name,
  total_pov = as.numeric(county_raw$`Poverty Percent, All Ages`),
  child_pov = as.numeric(county_raw$`Poverty Percent, Age 0-17`),
  mhi = as.numeric(county_raw$`Median Household Income`)
)


write.csv(state,
          "state_poverty.csv",
          row.names = FALSE)

write.csv(county,
          "county_poverty.csv",
          row.names = FALSE)
