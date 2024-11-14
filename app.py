import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load and prepare data from CSV file
def load_data(file):
    df = pd.read_csv(file)
    df = df[['Region', 'Country', '2022']].dropna()  # Filter to use 2022 data
    df.columns = ['source', 'target', 'value']
    df['value'] = df['value'].astype(float)  # Ensure values are numbers
    return df

# Create a Sankey diagram
def create_sankey(data, title="Sankey Diagram"):
    sources = data['source'].tolist()
    targets = data['target'].tolist()
    values = data['value'].tolist()

    # Unique labels
    all_labels = list(pd.unique(sources + targets))
    label_map = {label: i for i, label in enumerate(all_labels)}

    # Map sources and targets to their index
    data['source_index'] = data['source'].map(label_map)
    data['target_index'] = data['target'].map(label_map)

    # Sankey diagram with basic settings
    fig = go.Figure(go.Sankey(
        node=dict(
            label=all_labels,
            pad=15,
            thickness=20,
            color='lightblue'
        ),
        link=dict(
            source=data['source_index'],
            target=data['target_index'],
            value=values,
            color='rgba(0,100,200,0.4)'  # Semi-transparent blue
        )
    ))
    fig.update_layout(title_text=title, font_size=12)
    return fig

# Main function for Streamlit app
def main():
    st.title("Simple Sankey Diagram Visualization")
    st.write("Upload a CSV file to see a Sankey diagram of the data.")

    # File upload
    file = st.file_uploader("Upload CSV", type=["csv"])
    if file:
        data = load_data(file)
        st.write("### Original Data")
        st.plotly_chart(create_sankey(data, title="Original Data"))

        # Modify data with a multiplier
        st.write("### Adjust Data Values")
        multiplier = st.slider("Multiplier", 0.5, 3.0, 1.0)
        if st.button("Update Visualization"):
            data['value'] *= multiplier
            st.plotly_chart(create_sankey(data, title=f"Modified Data (x{multiplier})"))

if __name__ == "__main__":
    main()
