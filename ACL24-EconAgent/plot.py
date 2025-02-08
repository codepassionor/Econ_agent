import numpy as np
import matplotlib.pyplot as plt
import pickle as pkl
import pandas as pd

with open('/Users/heyangfan/Desktop/ACL24-EconAgent/data/complex-0.1-0.1-1-0.1-0.05-100agents-240months/dense_log.pkl', 'rb') as f:
    dense_log = pkl.load(f)
# print(list(dense_log["states"]))
# dense_log_world = dense_log["states"][2]['2']['endogenous']['age']
# dense_log_world = dense_log["states"][2]['2']['endogenous']['Consumption Rate']


# # 假设 num_agents 是 Agent 的总数
# num_agents = 100  # 根据实际情况调整

# # ----------------------------------------------
# # 阶段1: 计算每个 Agent 的长期平均失业率
# # ----------------------------------------------
# # 初始化字典，存储每个 Agent 的失业时间步数和总时间步数
# agent_unemployment = {str(i): {"unemployed_steps": 0, "total_steps": 0} for i in range(num_agents)}

# # 遍历所有时间步
# for timestep in range(len(dense_log["states"])):
#     # 遍历所有 Agent
#     for i in range(num_agents):
#         agent_id = str(i)
#         # 检查当前时间步是否存在该 Agent
#         if agent_id in dense_log["states"][timestep]:
#             agent_data = dense_log["states"][timestep][agent_id]
#             # 统计失业状态（offer 为空字符串）
#             offer = agent_data['endogenous']['offer']
#             agent_unemployment[agent_id]["total_steps"] += 1
#             if offer == '':
#                 agent_unemployment[agent_id]["unemployed_steps"] += 1

# # 计算每个 Agent 的长期平均失业率
# agent_unemployment_rate = {}
# for agent_id in agent_unemployment:
#     total_steps = agent_unemployment[agent_id]["total_steps"]
#     if total_steps > 0:
#         rate = agent_unemployment[agent_id]["unemployed_steps"] / total_steps
#     else:
#         rate = 0  # 如果 Agent 从未出现，失业率设为 0
#     agent_unemployment_rate[agent_id] = rate

# # ----------------------------------------------
# # 阶段2: 根据长期失业率分组，并统计 consumption 的平均值
# # ----------------------------------------------
# low_unemployment_consumption = []  # 低失业率组（平均失业率 < 0.3）
# high_unemployment_consumption = []  # 高失业率组（平均失业率 > 0.7）

# # 再次遍历所有时间步和 Agent，收集 consumption 数据
# for timestep in range(len(dense_log["states"])):
#     for i in range(num_agents):
#         agent_id = str(i)
#         if agent_id in dense_log["states"][timestep]:
#             agent_data = dense_log["states"][timestep][agent_id]
#             consumption = agent_data['consumption']['consumption_rate']  # 假设 consumption 是 Coin 字段
#             rate = agent_unemployment_rate[agent_id]
            
#             # 根据长期失业率分组
#             if rate < 0.3:
#                 low_unemployment_consumption.append(consumption)
#             elif rate > 0.7:
#                 high_unemployment_consumption.append(consumption)

# # 计算平均值
# avg_low = sum(low_unemployment_consumption) / len(low_unemployment_consumption) if low_unemployment_consumption else 0
# avg_high = sum(high_unemployment_consumption) / len(high_unemployment_consumption) if high_unemployment_consumption else 0

# print(f"低失业率组（平均失业率 < 0.3）的 consumption 平均值: {avg_low}")
# print(f"高失业率组（平均失业率 > 0.7）的 consumption 平均值: {avg_high}")
    
# 假设 dense_log 已经被加载
# dense_log = ...

# 定义存储数据的列表
years = []
inflation_rates = []
unemployment_rates = []
nominal_gdp = []
nominal_gdp_growth = []
price_levels = []  # 存储价格水平

# 获取初始参数
base_price = 1.0  # 假设基期价格为1
prev_year_gdp = None

# 遍历数据，按时间步存储
for timestep, timestep_data in enumerate(dense_log['world']):
    # 假设每个时间步代表一个月，按年汇总
    if timestep % 12 == 0:
        year = timestep // 12 # 假设起始年份是2024
        years.append(year)
        
        # 获取当前时间步的数据
        current_price = timestep_data['Price']
        current_products = timestep_data['#Products']
        
        # 计算价格水平
        price_levels.append(current_price)
        
        # 通货膨胀率计算（同比）
        if len(price_levels) >= 2:
            inflation_rate = (price_levels[-1] - price_levels[-2]) / price_levels[-2] * 100
        else:
            inflation_rate = 0
        inflation_rates.append(inflation_rate)
        
        # 失业率计算
        unemployed = 0
        total_agents = 0
        for agent_id in range(len(dense_log['states'][timestep])):
            if agent_id == 100:
                break
            if agent_id == 'p':  # 跳过平台agent
                continue
            if dense_log['states'][timestep][f"{agent_id}"]['endogenous']['offer'] == '':  # 如果 offer 为空，表示失业
                unemployed += 1
            total_agents += 1
        unemployment_rate = unemployed / total_agents * 100 if total_agents != 0 else 0
        unemployment_rates.append(unemployment_rate)
        
        # 计算名义GDP（生产量 × 价格）
        current_gdp = current_products * current_price
        nominal_gdp.append(current_gdp)
        
        # GDP增长率计算（同比）
        if len(nominal_gdp) >= 2:
            gdp_growth = (nominal_gdp[-1] - nominal_gdp[-2]) / nominal_gdp[-2] * 100
        else:
            gdp_growth = 0
        nominal_gdp_growth.append(gdp_growth)

# 创建DataFrame
df = pd.DataFrame({
    "Year": years,
    "Price Level": price_levels,
    "Inflation Rate (%)": inflation_rates,
    "Unemployment Rate (%)": unemployment_rates,
    "Nominal GDP": nominal_gdp,
    "Nominal GDP Growth (%)": nominal_gdp_growth
})

df.to_csv("economic_data.csv", index=False, encoding="utf-8")

# 指标名称及对应的列
indicators = {
    'Price Level': 'Price Level',
    'Inflation Rate': 'Inflation Rate (%)',
    'Unemployment Rate': 'Unemployment Rate (%)',
    'Nominal GDP': 'Nominal GDP',
    'Nominal GDP Growth': 'Nominal GDP Growth (%)'
}

# 遍历每个指标，分别绘制并保存
for title, column in indicators.items():
    plt.figure(figsize=(10, 6))
    plt.plot(df['Year'], df[column], marker='o', linestyle='-')
    
    plt.title(f'{title} Over Time')
    plt.xlabel('Year')
    plt.ylabel(title)
    plt.grid(True)

    # 保存不同格式
    filename = title.lower().replace(" ", "_")  # 处理文件名
    plt.savefig(f'{filename}.png', dpi=300, bbox_inches='tight')
    plt.savefig(f'{filename}.pdf', bbox_inches='tight')

    plt.close()  # 关闭图像，防止内存占用
