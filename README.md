# :unicorn: [venture-unicorns](https://leoncensh-networkx-saas.hf.space/) 

## Analysis of VC-backed unicorns using CB Insights data of 09-21-2024
This is a repo for visualizing and analyzing CB Insights data, focusing on **network relationships and valuations**. It combines data processing, graph construction, and interactive visualizations using libraries **pandas, networkx, plotly, and gradio**.

### Features
- **Data Preprocessing:** Automatically cleans and standardizes column names and filters specific entries 
- **Interactive Graph Visualization:** Use **networkx** and **plotly** to create interactive network graphs of relationships within the dataset.
- **Web Interface:** A gradio-based UI allows users to explore data and visualizations interactively.

**Figure 1. Y Combinator** 

![image](https://github.com/user-attachments/assets/728df22f-db7d-4fda-83e1-56a04fbd02af)

**Figure 2. Healthcare Unicorns between 5 and 10 Billion**

![image](https://github.com/user-attachments/assets/e5a79d25-ad27-40ae-ad55-f3b76415fc0a)

**Figure 3. [Greylock](https://jobs.greylock.com/jobs?stages=10-100+employees&stages=100-1000+employees&stages=1000%2B+employees&locations=United+States&skills=SQL) and M12 Ventures unicorns**

![image](https://github.com/user-attachments/assets/fb0eb2d5-f7f8-4106-a59c-f934f2aa2646)

##### **Note:** All companies are in green. Venture firms have different colors. The company circle varies proportionately to the **private valuation**. 

### Clone this Repository

```bash
git clone https://github.com/LNshuti/saas-winners.git
```

### Setup your Environment
```bash
conda env create --file=environment.yaml
```

### Activate your Environment
```bash
conda activate saas-winers
```

### Install Dependencies
```bash 
pip install -r requirements.txt
```

### Run the **app** 
```bash
python app.py
```
**If you found the app useful, please make sure to give us a star!**

![image](https://github.com/user-attachments/assets/9259c9c9-2930-4071-b9d5-780e6ffe3d40)
