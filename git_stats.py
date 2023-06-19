import argparse
import json
import pandas as pd
from git import Repo

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

    print(f"Added lines: {added_lines}")
    print(f"Deleted lines: {deleted_lines}")

# 根据文件后缀判断是前端还是后端
def infer_file_type(file_path):
    file_type = file_path.split(".")[-1].lower()
    if file_type in ["js", "ts", "vue", "html", "css", "scss", "less"]:
        return "Frontend"
    elif file_type in ["py", "java", "go", "c", "cpp", "h", "hpp", "rs"]:
        return "Backend"
    else:
        return "Other"

# 对提交信息进行归类
def infer_commit_type(commit_message):
    for keyword, commit_type in COMMIT_TYPES.items():
        if keyword in commit_message.lower():
            return commit_type
    return "Other"
    
# 收集git数据
def collect_git_data(repo_path):
    repo = Repo(repo_path)
    data = []

    for commit in repo.iter_commits():
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
        # 通过Head获取RefLogEntry信息归类操作类型
        do_type = commit.reflog_entry.message.split(":")[0]

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
            # 当前commit影响的分支
            

            dependencies = []
            if dev_type == "Frontend":
                if file.endswith(".vue"):
                    dependencies = [item.strip() for item in open(file).readlines() if item.strip().startswith("import")]
                elif file.endswith(".js"):
                    dependencies = [item.strip() for item in open(file).readlines() if item.strip().startswith("import")]
                elif file.endswith(".css"):
                    dependencies = [item.strip() for item in open(file).readlines() if item.strip().startswith("@import")]
            if dev_type == "Backend":
                if file.endswith(".py"):
                    dependencies = [item.strip() for item in open(file).readlines() if item.strip().startswith("from")]
                elif file.endswith(".java"):
                    dependencies = [item.strip() for item in open(file).readlines() if item.strip().startswith("import")]
                elif file.endswith(".go"):
                    dependencies = [item.strip() for item in open(file).readlines() if item.strip().startswith("import")]
                elif file.endswith(".c"):
                    dependencies = [item.strip() for item in open(file).readlines() if item.strip().startswith("#include")]
                elif file.endswith(".cpp"):
                    dependencies = [item.strip() for item in open(file).readlines() if item.strip().startswith("#include")]
                elif file.endswith(".h"):
                    dependencies = [item.strip() for item in open(file).readlines() if item.strip().startswith("#include")]
                elif file.endswith(".hpp"):
                    dependencies = [item.strip() for item in open(file).readlines() if item.strip().startswith("#include")]
                elif file.endswith(".rs"):
                    dependencies = [item.strip() for item in open(file).readlines() if item.strip().startswith("use")]
            data.append({
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
                "file_type": file.split(".")[-1].lower(), # 文件类型
                "dev_type": dev_type, # 开发类型
                "commit_count": commit_count,
                "commit_size": commit_size,
                "commit_stability": commit_stability,
                "commit_conflict": commit_conflict,
                "code_contribution": code_contribution,
                "affected_files": json.dumps(affected_files),
                "dependencies": json.dumps(dependencies), # 依赖
                "dependencies_count": len(dependencies), # 依赖数量
                "do_type": do_type, # 操作类型

            })
    return data

def save_to_csv(data, output_csv_path):
    df = pd.DataFrame(data)
    df.to_csv(output_csv_path, index=False)

def main():
    parser = argparse.ArgumentParser(description="Collect git data.")
    parser.add_argument("repository_path", help="Path to the git repository.")
    parser.add_argument("output_csv_path", help="Path to the output CSV file.")
    args = parser.parse_args()

    data = collect_git_data(args.repository_path)
    save_to_csv(data, args.output_csv_path)

if __name__ == "__main__":
    main()
