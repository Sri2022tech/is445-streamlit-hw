import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title = "Illinois Building Inventory", layout = "wide")

st.title("Illinois Building Inventory")
st.write("Exploring construction and usage of building across IL.")

url = "https://raw.githubusercontent.com/UIUC-iSchool-DataViz/is445_data/main/building_inventory.csv"
df = pd.read_csv(url)

df["Year Constructed"] = pd.to_numeric(df["Year Constructed"], errors = "coerce")
df = df[df["Year Constructed"].between(1800,2026)].copy()
df["Decade"] = (df["Year Constructed"] // 10 * 10).astype(int)

counties = ["All Counties"] + sorted(df["County"].dropna().unique().tolist())
county = st.selectbox("Select a County", counties)

if county != "All Counties":
  df = df[df["County"] == county]

st.header("Buildings Constructed by Decade")

decades = df.groupby("Decade").size().reset_index(name = "Buildings")

chart1 = alt.Chart(decades).mark_line(
  point = True, color = "steelblue"
).encode(
  x = alt.X("Decade:Q", title = "Decade", scale = alt.Scale(zero = False)),
  y = alt.Y("Buildings:Q", title = "Number of Buildings"),
  tooltip = ["Decade", "Buildings"]
).properties(height = 350)

st.altair_chart(chart1, use_container_width = True)

st.write("""
The line chart shows the number of buildings constructed during each decade. The x-axis represents the decade, while the y-axis
shows the number of buildings. I chose a line chart because it makes changes over time easy to identify. The blue line and points help
highlight changes in construction activity. With more time, I would add the ability to compare multiple counties. 
""")

st.header("Building Usage Categories")

usage = df["Usage Description"].fillna("Unknown").value_counts()
top = usage.head(7)
other = usage.iloc[7:].sum()

if other > 0: 
  top = pd.concat([top, pd.Series({"Other": other})])

usage_data = top.reset_index()
usage_data.columns = ["Usage", "Buildings"]

chart2 = alt.Chart(usage_data).mark_arc(innerRadius = 65).encode(
  theta = alt.Theta("Buildings:Q"),
  color = alt.Color("Usage:N", title = "Building Usage"),
  tooltip = ["Usage", "Buildings"]
).properties(height = 400)

st.altair_chart(chart2, use_container_width = True)

st.write("""
This donut chart shows how buildings are distributed across different usage categories. Each color represents a different type of building,
and the size of each section represents its share of the total. I chose a donut chart because it makes the proportions of 
building categories easy to compare. Smaller categories are combined into an other group to keep the chart readable. With more time, I would add an option 
to explore the individual categories in greater detail.
""")

st.header("Comparison to Homework 5")

st.write("""
For Homework 5, I used the Bigfoot sightings dataset and created a bar chart of sightings by season and a scatterplot of sighting locations.
This assignment uses a different dataset and two new visualization types. I used a line chart and a donut chart. The Streamlit county dropdown also allows
users to filter both of the visualizations.
""")
