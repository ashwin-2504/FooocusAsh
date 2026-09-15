import os
import sys
import subprocess


root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root)
os.chdir(root)


def update_repository():
    # Try using standard git CLI via subprocess first (works in Colab and all standard git environments)
    try:
        fetch_res = subprocess.run(["git", "fetch"], capture_output=True, text=True, check=False)
        if fetch_res.returncode == 0:
            pull_res = subprocess.run(["git", "pull", "--ff-only"], capture_output=True, text=True, check=False)
            if pull_res.returncode == 0:
                stdout_str = pull_res.stdout.strip()
                if "Already up to date" in stdout_str or "Already up-to-date" in stdout_str:
                    print("Already up-to-date")
                else:
                    print("Fast-forward merge")
                return True
            else:
                print("Update failed - Did you modify any file?")
                print(pull_res.stderr or pull_res.stdout)
                return False
    except Exception as git_cli_err:
        print(f"Git CLI update skipped/failed: {git_cli_err}")

    # Fallback to pygit2 if available
    try:
        import pygit2
        pygit2.option(pygit2.GIT_OPT_SET_OWNER_VALIDATION, 0)

        repo = pygit2.Repository(os.path.abspath(os.path.dirname(__file__)))
        branch_name = repo.head.shorthand
        remote_name = 'origin'
        remote = repo.remotes[remote_name]

        remote.fetch()

        local_branch_ref = f'refs/heads/{branch_name}'
        local_branch = repo.lookup_reference(local_branch_ref)

        remote_reference = f'refs/remotes/{remote_name}/{branch_name}'
        remote_commit = repo.revparse_single(remote_reference)

        merge_result, _ = repo.merge_analysis(remote_commit.id)

        if merge_result & pygit2.GIT_MERGE_ANALYSIS_UP_TO_DATE:
            print("Already up-to-date")
        elif merge_result & pygit2.GIT_MERGE_ANALYSIS_FASTFORWARD:
            local_branch.set_target(remote_commit.id)
            repo.head.set_target(remote_commit.id)
            repo.checkout_tree(repo.get(remote_commit.id))
            repo.reset(local_branch.target, pygit2.GIT_RESET_HARD)
            print("Fast-forward merge")
        elif merge_result & pygit2.GIT_MERGE_ANALYSIS_NORMAL:
            print("Update failed - Did you modify any file?")
        return True
    except Exception as e:
        print('Update failed.')
        print(str(e))
        return False


update_repository()
print('Update process completed.')
from launch import *

