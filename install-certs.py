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

# Install dependencies into local venv
print('Initializing python3-venv...')
subprocess.run(['pipenv', 'install'], check=True)
print('Initializing python3-venv...DONE.')

# Launch main script inside the venv
cmd_line = ['pipenv', 'run', 'python', 'install-certs-main.py']
cmd_line.extend(sys.argv[1:])
try:
    subprocess.run(cmd_line, check=True)
except subprocess.CalledProcessError as e:
    if e.returncode == 11:
        # Indicates that the subprocess already printed the error.
        exit(11)
    else:
        raise e
