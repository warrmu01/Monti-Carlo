# Monte Carlo Analysis of Utility O&M Budget Risk

## Overview
This project analyzes annual **Operations & Maintenance (O&M) budget risk** for a regulated utility operations department using **Monte Carlo simulation**.  
Rather than producing a single-point forecast, the model quantifies uncertainty, estimates the probability of budget overruns, and identifies the primary drivers of financial risk.

The goal is to support **forecast confidence and cost-management decisions** under realistic cost volatility.

---

## Business Question
**How likely is a utility operations department to exceed its annual O&M budget given historical volatility in labor, materials, and unplanned maintenance costs?**

---

## Objective
Quantify annual budget risk using Monte Carlo simulation by:

- Estimating the probability and magnitude of budget overruns  
- Evaluating forecast confidence using percentile-based outcomes  
- Identifying which cost categories contribute most to overall risk  

---

## Modeling Approach
- Costs are modeled at a **monthly level** and aggregated annually  
- Three O&M cost categories are simulated:
  - **Labor**
  - **Materials**
  - **Unplanned Maintenance**
- Each category is assigned a realistic expected cost and volatility  
- **10,000 simulated years** are generated to create a distribution of possible annual outcomes  
- A fixed annual budget (expected cost + contingency buffer) is used to assess overrun risk  

All data used is **synthetic** and designed to reflect realistic utility cost behavior.  
The focus is on **risk modeling**, not forecasting exact dollar values.

---

## Key Assumptions
- Costs follow independent normal distributions (non-negative)  
- Labor costs are relatively stable; maintenance costs are highly volatile  
- Monthly volatility aggregates to realistic annual uncertainty  
- Budget includes a modest contingency buffer (3%)  

---

## Key Insights
Based on the simulation results:

- **Budget overrun risk is material**  
  There is a **32.6% probability** that annual O&M costs exceed the budget, indicating that roughly **1 in 3 years** may require corrective action or contingency funding.

- **Budgeting is closer to a median outcome than a risk-adjusted forecast**  
  The approved budget falls below the **90th percentile (P90)** of simulated outcomes, suggesting limited protection against high-cost scenarios.

- **Maintenance costs drive the majority of risk**  
  Unplanned maintenance accounts for **~61% of total cost variance**, making it the most impactful lever for reducing budget risk.

- **Overruns are moderate but meaningful**  
  When the budget is exceeded, the average overrun is approximately **$365K**, with a probability-weighted expected exposure of **~$119K annually**.

- **Reducing volatility matters more than reducing averages**  
  Targeted actions that reduce maintenance cost variability could materially improve forecast confidence without reducing service levels.

---

## Outputs
The model produces:

- An **Excel report** summarizing risk metrics, assumptions, and risk drivers  
- A **distribution chart** visualizing simulated annual O&M costs relative to the budget  

*(Generated outputs are not committed to the repository and can be reproduced by running the model.)*
