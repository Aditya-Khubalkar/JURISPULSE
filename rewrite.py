import os
import subprocess

editor_script = """import sys
file = sys.argv[1]
with open(file, 'r') as f:
    lines = f.readlines()
with open(file, 'w') as f:
    for line in lines:
        if line.startswith('pick '):
            f.write(line.replace('pick ', 'edit '))
        else:
            f.write(line)
"""

with open("editor.py", "w") as f:
    f.write(editor_script)

env = os.environ.copy()
env['GIT_SEQUENCE_EDITOR'] = 'python editor.py'

print('Starting rebase...')
subprocess.run(['git', 'rebase', '-i', '--root'], env=env)

date_str = '2026-09-27T12:00:00+0530'
env_amend = os.environ.copy()
env_amend['GIT_COMMITTER_DATE'] = date_str

i = 0
while True:
    i += 1
    if not os.path.exists('.git/rebase-merge'):
        break
    
    res = subprocess.run(['git', 'commit', '--amend', '--no-edit', f'--date={date_str}'], env=env_amend, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode != 0:
        print('Amend failed, aborting...')
        subprocess.run(['git', 'rebase', '--abort'])
        break

    res = subprocess.run(['git', 'rebase', '--continue'], env=env_amend, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode != 0 and not os.path.exists('.git/rebase-merge'):
        break
    if res.returncode != 0:
        print('Rebase continue failed.')
        break

print(f'Done! Processed {i} commits.')
