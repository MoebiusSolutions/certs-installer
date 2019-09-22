#!/usr/bin/env python3

# ----------------
# This script wraps install-certs-main.sh by first loading a python virtual environment,
# then launching install-certs-main.sh from that environment. This allows the packages
# of this module to be isolated from system packages.
# ----------------

import sys
import subprocess

def _is_package_installed(package_name):
    result = subprocess.run(['dpkg', '-s', package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        return True
    stdout = result.stdout.decode('utf-8')
    stderr = result.stderr.decode('utf-8')
    if 'not installed' in stderr:
        return False
    else:
        print(stdout)
        print(stderr, file=sys.stderr)
        raise('Failed to verify %s was installed' % package_name)

if not _is_package_installed('python3-venv'):
    print('Attempting to install python3-venv...')
    subprocess.run(['sudo', 'apt', '-y', 'install', 'python3-venv'], check=True)
    print('Attempting to install python3-venv...DONE.')

print('Initializing python3-venv...')
# Creates a Virtual Environment containing Python3 and Pip3
subprocess.run(['python3', '-m', 'venv', 'venv'], check=True)
# Install dependencies into local venv
subprocess.run(['venv/bin/pip', 'install', '-r', 'pip-requirements.txt'], check=True)
print('Initializing python3-venv...DONE.')

# Launch main script inside the venv
cmd_line = ['venv/bin/python3', 'install-certs-main.py']
cmd_line.extend(sys.argv[1:])
subprocess.run(cmd_line, check=True)