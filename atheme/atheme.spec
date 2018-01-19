## Define global settings
%global _hardened_build 1
%global major_version 7
%global minor_version 2
%global micro_version 9
%global build_with_plugins 0

# Using atheme-services as a name would be fine, but that would
# require either A) Some folders named atheme and others named
# atheme-services or B) require me to list every directory
# on the configure line and make them point to -services.
# If this were to become an official package, I would consider it.
Name:		atheme
Version:	%{major_version}.%{minor_version}.%{micro_version}
Release:	2%{?dist}
Summary:	Services for IRC Networks

Group:		System Environment/Daemons
License:	MIT
URL:		https://atheme.net
Source0:	https://github.com/%{name}/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.bz2
Source1:	%{name}.service
Source2:	%{name}.logrotate
Source3:	%{name}.init

BuildRequires:	cracklib-devel
BuildRequires:	perl-ExtUtils-Embed
BuildRequires:	openssl-devel
BuildRequires:	openldap-devel
BuildRequires:	pcre-devel
BuildRequires:	qrencode-devel

Requires:	openssl
Requires:	pcre
Requires:	cracklib

# OS Specific Requirements
%if 0%{?fedora} || 0%{?rhel} >= 7
BuildRequires:	systemd
Requires(post):	systemd
Requires(preun): systemd
Requires(postun): systemd
Requires:	systemd
%else
Requires:	initscripts
%endif


%description
Atheme is a feature-packed, extremely customisable IRC services
daemon that is secure, stable and scalable.

%package	libcore
Summary:	Atheme IRC Services core library
Group:		System Environment/Libraries

%description	libcore
Atheme is a feature-packed, extremely customisable IRC services
daemon that is secure, stable and scalable.

%package	devel
Summary:	Atheme development headers
Requires:	atheme = %{version}-%{release}

%description	devel
Atheme is a feature-packed, extremely customisable IRC services
daemon that is secure, stable and scalable.

This package contains the development headers required for developing
against atheme.

%prep
%setup -q -n %{name}-%{version}

# I am explicitly calling ldap, perl, pcre, cracklib support
# I am disabling internationalization as EL6 refuses to build
# with it enabled. This happens even though gettext-devel is
# installed. Until this is resolved, it is staying disabled.
%build
%configure \
	--sysconfdir="%{_sysconfdir}/%{name}" \
  --bindir="%{_sbindir}" \
  --docdir="%{_docdir}/%{name}" \
	--enable-fhs-paths \
	--enable-warnings \
	--enable-contrib \
	--enable-large-net \
	--disable-rpath \
	--with-cracklib \
	--with-pcre \
	--with-perl \
	--with-ldap \
	--without-libmowgli \
	--disable-nls

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

%{__mkdir} -p ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d
%{__install} -m 0644 %{SOURCE2} \
	${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/%{name}

%{__mkdir} -p ${RPM_BUILD_ROOT}%{_sbindir}
%{__mkdir} -p ${RPM_BUILD_ROOT}%{_var}/log

# OS Specific
%if 0%{?fedora} || 0%{?rhel} >= 7
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_unitdir}
%{__install} -m 0644 %{SOURCE1} \
	${RPM_BUILD_ROOT}%{_unitdir}/atheme.service
%else
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_initddir}
%{__install} -m 0755 %{SOURCE3} ${RPM_BUILD_ROOT}%{_initddir}/%{name}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_localstatedir}/run/%{name}
%endif

# development headers
%{__mkdir} -p ${RPM_BUILD_ROOT}/%{_includedir}/%{name}/{inline,protocol}
%{__install} -m 0644 include/*.h \
	${RPM_BUILD_ROOT}%{_includedir}/%{name}
%{__install} -m 0644 include/inline/*.h \
	${RPM_BUILD_ROOT}%{_includedir}/%{name}/inline
%{__install} -m 0644 include/protocol/*.h \
	${RPM_BUILD_ROOT}%{_includedir}/%{name}/protocol

%pre
# Since we are not an official Fedora build, we don't get an
# assigned uid/gid. This may make it difficult when installed
# on multiple systems that have different package sets.
%{_sbindir}/groupadd -r %{name} 2>/dev/null || :
%{_sbindir}/useradd -r -g %{name} \
	-s /sbin/nologin -d %{_datadir}/%{name} \
	-c 'Atheme IRC Services' %{name} 2>/dev/null || :

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
%doc /usr/share/doc/%{name}/*
%{_sbindir}/%{name}-services
%{_sbindir}/dbverify
%{_sbindir}/ecdsakeygen
%dir %attr(0750,-,-) %{_sysconfdir}/%{name}
%dir %attr(0700,atheme,atheme) %{_var}/log/%{name}
%dir %attr(0700,atheme,atheme) %{_sharedstatedir}/%{name}
%dir %{_datadir}/%{name}
%dir %{_libdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.motd
%config(noreplace) %attr(-,root,root) %{_sysconfdir}/logrotate.d/%{name}
%ghost %attr(0640,-,-) %config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%{_sysconfdir}/%{name}/*.example
%{_sysconfdir}/%{name}/*-example
%{_libdir}/%{name}/*
%{_datadir}/%{name}/*
%{_libdir}/libmowgli-2.so
%{_libdir}/libmowgli-2.so.0
%{_libdir}/libmowgli-2.so.0.0.0
#%dir %{_prefix}/tmpfiles.d
#%{_prefix}/lib/tmpfiles.d/atheme.conf

# OS Specific
%if 0%{?fedora} || 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%else
%{_initddir}/%{name}
%{_var}/run/%{name}
%endif

%files libcore
%defattr(-,root,root)
%{_libdir}/libathemecore.so.1
%{_libdir}/libathemecore.so.1.0.0

# development headers
%files devel
%defattr (0644,root,root,0755)
%dir %{_includedir}/%{name}
%dir %{_includedir}/%{name}/inline
%dir %{_includedir}/%{name}/protocol
%{_includedir}/%{name}/*.h
%{_includedir}/%{name}/inline/*.h
%{_includedir}/%{name}/protocol/*.h
%dir %{_includedir}/libmowgli-2
%{_includedir}/libmowgli-2/*
%{_libdir}/pkgconfig/atheme-services.pc
%{_libdir}/pkgconfig/libmowgli-2.pc
%{_libdir}/libathemecore.so

%changelog
* Wed Jan 17 2018 Louis Abel <louis@shootthej.net> - 7.2.9-2
- Fedora 27 Rebuild
- Separated libcore from main package
- Changed permissions to be more restrictive
- Rearranged libraries for devel package

* Wed Jul 12 2017 Louis Abel <louis@shootthej.net> - 7.2.9-2
- Fedora 26 Rebuild
- Version upgrade to 7.2.9

* Fri Feb 3 2017 Louis Abel <louis@shootthej.net> - 7.2.7-2
- Added atheme.conf as a ghost config file
- Fixed source0 url and name

* Wed Feb 1 2017 Louis Abel <louis@shootthej.net> - 7.2.7-1
- Rebase for version 7.2.7

* Wed Apr 6 2016 Louis Abel <louis@shootthej.net> - 7.2.6-1
- Initial build for Atheme 7.2.6

