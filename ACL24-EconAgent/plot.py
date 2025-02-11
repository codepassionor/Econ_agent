import numpy as np
import matplotlib.pyplot as plt
import pickle as pkl
import pandas as pd

with open('your_pkl_path', 'rb') as f:
    dense_log = pkl.load(f)

years = []
inflation_rates = []
unemployment_rates = []
nominal_gdp = []
nominal_gdp_growth = []
price_levels = []

base_price = 1.0
prev_year_gdp = None

for timestep, timestep_data in enumerate(dense_log['world']):
    if timestep % 12 == 0:
        year = timestep // 12
        years.append(year)
        
        current_price = timestep_data['Price']
        current_products = timestep_data['#Products']
        
        price_levels.append(current_price)
        
        if len(price_levels) >= 2:
            inflation_rate = (price_levels[-1] - price_levels[-2]) / price_levels[-2] * 100
        else:
            inflation_rate = 0
        inflation_rates.append(inflation_rate)
        
        unemployed = 0
        total_agents = 0
        for agent_id in range(len(dense_log['states'][timestep])):
            if agent_id == 100:
                break
            if agent_id == 'p':
                continue
            if dense_log['states'][timestep][f"{agent_id}"]['endogenous']['offer'] == '':
                unemployed += 1
            total_agents += 1
        unemployment_rate = unemployed / total_agents * 100 if total_agents != 0 else 0
        unemployment_rates.append(unemployment_rate)
        
        current_gdp = current_products * current_price
        nominal_gdp.append(current_gdp)
        
        if len(nominal_gdp) >= 2:
            gdp_growth = (nominal_gdp[-1] - nominal_gdp[-2]) / nominal_gdp[-2] * 100
        else:
            gdp_growth = 0
        nominal_gdp_growth.append(gdp_growth)

df = pd.DataFrame({
    "Year": years,
    "Price Level": price_levels,
    "Inflation Rate (%)": inflation_rates,
    "Unemployment Rate (%)": unemployment_rates,
    "Nominal GDP": nominal_gdp,
    "Nominal GDP Growth (%)": nominal_gdp_growth
})

df.to_csv("economic_data.csv", index=False, encoding="utf-8")

indicators = {
    'Price Level': 'Price Level',
    'Inflation Rate': 'Inflation Rate (%)',
    'Unemployment Rate': 'Unemployment Rate (%)',
    'Nominal GDP': 'Nominal GDP',
    'Nominal GDP Growth': 'Nominal GDP Growth (%)'
}

for title, column in indicators.items():
    plt.figure(figsize=(10, 6))
    plt.plot(df['Year'], df[column], marker='o', linestyle='-')
    
    plt.title(f'{title} Over Time')
    plt.xlabel('Year')
    plt.ylabel(title)
    plt.grid(True)

    filename = title.lower().replace(" ", "_")
    plt.savefig(f'{filename}.png', dpi=300, bbox_inches='tight')
    plt.savefig(f'{filename}.pdf', bbox_inches='tight')

    plt.close()
