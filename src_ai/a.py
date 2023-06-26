from git import Repo

def print_head_log_with_commits(repo_path):
    repo = Repo(repo_path)
    head = repo.head
    for entry in head.log():
        new_commit = repo.commit(entry.newhexsha)
        old_commit = repo.commit(entry.oldhexsha)
        print(f"RefLogEntry message: {entry.message}")
        print(f"New commit message: {new_commit.message}")
        print(f"Old commit message: {old_commit.message}")

if __name__ == "__main__":
    print_head_log_with_commits(".")


