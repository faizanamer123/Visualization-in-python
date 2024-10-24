import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def draw_beautiful_sankey(data):
    # Prepare unique labels and indices
    sources = data['source'].unique().tolist()
    targets = data['target'].unique().tolist()
    all_labels = sources + [label for label in targets if label not in sources]
    node_indices = {label: i for i, label in enumerate(all_labels)}

    # Assign indices to sources and targets
    data['source_index'] = data['source'].apply(lambda x: node_indices[x])
    data['target_index'] = data['target'].apply(lambda x: node_indices[x])

    # Define custom colors for categories
    color_palette = [
        "#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A",
        "#19D3F3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"
    ]
    node_colors = color_palette * (len(all_labels) // len(color_palette) + 1)

    # Create Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=20,
            thickness=30,
            line=dict(color="gray", width=0.5),
            label=all_labels,
            color=node_colors[:len(all_labels)]
        ),
        link=dict(
            source=data['source_index'],
            target=data['target_index'],
            value=data['value'],
            color=['rgba(0, 128, 255, 0.4)' if val >= 300 else 'rgba(255, 99, 71, 0.4)' for val in data['value']]
        ))])

    fig.update_layout(
        title_text="Enhanced Interactive Budget Visualization",
        font_size=12,
        margin=dict(l=50, r=50, t=50, b=50),
        paper_bgcolor='lightgray'
    )
    return fig

# Load data
def load_data(file_path):
    return pd.read_csv(file_path)

# Main Streamlit App
def main():
    st.title("Beautiful & Interactive Budget Visualization")
    st.markdown(
        """
        This visualization showcases a detailed budget breakdown with multiple categories, allowing for an interactive and appealing overview of the budget data.
        """
    )

    # File Upload
    st.sidebar.header("Upload Your Enhanced Budget Data")
    uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.write("### Uploaded Enhanced Budget Data")
        st.dataframe(data)

        fig = draw_beautiful_sankey(data)
        st.plotly_chart(fig)

    else:
        st.write("### Default Enhanced Budget Data Visualization")
        data = load_data('budget_data.csv')
        st.dataframe(data)

        fig = draw_beautiful_sankey(data)
        st.plotly_chart(fig)

    # Sidebar to adjust data
    st.sidebar.header("Adjust Data")
    new_source = st.sidebar.text_input("New Source")
    new_target = st.sidebar.text_input("New Target")
    new_value = st.sidebar.number_input("New Value", min_value=0, value=0)

    if st.sidebar.button("Add Entry"):
        if new_source and new_target and new_value > 0:
            new_entry = pd.DataFrame({
                'source': [new_source],
                'target': [new_target],
                'value': [new_value]
            })
            data = pd.concat([data, new_entry], ignore_index=True)
            st.write("### Updated Enhanced Budget Data")
            st.dataframe(data)

            fig = draw_beautiful_sankey(data)
            st.plotly_chart(fig)
        else:
            st.sidebar.error("Please enter valid data!")

if __name__ == "__main__":
    main()

