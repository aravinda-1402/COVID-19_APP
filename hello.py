# Hi Team, thank you for reviewing my submission!
# In under 30 minutes, I built this interactive COVID-19 dashboard using Preswald's tools and documentation (https://docs.preswald.com/).
# With more time, I would explore advanced data imputation, query result caching, and richer UI features like dropdown filters or toggles.
# Looking forward to the opportunity to build scalable, real-world data products like this with your team!


# 1. Load the dataset
from preswald import connect, get_df

connect()  
df = get_df("data/covid.csv")  

# Basic data cleaning as it was messy
import pandas as pd
numeric_cols = [
    "Confirmed", "Deaths", "Recovered", "Active",
    "New cases", "New deaths", "New recovered",
    "Deaths / 100 Cases", "Recovered / 100 Cases",
    "Deaths / 100 Recovered", "1 week change", "1 week % increase"
]
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Dropping rows where core metrics are missing. If I had more time I would have thought about other ways of handling missing values like imputation
df = df.dropna(subset=["Confirmed", "Deaths", "Recovered", "Active"])

# 2. Query or manipulate the data
from preswald import query

sql = """
SELECT "Country/Region", "WHO Region", "Confirmed", "Deaths", "Recovered", "Active"
FROM "data/covid.csv"
WHERE "Active" IS NOT NULL AND CAST("Active" AS DOUBLE) > 10000
"""
filtered_df = query(sql, "data/covid.csv")

# 3. Build an interactive UI
from preswald import table, text

text("# 🦠 Global COVID-19 Impact App")

text("**Welcome!** This dashboard provides **real-time insights** into global COVID-19 trends.\n\n")
text("It specifically focuses on **countries with more than 10,000 active cases**, showcasing comparative case counts and outcomes by region.")
table(filtered_df, title="🌐 Countries with >10,000 Active Cases")

# 4. Create a visualization
from preswald import plotly
import plotly.express as px

text("### ⚖️ Recovery vs Mortality Analysis")
text("This scatter plot compares the **number of recovered cases** against **reported deaths** across countries. Points are color-coded by WHO region, enabling a visual understanding of relative recovery and mortality outcomes worldwide.")

fig = px.scatter(df, x="Recovered", y="Deaths", color="WHO Region", title="📉 Deaths vs Recoveries by Country")
plotly(fig)

# Bar Chart: Top 15 by Confirmed Cases
top_confirmed = df.sort_values("Confirmed", ascending=False).head(15)
fig_bar = px.bar(
    top_confirmed,
    x="Country/Region",
    y="Confirmed",
    color="WHO Region",
    title="📊 Top 15 Countries by Confirmed Cases"
)
text("### 🧮 Highest Confirmed Case Counts")
text("The bar chart below ranks the **top 15 countries** by total number of **confirmed COVID-19 cases**.")
plotly(fig_bar)
