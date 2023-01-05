import os
from pathlib import Path
import shutil
import urllib.request
import zipfile
import re
import subprocess
import moesol.common_utils

_CURRENT_CA_BUNDLE = 'certificates_pkcs7_DoD.zip'
_CACHE_DIR = Path.home()/'.moesol/dod-cert-cache'
# Example: .../certificates_pkcs7_v5-6_dod_processed/
_PROCESSED_CERTS_DIR = _CACHE_DIR/(Path(_CURRENT_CA_BUNDLE).stem+'_processed')

def download_certs():
    url = f'https://dl.dod.cyber.mil/wp-content/uploads/pki-pke/zip/{_CURRENT_CA_BUNDLE}'
    # Example: .../certificates_pkcs7_v5-6_dod.zip
    zip_file = _CACHE_DIR/_CURRENT_CA_BUNDLE
    # Example: .../certificates_pkcs7_v5-6_dod/
    unzip_dir = _CACHE_DIR/Path(_CURRENT_CA_BUNDLE).stem

    _CACHE_DIR.mkdir(parents=True, exist_ok=True)

    temp_cert_bundle = '/tmp/DoD_certs/temp.cer'
    temp_cert_prefix = '/tmp/DoD_certs/temp-cert-'

    print('Downloading DoD certs...')
    print(f'[{url}]')
    urllib.request.urlretrieve(url, zip_file)
    print('Downloading DoD certs...DONE.')

    print('Unzipping DoD certs...')
    if unzip_dir.exists():
        shutil.rmtree(unzip_dir)
    unzip_dir.mkdir(parents=True)
    with zipfile.ZipFile(zip_file) as zip:
        zip.extractall(unzip_dir)
    print('Unzipping DoD certs...DONE.')

    cert_bundle_file = None
    for root, dirs, files in os.walk(unzip_dir):
        for c in files:
            if c.endswith('DoD.der.p7b'):
                cert_bundle_file = Path(root)/c
                break

    # TODO: Use import OpenSSL

    if not cert_bundle_file:
        raise f'Failed to find *DoD.der.p7b in the DoD bundle under [{unzip_dir}]'

    if _PROCESSED_CERTS_DIR.exists():
        shutil.rmtree(_PROCESSED_CERTS_DIR)
    _PROCESSED_CERTS_DIR.mkdir(parents=True)

#    i = 0
#    with open(cert_bundle_file, 'rb') as f:
#        cert_bundle_bytes = f.read()
#        cert_bundle = moesol.openssl_ext.get_certificates(OpenSSL.crypto.load_pkcs7_data(OpenSSL.crypto.FILETYPE_ASN1, cert_bundle_bytes))
#        for cert in cert_bundle:
#            print('A')
#            print(cert.get_subject())
#            cert_bytes = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
#            print('B')
#            if i != 2 and i != 3:
#                with open(_PROCESSED_CERTS_DIR/(f'{i}.pem'), 'wb') as pem:
#                    print('C')
#                    pem.write(cert_bytes)
#            print('D')
#            i += 1
#

    cert_bundle_pem_file = _PROCESSED_CERTS_DIR/'DoD.pem.p7b'

    # NOTE: We would have used pyopenssl to do this conversion, but pyopenssl doesn't currently support
    # PKCS7 files containing muliple certs.
    print('Converting DoD bundle to PEM...')
    subprocess.run(['openssl', 'pkcs7', '-print_certs', '-inform', 'DER', '-outform', 'PEM', '-in', str(cert_bundle_file), '-out', str(cert_bundle_pem_file)], check=True)
    print('Converting DoD bundle to PEM...DONE.')

    print('Splitting PEM DoD bundle...')
    with open(cert_bundle_pem_file, 'r') as f:
        cert_bundle_pem = f.read()
    cert_pems = moesol.common_utils.find_sections(cert_bundle_pem, re.compile('-----BEGIN CERTIFICATE-----'), re.compile('-----END CERTIFICATE-----'))
    i = 0
    for cert_pem in cert_pems:
        with open(_PROCESSED_CERTS_DIR/(f'DoD.{i}.pem.crt'), 'w') as cert_pem_file:
            cert_pem_file.write(cert_pem)
        i += 1
    print('Splitting PEM DoD bundle...DONE.')

def get_cert_files():
    cert_files = []
    for file in os.listdir(_PROCESSED_CERTS_DIR):
        if re.compile('DoD\\.\\d+\\.pem\\.crt').match(file):
            cert_files.append(_PROCESSED_CERTS_DIR/file)
    return cert_files


