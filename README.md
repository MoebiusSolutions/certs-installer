Certificates Installer
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

**NOTE**: We've added the centralized files for Chrome/Chromium the `--to-mozilla` option.
This is a bit of a temporary kluge. In the future we should replace this with a dedicated `--to-chrome` option.

List Firefox/Thunderbird (and Chrome) profiles:

	./install-certs.py --list-mozilla

	Program      	Profile Name               			ID
	--------------------------------------------------------------------
	Firefox      	default                    			uc5tmpul.default
	Thunderbird  	default                    			0aauf7kx.default
	Thunderbird  	MyProfile                  			9sk6jas1.MyProfile
	Chrome          ~/.pki/nssdb                        .pki/nssdb
	Chromium Snap   ~/snap/chromium/current/.pki/nssdb  snap/chromium/current/.pki/nssdb

Install DoD CAs to Firefox/Thunderbird profile and the OS system store:

	# To Thunderbird profile
	./install-certs.py --download-install-dod-ca-certs \
	  --to-system --to-mozilla 9sk6jas1.MyProfile

	# To centralized Chrome file
	./install-certs.py --download-install-dod-ca-certs \
	  --to-system --to-mozilla .pki/nssdb


Other Examples
----------------

Get program usage:

	./install-certs.py

Install DoD CAs to Firefox/Thunderbird profile:

	./install-certs.py --download-install-dod-ca-certs --to-mozilla 9sk6jas1.MyProfile

Install an arbitrary set of CA certs (that match `MyCA-*.crt`) to Firefox/Thunderbird profile:

	./install-certs.py --install-ca-certs ~/Downloads 'MyCA-*.crt' --to-mozilla 9sk6jas1.MyProfile

Install DoD CAs to the Linux system store:

	./install-certs.py --download-install-dod-ca-certs --to-system

Install an arbitrary set of CA certs (in `~/Downloads`, that match `MyCA-*.crt`)
to the Linux system store:

	./install-certs.py --install-ca-certs ~/Downloads 'MyCA-*.crt' --to-system

