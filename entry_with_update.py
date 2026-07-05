import os
import sys
import subprocess
import builtins
from datetime import datetime

_original_print = builtins.print
_at_line_start = True

def print_with_timestamp(*args, **kwargs):
    global _at_line_start
    ts = datetime.now().strftime("[%Y-%m-%d %H:%M:%S.%f]")[:-3]
    end = kwargs.get('end', '\n')
    
    if args:
        msg = " ".join(map(str, args))
        if _at_line_start:
            formatted_msg = f"{ts} {msg}"
        else:
            formatted_msg = msg
        if end.endswith('\n'):
            _at_line_start = True
        else:
            _at_line_start = False
        _original_print(formatted_msg, **kwargs)
    else:
        if _at_line_start:
            _original_print(f"{ts}", **kwargs)
        else:
            _original_print("", **kwargs)
        if end.endswith('\n'):
            _at_line_start = True
        else:
            _at_line_start = False

builtins.print = print_with_timestamp

# Programmatically remove cupy on Google Colab to avoid the NumPy C-API incompatibility crash
if os.path.exists('/content'):
    print("Google Colab detected. Programmatically uninstalling conflicting cupy package...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "uninstall", "-y", "cupy-cuda12x", "cupy-cuda11x", "cupy-cuda13x", "cupy"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("Conflicting cupy package uninstalled successfully.")
    except Exception as e:
        print(f"Failed to uninstall cupy: {e}")

root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root)
os.chdir(root)


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
except Exception as e:
    print('Update failed.')
    print(str(e))

print('Update succeeded.')
from launch import *
