## Define global settings
%global _hardened_build 1
%global major_version 2
%global minor_version 0
%global micro_version 23
%global build_with_all_plugins 1

Name:		inspircd
Version:	%{major_version}.%{minor_version}.%{micro_version}
Release:	3%{?dist}
Summary:	Modular Internet Relay Chat server written in C++

Group:		Applications/Communications
License:	GPLv2
URL:		http://www.inspircd.org/
Source0:	https://github.com/inspircd/inspircd/archive/v%{version}.tar.gz
Source1:	%{name}.service
Source2:	%{name}.init
Source3:	%{name}.util.script
Source4:	%{name}.logrotate
Source5:	%{name}.README

BuildRequires:	perl(LWP::Simple)
BuildRequires:	perl(LWP::Protocol::https)
BuildRequires:	perl(Crypt::SSLeay)
BuildRequires:	perl(IO::Socket::SSL)
BuildRequires:	perl(Getopt::Long)
BuildRequires:	gcc-c++
BuildRequires:	openssl-devel
BuildRequires:	tre-devel
BuildRequires:	postgresql-devel
BuildRequires:	sqlite-devel
BuildRequires:	geoip-devel
BuildRequires:	openldap-devel
BuildRequires:	pcre-devel

## As far as I'm aware, the other packages can be installed
## when the modules are enabled. This is mentioned in the
## README. Essentially, there's no direct requirement for
## the packages we compiled against.
Requires:	openssl
Requires:	perl(Getopt::Long)

# OS Specific Requirements
%if 0%{?fedora} || 0%{?rhel} >= 7
BuildRequires:	systemd
BuildRequires:	mariadb-devel
Requires(post):	systemd
Requires(preun): systemd
Requires(postun): systemd
Requires:	systemd
%else
BuildRequires:	mysql-devel
Requires:	initscripts
%endif

%description
InspIRCd is a modular Internet Relay Chat (IRC) server written in C++ for Linux,
 BSD, Windows and Mac OS X systems.

It was created from scratch to be stable, modern and lightweight. It avoids a
number of design flaws and performance issues that plague other more 
established projects, such as UnrealIRCd, while providing the same level of
feature parity.

It provides a tunable number of features through the use of an advanced but well
documented module system. By keeping core functionality to a minimum we hope to
increase the stability, security and speed of InspIRCd while also making it
customisable to the needs of many different users.

And after all it's free and open source.

%package	devel
Summary:	InspIRCd development headers
Requires:	inspircd = %{version}-%{release}

%description	devel
This package contains the development headers required for developing against
inspircd.

%prep
%setup -q

## Enable all extras EXCEPT gnutls, mssql, and stdlib
%build
%_configure --enable-extras=m_ssl_openssl.cpp \
	--enable-extras=m_ldapauth.cpp \
	--enable-extras=m_ldapoper.cpp \
	--enable-extras=m_mysql.cpp \
	--enable-extras=m_pgsql.cpp \
	--enable-extras=m_regex_pcre.cpp \
	--enable-extras=m_regex_posix.cpp \
	--enable-extras=m_regex_tre.cpp \
	--enable-extras=m_sqlite3.cpp \
	--enable-extras=m_geoip.cpp

# Add all plugins
%if "%{build_with_all_plugins}" == "1"
for i in $(./modulemanager list | awk '/^m_/ && !/gnutls/ && !/re2/ {print $1}') 
	do ./modulemanager install $i
done
%endif

# We're no longer supported :(
%configure --disable-interactive \
	--enable-openssl \
	--prefix=%{_datadir}/%{name} \
	--module-dir=%{_libdir}/%{name}/modules \
	--config-dir=%{_sysconfdir}/%{name} \
	--binary-dir=%{_bindir} \
	--data-dir=%{_sharedstatedir}/%{name} \
	--log-dir=%{_var}/log/%{name} \
	--enable-epoll \
	--disable-kqueue

make %{?_smp_mflags}

# Extra documentation
cp %{SOURCE5} %{_builddir}/%{name}-%{version}/README.info

%install
rm -rf $RPM_BUILD_ROOT
%make_install

%{__mkdir} -p ${RPM_BUILD_ROOT}/%{_libexecdir}/%{name}
%{__install} -m 0755 %{SOURCE3} \
	${RPM_BUILD_ROOT}/%{_libexecdir}/%{name}/ircdutil

%{__mkdir} -p ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d
%{__install} -m 0644 %{SOURCE4} \
	${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/%{name}

# Symlinks in our home directory
pushd ${RPM_BUILD_ROOT}%{_datadir}/%{name}
	%{__mkdir} bin
	%{__mv} inspircd bin
	%{__ln_s} %{_sysconfdir}/%{name} conf
	%{__ln_s} %{_var}/log/%{name} logs
	%{__ln_s} %{_libdir}/%{name}/modules modules
	%{__ln_s} %{_sharedstatedir}/%{name} data
popd

# OS Specific
%if 0%{?fedora} || 0%{?rhel} >= 7
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_unitdir}
%{__install} -m 0644 %{SOURCE1} \
	${RPM_BUILD_ROOT}%{_unitdir}/inspircd.service
%else
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_initddir}
%{__install} -m 0755 %{SOURCE2} ${RPM_BUILD_ROOT}%{_initddir}/%{name}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_localstatedir}/run/%{name}
%endif

# development headers
%{__mkdir} -p ${RPM_BUILD_ROOT}/%{_includedir}/%{name}/{commands,modes,threadengines}
%{__install} -m 0644 include/*.h \
	${RPM_BUILD_ROOT}%{_includedir}/%{name}
%{__install} -m 0644 include/commands/*.h \
	${RPM_BUILD_ROOT}%{_includedir}/%{name}/commands
%{__install} -m 0644 include/modes/*.h \
	${RPM_BUILD_ROOT}%{_includedir}/%{name}/modes
%{__install} -m 0644 include/threadengines/*.h \
	${RPM_BUILD_ROOT}%{_includedir}/%{name}/threadengines

%pre
# Since we are not an official Fedora build, we don't get an
# assigned uid/gid. This may make it difficult when installed
# on multiple systems that have different package sets.
%{_sbindir}/groupadd -r %{name} 2>/dev/null || :
%{_sbindir}/useradd -r -g %{name} \
	-s /sbin/nologin -d %{_datadir}/inspircd \
	-c 'InspIRCd Server' inspircd 2>/dev/null || :

%preun
%if 0%{?fedora} || 0%{?rhel} >= 7
%systemd_preun %{name}.service
%else
if [ $1 = 0 ]; then
	[ -f /var/lock/subsys/%{name} ] && /sbin/service %{name} stop
	[ -f %{_initddir}/%{name} ] && chkconfig --del %{name}
fi
%endif

%post
%if 0%{?fedora} || 0%{?rhel} >= 7
%systemd_post %{name}.service
%else
/sbin/chkconfig --add %{name}
%endif

%postun
%if 0%{?fedora} || 0%{?rhel} >= 7
%systemd_postun_with_restart %{name}.service
%else
if [ "$1" -ge "1" ]; then
	[ -f /var/lock/subsys/%{name} ] && /sbin/service %{name} restart >/dev/null 2>&1
fi
%endif

%files
%defattr(-, inspircd, inspircd, -)
%doc docs/COPYING docs/Doxyfile docs/rfc/* README.md README.info

%{_bindir}/%{name}
%dir %attr(0700,-,-) %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/examples
%{_sysconfdir}/%{name}/examples/*.example
%dir %{_sysconfdir}/%{name}/examples/aliases
%{_sysconfdir}/%{name}/examples/aliases/*.example
%dir %{_sysconfdir}/%{name}/examples/modules
%{_sysconfdir}/%{name}/examples/modules/*.example
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/modules
%{_libdir}/%{name}/modules/*
%dir %{_var}/log/%{name}
%dir %{_sharedstatedir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/.gdbargs

# Do I need perms on the symlinks?
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/ircdutil
%dir %{_datadir}/%{name}/bin
%{_datadir}/%{name}/bin/%{name}
%{_datadir}/%{name}/conf
%{_datadir}/%{name}/logs
%{_datadir}/%{name}/data
%{_datadir}/%{name}/modules
%config(noreplace) %attr(-,root,root) %{_sysconfdir}/logrotate.d/%{name}

# OS Specific
%if 0%{?fedora} || 0%{?rhel} >= 7
%{_unitdir}/inspircd.service
%else
%{_initddir}/inspircd
%{_var}/run/%{name}
%endif

# development headers
%files devel
%defattr (0644,root,root,0755)
%dir %{_includedir}/%{name}
%dir %{_includedir}/%{name}/commands
%dir %{_includedir}/%{name}/modes
%dir %{_includedir}/%{name}/threadengines
%{_includedir}/%{name}/*.h
%{_includedir}/%{name}/commands/*.h
%{_includedir}/%{name}/modes/*.h
%{_includedir}/%{name}/threadengines/*.h

%changelog
* Tue Feb 7 2017 Louis Abel <louis@shootthej.net> - 2.0.23-3
- Fixed init script description for EL6

* Tue Nov 1 2016 Louis Abel <louis@shootthej.net> - 2.0.23-2
- Version rebase to 2.0.23
- Combined all compiled modules into a single package
- Removed support for re2 which requires stdlib/c++11

* Sat Apr 9 2016 Louis Abel <louis@shootthej.net> - 2.0.21-2
- Extra plugins package created
- devel package created
- Fixed enable-extras
- Added extra build requirements that were not needed before

* Fri Apr 8 2016 Louis Abel <louis@shootthej.net> - 2.0.21-1
- Initial build for InspIRCd 2.0.21

