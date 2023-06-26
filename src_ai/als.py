import pandas as pd

# 导入CSV文件
df = pd.read_csv('out.csv')

# 统计每个作者的提交次数
author_counts = df['author'].value_counts()

# 计算每次提交的文件影响
# 假设"files_changed"列包含每次提交修改的文件数
df['files_impact'] = df.groupby('commit_id')['affected_files'].transform('sum')

# 计算代码规模
# 假设'additions'和'deletions'列包含了代码的新增和删除行数
df['code_scale'] = df['commit_size']

# 分析提交类型
# 假设提交类型包含在'message'列中，并且可以通过关键词来识别
df['commit_type'] = df['commit_type']

# 输出结果
print("Author counts:\n", author_counts)
print("Files impact per commit:\n", df[['commit_id', 'files_impact']])
print("Code scale per commit:\n", df[['commit_id', 'code_scale']])
print("Commit type counts:\n", df['commit_type'].value_counts())
