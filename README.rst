rpmspecs
^^^^^^^^

These are RPM spec files that I have created over time while working on my own or at various companies. Some of these are for fun, some of them are for reasons usually in the realm of "a customer wanted $x". 

.. contents::

Information
-----------

All of my (better created) RPM specs will be here. 

**Note:** I am not responsible for system damages, break-ins, or faulty code of the software that can cause the formerly listed. Always develop and test in an isolated environment at all times. **Always keep SELinux enabled.**

Frequently Asked Questions
--------------------------

Do you have any SRPMS available?
++++++++++++++++++++++++++++++++

They'll normally be available from my copr builds, if you are interested in making changes and using mock for yourself.

Have any documentation or guides?
+++++++++++++++++++++++++++++++++

If you're starting out rpm packaging, please consider reading the following documentation. The packaging guidelines may seem strict, but they are deemed best practices if you are considering on being a package maintainer (sponsored or not). Keep in mind, **I am always learning**. I am in no way an expert, nor do I claim to be.

`FHS <http://www.pathname.com/fhs/>`_

`Fedora: Fedora Packaging Guidelines <https://fedoraproject.org/wiki/Packaging:Guidelines>`_

`Fedora: How to create an RPM package <https://fedoraproject.org/wiki/How_to_create_an_RPM_package>`_

What you should get from the above is there are specific guidelines that should be followed, for maintainability, portability, and easy review. My RPM specs will have an FAQ of the "purpose". 

Why are you still trying to support CentOS 6?
+++++++++++++++++++++++++++++++++++++++++++++

Multiple reasons. The primary reason is that CentOS 6 still widely used, and will more than likely be the case for a quite a few years. A secondary reason is a fight against systemd, and I respect a user's choice in what distribution they want to use.

**I am in no way against one init system or another. I am just attempting to promote compatibility with other releases for the life of the release.** [#f1]_

When do you stop supporting a particular release?
+++++++++++++++++++++++++++++++++++++++++++++++++

For Enterprise Linux, usually phase 3 of support or at most, a year before the expected EOL date. For Fedora, a month before the expected EOL date. The exception is when a newer major release is pushed later from its expected release.

What if $package cannot be compiled on a release you support?
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This is a good question and is unfortunately somewhat hard to answer.

If an RPM compiles on all releases I support and then doesn't during a version rebase, I typically try to figure out what changed or what I can do to ensure it builds properly, even if this requires logic to separate out the "problem" releases and what they need instead. 

In the case of making patches, I usually dislike making patches, in the case of modifying source code. If a patch has to be made to the source code, I will not provide it in the RPM unless it is a reasonable patch and does not break other releases and can be submitted upstream. 

If it's a patch for the actual build process, then I will provide a patch because it does not modify the source code of the application directly. In the case that no changes can ensure the package will build, I will stop providing support for that release from then on.

Do you have any repositories?
+++++++++++++++++++++++++++++

Yes, I do. I have two, actually. I have a copr and a personal repository. **Please avoid using Super Syrkit as a daily repository. It's not updated fast enough and is horribly disorganized to be used as such. Certain things built will only be in copr. My repository cannot be considered as a trusted source.**

`Copr <https://copr.fedorainfracloud.org/coprs/nalika/>`_

`Super Syrkit <https://syrkit.bromosapien.net/f23>`_

Do you take requests?
+++++++++++++++++++++

I normally don't. But, if what you're asking for doesn't have an RPM or project in copr, I'll consider it based on what it is, and if it fits licensing and guidelines. You can drop me an email or a line here and I will get back to you.

Do you package for other systems?
+++++++++++++++++++++++++++++++++

At this present time, I do not. I have considered packaging for Ubuntu or OpenSUSE. However those, much like Arch, already have plenty of maintainers with tons upon tons of packages (up to date or not) and their own build systems similar to Fedora. So some of the packages you may see here may already exist for those distributions in base or extra repositories they provide.

.. rubric:: Footnotes

.. [#f1] https://wiki.centos.org/About/Product
