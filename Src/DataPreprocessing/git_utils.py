# -*- encoding = utf-8 -*-
"""
@description: Git instruction operation tool script
@date: 2023/12/20 8:44
@File : git_utils
@Software : PyCharm
"""

import subprocess
import os
import sys

# Print the modification history based on the file name
def logs(p, t, c):
    subprocess.Popen("git log --oneline --reverse *" + p + " > " + t,
                     cwd=os.path.dirname(c), shell=True, stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)


# Obtain the source file before refactoring based on the commit ID and file path
def show(i, p, t, c):
    subprocess.Popen("git show " + i + "^^:" + p + " > " + t,
                     cwd=os.path.dirname(c), shell=True,
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def logs2(p, t, c):
    subprocess.Popen("git log --oneline --reverse HEAD~" + p + " > " + t,
                     cwd=os.path.dirname(c), shell=True, stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)


# argv[0] is the path to the Python file being called
# argv[2]: Relative path of source files in project
# argv[3]: The path to save
# argv[4]: working directory
op = sys.argv[1]
path = sys.argv[2]
to = sys.argv[3]
cd = sys.argv[4]
if __name__ == "__main__":
    if op == "2":
        # argv[5]: commit id
        id = sys.argv[5]
        show(id, path, to, cd)
    elif op == "1":
        logs(path, to, cd)
    elif op == "3":
        logs2(path, to, cd)
