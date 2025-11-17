import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(page_title="Zara Sales Analysis", layout="wide")
st.title("Zara Sales Analysis Visualization")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("myproject/zara.csv", sep=";")
    return df

df = load_data()

# Data preprocessing for later use
df["sales"] = df["price"] * df["Sales Volume"]

# Create bins for price analysis
bins = [0, 100, 200, 300, 400, 500]
df["price_bin"] = pd.cut(df["price"], bins=bins).astype(str)

# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Category Analysis",
    "Promotion & Seasonal Effects",
    "Price Analysis",
    "Product Performance",
    "Gender/Section Analysis",
    "Product Position Analysis",
    "Price-Category Heatmap"
])

# ==================== TAB 1: CATEGORY ANALYSIS ====================
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # Average sales volume by category (bar)
        df_sum = df.groupby(["terms"])["Sales Volume"].sum()
        counts = df["terms"].value_counts()
        average = df_sum / counts
        
        fig_avg_bar = px.bar(
            x=average.index,
            y=average.values,
            labels={"x": "Category", "y": "Average Sales Volume"},
            title="Average Sales Volume by Category",
            color=average.values,
            color_continuous_scale="Viridis"
        )
        fig_avg_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_avg_bar, use_container_width=True)
    
    with col2:
        # Sales percentage by category (pie)
        fig_pie = px.pie(
            values=df_sum.values,
            names=df_sum.index,
            title="Sales Percentage by Category"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Total sales by category (bar)
    fig_total = px.bar(
        x=df_sum.index,
        y=df_sum.values,
        labels={"x": "Category", "y": "Total Sales Volume"},
        title="Total Sales Volume by Category",
        color=df_sum.values,
        color_continuous_scale="Blues"
    )
    fig_total.update_layout(showlegend=False)
    st.plotly_chart(fig_total, use_container_width=True)

# ==================== TAB 2: PROMOTION & SEASONAL EFFECTS ====================
with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        # Promotion effect on average sales
        df_sum_promo = df.groupby(["Promotion"])["Sales Volume"].sum()
        counts_promo = df["Promotion"].value_counts()
        average_promo = df_sum_promo / counts_promo
        
        fig_promo = px.bar(
            x=average_promo.index,
            y=average_promo.values,
            labels={"x": "Promotion", "y": "Average Sales Volume"},
            title="Promotion Effect on Average Sales",
            color=average_promo.values,
            color_continuous_scale="Greens"
        )
        fig_promo.update_layout(showlegend=False)
        st.plotly_chart(fig_promo, use_container_width=True)
    
    with col2:
        # Seasonal effect on average sales (FIXED: use Seasonal counts)
        df_sum_seasonal = df.groupby(["Seasonal"])["Sales Volume"].sum()
        counts_seasonal = df["Seasonal"].value_counts()
        average_seasonal = df_sum_seasonal / counts_seasonal
        
        fig_seasonal = px.bar(
            x=average_seasonal.index,
            y=average_seasonal.values,
            labels={"x": "Seasonal", "y": "Average Sales Volume"},
            title="Seasonal Effect on Average Sales",
            color=average_seasonal.values,
            color_continuous_scale="Oranges"
        )
        fig_seasonal.update_layout(showlegend=False)
        st.plotly_chart(fig_seasonal, use_container_width=True)

# ==================== TAB 3: PRICE ANALYSIS ====================
with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        # Price vs Sales Volume (scatter)
        fig_scatter = px.scatter(
            df,
            x="price",
            y="Sales Volume",
            title="Price vs Sales Volume",
            labels={"price": "Price", "Sales Volume": "Sales Volume"},
            opacity=0.6
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        # Price distribution histogram
        fig_hist = px.histogram(
            df,
            x="Sales Volume",
            nbins=30,
            title="Sales Volume Distribution",
            labels={"Sales Volume": "Sales Volume"},
            color_discrete_sequence=["skyblue"]
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    
    # Price by category (box plot)
    fig_box = px.box(
        df,
        x="terms",
        y="price",
        title="Price Distribution by Category",
        labels={"terms": "Category", "price": "Price"}
    )
    st.plotly_chart(fig_box, use_container_width=True)

# ==================== TAB 4: PRODUCT PERFORMANCE ====================
with tab4:
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 10 products by sales volume
        df_top10 = df.nlargest(n=10, columns=["Sales Volume"])
        fig_top10 = px.bar(
            df_top10,
            x="name",
            y="Sales Volume",
            title="Top 10 Products by Sales Volume",
            labels={"name": "Product Name", "Sales Volume": "Sales Volume"},
            color="Sales Volume",
            color_continuous_scale="Reds"
        )
        fig_top10.update_xaxes(tickangle=-45)
        fig_top10.update_layout(showlegend=False)
        st.plotly_chart(fig_top10, use_container_width=True)
    
    with col2:
        # Total sales revenue by category
        df_sum_revenue = df.groupby(["terms"])["sales"].sum()
        fig_revenue = px.bar(
            x=df_sum_revenue.index,
            y=df_sum_revenue.values,
            title="Total Sales Revenue by Category",
            labels={"x": "Category", "y": "Sales Revenue"},
            color=df_sum_revenue.values,
            color_continuous_scale="Purples"
        )
        fig_revenue.update_layout(showlegend=False)
        st.plotly_chart(fig_revenue, use_container_width=True)

# ==================== TAB 5: GENDER/SECTION ANALYSIS ====================
with tab5:
    col1, col2 = st.columns(2)
    
    with col1:
        # Total sales by gender
        df_sum_section = df.groupby(["section"])["Sales Volume"].sum()
        fig_section = px.bar(
            x=df_sum_section.index,
            y=df_sum_section.values,
            title="Total Sales Volume by Gender",
            labels={"x": "Gender", "y": "Sales Volume"},
            color=df_sum_section.values,
            color_continuous_scale="Teal"
        )
        fig_section.update_layout(showlegend=False)
        st.plotly_chart(fig_section, use_container_width=True)
    
    with col2:
        # Sales category distribution by gender (pie)
        counts_section = df["section"].value_counts()
        fig_section_pie = px.pie(
            values=counts_section.values,
            names=counts_section.index,
            title="Sales Category Distribution by Gender"
        )
        st.plotly_chart(fig_section_pie, use_container_width=True)
    
    # Average sales by gender
    counts_section = df["section"].value_counts()
    average_section = df_sum_section / counts_section
    fig_avg_section = px.bar(
        x=average_section.index,
        y=average_section.values,
        title="Average Sales Volume by Gender",
        labels={"x": "Gender", "y": "Average Sales Volume"},
        color=average_section.values,
        color_continuous_scale="Teal"
    )
    fig_avg_section.update_layout(showlegend=False)
    st.plotly_chart(fig_avg_section, use_container_width=True)

# ==================== TAB 6: PRODUCT POSITION ANALYSIS ====================
with tab6:
    col1, col2 = st.columns(2)
    
    with col1:
        # Average sales by product position (bar)
        df_sum_position = df.groupby(["Product Position"])["Sales Volume"].sum()
        counts_position = df["Product Position"].value_counts()
        average_position = df_sum_position / counts_position
        
        fig_position = px.bar(
            x=average_position.index,
            y=average_position.values,
            title="Average Sales Volume by Product Position",
            labels={"x": "Product Position", "y": "Average Sales Volume"},
            color=average_position.values,
            color_continuous_scale="Plasma"
        )
        fig_position.update_layout(showlegend=False)
        st.plotly_chart(fig_position, use_container_width=True)
    
    with col2:
        # Sales distribution by product position (violin)
        fig_violin = px.violin(
            df,
            x="Product Position",
            y="Sales Volume",
            title="Sales Volume Distribution by Product Position",
            labels={"Product Position": "Product Position", "Sales Volume": "Sales Volume"}
        )
        st.plotly_chart(fig_violin, use_container_width=True)
    
    # Promotion vs Product Position heatmap
    heatmap_data = df.pivot_table(
        index=["Promotion"],
        columns=["Product Position"],
        values=["Sales Volume"],
        aggfunc="sum"
    )
    heatmap_data.columns = heatmap_data.columns.get_level_values(1)
    
    fig_heatmap = px.imshow(
        heatmap_data,
        title="Promotion vs Product Position (Sales Volume)",
        labels=dict(x="Product Position", y="Promotion", color="Sales Volume"),
        color_continuous_scale="YlGnBu",
        text_auto=True
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

# ==================== TAB 7: PRICE-CATEGORY HEATMAP ====================
with tab7:
    # Price bins vs categories heatmap
    heatmap_data2 = df.pivot_table(
        index=["price_bin"],
        columns=["terms"],
        values=["Sales Volume"],
        aggfunc="sum"
    )
    heatmap_data2.columns = heatmap_data2.columns.get_level_values(1)
    
    fig_heatmap2 = px.imshow(
        heatmap_data2,
        title="Price Range vs Category (Sales Volume)",
        labels=dict(x="Category", y="Price Range", color="Sales Volume"),
        color_continuous_scale="YlGnBu",
        text_auto=True
    )
    st.plotly_chart(fig_heatmap2, use_container_width=True)

st.success("✓ Zara Sales Analysis Dashboard Loaded Successfully")
