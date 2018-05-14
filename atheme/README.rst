atheme
^^^^^^^^

This is for the Atheme IRC Services

.. contents::

Information
-----------


What is the end goal?
+++++++++++++++++++++

The end goal is to create an RPM that follows the Fedora Project RPM guidelines to the maximum possible. This includes, but is not limited to:

* FHS (Filesystem Hierarchy Standard)
* Use of rpmlint to check the rpm for warnings and errors
* Use of mock to build the rpm (it **must** build in mock)
* Use of systemd units for CentOS 7, Fedora, or related (eg, SystemV-style initscripts are forbidden and **should not** be used under any circumstances)
* Use of SystemV-style initscripts or UpStart scripts for CentOS 6 or related if possible

Please see the below for more information. 

`FHS <http://www.pathname.com/fhs/>`_

`Fedora: Fedora Packaging Guidelines <https://fedoraproject.org/wiki/Packaging:Guidelines>`_

`Fedora: How to create an RPM package <https://fedoraproject.org/wiki/How_to_create_an_RPM_package>`_

But why an RPM?
+++++++++++++++

You should **never** compile on a package based system. It does not matter if it's RPM based (Red Hat, Fedora, CentOS, SuSE) or DEB based (Debian, Ubuntu). 

This RPM is to help others who wish to run the latest Atheme on their CentOS or Fedora machines without compiling it themselves.

Why are you trying to support CentOS 6 still?
+++++++++++++++++++++++++++++++++++++++++++++

Please read my main rpmspecs FAQ for this answer.

Do you have a repository that I can install your RPM?
+++++++++++++++++++++++++++++++++++++++++++++++++++++

Yes, I do.

`Copr <https://copr.fedorainfracloud.org/coprs/nalika/>`_ 

Did you make any changes to the code?
+++++++++++++++++++++++++++++++++++++

Simple answer: No.

Long answer: If you review my spec file, you will find that I do not modify the source code of Atheme. 

So what did you change?
+++++++++++++++++++++++

These are the things that differ from a regular compiled version of Atheme:

* Software compiled and installed according to the Fedora Packaging Guidelines
* logrotate configuration provided
* Enterprise Linux 6: initscript created

  * initscript complies and works with /etc/rc.d/init.d/functions

* Enterprise Linux 7: systemd unit created

**Notice: No code changes are made.**

What if I want custom options?
++++++++++++++++++++++++++++++

Go ahead and take my spec file and modify it to your needs.

Do you support the software?
++++++++++++++++++++++++++++

In this instance, I do not provide support for this software. If you, however, feel that there is a problem with the packaging or other issues because of how it was built, please do not hesitate to open an issue and I will investigate with you. As long as we do not have to make code changes or patches to the actual code, then we should be fine. I'm trying to avoid making changes to their source code directly.

I do not know if atheme will support you directly since this is packaged. It appears they may be fine with it, as long as you can show the compilation options. Either way, I suggest try compiling it by hand on another server (preferrably on a sandbox) to replicate any issue you have and see if the issue also occurs, using similar configure options I have used. If the issue can be reproduced, you can probably try to ask them for support. If you can't, open an issue here and I will work with you. **You may not be the only one that has issues, so it's important that we work together to ensure most, if not all potential problems are resolved.**

I can't get the service to start?
+++++++++++++++++++++++++++++++++

The service not coming up usually is due to not having a configuration in /etc/atheme. I highly recommend grabbing an "example" configuration. Their examples are very well commented. If you have grabbed an example configuration and still cannot get the service to start, ensure you have configured atheme correctly. The on-screen errors or errors in the logs will tell you what the direct problem is.

You can view the logs in: /var/log/atheme or journalctl -u atheme

I can't get this to build. Help?
++++++++++++++++++++++++++++++++

Ensure you are using mock and that your .rpmmacros are setup correctly. The common channels on freenode will ask if you're using mock, and if you're not, 'why?' and suggest you to. See rpmdev-setuptree.

Do you support other architectures/Can it build in $ARCH architecture?
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

I only have x86 systems, so I'm unable to try it out on ARM, PPC64, etc. However, if you want to take my srpm and try, go for it. I would love to see the results. If it works, I will add the architecture to the copr repo (if available).

I'd like to contribute to this or make a change...
++++++++++++++++++++++++++++++++++++++++++++++++++

Go ahead. I'll more than likely approve it. I appreciate all the help I can get to ensure this software works while reaching to the maximum of the Fedora RPM Guidelines.

Build Process
-------------

Packages
++++++++

* Ensure you have the following installed: 

  * rpm-build
  * rpmdevtools
  * rpmlint
  * mock (CentOS: epel)

Build
+++++

* Download the build files in this git
* Download the tar file from `their git <https://github.com/atheme/atheme/releases>`_
* Alternatively, you can download my source RPM from my copr.
* Setup your tree for your build account if needed: rpmdev-setuptree
* Place the files in the appropriate directories under ~/rpmbuild (all source files for the rpm go to SOURCES, .spec goes to SPECS)

  * Source files (from this git and atheme site) go in ~/rpmbuild/SOURCES
  * Spec files (from this git) go in ~/rpmbuild/SPECS

* rpmbuild -bs ~/rpmbuild/SPECS/atheme.spec
* mock -r dist-X-arch ~/rpmbuild/SRPMS/atheme-*.src.rpm 

  * Replace dist with fedora or centos
  * Replace X with version number 6 or 7
  * Replace arch with your appropriate architecture

