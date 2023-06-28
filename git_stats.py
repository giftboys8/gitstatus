import argparse
import json
import pandas as pd
from git import Repo
from datetime import datetime
import os

class Collector:
    def __init__(self):
        self.data = []
        self.coroutine = self._collector()
        next(self.coroutine)  # 需要先调用next()来启动协程

    def _collector(self):
        while True:
            x = yield  # 用作表达式的yield可以接收send()方法发送的值
            self.data.append(x)

    def send(self, x):
        self.coroutine.send(x)

    def get_data(self):
        return self.data

# 代码提交类型
COMMIT_TYPES = {
    "feature": "Feature",
    "fix": "Bugfix",
    "bug": "Bugfix",
    "refactor": "Refactor",
}

# 统计代码行数
def count_code_lines(repo_path, start_commit_sha, end_commit_sha):
    repo = Repo(repo_path)
    start_commit = repo.commit(start_commit_sha)
    end_commit = repo.commit(end_commit_sha)

    diff_index = start_commit.diff(end_commit)
    added_lines = 0
    deleted_lines = 0

    for diff in diff_index.iter_change_type('M'):
        added_lines += diff.diff.count('\n+')
        deleted_lines += diff.diff.count('\n-')

# 根据文件后缀判断是前端还是后端
def infer_file_type(file_path) -> str:
    file_type = file_path.split(".")[-1].lower()
    if file_type in ["js", "ts", "vue", "html", "css", "scss", "less"]:
        return "Frontend"
    elif file_type in ["py", "java", "go", "c", "cpp", "h", "hpp", "rs"]:
        return "Backend"
    else:
        return "Other"
    
# 通过file字段的内容来确认文件类别（包含:config/conf为[配置文件]，test为[测试文件]，svg/png为[资源文件]，其他为[其他文件]）
def infer_file_category(file_path) -> str:
    file_category = file_path.lower()
    if file_category in ["config", "conf"]:
        return "Config"
    elif file_category in ["test"]:
        return "Test"
    elif file_category in [".svg", ".png"]:
        return "Resource"
    elif file_category in [".md"]:
        return "Document"
    elif file_category in ["util", "utils"]:
        return "Util"
    elif file_category in ["service", "services"]:
        return "Interface"
    elif file_category in ["impl", "impls"]:
        return "Impl"
    elif file_category in ["page"]:
        return "Page"
    elif file_category in ["component", "components"]:
        return "Component"
    else:
        return "Other"

# 对提交信息进行归类
def infer_commit_type(commit_message):
    for keyword, commit_type in COMMIT_TYPES.items():
        if keyword in commit_message.lower():
            return commit_type
    return "Other"


# 获取提交信息    
def get_commits(repo):
    for commit in repo.iter_commits():
        yield commit

def collect_git_data(repo_path):
    repo = Repo(repo_path)
    commits_in_range = get_commits(repo)

    # data = []

    for commit in commits_in_range:
        commit_id = commit.hexsha
        branches = [item.name for item in repo.branches if commit_id in item.commit.hexsha]
        commit_message = commit.message.strip().replace("\n", " ")
        commit_time = commit.committed_datetime
        commit_weekday = commit_time.weekday()
        commit_hour = commit_time.hour
        commit_month = commit_time.month
        commit_day = commit_time.day
        author = commit.author.name
        commit_type = infer_commit_type(commit_message)
        affected_files = [item.a_path for item in commit.diff(None)]
        commit_conflict = len(commit.parents) > 1 or "conflict" in commit_message.lower()
        c = Collector()  # 创建协程

        for file, file_stats in commit.stats.files.items():
            commit_count = 1
            commit_size = file_stats["lines"]
            commit_stability = len(repo.git.log("--oneline", "--follow", "--", file).splitlines())
            try:
                code_contribution = repo.git.blame("--line-porcelain", file).count(f"author {author}")
            except Exception as e:
                print(f"Error processing file {file}: {e}")
                code_contribution = 0
            dev_type = infer_file_type(file)
            file_category = infer_file_category(file)
            
            # 发送数据给协程
            c.send(
                {
                  "branches": json.dumps(branches),
                  "commit_id": commit_id,
                  "commit_time": commit_time,
                  "commit_weekday": commit_weekday,
                  "commit_hour": commit_hour,
                  "commit_month": commit_month,
                  "commit_day": commit_day,
                  "commit_message": commit_message,
                  "commit_type": commit_type,
                  "author": author,
                  "file": file,
                  "file_type": file.split(".")[-1].lower().strip('"'),
                  "dev_type": dev_type, # 开发类型
                  "commit_count": commit_count,
                  "commit_size": commit_size,
                  "commit_stability": commit_stability,
                  "commit_conflict": commit_conflict,
                  "code_contribution": code_contribution,
                  "affected_files": json.dumps(affected_files),
                  "file_category": file_category, # 文件类别
                  # "dependencies": json.dumps(dependencies), # 依赖
                  # "dependencies_count": len(dependencies), # 依赖数量
                }
            )  

    return c.get_data()

def save_to_csv(data, output_csv_path):
    df = pd.DataFrame(data)
    df.to_csv(output_csv_path, index=False)

def main():
    parser = argparse.ArgumentParser(description="Collect git data.")
    parser.add_argument("repository_path", help="Path to the git repository.")
    args = parser.parse_args()
    repr_name = args.repository_path.split(os.sep)[-1]

    # 系统目录分隔符
    output_csv_path = f"{repr_name}_git_data.csv"
    data = collect_git_data(args.repository_path)

    # 创建文件夹
    folder_name = repr_name
    if not os.path.exists(folder_name): 
        os.makedirs(folder_name, exist_ok=True)

    save_to_csv(data, f"{folder_name}{os.sep}{output_csv_path}")

if __name__ == "__main__":
    main()



