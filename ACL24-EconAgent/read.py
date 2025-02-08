import pickle

# 打开并读取 pkl 文件
with open('/Users/heyangfan/Desktop/ACL24-EconAgent/data/gpt-3-full-100agents-240months/dialog4ref_36.pkl', 'rb') as f:
    data = pickle.load(f)

# 打印出文件中的内容
print(data)
