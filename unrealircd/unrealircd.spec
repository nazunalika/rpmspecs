## Define global settings
%global _hardened_build 1
%global major_version 4
%global minor_version 0
%global micro_version 2

Name:		unrealircd
Version:	%{major_version}.%{minor_version}.%{micro_version}
Release:	1%{?dist}
Summary:	UnrealIRC Daemon

Group:		System Environment/Daemons
License:	GPL
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

%prep
%setup -q

# Extra documentation.
cp %{SOURCE6} %{_builddir}/%{name}-%{version}/README
cp %{SOURCE10} %{_builddir}/%{name}-%{version}/README.forking

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

# OS Specific
%if 0%{?fedora} || 0%{?rhel} >= 7
%{_unitdir}/unrealircd.service
%doc README.forking
%else
%{_initddir}/unrealircd
%{_localstatedir}/run/%{name}
%endif

%changelog
* Sat Apr 2 2016 Louis Abel <louis@shootthej.net> - 4.0.2-1
- Initial build for UnrealIRCd 4.0.2
- Enterprise Linux 6: Most functions moved to initscript
- util script created to compensate for lack of initscript in
- Enterprise Linux 7

