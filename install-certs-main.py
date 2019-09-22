#!venv/bin/python

from pathlib import Path
import moesol.dod_cert_utils as dod_cert_utils
import moesol.mozilla_utils as mozilla_utils

def prompt_for_response(prompt, response_mapping, default_response):
	while True:
		response = str(input(prompt)).lower().strip()
		if response == '':
			return response_mapping[default_response]
		if response in response_mapping:
			return response_mapping[response]

def read_config(mozilla_profiles):
	prompt = (
		'Install To:\n'
		'\n'
		'1. Both\n'
		'2. Linux System Store\n'
		'3. Firefox/Thunderbird\n'
		'\n'
		'Selection [1]? ')
	target_selection = prompt_for_response(prompt, {'1':['system','mozilla'], '2':['system'], '3':['mozilla'], }, '1')

	prompt = ''
	value_mapping = {}
	i = 1
	for profile in mozilla_profiles:
		prompt += ( '%s. %s - %s (%s)\n' % (i, profile['Program'], profile['Name'], profile['Path']) )
		value_mapping[str(i)] = profile
		i += 1
	prompt += '\n'
	prompt += 'Selection [1]? '
	mozilla_selection = None
	if ('mozilla' in target_selection):
		mozilla_selection = prompt_for_response(prompt, value_mapping, '1')

	return {
		'target_selection': target_selection,
		'mozilla_selection': mozilla_selection
	}

mozilla_profiles = []
mozilla_profiles.extend(mozilla_utils.read_firefox_profiles())
mozilla_profiles.extend(mozilla_utils.read_thunderbird_profiles())

config = read_config(mozilla_profiles)

dod_cert_utils.download_certs()
dod_cert_files = dod_cert_utils.get_cert_files()
if 'mozilla' in config['target_selection']:
	mozilla_utils.import_certs(Path(config['mozilla_selection']['AbsoluteDir']), dod_cert_files)

#print(print_mozilla_profiles())
#print(read_config())

#def action_list_all_mozilla_profiles(args):
#def action_load_dod_certs(args):
#def read_mozilla_profiles(prog_home_path, prog_name):
#def extract_dod_certs():
#def import_dod_certs():
#def download_dod_certs():
#def verify_apt_package_installed(package_name):
