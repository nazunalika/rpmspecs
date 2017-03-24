## Time to properly make a kmod rpm for ena, because apparently the CentOS people don't know
## how to include it in the AMI they manage (why?). Meanwhile the one who made the original
## spec, he should feel shame. He was doing a LOT of unnecessary work.

# This is a rebuild of a prior RPM I worked on to try to simplify it and make it ignore
# the kernel version. This way I don't have to consistently keep rebuilding it for each new
# kernel that arrives. In the event upstream (aka Red Hat) decides to change the kABI, this
# RPM will have to be rebuilt. This sometimes happens when minor versions are released and 
# is generally rare. This is also to avoid dkms and akmod, which I'm not a fan of for EL.

%global _modprobe_d	%{_prefix}/lib/modprobe.d/
%global _grubby		%{_sbindir}/grubby --update-kernel=ALL
%global _dracutopts	net.ifnames=0
%define kmod_name	ena
%define kernel_version	3.10.0-514.10.2
## Defining a kernel version because kversion is not defined for some reason
%{!?kversion: %define kversion %{kernel_version}.el7.%{_target_cpu}}

Name:		%{kmod_name}-kmod
Version:	1.1.3
Release:	2%{?dist}
Summary:	%{kmod_name} kernel module{s}
Epoch:		1

Group:		System Environment/Kernel
License:	GPLv2
URL:		https://aws.amazon.com
Source0:	%{kmod_name}-%{version}.tar.gz

# Beyond this point, this RPM is for EL7 only. There is no reason to build for EL6.
Source10:	kmodtool-%{kmod_name}-el7.sh

BuildRequires:	redhat-rpm-config
#BuildRequires:	perl
ExclusiveArch:	x86_64

# Magic
%{expand:%(sh %{SOURCE10} rpmtemplate %{kmod_name} %{kversion} "")}
%define debug_package %{nil}

%description
This package provides the %{kmod_name} kernel module(s).
It is built to depend on the specific ABI provided by a range of releases
of the same variant of the Linux kernel and not on any one specific build.

%prep
%setup -q -n %{kmod_name}-%{version}
echo "override %{kmod_name} * weak-updates/%{kmod_name}" > kmod-%{kmod_name}.conf

%build
pushd kernel/linux/ena
%{__make} KSRC=%{_usrsrc}/kernels/%{kversion}
popd

%install
%{__install} -d %{buildroot}/lib/modules/%{kversion}/extra/%{kmod_name}/
%{__install} -d %{buildroot}%{_sysconfdir}/depmod.d/
%{__install} -d %{buildroot}%{_defaultdocdir}/kmod-%{kmod_name}-%{version}/
# We don't have a man page. Thanks a lot Amazon.
%{__install} -d %{buildroot}%{_mandir}/man7/
%{__install} kernel/linux/ena/README %{buildroot}%{_defaultdocdir}/kmod-%{kmod_name}-%{version}/
%{__install} kernel/linux/ena/COPYING %{buildroot}%{_defaultdocdir}/kmod-%{kmod_name}-%{version}/
%{__install} kernel/linux/ena/RELEASENOTES.md %{buildroot}%{_defaultdocdir}/kmod-%{kmod_name}-%{version}/
%{__install} kernel/linux/ena/ena.ko %{buildroot}/lib/modules/%{kversion}/extra/%{kmod_name}/
%{__install} kmod-%{kmod_name}.conf %{buildroot}%{_sysconfdir}/depmod.d/

# Doing a strip, you feel
find %{buildroot} -type f -name \*.ko -exec %{__strip} --strip-debug \{\} \;

# We don't have plans for secure boot since this is AWS. Perl requirement removed.

%post
# This is AWS specific - The names will change to ens192, and the system
# cannot be used anymore. This is to get around that fact.
if [ "$1" -eq "1" ]; then
  %{_grubby} --args="%{_dracutopts}" &>/dev/null
  sed -i -e 's/GRUB_CMDLINE_LINUX="/GRUB_CMDLINE_LINUX="%{_dracutopts} /g' /etc/default/grub
fi ||:

%postun
if [ "$1" -eq "0" ]; then
  %{_grubby} --remove-args='%{_dracutopts}' &>/dev/null
  sed -i -e 's/%{_dracutopts} //g' /etc/default/grub
fi

%clean
%{__rm} -rf %{buildroot}

%changelog
* Thu Mar 23 2017 Louis Abel <tucklesepk@gmail.com> - 1.1.3-2
- Initial build to elrepo specifications

