import re
import logging
import pandas as pd
import plotly.graph_objects as go
import networkx as nx
import gradio as gr

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load and preprocess the dataset
file_path = "cbinsights_data.csv"  

try:
    data = pd.read_csv(file_path, skiprows=1)
    logger.info("CSV file loaded successfully.")
except FileNotFoundError:
    logger.error(f"File not found: {file_path}")
    raise
except Exception as e:
    logger.error(f"Error loading CSV file: {e}")
    raise

# Standardize column names
data.columns = data.columns.str.strip().str.lower()
logger.info(f"Standardized Column Names: {data.columns.tolist()}")

# Filter out Health since Healthcare is the correct Market Segment
data = data[data.industry != 'Health']

# Identify the valuation column
valuation_columns = [col for col in data.columns if 'valuation' in col.lower()]
if len(valuation_columns) != 1:
    logger.error("Unable to identify a single valuation column.")
    raise ValueError("Dataset must contain one column with 'valuation' name.")

valuation_column = valuation_columns[0]
logger.info(f"Using valuation column: {valuation_column}")

# Clean and prepare data
data["Valuation_Billions"] = data[valuation_column].replace({'\$': '', ',': ''}, regex=True)
data["Valuation_Billions"] = pd.to_numeric(data["Valuation_Billions"], errors='coerce')
data = data.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
data.rename(columns={
    "company": "Company",
    "date_joined": "Date_Joined",
    "country": "Country",
    "city": "City",
    "industry": "Industry",
    "select_investors": "Select_Investors"
}, inplace=True)

logger.info("Data cleaned and columns renamed.")

# Build investor-company mapping
def build_investor_company_mapping(df):
    mapping = {}
    for _, row in df.iterrows():
        company = row["Company"]
        investors = row["Select_Investors"]
        if pd.notnull(investors):
            for investor in investors.split(","):
                investor = investor.strip()
                if investor:
                    mapping.setdefault(investor, []).append(company)
    return mapping

investor_company_mapping = build_investor_company_mapping(data)
logger.info("Investor to company mapping created.")

# Filter by country, industry, investor selection, and company
def filter_investors(selected_country, selected_industry,
                     selected_investors, selected_company,
                     exclude_countries, exclude_industries,
                     exclude_companies, exclude_investors):
    filtered_data = data.copy()

    # Inclusion filters
    if selected_country != "All":
        filtered_data = filtered_data[filtered_data["Country"] == selected_country]
    if selected_industry != "All":
        filtered_data = filtered_data[filtered_data["Industry"] == selected_industry]
    if selected_company != "All":
        filtered_data = filtered_data[filtered_data["Company"] == selected_company]
    if selected_investors:
        pattern = '|'.join([re.escape(inv) for inv in selected_investors])
        filtered_data = filtered_data[filtered_data["Select_Investors"].str.contains(pattern,
                                                                                     na=False)]

    # Exclusion filters
    if exclude_countries:
        filtered_data = filtered_data[~filtered_data["Country"].isin(exclude_countries)]
    if exclude_industries:
        filtered_data = filtered_data[~filtered_data["Industry"].isin(exclude_industries)]
    if exclude_companies:
        filtered_data = filtered_data[~filtered_data["Company"].isin(exclude_companies)]
    if exclude_investors:
        pattern = '|'.join([re.escape(inv) for inv in exclude_investors])
        filtered_data = filtered_data[~filtered_data["Select_Investors"].str.contains(pattern, 
                                                                                      na=False)]

    investor_company_mapping_filtered = build_investor_company_mapping(filtered_data)
    filtered_investors = list(investor_company_mapping_filtered.keys())
    return filtered_investors, filtered_data

# Generate Plotly graph
def generate_graph(investors, filtered_data):
    if not investors:
        logger.warning("No investors selected.")
        return go.Figure()

    # Create a color map for investors
    unique_investors = investors
    num_colors = len(unique_investors)
    color_palette = [
        "#377eb8", "#e41a1c", "#4daf4a", "#984ea3",
        "#ff7f00", "#ffff33", "#a65628", "#f781bf", "#999999"
    ]
    while num_colors > len(color_palette):
        color_palette.extend(color_palette)

    investor_color_map = {investor: color_palette[i] for i, investor in enumerate(unique_investors)}

    G = nx.Graph()
    for investor in investors:
        companies = filtered_data[filtered_data["Select_Investors"].str.contains(re.escape(investor), na=False)]["Company"].tolist()
        for company in companies:
            G.add_node(company)
            G.add_node(investor)
            G.add_edge(investor, company)

    pos = nx.spring_layout(G, seed=42)
    edge_x, edge_y = [], []

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color='#aaaaaa'),
        hoverinfo='none',
        mode='lines'
    )

    node_x, node_y, node_text, node_textposition = [], [], [], []
    node_color, node_size, node_hovertext = [], [], []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        if node in investors:
            node_text.append(node)  # Add investor labels
            node_color.append(investor_color_map[node])
            node_size.append(30)
            node_hovertext.append(f"Investor: {node}")
            node_textposition.append('top center')
        else:
            valuation = filtered_data.loc[filtered_data["Company"] == node, "Valuation_Billions"].values
            industry = filtered_data.loc[filtered_data["Company"] == node, "Industry"].values
            size = valuation[0] * 5 if len(valuation) > 0 and not pd.isnull(valuation[0]) else 15
            node_size.append(max(size, 10))
            node_color.append("#a6d854")
            hovertext = f"Company: {node}"
            if len(industry) > 0 and not pd.isnull(industry[0]):
                hovertext += f"<br>Industry: {industry[0]}"
            if len(valuation) > 0 and not pd.isnull(valuation[0]):
                hovertext += f"<br>Valuation: ${valuation[0]:.2f}B"
            node_hovertext.append(hovertext)
            if len(filtered_data) < 15 or node in filtered_data.nlargest(5, "Valuation_Billions")["Company"].tolist():
                node_text.append(node)  # Add company labels
                node_textposition.append('bottom center')
            else:
                node_text.append("")  # Hide company labels
                node_textposition.append('bottom center')

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        text=node_text,
        textposition=node_textposition,
        mode='markers+text',
        hoverinfo='text',
        hovertext=node_hovertext,
        textfont=dict(size=10),  # Adjust label font size
        marker=dict(
            showscale=False,
            size=node_size,
            color=node_color,
            line=dict(width=0.5, color='#333333')
        )
    )

    # Compute total market cap
    total_market_cap = filtered_data["Valuation_Billions"].sum()

    fig = go.Figure(data=[edge_trace, node_trace])

    fig.update_layout(
        title="",
        titlefont_size=24,
        margin=dict(l=20, r=20, t=60, b=20),
        hovermode='closest',
        width=1200,
        height=800,
        autosize=True,
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        showlegend=False,  # Hide the legend to maximize space
        annotations=[
            dict(
                x=0.5, y=1.1, xref='paper', yref='paper',
                text=f"Total Market Cap of Companies: ${total_market_cap:.2f}B",
                showarrow=False, font=dict(size=14), xanchor='center'
            )
        ]
    )

    return fig

# Gradio app
def app(selected_country, selected_industry, selected_company, selected_investors,
        exclude_countries, exclude_industries, exclude_companies, exclude_investors):
    investors, filtered_data = filter_investors(
        selected_country, selected_industry, selected_investors, selected_company,
        exclude_countries, exclude_industries, exclude_companies, exclude_investors
    )
    if not investors:
        return go.Figure()
    graph = generate_graph(investors, filtered_data)
    return graph

def main():
    country_list = ["All"] + sorted(data["Country"].dropna().unique())
    industry_list = ["All"] + sorted(data["Industry"].dropna().unique())
    company_list = ["All"] + sorted(data["Company"].dropna().unique())
    investor_list = sorted(investor_company_mapping.keys())

    with gr.Blocks(title="Venture Networks Visualization") as demo:
        gr.Markdown("# Venture Networks Visualization")
        with gr.Row():
            country_filter = gr.Dropdown(choices=country_list, label="Country", value="All")
            industry_filter = gr.Dropdown(choices=industry_list, label="Industry", value="All")
            company_filter = gr.Dropdown(choices=company_list, label="Company", value="All")
            investor_filter = gr.Dropdown(choices=investor_list, label="Select Investors", value=[], multiselect=True)
        with gr.Row():
            exclude_country_filter = gr.Dropdown(choices=country_list[1:], label="Exclude Country", value=[], multiselect=True)
            exclude_industry_filter = gr.Dropdown(choices=industry_list[1:], label="Exclude Industry", value=[], multiselect=True)
            exclude_company_filter = gr.Dropdown(choices=company_list[1:], label="Exclude Company", value=[], multiselect=True)
            exclude_investor_filter = gr.Dropdown(choices=investor_list, label="Exclude Investors", value=[], multiselect=True)
        graph_output = gr.Plot(label="Network Graph")

        inputs = [country_filter, industry_filter, company_filter, investor_filter,
                  exclude_country_filter, exclude_industry_filter, exclude_company_filter, exclude_investor_filter]
        outputs = [graph_output]

        # Set up event triggers for all inputs
        for input_control in inputs:
            input_control.change(app, inputs, outputs)

        gr.Markdown("**Instructions:** Use the dropdowns to filter the network graph. You can include or exclude specific countries, industries, companies, or investors.")

    demo.launch()

if __name__ == "__main__":
    main()
