import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Custom CSS for a sleek look
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        padding: 20px;
    }
    .stApp {
        max-width: 1200px;
        margin: auto;
        font-family: 'Segoe UI', sans-serif;
    }
    .stSidebar {
        background-color: #2e3a4e;
        color: white;
        padding: 20px;
        border-radius: 10px;
    }
    .stSidebar .stSelectbox label, .stSidebar .stRadio label, .stSidebar .stMultiSelect label {
        color: white;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #1a2a3a;
        font-weight: 600;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .css-1d391kg e16zpvfo0 { /* This targets the plot area background, adjust if needed */
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
        font-size: 16px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Athlete Data Visualization App")
st.write("Explore and visualize your athlete data with various charts!")

# Sidebar for file upload and chart selection
st.sidebar.header("Upload your Data")
uploaded_file = st.sidebar.file_uploader("Upload your 'athletes_new.csv' file", type=["csv"])

df = None # Initialize df outside the if block

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("File loaded successfully!")

    st.sidebar.header("Chart Settings")
    chart_type = st.sidebar.selectbox(
        "Select a Chart Type",
        ("Data Overview", "Pair Plot", "Heatmap", "Box Plot", "Scatter Plot",
         "Histogram", "Count Plot", "Violin Plot", "Joint Plot", "FacetGrid (Categorical)", "PairGrid (Custom)")
    )

    st.header(f"Generating: {chart_type}")

    # Common data types for selections
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist() # Added bool and category

    if chart_type == "Data Overview":
        st.subheader("Raw Data Sample")
        st.dataframe(df.head())

        st.subheader("Data Info")
        buffer = pd.io.common.StringIO()
        df.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)

        st.subheader("Descriptive Statistics")
        st.write(df.describe())

    elif chart_type == "Pair Plot":
        st.subheader("Pair Plot")
        if len(numeric_cols) < 2:
            st.warning("Not enough numeric columns to generate a pair plot.")
        else:
            selected_cols_pair = st.sidebar.multiselect("Select columns for Pair Plot", numeric_cols, default=numeric_cols[:min(5, len(numeric_cols))])
            if selected_cols_pair:
                hue_option = st.sidebar.selectbox("Select Hue for Pair Plot (optional)", ['None'] + categorical_cols)
                sns.set_style("whitegrid")
                fig = sns.pairplot(df[selected_cols_pair + ([hue_option] if hue_option != 'None' else [])].dropna(), hue=hue_option if hue_option != 'None' else None)
                st.pyplot(fig)
                plt.clf()
            else:
                st.info("Please select at least two numeric columns for the Pair Plot.")

    elif chart_type == "Heatmap":
        st.subheader("Correlation Heatmap")
        if len(numeric_cols) < 2:
            st.warning("Not enough numeric columns to generate a heatmap.")
        else:
            correlation_matrix = df[numeric_cols].corr()
            plt.figure(figsize=(10, 8))
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
            plt.title('Correlation Heatmap of Numeric Features')
            st.pyplot(plt)
            plt.clf()

    elif chart_type == "Box Plot":
        st.subheader("Box Plot")
        if not numeric_cols:
            st.warning("No numeric columns found for Box Plot.")
        else:
            selected_y = st.sidebar.selectbox("Select a numeric column (Y-axis)", numeric_cols)
            selected_x = st.sidebar.selectbox("Select a categorical column (X-axis)", ['None'] + categorical_cols)

            if selected_y:
                plt.figure(figsize=(10, 6))
                if selected_x != 'None':
                    sns.boxplot(x=df[selected_x], y=df[selected_y])
                    plt.title(f'Box Plot of {selected_y} by {selected_x}')
                    plt.xticks(rotation=45, ha='right')
                else:
                    sns.boxplot(y=df[selected_y])
                    plt.title(f'Box Plot of {selected_y}')
                plt.ylabel(selected_y)
                plt.tight_layout()
                st.pyplot(plt)
                plt.clf()
            else:
                st.info("Please select a numeric column for the Box Plot.")

    elif chart_type == "Scatter Plot":
        st.subheader("Scatter Plot")
        if len(numeric_cols) < 2:
            st.warning("Not enough numeric columns for Scatter Plot.")
        else:
            selected_x = st.sidebar.selectbox("Select X-axis", numeric_cols)
            selected_y = st.sidebar.selectbox("Select Y-axis", [col for col in numeric_cols if col != selected_x])
            hue_options = ['None'] + categorical_cols
            selected_hue = st.sidebar.selectbox("Select Hue (optional)", hue_options)

            if selected_x and selected_y:
                plt.figure(figsize=(10, 6))
                if selected_hue != 'None':
                    sns.scatterplot(x=df[selected_x], y=df[selected_y], hue=df[selected_hue])
                else:
                    sns.scatterplot(x=df[selected_x], y=df[selected_y])
                plt.title(f'Scatter Plot of {selected_y} vs {selected_x}')
                plt.xlabel(selected_x)
                plt.ylabel(selected_y)
                plt.tight_layout()
                st.pyplot(plt)
                plt.clf()
            else:
                st.info("Please select both X and Y axes for the Scatter Plot.")

    elif chart_type == "Histogram":
        st.subheader("Histogram")
        if not numeric_cols:
            st.warning("No numeric columns found for Histogram.")
        else:
            selected_col = st.sidebar.selectbox("Select a numeric column", numeric_cols)
            if selected_col:
                plt.figure(figsize=(10, 6))
                sns.histplot(df[selected_col].dropna(), kde=True)
                plt.title(f'Histogram of {selected_col}')
                plt.xlabel(selected_col)
                plt.ylabel('Frequency')
                plt.tight_layout()
                st.pyplot(plt)
                plt.clf()
            else:
                st.info("Please select a numeric column for the Histogram.")

    elif chart_type == "Count Plot":
        st.subheader("Count Plot")
        if not categorical_cols:
            st.warning("No categorical columns found for Count Plot.")
        else:
            selected_col = st.sidebar.selectbox("Select a categorical column", categorical_cols)
            if selected_col:
                plt.figure(figsize=(10, 6))
                # Consider limiting categories for readability if too many
                top_n = st.sidebar.slider("Show top N categories (0 for all)", 0, len(df[selected_col].value_counts()), 15)
                if top_n > 0:
                    data_to_plot = df[selected_col].value_counts().nlargest(top_n).index
                    sns.countplot(y=df[selected_col][df[selected_col].isin(data_to_plot)].dropna(), order=data_to_plot)
                else:
                    sns.countplot(y=df[selected_col].dropna(), order=df[selected_col].value_counts().index)
                
                plt.title(f'Count Plot of {selected_col}')
                plt.xlabel('Count')
                plt.ylabel(selected_col)
                plt.tight_layout()
                st.pyplot(plt)
                plt.clf()
            else:
                st.info("Please select a categorical column for the Count Plot.")

    elif chart_type == "Violin Plot":
        st.subheader("Violin Plot")
        if not numeric_cols:
            st.warning("No numeric columns found for Violin Plot.")
        else:
            selected_y = st.sidebar.selectbox("Select a numeric column (Y-axis)", numeric_cols, key='violin_y')
            selected_x = st.sidebar.selectbox("Select a categorical column (X-axis)", ['None'] + categorical_cols, key='violin_x')
            
            if selected_y:
                plt.figure(figsize=(10, 6))
                if selected_x != 'None':
                    sns.violinplot(x=df[selected_x], y=df[selected_y])
                    plt.title(f'Violin Plot of {selected_y} by {selected_x}')
                    plt.xticks(rotation=45, ha='right')
                else:
                    sns.violinplot(y=df[selected_y])
                    plt.title(f'Violin Plot of {selected_y}')
                plt.ylabel(selected_y)
                plt.tight_layout()
                st.pyplot(plt)
                plt.clf()
            else:
                st.info("Please select a numeric column for the Violin Plot.")

    elif chart_type == "Joint Plot":
        st.subheader("Joint Plot")
        if len(numeric_cols) < 2:
            st.warning("Not enough numeric columns for Joint Plot.")
        else:
            selected_x = st.sidebar.selectbox("Select X-axis", numeric_cols, key='joint_x')
            selected_y = st.sidebar.selectbox("Select Y-axis", [col for col in numeric_cols if col != selected_x], key='joint_y')
            kind_options = ['scatter', 'hist', 'kde', 'reg']
            selected_kind = st.sidebar.selectbox("Select plot kind", kind_options, key='joint_kind')

            if selected_x and selected_y:
                g = sns.jointplot(x=df[selected_x], y=df[selected_y], kind=selected_kind, height=7)
                g.set_axis_labels(selected_x, selected_y)
                st.pyplot(g)
                plt.clf()
            else:
                st.info("Please select both X and Y axes for the Joint Plot.")

    elif chart_type == "FacetGrid (Categorical)":
        st.subheader("FacetGrid for Categorical Data")
        if not numeric_cols or not categorical_cols:
            st.warning("Need both numeric and categorical columns for FacetGrid.")
        else:
            selected_num_col = st.sidebar.selectbox("Select numeric column (Y-axis)", numeric_cols, key='facet_num')
            selected_cat_col = st.sidebar.selectbox("Select categorical column (Facet by)", categorical_cols, key='facet_cat')
            plot_kind = st.sidebar.selectbox("Select plot kind inside facets", ["hist", "kde", "scatter", "box", "violin"], key='facet_kind')

            if selected_num_col and selected_cat_col:
                # Limit to top N categories for better visualization if many
                top_n_facet = st.sidebar.slider("Limit categories to top N (0 for all)", 0, len(df[selected_cat_col].value_counts()), 10, key='facet_top_n')
                
                data_for_facet = df
                if top_n_facet > 0:
                    top_categories = df[selected_cat_col].value_counts().nlargest(top_n_facet).index
                    data_for_facet = df[df[selected_cat_col].isin(top_categories)]

                g = sns.FacetGrid(data_for_facet.dropna(subset=[selected_num_col, selected_cat_col]), col=selected_cat_col, col_wrap=3, height=3, aspect=1.2, sharey=False)
                
                if plot_kind == "hist":
                    g.map(sns.histplot, selected_num_col, kde=True)
                elif plot_kind == "kde":
                    g.map(sns.kdeplot, selected_num_col, fill=True)
                elif plot_kind == "scatter":
                    # For scatter, we need another numeric variable or just use the index for X for a strip-like plot
                    # For simplicity, let's make it a strip plot if only one variable is selected
                    g.map(sns.stripplot, x=selected_num_col, orient="h") # Using stripplot instead of scatter
                elif plot_kind == "box":
                    g.map(sns.boxplot, y=selected_num_col)
                elif plot_kind == "violin":
                    g.map(sns.violinplot, y=selected_num_col)

                g.set_axis_labels(selected_num_col, "Density/Value")
                g.set_titles(col_template="{col_name}")
                g.tight_layout()
                st.pyplot(g)
                plt.clf()
            else:
                st.info("Please select both a numeric and a categorical column for FacetGrid.")

    elif chart_type == "PairGrid (Custom)":
        st.subheader("PairGrid with Custom Plots")
        if len(numeric_cols) < 2:
            st.warning("Not enough numeric columns for PairGrid.")
        else:
            selected_cols_pairgrid = st.sidebar.multiselect("Select columns for PairGrid", numeric_cols, default=numeric_cols[:min(4, len(numeric_cols))], key='pairgrid_cols')
            hue_option_pairgrid = st.sidebar.selectbox("Select Hue for PairGrid (optional)", ['None'] + categorical_cols, key='pairgrid_hue')

            if len(selected_cols_pairgrid) >= 2:
                g = sns.PairGrid(df[selected_cols_pairgrid + ([hue_option_pairgrid] if hue_option_pairgrid != 'None' else [])].dropna(), hue=hue_option_pairgrid if hue_option_pairgrid != 'None' else None)

                # Map to different plots
                g.map_diag(sns.histplot, kde=True) # Histograms on the diagonal
                g.map_upper(sns.scatterplot) # Scatter plots on the upper triangle
                g.map_lower(sns.kdeplot, fill=True) # KDE plots on the lower triangle

                g.add_legend()
                g.tight_layout()
                st.pyplot(g)
                plt.clf()
            else:
                st.info("Please select at least two numeric columns for the PairGrid.")


else:
    st.info("Please upload your 'athletes_new.csv' file to get started.")
    # Display a placeholder image if no file is uploaded
    st.markdown("<h3>Example Data Visualization</h3>", unsafe_allow_html=True)
    st.image("https://via.placeholder.com/600x400.png?text=Upload+CSV+to+See+Charts", caption="Upload your data to generate visualizations")
    # You can generate a default plot here if you have some sample data to use when no file is uploaded
    # For now, a placeholder image is used.

st.sidebar.markdown("---")
st.sidebar.info("Developed with ❤️ using Streamlit, Seaborn, and Matplotlib")