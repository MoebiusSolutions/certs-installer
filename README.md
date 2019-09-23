Certifiate Installer
================

Overview
----------------

This is a small Python 3 script that can be used to download
and install DoD and other CA and Email x509 certificates to
various destinations, including Firefox, Thunderbird, and the
Linux trust store.


Compatibility
----------------

| OS | Support |
|-|-|
| Ubuntu 18 | Primary target |
| CentOS 7 | Trivial to support, but scripts not actively tested agains |
| Windows 10 | Not current supported due to `certutil` compatibility issues |


Example Usage
----------------

Get program usage:

	./install-certs.py

List Firefox/Thunderbird profiles:

	./install-certs.py --list-mozilla

Install DoD CAs to Firefox/Thunderbird profile:

	./install-certs.py --download-install-dod-ca-certs --to-mozilla 9sk6jas1.MyProfile

Install an arbitrary set of CA certs (that match `MyCA-*.crt`) to Firefox/Thunderbird profile:

	./install-certs.py --install-ca-certs ~/Downloads 'MyCA-*.crt' --to-mozilla 9sk6jas1.MyProfile

Install DoD CAs to the Linux system store:

	./install-certs.py --download-install-dod-ca-certs --to-system

Install an arbitrary set of CA certs (that match `MyCA-*.crt`) to Linux system store:

	./install-certs.py --install-ca-certs ~/Downloads 'MyCA-*.crt' --to-system

