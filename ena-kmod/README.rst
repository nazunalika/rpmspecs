ena-kmod
^^^^^^^^

This is for the ena AWS driver.

.. contents::

Information
-----------

Why?
++++

There are a few reasons why I built this one. The main one is that at my current job, there is a need and we refuse (or trying to refuse) to use Amazon Linux. Unfortunately, the AMI for CentOS 7 does not have the ena driver, so the throughput is garbage. This kmod is to fulfill a need. The other reason is need to practice my kmod building a bit.

What is the end goal?
+++++++++++++++++++++

The end goal is to create an RPM that follows the Fedora Project RPM guidelines to the maximum possible. This includes, but is not limited to:

* FHS (Filesystem Hierarchy Standard)
* Use of rpmlint to check the rpm for warnings and errors
* Use of mock to build the rpm (it **must** build in mock)
* Use of systemd units for CentOS 7, Fedora, or related (eg, SystemV-style initscripts are forbidden and **should not** be used under any circumstances)
* Use of SystemV-style initscripts or UpStart scripts for CentOS 6 or related if possible
* Use of kmod specs provided by rpmfusion and others

Please see the below for more information. 

`FHS <http://www.pathname.com/fhs/>`_

`Fedora: Fedora Packaging Guidelines <https://fedoraproject.org/wiki/Packaging:Guidelines>`_

`Fedora: How to create an RPM package <https://fedoraproject.org/wiki/How_to_create_an_RPM_package>`_

`RPM Fusion: Kmods2 <https://rpmfusion.org/Packaging/KernelModules/Kmods2>`_

But why an RPM?
+++++++++++++++

You should **never** compile on a package based system. It does not matter if it's RPM based (Red Hat, Fedora, CentOS, SuSE) or DEB based (Debian, Ubuntu). 

This RPM is to help others who wish to run the ena driver on their AWS CentOS 7 machines.

Why don't you support EL6?
++++++++++++++++++++++++++

This release is for EL6 only. EL6 starts phase 3 in May of 2017 and because my current job no longer builds EL6 machines, I have decided to ignore supporting the driver for that that release.

Do you have a repository that I can install your RPM?
+++++++++++++++++++++++++++++++++++++++++++++++++++++

Yes, I do.

`Copr <https://copr.fedorainfracloud.org/coprs/nalika/>`_ 

Did you make any changes to the code?
+++++++++++++++++++++++++++++++++++++

Simple answer: No.

Long answer: If you review my spec file, you will find that I do not modify the source code of the ena driver.

So what did you change?
+++++++++++++++++++++++

I ensured that the kmod can be used with any kernel version without recompiling.

**Notice: No code changes are made.**

What if I want custom options?
++++++++++++++++++++++++++++++

Go ahead and take my spec file and modify it to your needs. I doubt you'll need to change anything.

Do you support the driver?
++++++++++++++++++++++++++

I do not support the driver.

Wait... someone already has an RPM spec... why are you making your own?
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

They made it overcomplicated. WAY overcomplicated. And they didn't take into account name changes on the interfaces in EL7.

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
* Download the tar file from AWS
* Alternatively, download the RPM source from my copr
* Setup your tree for your build account if needed: rpmdev-setuptree
* Place the files in the appropriate directories under ~/rpmbuild (all source files for the rpm go to SOURCES, .spec goes to SPECS)

  * Source files (from this git and ena site) go in ~/rpmbuild/SOURCES
  * Spec files (from this git) go in ~/rpmbuild/SPECS

* rpmbuild -bs ~/rpmbuild/SPECS/ena-kmod.spec
* mock -r dist-7-x86_64 ~/rpmbuild/SRPMS/ena-kmod-*.src.rpm 

.. rubric:: Footnotes

