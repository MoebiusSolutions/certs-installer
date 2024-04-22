import os
from pathlib import Path
from OpenSSL import crypto  # will be a dependency that was ALREADY installed into the local venv via pip3.
import configparser
import subprocess

_subprocess_provider = subprocess

def print_profiles(profiles):
    print('')
    print('%-16s %-40s %-30s' % ("Program", "Profile Name", "ID"))
    print('--------------------------------------------------------------------------------------')
    for profile_name in profiles:
        profile = profiles[profile_name]
        print('%-16s %-40s %-30s' % (profile["Program"], profile["Name"], profile["Path"]))
    print('')

def read_profiles():
    profiles = {}
    profiles.update(read_firefox_profiles())
    profiles.update(read_thunderbird_profiles())
    profiles.update(read_chrome_profiles())
    return profiles

def read_firefox_profiles():
    return _read_mozilla_profiles(Path.home()/'.mozilla/firefox', 'Firefox')

def read_thunderbird_profiles():
	return _read_mozilla_profiles(Path.home()/'.thunderbird', 'Thunderbird')

def import_ca_certs(profile_dir, cert_files):
    print("Importing CA Certs into Mozilla Profile...")
    for cert_file in cert_files:
        with open(cert_file, 'rb') as f:
            cert_file_bytes = f.read()
        cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_file_bytes)
        cert_common_name = cert.get_subject().CN
        print('CERT: '+cert_common_name)
        # NOTE: certutil is a mozilla tool
        _subprocess_provider.run(
            ["certutil", "-A", "-d", "sql:"+str(profile_dir), "-t", "CT,CT,CT", "-i", str(cert_file), "-n", cert_common_name],
            check=True)
    print("Importing CA Certs into Mozilla Profile...DONE.")

def _read_mozilla_profiles(prog_home_dir, prog_name):
    profiles_config = configparser.ConfigParser()
    profiles_config.read(prog_home_dir / 'profiles.ini')
    profiles = {}
    # Parse config file
    for section in profiles_config.sections():
        if section.startswith("Profile"):
            section = profiles_config[section]
            profiles[section['Path']] = section
    # Identify absolute paths
    for profile_name in profiles:
        profile = profiles[profile_name]
        if profile['IsRelative'] == '1':
            profile['AbsoluteDir'] = str(prog_home_dir/profile['Path'])
        else:
            profile['AbsoluteDir'] = str(Path(profile['Path']))
    # Identify program
    for profile_name in profiles:
        profile = profiles[profile_name]
        profile['Program'] = prog_name
    return profiles

# TODO: Add a top level --to-chrome option instead of hacking chrome into the mozilla profiles
def read_chrome_profiles():
    '''
    Returns hard coded paths for Chrome/Chromium that mirrors
    the structure returned for Mozilla profile dirs.
    '''
    profiles = {}
    profile = {
        'Path': '.pki/nssdb',
        'AbsoluteDir': str(Path.home()/'.pki/nssdb'),
        'Name': '~/.pki/nssdb',
        'Program': 'Chrome'
    }
    profiles[profile['Path']] = profile
    profile = {
        'Path': 'snap/chromium/current/.pki/nssdb',
        'AbsoluteDir': str(Path.home()/'snap/chromium/current/.pki/nssdb'),
        'Name': '~/snap/chromium/current/.pki/nssdb',
        'Program': 'Chromium Snap'
    }
    profiles[profile['Path']] = profile
    return profiles

# Used for unit testing
def _set_subprocess_provider(provider):
    _subprocess_provider = provider
