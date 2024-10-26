import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def sankey(data):
    sources = data['source'].unique().tolist()
    targets = data['target'].unique().tolist()
    all_labels = sources + [label for label in targets if label not in sources]
    node_indices = {label: i for i, label in enumerate(all_labels)}

    data['source_index'] = data['source'].apply(lambda x: node_indices[x])
    data['target_index'] = data['target'].apply(lambda x: node_indices[x])

    color_palette = [
        "#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A",
        "#19D3F3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"
    ]
    node_colors = color_palette * (len(all_labels) // len(color_palette) + 1)
    
    max_val = data['value'].max()
    link_colors = [
        f'rgba(0, {128 + int(127 * (val / max_val))}, {255 - int(128 * (val / max_val))}, 0.5)'
        if val >= 300 else f'rgba(255, {int(99 * (val / max_val))}, 71, 0.4)'
        for val in data['value']
    ]

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=25,
            thickness=30,
            line=dict(color="black", width=0.8),
            label=all_labels,
            color=node_colors[:len(all_labels)]
        ),
        link=dict(
            source=data['source_index'],
            target=data['target_index'],
            value=data['value'],
            color=link_colors
        ))])

    fig.update_layout(
        title_text="<b>Budget Visualization for 2024-25</b>",
        title_font=dict(size=20, color='#2c3e50'),
        font=dict(size=14, color='#34495e'),
        paper_bgcolor='#ecf0f1',  
        margin=dict(l=50, r=50, t=80, b=50)
    )
    return fig

def load_data(file_path):
    return pd.read_csv(file_path)

def main():
    st.set_page_config(page_title="Budget Visualization", layout="wide")
    st.title("Budget Visualization")
    st.markdown(
    )

    st.sidebar.header("📊 Upload Your Budget Data")
    uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.write("### Uploaded Enhanced Budget Data")
        st.dataframe(data)

        fig = sankey(data)
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.write("### Default Enhanced Budget Data Visualization")
        data = load_data('budget_data.csv')
        st.dataframe(data)

        fig = sankey(data)
        st.plotly_chart(fig, use_container_width=True)

    st.sidebar.header("✏️ Adjust Data")
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

            fig = sankey(data)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.sidebar.error("Please enter valid data!")

if __name__ == "__main__":
    main()


