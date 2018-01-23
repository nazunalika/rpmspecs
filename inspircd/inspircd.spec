## Define global settings
%global _hardened_build 1
%global major_version 2
%global minor_version 0
%global micro_version 25

## Define conditionals
## Change to "without" if needed
%bcond_without all_plugins
%bcond_without mysql
%bcond_without pgsql
%bcond_without sqlite
%bcond_without ldap
%bcond_without geoip
%bcond_without regex_engines

%global extras_version 0.0.0+git1516494055.068bd62

Name:		inspircd
Version:	%{major_version}.%{minor_version}.%{micro_version}
Release:	3%{?dist}
Summary:	Modular Internet Relay Chat server written in C++

Group:		Applications/Communications
License:	GPLv2
URL:		http://www.inspircd.org
Source0:	https://github.com/inspircd/inspircd/archive/v%{version}.tar.gz
Source1:	%{name}.service
Source2:	%{name}.init
Source3:	%{name}.logrotate
Source4:	%{name}.README
Source5:	%{name}-extras-%{extras_version}.tar.gz

Provides:	%{name} = %{version}-%{release}
Provides:	%{name}2

Patch1:		%{name}-2.0.25_default-inspircd-conf.patch
Patch2:		%{name}-2.0.25_default-modules-conf.patch

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
BuildRequires:	qrencode-devel

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
Inspircd is a modular Internet Relay Chat (IRC) server written in C++ for Linux,
 BSD, Windows and Mac OS X systems.

It was created from scratch to be stable, modern and lightweight. It avoids a
number of design flaws and performance issues that plague other more 
established projects, such as UnrealIRCd, while providing the same level of
feature parity.

It provides a tunable number of features through the use of an advanced but well
documented module system. By keeping core functionality to a minimum we hope to
increase the stability, security and speed of Inspircd while also making it
customisable to the needs of many different users.

And after all it's free and open source.

%package	devel
Summary:	Inspircd development headers
Requires:	inspircd = %{version}-%{release}

%description	devel
This package contains the development headers required for developing against
inspircd.

################################################################################
# Modules

%package	modules-openssl
Summary:	OpenSSL Module for Inspircd
Group:		System Environment/Libraries
Requires:	inspircd = %{version}-%{release}
Requires:	openssl-libs

%description	modules-openssl
Inspircd is a modular Internet Relay Chat (IRC) server written in C++ for Linux.

This provides the openssl module for inspircd. It is recommended to install this
module to allow secure connections to your irc server.

%if %{with sqlite}
%package	modules-sqlite3
Summary:	SQLite 3 Backend Module for Inspircd
Group:		System Environment/Libraries
Requires:	inspircd = %{version}-%{release}
Requires:	sqlite-libs

%description	modules-sqlite3
Inspircd is a modular Internet Relay Chat (IRC) server written in C++ for Linux.

This provides the sqlite3 module for inspircd.
%endif

%if %{with mysql}
%package	modules-mysql
Summary:	MySQL Backend Module for Inspircd
Group:		System Environment/Libraries
Requires:	inspircd = %{version}-%{release}
Requires:	mysql-libs

%description	modules-mysql
Inspircd is a modular Internet Relay Chat (IRC) server written in C++ for Linux.

This provides the mysql module for inspircd.
%endif

%if %{with pgsql}
%package	modules-postgresql
Summary:	Postgresql Backend Module for Inspircd
Group:		System Environment/Libraries
Requires:	inspircd = %{version}-%{release}
Requires:	postgresql-libs

%description	modules-postgresql
Inspircd is a modular Internet Relay Chat (IRC) server written in C++ for Linux.

This provides the postgresql module for inspircd.
%endif

%if %{with ldap}
%package	modules-ldap
Summary:	LDAP Backend Module for Inspircd
Group:		System Environment/Libraries
Requires:	inspircd = %{version}-%{release}
Requires:	openldap

%description	modules-ldap
Inspircd is a modular Internet Relay Chat (IRC) server written in C++ for Linux.

This provides the ldap module for inspircd.
%endif

%if %{with geoip}
%package        modules-geoip
Summary:        GeoIP Backend Module for Inspircd
Group:          System Environment/Libraries
Requires:       inspircd = %{version}-%{release}
Requires:       geoip

%description    modules-geoip
Inspircd is a modular Internet Relay Chat (IRC) server written in C++ for Linux.

This provides the geoip module for inspircd.
%endif

%if %{with regex_engines}
%package        modules-pcre
Summary:        pcre Regex Module for Inspircd
Group:          System Environment/Libraries
Requires:       inspircd = %{version}-%{release}
Requires:       pcre

%description    modules-pcre
Inspircd is a modular Internet Relay Chat (IRC) server written in C++ for Linux.

This provides the pcre module for inspircd.

%package        modules-tre
Summary:        Tre Regex Module for Inspircd
Group:          System Environment/Libraries
Requires:       inspircd = %{version}-%{release}
Requires:       tre

%description    modules-tre
Inspircd is a modular Internet Relay Chat (IRC) server written in C++ for Linux.

This provides the tre module for inspircd.

%package        modules-posix
Summary:        POSIX Regex Module for Inspircd
Group:          System Environment/Libraries
Requires:       inspircd = %{version}-%{release}

%description    modules-posix
Inspircd is a modular Internet Relay Chat (IRC) server written in C++ for Linux.

This provides the posix module for inspircd.
%endif

%prep
%setup -q -a 5
%patch1
%patch2

## Enable all extras EXCEPT gnutls, mssql, and stdlib
## Doing symlinks instead of calling the configure script
pushd src/modules/

%if %{with mysql}
%{__ln_s} -v extra/m_mysql.cpp .
%endif

%if %{with pgsql}
%{__ln_s} -v extra/m_pgsql.cpp .
%endif

%if %{with sqlite}
%{__ln_s} -v extra/m_sqlite3.cpp .
%endif

%if %{with ldap}
%{__ln_s} -v extra/m_ldapauth.cpp .
%{__ln_s} -v extra/m_ldapoper.cpp .
%endif

%if %{with geoip}
%{__ln_s} -v extra/m_geoip.cpp .
%endif

%if %{with regex_engines}
%{__ln_s} -v extra/m_regex_pcre.cpp .
%{__ln_s} -v extra/m_regex_posix.cpp .
%{__ln_s} -v extra/m_regex_tre.cpp .
%endif

%{__ln_s} -v extra/m_ssl_openssl.cpp .

# Extras will be done here as symlinks
for x in \
  m_accounthost.cpp \
  m_antibear.cpp \
  m_antibottler.cpp \
  m_anticaps.cpp \
  m_antirandom.cpp \
  m_ascii.cpp \
  m_authy.cpp \
  m_autodrop.cpp \
  m_autokick.cpp \
  m_bannegate.cpp \
  m_blockhighlight.cpp \
  m_cap_chghost.cpp \
  m_capnotify.cpp \
  m_changecap.cpp \
  m_ciphersuitejoin.cpp \
  m_classban.cpp \
  m_conn_banner.cpp \
  m_conn_delayed_join.cpp \
  m_conn_matchident.cpp \
  m_conn_vhost.cpp \
  m_custompenalty.cpp \
  m_dccblock.cpp \
  m_deferaccept.cpp \
  m_disablemodes.cpp \
  m_extbanredirect.cpp \
  m_findxline.cpp \
  m_flashpolicyd.cpp \
  m_forceident.cpp \
  m_fullversion.cpp \
%if %{with geoip}
  m_geoipban.cpp \
%endif
  m_hideidle.cpp \
  m_identmeta.cpp \
  m_invitenotify.cpp \
  m_ircv3_sts.cpp \
  m_ircxusernames.cpp \
  m_join0.cpp \
  m_joinoninvite.cpp \
  m_joinpartsno.cpp \
  m_joinpartspam.cpp \
  m_lusersnoservices.cpp \
  m_messagelength.cpp \
  m_namedstats.cpp \
  m_nickdelay.cpp \
  m_nickin001.cpp \
  m_nocreate.cpp \
  m_noctcp_user.cpp \
  m_nooponcreate.cpp \
  m_nouidnick.cpp \
  m_opmoderated.cpp \
  m_override_umode.cpp \
  m_pretenduser.cpp \
  m_privdeaf.cpp \
  m_qrcode.cpp \
  m_quietban.cpp \
  m_rehashsslsignal.cpp \
  m_replaymsg.cpp \
  m_require_auth.cpp \
  m_requirectcp.cpp \
  m_rotatelog.cpp \
  m_rpg.cpp \
  m_sha1.cpp \
  m_slowmode.cpp \
  m_solvemsg.cpp \
  m_stats_unlinked.cpp \
  m_svsoper.cpp \
  m_timedstaticquit.cpp \
  m_topicall.cpp \
  m_totp.cpp ; do
    %{__ln_s} -v ../../%{name}-extras-%{extras_version}/2.0/$x . 
done

popd

%build

# Add all plugins
# In the future, we'll make these modules as part of an -extras package
# Note: We will eventually cut this over into a master download from git
#       and do our own symlinking/install.
#%if %{with all_plugins}
#for i in $(./modulemanager list | awk '/^m_/ && !/gnutls/ && !/re2/ {print $1}') 
#	do ./modulemanager install $i
#done
#%endif

# We're no longer supported :(
%configure --disable-interactive \
	--enable-openssl \
	--prefix=%{_datadir}/%{name} \
	--module-dir=%{_libdir}/%{name}/modules \
	--config-dir=%{_sysconfdir}/%{name} \
	--binary-dir=%{_sbindir} \
	--data-dir=%{_sharedstatedir}/%{name} \
	--log-dir=%{_var}/log/%{name} \
	--enable-epoll \
	--disable-kqueue

make %{?_smp_mflags}

# Extra documentation
cp %{SOURCE4} %{_builddir}/%{name}-%{version}/README.info

%install
rm -rf $RPM_BUILD_ROOT
%make_install

%{__mkdir} -p ${RPM_BUILD_ROOT}/%{_libexecdir}/%{name}

%{__mkdir} -p ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d
%{__install} -m 0644 %{SOURCE3} \
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
	-c 'Inspircd Server' inspircd 2>/dev/null || :

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
%defattr(-, root, root, -)
%doc docs/COPYING docs/Doxyfile docs/rfc/* README.md README.info

%{_sbindir}/%{name}
%dir %attr(0750,root,inspircd) %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/examples
%{_sysconfdir}/%{name}/examples/*.example
%dir %{_sysconfdir}/%{name}/examples/aliases
%{_sysconfdir}/%{name}/examples/aliases/*.example
%dir %{_sysconfdir}/%{name}/examples/modules
%{_sysconfdir}/%{name}/examples/modules/*.example
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/modules
%{_libdir}/%{name}/modules/*
%dir %attr(0700,inspircd,inspircd) %{_var}/log/%{name}
%dir %attr(-,inspircd,inspircd) %{_var}/lib/%{name}
%dir %{_datadir}/%{name}

# Do I need perms on the symlinks?
%dir %{_libexecdir}/%{name}
%dir %{_datadir}/%{name}/bin
%{_datadir}/%{name}/bin/%{name}
%{_datadir}/%{name}/conf
%{_datadir}/%{name}/logs
%{_datadir}/%{name}/data
%{_datadir}/%{name}/modules
%attr(-,inspircd,inspircd) %{_datadir}/%{name}/.gdbargs
%config(noreplace) %attr(-,root,root) %{_sysconfdir}/logrotate.d/%{name}

# All excludes
%exclude %{_libdir}/%{name}/modules/m_ssl_openssl.so
%exclude %{_libdir}/%{name}/modules/m_ldap*.so
%exclude %{_libdir}/%{name}/modules/m_regex_*.so
%exclude %{_libdir}/%{name}/modules/m_geoip.so
%exclude %{_libdir}/%{name}/modules/m_mysql.so
%exclude %{_libdir}/%{name}/modules/m_pgsql.so
%exclude %{_libdir}/%{name}/modules/m_sqlite3.so

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

%files modules-openssl
%defattr(-, root, root, -)
%{_libdir}/%{name}/modules/m_ssl_openssl.so

%if %{with ldap}
%files modules-ldap
%defattr(-, root, root, -)
%{_libdir}/%{name}/modules/m_ldapauth.so
%{_libdir}/%{name}/modules/m_ldapoper.so
%endif

%if %{with regex_engines}
%files modules-pcre
%defattr(-, root, root, -)
%{_libdir}/%{name}/modules/m_regex_pcre.so

%files modules-posix
%defattr(-, root, root, -)
%{_libdir}/%{name}/modules/m_regex_posix.so

%files modules-tre
%defattr(-, root, root, -)
%{_libdir}/%{name}/modules/m_regex_tre.so
%endif

%if %{with geoip}
%files modules-geoip
%defattr(-, root, root, -)
%{_libdir}/%{name}/modules/m_geoip.so
%endif

%if %{with mysql}
%files modules-mysql
%defattr(-, root, root, -)
%{_libdir}/%{name}/modules/m_mysql.so
%endif

%if %{with pgsql}
%files modules-postgresql
%defattr(-, root, root, -)
%{_libdir}/%{name}/modules/m_pgsql.so
%endif

%if %{with sqlite}
%files modules-sqlite3
%defattr(-, root, root, -)
%{_libdir}/%{name}/modules/m_sqlite3.so
%endif

%changelog
* Thu Jan 18 2018 Louis Abel <louis@shootthej.net> - 2.0.25-3
- Separated core modules into separate RPM's
- Fixed logic

* Wed Jan 17 2018 Louis Abel <louis@shootthej.net> - 2.0.25-2
- Rearranged bindir to sbindir
- Rearranged default permissions:
 * Ensured specific files are owned by inspircd
 * All rest owned by root
- Added qrcode support
- Added patches for default config files to remove "conf"

* Sun Nov 12 2017 Louis Abel <louis@shootthej.net> - 2.0.25-1
- Rebase to 2.0.25
- Build for Fedora 27

* Wed Jul 12 2017 Louis Abel <louis@shootthej.net> - 2.0.24-2
- Rebuild for Fedora 26

* Fri May 19 2017 Louis Abel <louis@shootthej.net> - 2.0.24-1
- Rebase to 2.0.24

* Fri Feb 17 2017 Louis Abel <louis@shootthej.net> - 2.0.23-4
- Removed util script
- Changed systemd unit to work with ircd binaries

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
- Initial build for Inspircd 2.0.21

