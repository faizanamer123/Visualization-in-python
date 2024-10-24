import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Function to draw Sankey Diagram
def draw_sankey(data):
    sources = data['source'].unique().tolist()
    targets = data['target'].unique().tolist()

    all_labels = sources + [label for label in targets if label not in sources]

    node_indices = {label: i for i, label in enumerate(all_labels)}

    data['source_index'] = data['source'].apply(lambda x: node_indices[x])
    data['target_index'] = data['target'].apply(lambda x: node_indices[x])

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_labels,
            color="blue"
        ),
        link=dict(
            source=data['source_index'],
            target=data['target_index'],
            value=data['value']
        ))])

    fig.update_layout(title_text="Interactive Budget Visualization", font_size=10)
    return fig

# Load data
def load_data(file_path):
    return pd.read_csv(file_path)

# Main Streamlit App
def main():
    st.title("Interactive Budget Visualization")

    # File Upload
    st.sidebar.header("Upload Budget Data")
    uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.write("### Uploaded Budget Data")
        st.dataframe(data)

        fig = draw_sankey(data)
        st.plotly_chart(fig)

    else:
        st.write("### Default Budget Data Visualization")
        data = load_data('budget_data.csv')
        st.dataframe(data)

        fig = draw_sankey(data)
        st.plotly_chart(fig)

    # Adjust data
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
            st.write("### Updated Budget Data")
            st.dataframe(data)

            fig = draw_sankey(data)
            st.plotly_chart(fig)
        else:
            st.sidebar.error("Please enter valid data!")

if __name__ == "__main__":
    main()
