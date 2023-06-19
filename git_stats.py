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
        commit_message = commit.message.strip().replace("\n", " ")
        commit_time = commit.committed_datetime
        author = commit.author.name
        commit_type = infer_commit_type(commit_message)
        affected_files = [item.a_path for item in commit.diff(None)]
        commit_conflict = "conflict" in commit_message.lower()

        for file, file_stats in commit.stats.files.items():
            commit_count = 1
            commit_size = file_stats["lines"]
            commit_stability = len(repo.git.log("--oneline", "--follow", "--", file).splitlines())
            try:
                code_contribution = repo.git.blame("--line-porcelain", file).count(f"author {author}")
            except Exception as e:
                print(f"Error processing file {file}: {e}")
                code_contribution = 0
            data.append({
                "commit_id": commit_id,
                "commit_time": commit_time,
                "commit_message": commit_message,
                "commit_type": commit_type,
                "author": author,
                "file": file,
                "commit_count": commit_count,
                "commit_size": commit_size,
                "commit_stability": commit_stability,
                "commit_conflict": commit_conflict,
                "code_contribution": code_contribution,
                "affected_files": json.dumps(affected_files),
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
