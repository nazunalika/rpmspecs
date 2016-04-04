## Define global settings
%global _hardened_build 1
%global major_version 4
%global minor_version 0
%global micro_version 2
%global build_with_plugins 0

Name:		unrealircd
Version:	%{major_version}.%{minor_version}.%{micro_version}
Release:	2%{?dist}
Summary:	UnrealIRC Daemon

Group:		Applications/Communications
License:	GPLv2
URL:		http://www.unrealircd.com/
Source0:	https://www.unrealircd.org/unrealircd4/%{name}-%{version}.tar.gz
Source1:	%{name}.ircd.motd
Source2:	%{name}.ircd.rules
Source3:	%{name}.oper.motd
Source4:	%{name}.bot.motd
Source5:	%{name}.util.script
Source6:	%{name}.README
Source7:	%{name}.init
Source8:	%{name}.service
Source9:	%{name}.tune
Source10:	%{name}.README.forking
Source11:	%{name}.logrotate

# Plugins sources
%if "%{build_with_plugins}" == "1"
Source12:	antirandom.4.c
Source13:	antirandom.conf
Source14:	antirandom.README
Source15:	textban.4.c
Source16:	textban.README
Source17:	nocodes.4.c
Source18:	nocodes.README
Source19:	privdeaf.4.c
Source20:	privdeaf.README
Source21:	jumpserver.4.c
Source22:	jumpserver.README
Source23:	m_ircops.4.c
Source24:	m_ircops.README
Source25:	m_staff.4.c
Source26:	m_staff.conf
Source27:	m_staff.README
Source28:	m_banlink4.c
%endif

BuildRequires:	openssl-devel
BuildRequires:	tre-devel
BuildRequires:	zlib-devel
BuildRequires:	pcre2-devel
BuildRequires:	c-ares-devel
Requires:	openssl
Requires:	tre
Requires:	pcre2
Requires:	c-ares

%if 0%{?fedora} || 0%{?rhel} >= 7
BuildRequires:	systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires:	systemd
%else
Requires:	initscripts
%endif

%description
UnrealIRCd is an advanced IRC server that provides features for just
about everything.

%package devel
Group:		Development/Libraries
Summary:	Development headers for %{name}
Requires:	unrealircd = %{version}-%{release}

%description devel
The unrealircd-devel package contains the headers as part of the
unrealircd source. If you are planning on making your own modules
for unrealircd, you will need to install this package. If your
module will be using pcre2, tre, zlib, or c-ares, you will need
to install the -devel packages of those as well.

%if "%{build_with_plugins}" == "1"
%package AntiRandom
#Version:	1.4
Summary:	AntiRandom bot killer for %{name}
Requires:	unrealircd = %{version}-%{release}

%description AntiRandom
This module tries to detect random users (bots) and kills them (or
optionally: *line them). Note that by design this module could kill
innocent users (that look like having random nick/ident/realname) and
might also miss some "random" bots (because for the module they
didn't look random enough), that said.. the module seems to do a good
job :).

%package TextBan
#Version:	2.2
Summary:	TextBan plugin for %{name}
Requires:	unrealircd = %{version}-%{release}

%description TextBan
This module adds an extended ban ~T:<action>:<globmask> by which you
can instruct the ircd to take action upon encoutnering certain words
in the channel ("text ban"). Supported actions are 'block' (block the
entire sentence) and 'censor' (replace the word with <censored>). See
the README for more information. 

Example usage: +bb ~T:block:*http://* ~T:censor:*badword*

%package NoCodes
#Version:	1.2
Summary:	NoCodes plugin for %{name}
Requires:	unrealircd = %{version}-%{release}

%description NoCodes
This module will strip control codes (bold/underline/reverse) if the
channel is +S, and block such messages if the channel is +c. 

%package PrivDeaf
#Version:	1.2
Summary:	PrivDeaf plugin for %{name}
Requires:	unrealircd = %{version}-%{release}

%description PrivDeaf
This module adds a +D usermode that acts just like +d (don't receive
channel msgs) but for private messages instead, it only allows private
msgs/notices from servers, u-lines (services) and opers. 

%package JumpServer
#Version:	1.0
Summary:	JumpServer plugin for %{name}
Requires:	unrealircd = %{version}-%{release}

%description JumpServer
This module adds the ability to 'redirect' users to another server. 

Note however, that this is only supported by a few clients (mIRC).

%package m_ircops
#Version:	3.71
Summary:	m_ircops plugin for %{name}
Requires:	unrealircd = %{version}-%{release}

%description m_ircops
This (public) command shows a list of all IRCOps that are only 
(except hidden ones), along with their level (netadmin, services
 admin, ..) and their away status.

%package m_staff
#Version:	3.8
Summary:	m_staff plugin for %{name}
Requires:	unrealircd = %{version}-%{release}

%description m_staff
Adds a /STAFF command that displays the contents of a file (or
 URL if remote includes are enabled). 

%package m_banlink
#Version:	1.1
Summary:	m_banlink plugin for %{name}
Requires:	unrealircd = %{version}-%{release}

%description m_banlink
Adds the ability to link bans across multiple channels.

%endif


%prep
%setup -q

# Extra documentation.
cp %{SOURCE6} %{_builddir}/%{name}-%{version}/README
cp %{SOURCE10} %{_builddir}/%{name}-%{version}/README.forking

# Plugins
%if "%{build_with_plugins}" == "1"
# Module
cp %{SOURCE12} %{_builddir}/%{name}-%{version}/src/modules/third
cp %{SOURCE15} %{_builddir}/%{name}-%{version}/src/modules/third
cp %{SOURCE17} %{_builddir}/%{name}-%{version}/src/modules/third
cp %{SOURCE19} %{_builddir}/%{name}-%{version}/src/modules/third
cp %{SOURCE21} %{_builddir}/%{name}-%{version}/src/modules/third
cp %{SOURCE23} %{_builddir}/%{name}-%{version}/src/modules/third
cp %{SOURCE25} %{_builddir}/%{name}-%{version}/src/modules/third
cp %{SOURCE28} %{_builddir}/%{name}-%{version}/src/modules/third

# Config
cp %{SOURCE13} %{_builddir}/%{name}-%{version}/doc/conf
cp %{SOURCE26} %{_builddir}/%{name}-%{version}/doc/conf

# Docs
cp %{SOURCE14} %{_builddir}/%{name}-%{version}/doc
cp %{SOURCE16} %{_builddir}/%{name}-%{version}/doc
cp %{SOURCE18} %{_builddir}/%{name}-%{version}/doc
cp %{SOURCE20} %{_builddir}/%{name}-%{version}/doc
cp %{SOURCE22} %{_builddir}/%{name}-%{version}/doc
cp %{SOURCE24} %{_builddir}/%{name}-%{version}/doc
cp %{SOURCE27} %{_builddir}/%{name}-%{version}/doc
%endif

%build
%configure \
	--with-showlistmodes \
	--with-bindir=%{_bindir} \
	--with-datadir=%{_sharedstatedir}/%{name} \
	--with-pidfile=%{_localstatedir}/run/%{name}/ircd.pid \
	--with-confdir=%{_sysconfdir}/%{name} \
	--with-modulesdir=%{_libdir}/%{name} \
	--with-logdir=%{_localstatedir}/log/%{name} \
	--with-cachedir=%{_localstatedir}/cache/%{name} \
	--with-docdir=%{_docdir}/%{name}-%{version} \
	--with-tmpdir=%{_tmppath}/%{name} \
	--with-scriptdir=%{_libexecdir}/%{name} \
	--with-nick-history=2000 \
	--with-sendq=3000000 \
	--with-permissions=0644 \
	--with-fd-setsize=1024 \
	--with-system-tre \
	--with-system-pcre2 \
	--with-system-cares \
	--with-shunnotices \
	--with-topicisnuhost \
	--enable-dynamic-linking \
	--enable-ssl=%{_prefix}

make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}

# Unfortunately, the unrealircd folks have a broken make install.
# They even have a commit from 2001 where they put in:
# + @echo "Now install by hand; make install is broken."

# And...
# "Their fix was to make it broken." -remyabel

# Directories
## /etc/unrealircd, /usr/share/doc/unrealircd, /usr/bin
%{__install} -d -m 0755 \
	${RPM_BUILD_ROOT}%{_bindir}
%{__install} -d -m 0750 \
	${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}
%{__install} -d -m 0750 \
	${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/aliases
%{__install} -d -m 0750 \
	${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/help
%{__install} -d -m 0750 \
	${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/examples
%{__install} -d -m 0750 \
	${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/ssl
%{__install} -d -m 0755 \
	${RPM_BUILD_ROOT}%{_docdir}/%{name}-%{version}
## /usr/lib64/unrealircd
%{__install} -d -m 0755 \
	${RPM_BUILD_ROOT}%{_libdir}/%{name}
%{__install} -d -m 0755 \
	${RPM_BUILD_ROOT}%{_libdir}/%{name}/usermodes
%{__install} -d -m 0755 \
	${RPM_BUILD_ROOT}%{_libdir}/%{name}/chanmodes
%{__install} -d -m 0755 \
	${RPM_BUILD_ROOT}%{_libdir}/%{name}/snomasks
%{__install} -d -m 0755 \
	${RPM_BUILD_ROOT}%{_libdir}/%{name}/extbans
%{__install} -d -m 0755 \
	${RPM_BUILD_ROOT}%{_libdir}/%{name}/third
# /usr/libexec/unrealircd
%{__install} -d -m 0755 \
	${RPM_BUILD_ROOT}%{_libexecdir}/%{name}

## /var
%{__install} -d -m 0700 \
	${RPM_BUILD_ROOT}%{_sharedstatedir}/%{name}
%{__install} -d -m 0700 \
	${RPM_BUILD_ROOT}%{_localstatedir}/log/%{name}
%{__install} -d -m 0700 \
	${RPM_BUILD_ROOT}%{_localstatedir}/cache/%{name}

# Files
%{__install} -m 0755 src/ircd \
	${RPM_BUILD_ROOT}%{_bindir}/unrealircd
%{__install} -m 0644 doc/conf/*.conf \
	${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}
%{__install} -m 0644 doc/conf/aliases/*.conf \
	${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/aliases
%{__install} -m 0644 doc/conf/help/*.conf \
	${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/help
%{__install} -m 0600 doc/conf/examples/*.conf \
	${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/examples
%{__install} -m 0644 doc/conf/ssl/curl-ca-bundle.crt \
	${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/ssl

%{__install} -m 0755 src/modules/*.so \
	${RPM_BUILD_ROOT}%{_libdir}/%{name}
%{__install} -m 0755 src/modules/usermodes/*.so \
	${RPM_BUILD_ROOT}%{_libdir}/%{name}/usermodes
%{__install} -m 0755 src/modules/chanmodes/*.so \
	${RPM_BUILD_ROOT}%{_libdir}/%{name}/chanmodes
%{__install} -m 0755 src/modules/snomasks/*.so \
	${RPM_BUILD_ROOT}%{_libdir}/%{name}/snomasks
%{__install} -m 0755 src/modules/extbans/*.so \
	${RPM_BUILD_ROOT}%{_libdir}/%{name}/extbans

# Extras
%{__install} -m 0644 %{SOURCE1} \
	${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/ircd.motd
%{__install} -m 0644 %{SOURCE2} \
	${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/ircd.rules
%{__install} -m 0644 %{SOURCE3} \
	${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/oper.motd
%{__install} -m 0644 %{SOURCE4} \
	${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/bot.motd
%{__install} -m 0770 %{SOURCE5} \
	${RPM_BUILD_ROOT}%{_libexecdir}/%{name}/ircdutil
%{__install} -m 0600 %{SOURCE9} \
	${RPM_BUILD_ROOT}%{_sharedstatedir}/unrealircd/ircd.tune
%{__install} -d -m 0755 \
	${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d 
%{__install} -m 0644 %{SOURCE11} \
	${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/unrealircd

# OS Specific
%if 0%{?fedora} || 0%{?rhel} >= 7
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_unitdir}
%{__install} -m 0644 %{SOURCE8} \
	${RPM_BUILD_ROOT}%{_unitdir}/unrealircd.service
%else
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_initddir}
%{__install} -m 0755 %{SOURCE7} ${RPM_BUILD_ROOT}%{_initddir}/unrealircd
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_localstatedir}/run/%{name}
%endif

# Placeholder for plugins
%if "%{build_with_plugins}" == "1"
%{__install} -m 0755 src/modules/third/*.so \
	${RPM_BUILD_ROOT}%{_libdir}/%{name}/third
%endif

# development headers
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_includedir}/%{name}
%{__install} -m 0755 include/*.h \
	${RPM_BUILD_ROOT}%{_includedir}/%{name}

%pre
# Since we are not an official Fedora build, we don't get an
# assigned uid/gid. This may make it difficult when installed
# on multiple systems.
%{_sbindir}/groupadd -r unrealircd 2>/dev/null || :
%{_sbindir}/useradd -r -g unrealircd \
	-s /sbin/nologin -d %{_sysconfdir}/unrealircd \
	-c 'Unreal IRC Server' unrealircd 2>/dev/null || :

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
%defattr(-, unrealircd, unrealircd, -)
%doc doc/Authors doc/coding-guidelines doc/tao.of.irc README
%attr(-,root,root) %{_bindir}/unrealircd
%attr(-,root,root) %{_sysconfdir}/logrotate.d/unrealircd
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/help
%dir %{_sysconfdir}/%{name}/examples
%dir %{_sysconfdir}/%{name}/ssl
%dir %{_sysconfdir}/%{name}/aliases
%config(noreplace) %{_sysconfdir}/%{name}/*.conf
%config(noreplace) %{_sysconfdir}/%{name}/*.motd
%config(noreplace) %{_sysconfdir}/%{name}/*.rules
%config(noreplace) %{_sysconfdir}/%{name}/help/*.conf
%{_sysconfdir}/%{name}/examples/*.conf
%{_sysconfdir}/%{name}/ssl/curl-ca-bundle.crt
%config(noreplace) %{_sysconfdir}/%{name}/aliases/*.conf

%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/usermodes
%dir %{_libdir}/%{name}/chanmodes
%dir %{_libdir}/%{name}/snomasks
%dir %{_libdir}/%{name}/extbans
%dir %{_libdir}/%{name}/third
%{_libdir}/%{name}/*.so
%{_libdir}/%{name}/usermodes/*.so
%{_libdir}/%{name}/chanmodes/*.so
%{_libdir}/%{name}/snomasks/*.so
%{_libdir}/%{name}/extbans/*.so

%dir %{_localstatedir}/log/%{name}
%dir %{_localstatedir}/cache/%{name}
%dir %{_sharedstatedir}/%{name}
%{_sharedstatedir}/%{name}/ircd.tune
%{_libexecdir}/%{name}/ircdutil

# Add excludes for plugins
%exclude %{_libdir}/%{name}/third/*.so
%exclude %{_sysconfdir}/%{name}/antirandom.conf
%exclude %{_sysconfdir}/%{name}/m_staff.conf

# Plugins only
%if "%{build_with_plugins}" == "1"
%files AntiRandom
%doc doc/antirandom.README
%{_libdir}/%{name}/third/antirandom.4.so
%{_sysconfdir}/%{name}/antirandom.conf

%files TextBan
%doc doc/textban.README
%{_libdir}/%{name}/third/textban.4.so

%files NoCodes
%doc doc/nocodes.README
%{_libdir}/%{name}/third/nocodes.4.so

%files PrivDeaf
%doc doc/privdeaf.README
%{_libdir}/%{name}/third/privdeaf.4.so

%files JumpServer
%doc doc/jumpserver.README
%{_libdir}/%{name}/third/jumpserver.4.so

%files m_ircops
%doc doc/m_ircops.README
%{_libdir}/%{name}/third/m_ircops.4.so
%{_sysconfdir}/%{name}/m_staff.conf

%files m_staff
%doc doc/m_staff.README
%{_libdir}/%{name}/third/m_staff.4.so

%files m_banlink
%{_libdir}/%{name}/third/m_banlink4.so

%endif

# OS Specific
%if 0%{?fedora} || 0%{?rhel} >= 7
%{_unitdir}/unrealircd.service
%doc README.forking
%else
%{_initddir}/unrealircd
%{_localstatedir}/run/%{name}
%endif

%files devel
%defattr (0644,root,root,0755)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h

%changelog
* Sun Apr 3 2016 Louis Abel <louis@shootthej.net> - 4.0.2-2
- Added -devel package for headers
- Added various plugins
- Updated License to GPLv2
- Updated Group

* Sat Apr 2 2016 Louis Abel <louis@shootthej.net> - 4.0.2-1
- Initial build for UnrealIRCd 4.0.2
- Enterprise Linux 6: Most functions moved to initscript
- util script created to compensate for lack of initscript in
- Enterprise Linux 7

