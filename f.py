import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load Data
df = pd.read_csv(r"F:\data anlysist notes\flipkart_com-ecommerce_sample.csv.zip")

# Handle missing values
df = df.assign(
    retail_price=df["retail_price"].fillna(df["retail_price"].mean()),
    discounted_price=df["discounted_price"].fillna(df["discounted_price"].mean()),
    brand=df["brand"].fillna("Unknown"),
    product_specifications=df["product_specifications"].fillna("Not Available")
)

# Calculate Discount Percentage
df["discount_percentage"] = ((df["retail_price"] - df["discounted_price"]) / df["retail_price"]) * 100

top_products = df['product_category_tree'].value_counts().reset_index()
top_products.columns = ['top_products', 'total_count']

top_brands = df['brand'].value_counts().reset_index()
top_brands.columns = ['top_brands', 'total_count']

# Pie Chart
top_n = 10
fig_pie = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
fig_pie.add_trace(go.Pie(labels=top_products['top_products'][:top_n], values=top_products['total_count'][:top_n], name="Top Products"), 1, 1)
fig_pie.add_trace(go.Pie(labels=top_brands['top_brands'][:top_n], values=top_brands['total_count'][:top_n], name="Top Brands"), 1, 2)
fig_pie.update_layout(title_text="Top 10 Products & Brands")
fig_pie.show()

# Bar Chart
top_discount_brands = df.groupby("brand")["discount_percentage"].mean().reset_index().sort_values(by="discount_percentage", ascending=False).head(10)
fig_bar = px.bar(top_discount_brands, x="brand", y="discount_percentage", title="Top 10 Brands with Highest Discount", text_auto=True, color="discount_percentage", color_continuous_scale="blues")
fig_bar.show()

# Funnel Chart
df = df[df['product_rating'] != 'No rating available']
df['product_rating'] = df['product_rating'].astype(float)
top_rated_brands = df.groupby("brand")["product_rating"].mean().reset_index().sort_values(by="product_rating", ascending=False).head(5)
fig_funnel = px.funnel(
    top_rated_brands, 
    x="product_rating", 
    y="brand", 
    title="Top 5 Highest Rated Brands", 
    color="product_rating"
)

fig_funnel.show()

# Scatter Plot
ratings = df['product_rating'].value_counts().reset_index()
ratings.columns = ['Ratings', 'Counts']
fig_scatter = go.Figure()
fig_scatter.add_trace(go.Scatter(x=ratings['Ratings'], y=ratings['Counts'], mode='markers', marker=dict(size=16, color=ratings['Counts'], showscale=True)))
fig_scatter.update_layout(title="Product Ratings vs Count", xaxis_title="Ratings", yaxis_title="Count")
fig_scatter.show()

# Histogram
fig_hist = px.histogram(df, x="discount_percentage", nbins=30, title="Discount Percentage Distribution", color_discrete_sequence=["purple"])
fig_hist.show()
