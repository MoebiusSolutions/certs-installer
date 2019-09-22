import os
from pathlib import Path
from OpenSSL import crypto  # will be a dependency that was ALREADY installed into the local venv via pip3.
import configparser

def print_profiles(profiles):
    print('')
    print('%-12s %-26s %-30s' % ("Program", "Profile Name", "ID"))
    print('--------------------------------------------------------------------')
    for profile in profiles:
        print('%-12s %-26s %-30s' % (profile["Program"], profile["Name"], profile["Path"]))
    print('')

def read_firefox_profiles():
	return _read_mozilla_profiles(Path.home()/'.mozilla/firefox', 'Firefox')

def read_thunderbird_profiles():
	return _read_mozilla_profiles(Path.home()/'.thunderbird', 'Thunderbird')

def import_certs(profile_dir, cert_files):
    print("Importing Certs into Mozilla Profile...")
    for cert_file in cert_files:
        with open(cert_file, 'rb') as f:
            cert_file_bytes = f.read()
        cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_file_bytes)
        cert_common_name = cert.get_subject().CN
        print('CERT: '+cert_common_name)
        # NOTE: certutil is a mozilla tool
        #subprocess.run(
        #    ["certutil", "-A", "-d", "sql:"+str(profile_dir), "-t", "CT,CT,CT", "-i", cert_file, "-n", cert_common_name],
        #    check=True)
    print("Importing Certs into Mozilla Profile...DONE.")

def _read_mozilla_profiles(prog_home_dir, prog_name):
    profiles_config = configparser.ConfigParser()
    profiles_config.read(prog_home_dir / 'profiles.ini')
    profiles = []
    # Parse config file
    for section in profiles_config.sections():
        if section.startswith("Profile"):
            section = profiles_config[section]
            profiles.append(section)
    # Identify absolute paths
    for profile in profiles:
        if profile['IsRelative'] == '1':
            profile['AbsoluteDir'] = str(prog_home_dir/'default')
        else:
            profile['AbsoluteDir'] = str(Path(profile['Path']))
    # Identify program
    for profile in profiles:
        profile['Program'] = prog_name
    return profiles
