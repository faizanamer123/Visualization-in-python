import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load and prepare literacy data from CSV for Sankey visualization
def load_and_prepare_data(file_path):
    df = pd.read_csv(file_path)
    # Focus on recent data (e.g., literacy rates in 2022) and filter out rows with NaN values
    df = df[['Region', 'Country', '2022']].dropna()
    df.columns = ['source', 'target', 'value']
    df['value'] = df['value'].astype(float)
    return df

# Enhanced Sankey plot function with improved visuals
def sankey(data):
    sources = data['source'].unique().tolist()
    targets = data['target'].unique().tolist()
    all_labels = sources + [label for label in targets if label not in sources]
    node_indices = {label: i for i, label in enumerate(all_labels)}

    data['source_index'] = data['source'].apply(lambda x: node_indices[x])
    data['target_index'] = data['target'].apply(lambda x: node_indices[x])

    # Define a more refined color palette for nodes
    node_colors = [
        "#8e44ad", "#2980b9", "#16a085", "#e74c3c", "#f39c12",
        "#d35400", "#2ecc71", "#c0392b", "#3498db", "#9b59b6"
    ] * (len(all_labels) // 10 + 1)

    # Generate gradient colors for links based on literacy rate values
    max_value = data['value'].max()
    link_colors = [
        f'rgba({255 - int(200 * (val / max_value))}, {55 + int(200 * (val / max_value))}, {150 - int(100 * (val / max_value))}, 0.7)'
        for val in data['value']
    ]

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=25,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_labels,
            color=node_colors[:len(all_labels)],
            hovertemplate='%{label} has %{value} connections<extra></extra>'
        ),
        link=dict(
            source=data['source_index'],
            target=data['target_index'],
            value=data['value'],
            color=link_colors,
            hovertemplate='From %{source.label} to %{target.label}<br>Value: %{value}<extra></extra>'
        ))])

    # Update layout for better visualization aesthetics
    fig.update_layout(
        title_text="<b>2022 Literacy Rates - Regional vs. Country Distribution</b>",
        title_font=dict(size=22, color='#2c3e50'),
        font=dict(size=14, color='#2c3e50'),
        paper_bgcolor='#f8f9fa',
        margin=dict(l=40, r=40, t=80, b=40),
        plot_bgcolor='#ffffff',
        hovermode='x'
    )
    return fig

# Main Streamlit app
def main():
    st.set_page_config(page_title="Literacy Data Visualization", layout="wide")
    st.title("Literacy Data Visualization - 2022")
    st.markdown(
        """
        This interactive visualization provides insights into literacy rates across different regions and countries for 2022.
        Upload your data to see a customized visualization.
        """
    )

    # Sidebar for file upload
    st.sidebar.header("📊 Upload Literacy Data")
    uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file:
        data = load_and_prepare_data(uploaded_file)
        st.write("### Uploaded Literacy Data")
        st.dataframe(data)

        st.write("### Literacy Visualization")
        fig = sankey(data)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("### Please upload a literacy data CSV file.")

if __name__ == "__main__":
    main()



