## To install this RPM, you will need to have a thunar-dropbox package: https://syrkit.bromosapien.net/syndra/
## To build this rpm, you will need to have my custom tar ball: https://syrkit.bromosapien.net/syndra
## This tarball contains certain icons and modifications from dropbox's official tar
## This is updated routinely, typically once every month to two months

%define dbdir /opt/dropbox
%global __os_install_post %{nil}

Name:		dropbox-xfce
Version:	3.10.7
#Release:	2%{?dist}
Release:	2
Summary:	Dropbox for the XFCE Environment
BuildArch:	x86_64

Group:		Applications/Internet
License:	GPL
URL:		http://www.dropbox.com
Source0:	%{name}-%{version}.tgz

%{expand: %%define _sourcedir %{_sourcedir}/%{name}}

# Requirements for dropbox and servicemenu together
Requires:	Thunar
Requires:	thunar-dropbox
Requires:	perl
Requires:	recode
Requires:	sqlite
Requires:	xdg-utils

# Need to prevent rpmbuild from trying to add unnecessary requirements
AutoReqProv: no

%description
Dropbox is a solution for holding documents, pictures that wish to be saved in a remote location and be accessible across all machines connected to it. 

This package provides:
 * Dropbox

%prep
%setup -q -n dropbox-xfce-%{version}

%build

%install
rm -rf %{buildroot}
# Basic Folder Structure
%{__mkdir} -p %{buildroot}%{dbdir}
#%{__mkdir} -p %{buildroot}%{_datadir}/icons/hicolor/{16x16,22x22,24x24,32x32,48x48,64x64,256x256}/apps
%{__mkdir} -p %{buildroot}%{_datadir}/applications
%{__mkdir} -p %{buildroot}%{_datadir}/dropbox
%{__mkdir} -p %{buildroot}%{_datadir}/man/man1
%{__mkdir} -p %{buildroot}%{_bindir}

# Basic deployment
cp -R * %{buildroot}/%{dbdir}
mv %{buildroot}/%{dbdir}/dropbox.1.gz %{buildroot}%{_datadir}/man/
mv %{buildroot}/%{dbdir}/dropbox.desktop %{buildroot}%{_datadir}/applications/dropbox.desktop
mv %{buildroot}/%{dbdir}/dropboxd %{buildroot}%{_bindir}/dropbox
mv %{buildroot}/%{dbdir}/icons %{buildroot}%{_datadir}/icons

## Need to act like gnome sort of
ln -s %{_datadir}/dropbox %{buildroot}%{_datadir}/nautilus-dropbox

## Let's create some links to the images
## This is because dropbox acts weird when they're not in both places
ln -s %{dbdir}/images/emblems/emblem-dropbox-syncing.icon %{buildroot}%{_datadir}/dropbox/emblem-dropbox-syncing.icon
ln -s %{dbdir}/images/emblems/emblem-dropbox-syncing.png %{buildroot}%{_datadir}/dropbox/emblem-dropbox-syncing.png
ln -s %{dbdir}/images/emblems/emblem-dropbox-unsyncable.icon %{buildroot}%{_datadir}/dropbox/emblem-dropbox-unsyncable.icon
ln -s %{dbdir}/images/emblems/emblem-dropbox-unsyncable.png %{buildroot}%{_datadir}/dropbox/emblem-dropbox-unsyncable.png
ln -s %{dbdir}/images/emblems/emblem-dropbox-uptodate.icon %{buildroot}%{_datadir}/dropbox/emblem-dropbox-uptodate.icon
ln -s %{dbdir}/images/emblems/emblem-dropbox-uptodate.png %{buildroot}%{_datadir}/dropbox/emblem-dropbox-uptodate.png
ln -s %{dbdir}/images/emblems/emblem-dropbox-selsync.icon %{buildroot}%{_datadir}/dropbox/emblem-dropbox-selsync.icon
ln -s %{dbdir}/images/emblems/emblem-dropbox-selsync.png %{buildroot}%{_datadir}/dropbox/emblem-dropbox-selsync.png
ln -s %{dbdir}/images/emblems/emblem-dropbox-app.icon %{buildroot}%{_datadir}/dropbox/emblem-dropbox-app.icon
ln -s %{dbdir}/images/emblems/emblem-dropbox-app.svg %{buildroot}%{_datadir}/dropbox/emblem-dropbox-app.svg

%post

%files
%doc VERSION README ACKNOWLEDGEMENTS LICENSE
# Dropbox
%{dbdir}/*
%{_bindir}/*
%{_datadir}/*

%changelog
* Tue Oct 06 2015 Louis Abel <tucklesepk@gmail.com> - 3.10.8-2
- Version jump to 3.10.7

* Fri Sep 11 2015 Louis Abel <tucklesepk@gmail.com> - 3.8.8-2
- Version jump to 3.8.8
- RPM restructure effort
- Fixed icon and desktop issue

* Fri Jul 03 2015 Louis Abel <tucklesepk@gmail.com> - 3.6.8-1
- Version jump to 3.6.8

* Sun Dec 21 2014 Louis Abel <tucklesepk@gmail.com> - 3.4.6-1
- Version jump to 3.4.6

* Sun Dec 21 2014 Louis Abel <tucklesepk@gmail.com> - 3.0.3-1
- Version jump to 3.0.3

* Mon Sep 15 2014 Louis Abel <tucklesepk@gmail.com> - 2.10.29-1
- Minor version jump
- Fixed the requirements for /usr/bin/kdialog
  - This is to satisfy EL7 and Fedora at the same time

* Sat Aug 09 2014 Louis Abel <tucklesepk@gmail.com> - 2.10.27-1
* Version jump from 2.8.3 to 2.10.27

* Sun Jun 22 2014 Louis Abel <tucklesepk@gmail.com> - 2.8.3-1
- Version jump from 2.4.20 to 2.8.3
- Updated service menu to latest found version
- Added requirements for Dropbox
- Added requirements for the Dropbox Service menu by Hash87

* Sun Mar 23 2014 Louis Abel <tucklesepk@gmail.com> - 2.4.20-1
- Minor version update
- Added sqlite area
- Fixed Startup Script
- Cleaned up post by moving links to install (this should make upgrades more sane)

* Fri Dec 20 2013 Louis Abel <tucklesepk@gmail.com> - 2.4.10-1
- Initial package build

