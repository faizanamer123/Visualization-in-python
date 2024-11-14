import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load and prepare literacy data from CSV for Sankey visualization
def load_and_prepare_data(file_path):
    df = pd.read_csv(file_path)
    df = df[['Region', 'Country', '2022']].dropna()  # Focus on recent data
    df.columns = ['source', 'target', 'value']
    df['value'] = df['value'].astype(float)
    return df

# Generate an enhanced Sankey diagram
def generate_sankey(data, title="Sankey Diagram", node_colors=None):
    sources = data['source'].unique().tolist()
    targets = data['target'].unique().tolist()
    all_labels = sources + [label for label in targets if label not in sources]
    node_indices = {label: i for i, label in enumerate(all_labels)}

    data['source_index'] = data['source'].apply(lambda x: node_indices[x])
    data['target_index'] = data['target'].apply(lambda x: node_indices[x])

    if node_colors is None:
        node_colors = [
            "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
            "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
        ] * (len(all_labels) // 10 + 1)

    max_value = data['value'].max()
    link_colors = [
        f'rgba({255 - int(150 * (val / max_value))}, {100 + int(155 * (val / max_value))}, {50 + int(100 * (val / max_value))}, 0.7)'
        for val in data['value']
    ]

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=30,
            thickness=25,
            line=dict(color="black", width=0.7),
            label=all_labels,
            color=node_colors[:len(all_labels)]
        ),
        link=dict(
            source=data['source_index'],
            target=data['target_index'],
            value=data['value'],
            color=link_colors,
            hovertemplate='From %{source.label} to %{target.label}<br>Value: %{value}<extra></extra>'
        ))])

    fig.update_layout(
        title_text=f"<b>{title}</b>",
        title_font=dict(size=24, color='#1f2c56'),
        font=dict(size=16, color='#34495e'),
        paper_bgcolor='#f7f9fb',
        plot_bgcolor='#ffffff',
        margin=dict(l=40, r=40, t=100, b=40)
    )
    return fig

# Main Streamlit app
def main():
    st.set_page_config(page_title="Pro-Level Literacy Visualization", layout="wide")
    st.title("Pro-Level Literacy Visualization - Interactive Sankey Diagram")
    st.markdown("This visualization allows you to explore and interact with literacy data across regions and countries.")

    st.sidebar.header("📊 Upload Literacy Data")
    uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file:
        original_data = load_and_prepare_data(uploaded_file)

        # Display original data visualization
        st.write("### Original Literacy Data Visualization")
        fig_original = generate_sankey(original_data, title="Original 2022 Literacy Data")
        st.plotly_chart(fig_original, use_container_width=True)

        # Sidebar options to modify data
        st.sidebar.header("🔧 Modify Data")
        tax_change = st.sidebar.slider("Increase Tax Revenue (Multiplier)", min_value=1.0, max_value=3.0, step=0.1, value=1.0)
        expense_reduction = st.sidebar.slider("Decrease Development Expenses (%)", min_value=0, max_value=50, step=5, value=0)

        # First modified dataset (increasing value by a multiplier)
        modified_data_1 = original_data.copy()
        modified_data_1['value'] *= tax_change
        st.write(f"### Modified Visualization (Tax Revenue x{tax_change})")
        fig_modified_1 = generate_sankey(modified_data_1, title=f"Modified Data: Tax Revenue x{tax_change}")
        st.plotly_chart(fig_modified_1, use_container_width=True)

        # Second modified dataset (decreasing value)
        modified_data_2 = original_data.copy()
        modified_data_2['value'] *= (1 - expense_reduction / 100)
        st.write(f"### Modified Visualization (Reduced Development Expenses by {expense_reduction}%)")
        fig_modified_2 = generate_sankey(modified_data_2, title=f"Modified Data: Expenses Reduced by {expense_reduction}%")
        st.plotly_chart(fig_modified_2, use_container_width=True)
    else:
        st.write("### Please upload a literacy data CSV file.")

if __name__ == "__main__":
    main()
