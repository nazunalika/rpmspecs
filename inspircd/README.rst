inspircd
^^^^^^^^

This is for the popular InspIRCd server.

.. contents::

Information
-----------

Why?
++++

To be honest, I'm continuing my want to package ircd's and continuing my practice at RPM's. And compared to unrealircd, this so much easier to build, install, and configure. Plus, unlike other ircd's, it is not based on anothe daemon. It's built from the ground up. The RPM that the inspircd folks provide show no signs of a spec file and thus, it more than likely does not follow the fedora packaging guidelines. 

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

This RPM is to help others who wish to run the latest InspIRCd on their CentOS or Fedora machines without compiling it themselves.

Why are you trying to support CentOS 6 still?
+++++++++++++++++++++++++++++++++++++++++++++

Please read my main rpmspecs FAQ for this answer, and other answers to general RPM questions you may have.

Do you have a repository that I can install your RPM?
+++++++++++++++++++++++++++++++++++++++++++++++++++++

Yes, I do.

`Copr <https://copr.fedorainfracloud.org/coprs/nalika/>`_ 

Did you make any changes to the code?
+++++++++++++++++++++++++++++++++++++

Simple answer: No.

Long answer: If you review my spec file, you will find that I do not modify the source code of InspIRCd. I make simple changes their example config files.

So what did you change?
+++++++++++++++++++++++

These are the things that differ from a regular compiled version of InspIRCd:

* Software compiled and installed according to the Fedora Packaging Guidelines
* Separate plugins package made with all available modules from the modulemanager [#f4]_
* Compiled with almost all extras (gnutls, mssql, and stdlib are excluded) [#f1]_
* Compiled using epoll
* logrotate configuration provided
* Enterprise Linux 6: initscript created [#f2]_

  * initscript contains basic service functions from the inspircd script 
  * initscript complies and works with /etc/rc.d/init.d/functions

* Enterprise Linux 7: systemd unit created
* Enterprise Linux 7: utility script created to compensate for lack of initscript
* Custom README in /usr/share/doc/inspircd that details the above and other information
* Simple changes to their example configuration files (eg, inspircd.conf.example and modules.conf.example)

**Notice: No code changes are made.**

What if I want custom options?
++++++++++++++++++++++++++++++

Go ahead and take my spec file and modify it to your needs. I cannot imagine you'd want to make many changes as almost all extras were compiled in for an extras package.

Do you support the software?
++++++++++++++++++++++++++++

In this instance, I do not provide support for this software. Please view the InspIRCd `documentation <https://wiki.inspircd.org/>`_. If you, however, feel that there is a problem with the packaging or other issues because of how it was built, please do not hesitate to open an issue and I will investigate with you. As long as we do not have to make code changes or patches to the actual code, then we should be fine. I'm trying to avoid making changes to their source code directly.

I do not know if inspircd will support you directly since this is packaged. I have not looked far into their documentation, but it appears they may be ok with it, since they mention "if you are packaging" at one point. However, their "configure" scripts hint that non-interactive builds are not supported at all (and also probably because I made my own init scripts, systemd units/wrappers to handle the service, which I will be changing soon). This tells me they won't bother supporting you as a result.

I suggest try compiling it by hand on another server (preferrably on a sandbox) to replicate any issue you have and see if the issue also occurs, using similar configure options I have used. If the issue can be reproduced, you can probably try to ask them for support. If you can't, open an issue here and I will work with you. **You may not be the only one that has issues, so it's important that we work together to ensure most, if not all potential problems are resolved.**

I can't get the service to start?
+++++++++++++++++++++++++++++++++

The service not coming up usually is due to not having a configuration in /etc/inspircd. I highly recommend grabbing an "example" configuration and setting up a testnet. Their examples are heavily commented and have very useful information. **Do not skip any of it.**

A good way to troubleshoot is to run sudo -u inspircd /usr/bin/inspircd -nofork. This will tell you if there's actual problems. You can also view journalctl -u inspircd if on a systemd system. If you are interested in the debug functions that inspircd has: sudo -u inspircd /usr/libexec/inspircd/inspircd

I highly recommend reading the inspircd `documentation <https://wiki.inspircd.org/Introduction>`_.

Wait... they already have an RPM... why are you making your own?
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

A few reasons. Let's start with a couple of obvious ones.

* There are no spec files or source RPM files they have
* There source code indicate no obvious spec files or build path for how they build their RPM (it is somewhat clear that they may use mock)
* Their systemd unit from their RPM uses forking, when it clearly can be used as "simple" [#f3]_

Because of these reasons, I am continuing to work with this RPM and provide it in copr for other users who use Fedora and CentOS. 

I can't get this to build. Help?
++++++++++++++++++++++++++++++++

Ensure you are using mock and that your .rpmmacros are setup correctly. The common channels on freenode will ask if you're using mock, and if you're not, 'why?' and suggest you to. See rpmdev-setuptree.

Do you support other architectures/Can it build in $ARCH architecture?
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

I only have x86 systems, so I'm unable to try it out on ARM, PPC64, etc. However, if you want to take my srpm and try, go for it. I would love to see the results. If it works, I will add the architecture to the copr repo (if available).

I do plan on getting a raspberry pi at some point, which is ARM, and trying my hand at building it there. But that's in the future.

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
* Download the tar file from `their git <https://github.com/inspircd/inspircd/releases>`_
* Download or clone the inspircd-extras repo, rename the directory to inspircd-extras-0.0.0+git$(date +%s)$COMMIT

  * To get $COMMIT, you must clone the repo, go into the directory and run git describe HEAD --always

* tar czvf inspircd-extras-0.0.0+git$(date +%s)$COMMIT.tar.gz inspircd-extras-0.0.0+git$(date +%s)$COMMIT
* Change the extras_version variable in the spec file accordingly
* Alternatively, you can download my source RPM from my copr.
* Setup your tree for your build account if needed: rpmdev-setuptree
* Place the files in the appropriate directories under ~/rpmbuild (all source files for the rpm go to SOURCES, .spec goes to SPECS)

  * Source files (from this git and inspircd site) go in ~/rpmbuild/SOURCES
  * Spec files (from this git) go in ~/rpmbuild/SPECS

* rpmbuild -bs ~/rpmbuild/SPECS/inspircd.spec
* mock -r dist-X-arch ~/rpmbuild/SRPMS/inspircd-*.src.rpm 

  * Replace dist with fedora or epel
  * Replace X with version number 6 or 7
  * Replace arch with your appropriate architecture

Todo List
---------

Yes, I have a todo list. 

* Provide a working (albeit, insecure) configuration so service can run immediately on installation

  * This includes utilizing /etc/pki/tls/certs/make-dummy-cert to make a dummy certificate
  * This includes copying a configuration, motd, rules file that just works with warnings and information
  * This **does not** include removing the "die" lines. [#f5]_

* Branch out some modules into seperate packages
* Enable gnutls support (request by a user who uses my RPM)

.. rubric:: Footnotes

.. [#f1] stdlib could not be compiled on Enterprise Linux 6. I have also assumed because of an older GCC version on Enterprise Linux 7, it won't compile right either. And since I'm aiming to keep compatibility between multiple release versions, I won't make a patch to change c++11 to c++0x for Enterprise Linux. The module compiles, but with warnings that was concerning. I do not want that off chance of a crash or other weird issues to happen as a result of it being compiled into the build. Because of this, tre, pcre2, and posix are the regex engines implemented in this release. Also, for GnuTLS, why would you want to use that? Why would you even allow it to be an option? The fact they recommend it (because "performance") is a problem, in my opinion.
.. [#f2] Majority of their scripts and things they do is all in perl. I'm all for perl, don't get me wrong. Having the configure script as perl was one thing, and I was able to understand what they were doing when I reviewed it. However, their "script" that gets generated after running `make' was meant to be in /etc/rc.d/init.d, and it wasn't exactly the prettiest thing I've seen. To ensure that it works properly with the init system of RHEL 6, I rewrote it from the ground up. *However* I ensured that I kept their perl script around in case I missed something from their script or if the "developer" functions were needed.
.. [#f3] It's generally a good practice to try to make a service run without forking if at all possible. Using "forking" basically looks like the developer or admin didn't want to try to make the simple mode work. This usually comes down to laziness or not reading the systemd documentation, or even their own man pages. In inspircd's case, there is a --nofork option. However, there are cases that forking must be used. This is not one of them.
.. [#f4] All modules are compiled excluding ones that require c++11/c++0x to be compiled. Those will require the interested party to install the devel package and compile themselves.
.. [#f5] The reason why I won't remove the die lines if I actually configure an example configuration for inspircd, is because the developer(s) of the software want you to actually go through the entire configuration file and read through it. The examples have a lot of comments and explain things in a fair amount of detail. The "die" lines are there to make sure you have read through the documentation enough to have setup your ircd properly. The die lines prevent inspircd from running at all. At first, it'll say that it's deprecated. Systemd will say 4/NOPERMISSION, which is VERY confusing. Once you have read the documentation and removed the "die" lines, it will start up and run without issues.
