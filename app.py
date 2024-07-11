import networkx as nx
import matplotlib.pyplot as plt
import yfinance as yf
import gradio as gr

# List of venture-funded software companies
venture_funded_companies = {
    "Accel Partners": ["Meta", "Dropbox", "Spotify"],
    "Andreessen Horowitz": ["Airbnb", "Lyft", "Pinterest"],
    "GV (Google Ventures)": ["Uber", "LendingClub"],
    "Greylock Partners": ["Workday", "Palo Alto Networks"],
    "Lightspeed Venture Partners": ["Snap Inc.", "Grubhub", "AppDynamics"],
    "Benchmark": ["Snap Inc", "Uber", "WeWork"],
    "Norwest Venture Partners": ["LendingClub", "Opendoor"],
    "Emergence Capital Partners": ["Zoom Video Communications", "Box", "Salesforce"],
    "Trinity Ventures": ["New Relic", "Care.com", "TubeMogul"],
    "Citi Ventures": ["Square", "Nutanix"],
    "Sequoia Capital": ["Alphabet (Google)", "NVIDIA", "Dropbox", "Airbnb"],
    "Craft Ventures": ["Affirm", "Airbnb", "Eventbrite", "Meta", "Lyft", "Opendoor", "Palantir", "Reddit", "Uber"],
    "Y Combinator": ["Dropbox", "Airbnb", "Coinbase", "DoorDash", "Reddit", "Ginkgo Bioworks", "GitLab", "Instacart"]
}

# Map company names to their stock tickers (example, adjust as needed)
company_tickers = {
    "Meta": "META",
    "Dropbox": "DBX",
    "Spotify": "SPOT",
    "Airbnb": "ABNB",
    "Lyft": "LYFT",
    "Pinterest": "PINS",
    "Uber": "UBER",
    "LendingClub": "LC",
    "Workday": "WDAY",
    "Palo Alto Networks": "PANW",
    "Snap Inc.": "SNAP",
    "Grubhub": "GRUB",
    "AppDynamics": "", # No ticker, acquired by Cisco
    "WeWork": "WE",
    "Opendoor": "OPEN",
    "Zoom Video Communications": "ZM",
    "Box": "BOX",
    "Salesforce": "CRM",
    "New Relic": "NEWR",
    "Care.com": "CRCM",
    "TubeMogul": "", # No ticker, acquired by Adobe
    "Square": "SQ",
    "Nutanix": "NTNX",
    "Alphabet (Google)": "GOOGL",
    "NVIDIA": "NVDA",
    "Affirm": "AFRM",
    "Eventbrite": "EB",
    "Palantir": "PLTR",
    "Reddit": "", # No ticker, private
    "Coinbase": "COIN",
    "DoorDash": "DASH",
    "Ginkgo Bioworks": "DNA",
    "GitLab": "GTLB",
    "Instacart": "" # No ticker, private
}

# Function to get market cap from yfinance
def get_market_cap(ticker):
    if ticker:
        try:
            company = yf.Ticker(ticker)
            market_cap = company.info['marketCap']
            return market_cap
        except Exception as e:
            print(f"Error fetching market cap for {ticker}: {e}")
            return None
    return None

# Fetch market caps
company_market_caps = {company: get_market_cap(ticker) for company, ticker in company_tickers.items()}

# Visualization Function for Network Graph
def visualize_network():
    G = nx.Graph()
    
    # Define colors for categories
    category_colors = {
        "Accel Partners": "red",
        "Andreessen Horowitz": "blue",
        "GV (Google Ventures)": "green",
        "Greylock Partners": "purple",
        "Lightspeed Venture Partners": "orange",
        "Benchmark": "brown",
        "Norwest Venture Partners": "pink",
        "Emergence Capital Partners": "gray",
        "Trinity Ventures": "cyan",
        "Citi Ventures": "magenta",
        "Sequoia Capital": "yellow",
        "Craft Ventures": "lime",
        "Y Combinator": "teal",
    }
    
    # Add nodes to the graph
    for fund, companies in venture_funded_companies.items():
        for company in companies:
            market_cap = company_market_caps.get(company, 0)
            G.add_node(company, size=market_cap, category=fund)
    
    # Define edges (example: within each venture fund's portfolio)
    edges = []
    for fund, companies in venture_funded_companies.items():
        for i in range(len(companies)):
            for j in range(i + 1, len(companies)):
                edges.append((companies[i], companies[j]))
    
    G.add_edges_from(edges)
    
    # Get node sizes and colors
    sizes = [G.nodes[node]["size"] // 1e7 if G.nodes[node]["size"] else 100 for node in G.nodes]  # Scale size for visibility
    colors = [category_colors[G.nodes[node]["category"]] for node in G.nodes]
    
    # Plot the graph
    pos = nx.spring_layout(G, k=0.3)
    plt.figure(figsize=(15, 15))  # Increased plot size
    nx.draw(
        G,
        pos,
        node_size=sizes,
        node_color=colors,
        with_labels=True,
        font_size=10,
        alpha=0.7
    )
    plt.title("Network Graph of Venture Funded Software Companies")

    # Create legend
    for fund, color in category_colors.items():
        plt.scatter([], [], c=color, alpha=0.7, s=100, label=fund)
    plt.legend(scatterpoints=1, frameon=False, labelspacing=1, loc='upper left', fontsize='large')

    plt.show()
    return plt.gcf()

# Gradio App
def gradio_app():
    return visualize_network()

# Create the Gradio interface
interface = gr.Interface(
    fn=gradio_app,
    inputs=None,
    outputs="plot",
    live=False,
    title="Network Graph of Venture Funded Software Companies",
    description="Visualize the network graph of venture-funded software companies."
)

interface.launch()
