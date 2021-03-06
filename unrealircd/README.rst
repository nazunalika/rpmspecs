UnrealIRCd
^^^^^^^^^^

This is for the popular UnrealIRCd software. 

.. contents::

Information
-----------

Why?
++++

So you want to know **why** I made this one in particular. Here's a list of reasons. It comes down to this:

* Original RPM built by another user is for version 3.2.10.2
* Original RPM, even though it was built for CentOS 7, was still using an init script (no attempt to work with systemd)
* Original RPM was in EPEL at one point and isn't any longer.
* Original RPM allowed the software to package it's own libraries. [#f4]_
* No one has made an RPM for the 4.x series

Those are the main reasons why I started this. The supplementary reasons come down to my want to continue to practice on building RPM's.

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

This RPM is to help others who wish to run the latest UnrealIRCd on their CentOS or Fedora machines without compiling themselves or going through the "Config" annoyance.

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

Long answer: If you review my spec file, you will find that I do not modify the source code of UnrealIRCd. You will also notice that I do not have the UnrealIRCd source in my repository. The only changes I made were adding my own scripts and utilities to replace the functionality of a poorly designed script generated by the make process. See the next section. [#f3]_

So what did you change?
+++++++++++++++++++++++

These are the things that differ from a regular compiled version of UnrealIRCd:

* Software compiled and installed according to the Fedora Packaging Guidelines
* logrotate configuration provided
* Enterprise Linux 6: initscript created

  * initscript contains most functions unrealircd script
  * initscript complies and works with /etc/rc.d/init.d/functions

* Enterprise Linux 7: systemd unit created
* Enterprise Linux 7: utility script created to compensate for lack of initscript and unrealircd functions
* Custom README in /usr/share/doc/unrealircd that details the above and other information

**Notice: No code changes are made.**

What if I want custom options?
++++++++++++++++++++++++++++++

Go ahead and take my spec file and modify it to your needs. Example, with --with-fd-setsize, if you are expecting more than 1024 connections, increase it. 1024 seemed sane enough to me. If you increase it, you will need to adjust your ulimits accordingly for the unrealircd user. You can do this in: /etc/security/limits.conf

Do you support the software?
++++++++++++++++++++++++++++

In this instance, I do not provide support for this software. Please view the UnrealIRCd `documentation their website <https://www.unrealircd.org/docs/UnrealIRCd_4_documentation>`_. If you, however, feel that there is a problem with the packaging or other issues because of how it was built, please do not hesitate to open an issue and I will investigate with you. As long as we do not have to make code changes or patches to the actual code, then we should be fine. I'm trying to avoid making changes to their source code directly.

As a note, UnrealIRCd support forums **will not support you** because you are using a packaged version they are not providing (assuming it's a dead giveaway). They completely insist on compiling *everything* at all times. Even if you compiled it yourself and made your own systemd unit, they will automatically assume it came from a package. 

My suggestion, is if you're going to open an issue here or a forum post with them to troubleshoot, try to replicate your issue by compiling the software in a sandbox environment by hand and running it the recommended way they expect everyone to do. If you can replicate it, then I would ask them for help. If you are unable to replicate it, open an issue with me.

Wait, unrealircd won't support me? Why?
+++++++++++++++++++++++++++++++++++++++

There are a few reasons for this. Here are some that I can think of at the time of this writing.

* It's a packaged version from someone who does not develop the software.

  * Because of this, it is considered untrusted.
  * Because of this, it is considered "modified" as they do not know if patches or changes were made to their code [#f2]_

* I'm blatantly ignoring ./Config, and jumping to configure in the %build section [#f1]_
* I'm blatantly ignoring make install and doing the deployment method by hand in the %install section [#f1]_
* I'm providing a startup method that they do not support or provide (init and systemd)

I can't get the service to start?
+++++++++++++++++++++++++++++++++

There are a couple of "issues" I've ran into when trying to get the service to come up. Here are some reasons why the service may not come up right away.

  * /tmp has mount settings like noexec (why it insists on deploying to some tmp directory in the first place, I do not know)
  * You are missing /etc/unrealircd/unrealircd.conf (it will tell you this)
  * You have "bad" directives or settings in your /etc/unrealircd.conf

The best way to troubleshoot is to run sudo -u unrealircd /usr/bin/unrealircd. This will tell you if there's actual problems. You can also view journalctl -u unrealircd.

Before, I had an issue with making the systemd service work properly. I had to create a wrapper script in /usr/libexec/unrealircd to get around an issue that is created by the unrealircd developers. Essentially, using SuccessExitCode=255 will never allow the user to see if there's an issue starting up the service. This isn't an issue if it's forking. However, I'm trying to avoid forking where possible. [#f5]_

If you are having similar issues on Enterprise Linux 6, the terminal will tell you the error immediately. It's usually the things listed above.

I can't get this to build. Help?
++++++++++++++++++++++++++++++++

Ensure you are using mock and that your .rpmmacros are setup correctly. The common channels on freenode will ask if you're using mock, and if you're not, 'why?' and suggest you to. See rpmdev-setuptree.

Do you support other architectures/Can it build in $ARCH architecture?
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

I only have x86 systems, so I'm unable to try it out on ARM, PPC64, etc. However, if you want to take my srpm and try, go for it. I would love to see the results. If it works, I will add the architecture to the copr repo (if available).

How do you handle plugins?
++++++++++++++++++++++++++

I have multiple subpackages that get built along with unrealircd, to ensure they are built altogether and installed on a as-needed basis. I have provided a -devel package if you plan on building your own modules as well or have others you wish to compile against this.

**Special Note:** If you plan on doing your own build by taking my spec here, you will need to set the "build_with_plugins" to 0, otherwise you WILL be required to download every plugin that I build with unrealircd to get the sources. This will be much easier if you grab my srpm by itself. This is especially the case since the plugins do not get updated very often. For this git, by default, I have set that option to 0. 

The plugins I have built with this RPM are below.

* AntiRandom
* TextBan
* NoCodes
* PrivDeaf
* JumpServer
* m_ircops
* m_staff
* m_banlink

The versions of the plugins are "skewed" in that they match the version of UnrealIRCd. At some point, I'll fix this unless someone else does first.

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
* Download the tar file from `their website <http://www.unrealircd.com/>`_
* Alternatively, you can download my source RPM from my copr.
* Setup your tree for your build account if needed: rpmdev-setuptree
* Place the files in the appropriate directories under ~/rpmbuild (all source files for the rpm go to SOURCES, .spec goes to SPECS)

  * Source files (from this git and unrealircd site) go in ~/rpmbuild/SOURCES
  * Spec files (from this git) go in ~/rpmbuild/SPECS

* rpmbuild -bs ~/rpmbuild/SPECS/unrealircd.spec
* mock -r dist-X-arch ~/rpmbuild/SRPMS/unrealircd-*.src.rpm 

  * Replace dist with fedora or centos
  * Replace X with version number 6 or 7
  * Replace arch with your appropriate architecture

.. rubric:: Footnotes

.. [#f1] Three things. 1) In an attempt to follow the FHS, you have to make sure files and folders are set to sane permissions on top of putting files and folders in sane locations. 700 and 600 for directories and files respectively is not sane. That would be sane for say, /etc/unrealircd where the configs sit, but not somewhere like /usr/bin where it's 755. 2) They don't give you a way to really set the directory locations from their ./Config. And even if you do, the "hard coded" permissions in their Makefile will break an already existing directory. 3) Their make install ignores DESTDIR, which is normally used by the %make_install macro in an rpm spec. 
.. [#f2] No changes were made to their source code. Any changes would be submitted upstream first according to their coding guidelines. I am not a programmer, nor do I claim to be, so this won't happen in my case.
.. [#f3] This is because the "wrapper" is supposed to be used to start, stop, or make configuration changes to Unreal. However, the init script *and* systemd unit avoid this file. Because of how systemd handles its pid information compared to UpStart/SystemV/systemd forking, this file had to be modified to compensate. 
.. [#f4] As far as I know, this is considered bad practice. Refer to the Fedora Packaging Guidelines.
.. [#f5] They call exit(-1) constantly. So, if the server crashes? Error 255. The server doesn't come up right? 255. The server is shutting down gracefully? 255. I'm not sure why this is considered "sane" at all. But I'm not a programmer, so it's something I cannot completely comment on.
