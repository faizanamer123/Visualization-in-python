import streamlit as st
import pandas as pd
import plotly.graph_objects as go
def load_and_prepare_data(file):
    df = pd.read_csv(file)
    df = df[['Region', 'Country', '2022']].dropna()  
    df.columns = ['source', 'target', 'value']
    df['value'] = df['value'].astype(float)
    return df


def create_sankey(data, title="Sankey Diagram", custom_colors=None):
    sources = data['source'].unique().tolist()
    targets = data['target'].unique().tolist()
    all_labels = sources + [t for t in targets if t not in sources]
    label_to_index = {label: idx for idx, label in enumerate(all_labels)}
    
    data['source_index'] = data['source'].map(label_to_index)
    data['target_index'] = data['target'].map(label_to_index)

    if custom_colors is None:
        custom_colors = [
            "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
            "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
        ] * (len(all_labels) // 10 + 1)

    # Create Sankey plot
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=20,
            thickness=20,
            line=dict(color="gray", width=0.5),
            label=all_labels,
            color=custom_colors[:len(all_labels)]
        ),
        link=dict(
            source=data['source_index'],
            target=data['target_index'],
            value=data['value'],
            color='rgba(66, 135, 245, 0.5)', 
            hoverinfo='skip'  
        )
    )])

    fig.update_layout(
        title_text=f"<b>{title}</b>",
        title_font=dict(size=24, color='#1f2c56', family='Arial Black'),
        font=dict(size=14, color='#404040', family='Arial'),
        paper_bgcolor='whitesmoke',
        margin=dict(l=50, r=50, t=70, b=50),
        height=600, 
    )
    return fig

def main():
    st.set_page_config(page_title="Enhanced Literacy Visualization", layout="wide")
    st.title("Enhanced Literacy Data Visualization")
    st.markdown(
        "Upload your literacy data file to view the Sankey diagram. "
        "Modify data values dynamically to see their impact."
    )

    uploaded_file = st.file_uploader("📊 Upload Literacy Data (CSV)", type=["csv"])
    if uploaded_file:
        original_data = load_and_prepare_data(uploaded_file)
        st.write("### Original Data Visualization")
        fig = create_sankey(original_data, title="Original Literacy Data (2022)")
        st.plotly_chart(fig, use_container_width=True)


        st.write("### Modify Data and Generate New Visualizations")
        st.markdown(
            "Use the slider to adjust values and observe changes in the graph."
        )
        multiplier = st.slider("Value Multiplier", min_value=0.5, max_value=3.0, step=0.1, value=1.0)

        if st.button("Generate New Visualization"):
            modified_data = original_data.copy()
            modified_data['value'] *= multiplier
            modified_fig = create_sankey(modified_data, title=f"Modified Data (Multiplier x{multiplier})")
            st.plotly_chart(modified_fig, use_container_width=True)
    else:
        st.write("### Please upload a CSV file to start.")

if __name__ == "__main__":
    main()
