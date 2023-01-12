#!venv/bin/python

import sys
import os
from pathlib import Path
import moesol.common_utils as common_utils
import moesol.dod_cert_utils as dod_cert_utils
import moesol.mozilla_utils as mozilla_utils

# The exit code used to indiate that this process
# failed, but that this script printed details of the error.
# This allows the caller to safely swallow and exit code
# exception.
HANDLED_EXCEPTION_EXIT = 11

def get_required_arg(args):
	if len(args) < 1:
		print_usage_and_exit()
	return args.pop(0)

def print_usage_and_exit():
	usage = (
		'\n'
		f'{sys.argv[0]} - Utilities for Importing DoD and Other Certs\n'
		'\n'
		'--list-mozilla\n'
		'\n'
		'	Lists the available Firefox/Thunderbird profiles by ID.\n'
		'\n'
		'--download-install-dod-ca-certs\n'
		'\n'
		'	Downloads the latest DoD CA certs and installs them\n'
		'	to the designated target. Requires a "--to-..." option.\n'
		'\n'
		'--install-ca-certs <dir-path> <file-pattern>\n'
		'\n'
		'	Installs CA certs in <dir-path> that match <file-pattern>\n'
		'	to the designated target. Requires a "--to-..." option.\n'
		'\n'
		'	<file-pattern> may contain "*" to indicate a multi-char wildcard.\n'
		'\n'
		'--to-mozilla <profile-id>\n'
		'\n'
		'	Targets the specific Firefox/Thunderbird profile for installation\n'
		'	of the selected certificates.\n'
		'\n'
		'--to-system\n'
		'\n'
		'	Targets the system (OS) trust store for installation\n'
		'	of the selected certificates.\n'
		'\n' )
	print(usage, file=sys.stderr)
	exit(HANDLED_EXCEPTION_EXIT)

def print_error_and_exit(message):
	print('\nERROR: %s\n' % message, file=sys.stderr)
	exit(HANDLED_EXCEPTION_EXIT)

def parse_args(argv):
	args = []
	args.extend(argv)
	config = {
		'do_list_mozilla': False,
		'do_install_dod_ca_certs': False,
		'do_install_ca_certs': False,
		'install_ca_certs': None,
		'to_mozilla': None,
		'to_system': False
	}
	# Parse args
	while True:
		if len(args) < 1:
			break
		arg = args.pop(0)
		if '--list-mozilla' == arg:
			config['do_list_mozilla'] = True
		elif '--download-install-dod-ca-certs' == arg:
			config['do_install_dod_ca_certs'] = True
		elif '--install-ca-certs' == arg:
			config['do_install_ca_certs'] = True
			config['install_ca_certs'] = {
				'dir': Path(get_required_arg(args)),
				'file_pattern': common_utils.simple_pattern_to_regex(get_required_arg(args)) }
		elif '--to-mozilla' == arg:
			config['to_mozilla'] = True
			config['mozilla_profile'] = get_required_arg(args)
		elif '--to-system' == arg:
			config['to_system'] = True
	# Verify some primary action is specified 
	if (not config['do_list_mozilla']) and \
		(not config['do_install_dod_ca_certs']) and \
		(not config['do_install_ca_certs']):
		print_usage_and_exit()
	# If installing CA certs, verify a target is specified 
	if (config['do_install_dod_ca_certs'] or config['do_install_ca_certs']) and \
		not (config['to_mozilla'] or config['to_system']):
		print_usage_and_exit()
	return config

config = parse_args(sys.argv)
mozilla_profiles = mozilla_utils.read_profiles()

ca_cert_files = []
if config['do_list_mozilla']:
	mozilla_utils.print_profiles(mozilla_profiles)
if config['do_install_dod_ca_certs']:
	dod_cert_utils.download_certs()
	ca_cert_files.extend(dod_cert_utils.get_cert_files())
if config['do_install_ca_certs']:
	filenames = os.listdir(config['install_ca_certs']['dir'])
	ca_cert_files.extend(
		# Map filenames to full paths
		map(
			lambda filename: Path(config['install_ca_certs']['dir'])/filename,
			# Filter filesname by regex match
			filter(
				lambda filename: config['install_ca_certs']['file_pattern'].match(filename),
				filenames)))
if (config['do_install_dod_ca_certs'] or config['do_install_ca_certs']) and config['to_mozilla']:
	if not config['mozilla_profile'] in mozilla_profiles:
		print_error_and_exit('Unrecognized Firefox/Thudnerbird profile [%s]' % config['mozilla_profile'])
	profile = mozilla_profiles[config['mozilla_profile']]
	mozilla_utils.import_ca_certs(Path(profile['AbsoluteDir']), ca_cert_files)

if (config['to_system']):
	print('''
ATTENTION: --to-system has not been implemented yet, but here are commands to do it manually...

Identify the bundle name that you recently downloaded with --download-install-dod-ca-certs:

    grep "_CURRENT_CA_BUNDLE =" moesol/dod_cert_utils.py

Using that bundle name (sans ".zip"), you should have the extracted certs here:

    ~/.moesol/dod-cert-cache/<bundle-name>/

... for example:

    ~/.moesol/dod-cert-cache/certificates_pkcs7_DoD_processed/

You can then install the certs to the OS with:

    # Ubuntu/Debian
    sudo cp ~/.moesol/dod-cert-cache/certificates_pkcs7_DoD_processed/DoD.*.crt \\
        /usr/local/share/ca-certificates/
    sudo update-ca-certificates

    # RedHat/CentOS
    sudo cp ~/.moesol/dod-cert-cache/certificates_pkcs7_DoD_processed/DoD.*.crt \\
        /etc/pki/ca-trust/source/anchors/
    update-ca-trust extract
''')

print('')
print('[SUCCESS]')
print('')
