%define name pvm
%define version 3.4.6
%define release %mkrel 2
%define pvmpath %{_datadir}/pvm3
%define xpvmpath %{name}3/xpvm

Summary:	Parallel Virtual Machine (PVM)
Name: 		%name
Version: 	%version
Release: 	%release
License:	GPL
Group:		System/Cluster
Source0:	%{name}%{version}.tar.bz2
Source1:	%{name}d.init
Source2:	ftp://www.netlib.org/pvm3/book/%{name}-book.ps
Source5:	.bashrc.pvm
Source6:	.bash_profile
Source7:	genpubkey
Source8:	sendPublicKeyToHosts
Source9:	pvm.sh
Patch0:		%{name}-aimk.patch
Patch1:		%{name}-noenv.patch
Patch3:		xlibdir.patch
Patch4:		pvm3-gcc4.diff
Patch5:		pvm-ia64.patch
Patch6:		pvm-ia64-1.patch
Patch7:		pvm-ia64-2.patch
URL:		http://www.epm.ornl.gov/pvm/pvm_home.html
BuildRequires:	ncurses-devel >= 5.0
BuildRequires:	readline-devel
BuildRequires:	m4
BuildRequires:	tcl
BuildRequires:	tcl-devel
BuildRequires:	tk
BuildRequires:	tk-devel
Requires: 	initscripts >= 5.54
Requires: 	bash >= 2
Requires: 	shadow-utils
Requires: 	openssh-server
Requires: 	openssh-clients

%define		_pvm_root 	/usr/share/%{name}3

%ifarch x86_64
%define		_pvm_arch	LINUX64
%else
%ifarch %{ix86}
%define		_pvm_arch	LINUX
%else
%ifarch alpha
%define		_pvm_arch	LINUXALPHA
%else
%ifarch sparc sparc64
%define		_pvm_arch	LINUXSPARC
%else
%ifarch ppc
%define		_pvm_arch	LINUXPPC
%else
%ifarch hppa
%define		_pvm_arch	LINUXHPPA
%else
%ifarch ia64
%define         _pvm_arch       LINUX64
%else
%error "Unsupported architecture"
exit 1
%endif
%endif
%endif
%endif
%endif
%endif
%endif
%define pvmlib %{pvmpath}/lib/%{_pvm_arch}


%description
PVM is a software system that enables a collection of heterogeneous
computers to be used as a coherent and flexible concurrent
computational resource.

The individual computers may be shared- or local-memory
multiprocessors, vector supercomputers, specialized graphics engines,
or scalar workstations, that may be interconnected by a variety of
networks, such as ethernet, FDDI.

User programs written in C, C++ or Fortran access PVM through library
routines.

%package -n lib%{name}-devel
Summary:	PVM header files and static libraries
Group:		Development/Other
Requires:	%{name} = %{version}

%description -n lib%{name}-devel
This package contains PVM header files and static libraries.

%package examples
Summary:	PVM examples
Group:		System/Cluster
Requires:	lib%{name}-devel = %{version}

%description examples
This package contains PVM examples written in C and Fortran, and book
written in English.


%package xpvm
Summary:	A graphical interface for pvm
Group:		Monitoring
Requires:	%{name} = %{version}
Source3:	xpvm.src.1.2.5.tar.bz2
Source4:	xpvm.userguide.bz2
Group:          Development/Other
Url:            http://www.netlib.org/pvm3/
Requires:       pvm, tcl, tk
BuildRequires:	X11-devel, tk, tcl

%description xpvm
XPVM is a graphical console and monitor for PVM. It provides a
graphical interface to the PVM console commands and information,
along with several animated views to monitor the execution of PVM
programs.  These views provide information about the interactions
among tasks in a parallel PVM program, to assist in debugging and
performance tuning.

%prep 
%setup -q -n pvm3
ln -sf ${RPM_BUILD_DIR}/pvm3 ${RPM_BUILD_DIR}/%{name}-%{version}
%setup -q -T -D -a 3

%patch0 -p1
%patch1 -p1
#%patch2 -p1
%patch3 -p1
%patch4 -p1

%ifarch ia64
%patch5 -p1
%patch6 -p1
#%patch7 -p0
%endif

%ifarch x86_64
%patch5 -p1
%patch6 -p1
#%patch7 -p0
%endif

%build
cp -f lib/aimk lib/aimk.tmp
export PVM_ARCH=%_pvm_arch
sed -e "s!@PVM_ROOT@!%{_pvm_root}!" -e "s!@PVM_ARCH@!%{_pvm_arch}!" lib/aimk.tmp > lib/aimk
PCFLOPTS="-DDEFBINDIR=\\\"%{_pvm_root}/lib/$PVM_ARCH\\\""
PCFLOPTS="$PCFLOPTS -DDEFDEBUGGER=\\\"%{_pvm_root}/lib/debugger2\\\""
PCFLOPTS="$PCFLOPTS -DPVMDPATH=\\\"%{_pvm_root}/lib/%{_pvm_arch}/pvmd3\\\""
PCFLOPTS="$PCFLOPTS -DPVMROOT=\\\"%{_pvm_root}\\\" -fPIC -DUSE_INTERP_RESULT"
export PVM_ROOT=`pwd` 

make CFLOPTS="$PCFLOPTS"

XPVM_ROOT=${PVM_ROOT}/xpvm
export XPVM_ROOT=${XPVM_ROOT}
export PVM_ROOT=${PVM_ROOT}
# (tv) fix build with tcl-8.5:
perl -pi -e 's!(-lt(cl|k)8).[40]!\1.6!' $XPVM_ROOT/src/Makefile.aimk*
%ifarch x86_64
make -C ${XPVM_ROOT} CFLOPTS="$PCFLOPTS" XLIBDIR="-L /usr/X11R6/lib64"
%else
make -C ${XPVM_ROOT} CFLOPTS="$PCFLOPTS"
%endif

%install
mkdir -p %{buildroot}%{_pvm_root}/lib/%{_pvm_arch}
mkdir -p %{buildroot}/var/run/pvm3
mkdir -p %{buildroot}%{_pvm_root}/conf

install -d %{buildroot}{%{_bindir},%{_includedir},%{_libdir},%{_pvm_root}/conf,%{_docdir}/%{name}} \
	%{buildroot}/%{name}/{examples,gexamples,hoster,misc,tasker,xep} \
	%{buildroot}{%{_mandir}/man{1,3},/etc/rc.d/init.d,%{_sbindir}} \
	%{buildroot}/%{_sysconfdir}/profile.d

install %{SOURCE1}  %{buildroot}/etc/rc.d/init.d/pvm
install lib/%{_pvm_arch}/{pvm,pvmgs} %{buildroot}%{_pvm_root}/lib/%{_pvm_arch}
install lib/%{_pvm_arch}/pvmd3 %{buildroot}%{_pvm_root}/lib/%{_pvm_arch}
install lib/pvm		%{buildroot}%{_pvm_root}
install lib/debugger	%{buildroot}%{_pvm_root}/lib
install lib/debugger2	%{buildroot}%{_pvm_root}/lib
install lib/pvmgetarch	%{buildroot}%{_pvm_root}/lib
install lib/pvmtmparch	%{buildroot}%{_pvm_root}/lib
install lib/aimk	%{buildroot}%{_pvm_root}/lib
install lib/pvmd	%{buildroot}%{_pvm_root}/lib
install conf/%{_pvm_arch}.def %{buildroot}%{_pvm_root}/conf
install include/{fpvm3,pvm3,pvmproto,pvmtev}.h %{buildroot}%{_includedir}
install lib/%{_pvm_arch}/lib*.a %{buildroot}%{pvmlib}
install man/man1/* %{buildroot}%{_mandir}/man1
install man/man3/* %{buildroot}%{_mandir}/man3
install %{SOURCE5} %{buildroot}%{_pvm_root}/.bashrc
install %{SOURCE6} %{buildroot}%{_pvm_root}
install %{SOURCE7} %{buildroot}%{_pvm_root}
install %{SOURCE8} %{buildroot}%{_pvm_root}
install -m 755 %{SOURCE9} %{buildroot}%{_sysconfdir}/profile.d
touch %{buildroot}%{_pvm_root}/pvmhosts

# Examples
mkdir -p %{buildroot}%{_docdir}/%{name}/source
mv $RPM_BUILD_DIR/pvm3/examples %{buildroot}%{_docdir}/%{name}/source
mv $RPM_BUILD_DIR/pvm3/gexamples %{buildroot}%{_docdir}/%{name}/source
mv $RPM_BUILD_DIR/pvm3/hoster %{buildroot}%{_docdir}/%{name}/source
mv $RPM_BUILD_DIR/pvm3/misc %{buildroot}%{_docdir}/%{name}/source
mv $RPM_BUILD_DIR/pvm3/tasker %{buildroot}%{_docdir}/%{name}/source
mv $RPM_BUILD_DIR/pvm3/xep %{buildroot}%{_docdir}/%{name}/source
install %{SOURCE2}  %{buildroot}%{_docdir}/%{name}/pvm-book.ps
gzip -9nf %{buildroot}%{_docdir}/%{name}/pvm-book.ps

#xpvm
install -d %{buildroot}/usr/X11R6/bin
install -m 0755 $RPM_BUILD_DIR/%{xpvmpath}/src/%{_pvm_arch}/xpvm %{buildroot}%{_bindir}
LIBDIR=/usr/X11R6/lib/xpvm
install -d -m 755 %{buildroot}$LIBDIR
install -d -m 755 %{buildroot}$LIBDIR/src
install -d -m 755 %{buildroot}$LIBDIR/src/xbm
install -d -m 755 %{buildroot}$LIBDIR/src/help
install -m 0644 $RPM_BUILD_DIR/%{xpvmpath}/*.tcl %{buildroot}$LIBDIR
install -m 0644 $RPM_BUILD_DIR/%{xpvmpath}/src/xbm/*.xbm %{buildroot}$LIBDIR/src/xbm
install -m 0644 $RPM_BUILD_DIR/%{xpvmpath}/src/help/*.help %{buildroot}$LIBDIR/src/help
install -m 0644 $RPM_BUILD_DIR/%{xpvmpath}/README .
install -m 0644 %{SOURCE4} .


%pre
/usr/sbin/groupadd -g 12385 -r -f pvm > /dev/null 2>&1 ||:
#/usr/sbin/useradd -u 12385 -g pvm -d /usr/share/pvm3 -r -s /bin/bash pvm -p "" > /dev/null 2>&1 ||:

%postun
/usr/sbin/userdel pvm

%preun
#%_preun_service pvm

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_initrddir}/pvm
%config(noreplace) %{_sysconfdir}/profile.d/pvm.sh
#%dir %{_pvm_root}
#%dir %{_pvm_root}/lib
%attr(755,root,pvm) %{_pvm_root}/lib/debugger
%attr(755,root,pvm) %{_pvm_root}/lib/debugger2
%attr(755,root,pvm) %{_pvm_root}/lib/pvmgetarch
%attr(755,root,pvm) %{_pvm_root}/lib/pvmtmparch
%attr(755,root,pvm) %{_pvm_root}/pvm
%attr(755,root,pvm) %{_pvm_root}/lib/%{_pvm_arch}/pvmd3
%attr(755,root,pvm) %{_pvm_root}/lib/%{_pvm_arch}/pvm
%attr(755,root,pvm) %{_pvm_root}/lib/%{_pvm_arch}/pvmgs
%attr(644,root,pvm) %{_pvm_root}/pvmhosts
%attr(755,root,pvm) %{_pvm_root}/lib/pvmd
%dir %attr(775,root,pvm) /var/run/pvm3
%dir %attr(775,root,pvm) %{_pvm_root}
%attr(644,root,pvm) %{_pvm_root}/.bashrc
%attr(644,root,pvm) %{_pvm_root}/.bash_profile
%attr(755,root,pvm) %{_pvm_root}/genpubkey
%attr(755,root,pvm) %{_pvm_root}/sendPublicKeyToHosts
%attr(644,root,pvm) %{_pvm_root}/conf/%{_pvm_arch}.def
%{_mandir}/man1/*
%exclude %{_mandir}/man1/aimk.1*
%exclude %{_pvm_root}/conf

%files -n lib%{name}-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_pvm_root}/lib/aimk
%attr(755,root,pvm) %{_pvm_root}/conf
%attr(755,root,pvm) %{_includedir}/fpvm3.h
%attr(755,root,pvm) %{_includedir}/pvm3.h
%attr(755,root,pvm) %{_includedir}/pvmproto.h
%attr(755,root,pvm) %{_includedir}/pvmtev.h
%attr(755,root,pvm) %{pvmlib}/*.a
%{_mandir}/man1/aimk.1*
%{_mandir}/man3/*

%files examples
%defattr(644,root,root,755)
%{_docdir}/%{name}

%files xpvm
%defattr(-,root,root)
%doc xpvm.userguide.bz2 README
%attr(755,root,root) %{_bindir}/xpvm
%attr(755,root,root) /usr/X11R6/lib/xpvm



%changelog
* Tue Dec 07 2010 Oden Eriksson <oeriksson@mandriva.com> 3.4.6-2mdv2011.0
+ Revision: 614627
- the mass rebuild of 2010.1 packages

  + Antoine Ginies <aginies@mandriva.com>
    - remove old source

* Mon Feb 08 2010 Antoine Ginies <aginies@mandriva.com> 3.4.6-1mdv2010.1
+ Revision: 502371
- remove path7 (already done in pvm3.4.6); version 3.4.6

* Tue Sep 15 2009 Thierry Vignaud <tv@mandriva.org> 3.4.5-11mdv2010.0
+ Revision: 441968
- rebuild

* Tue Mar 03 2009 Guillaume Rousse <guillomovitch@mandriva.org> 3.4.5-10mdv2009.1
+ Revision: 347778
- fix build against tcl/tk 8.6
- drop useless patch

* Fri Aug 01 2008 Thierry Vignaud <tv@mandriva.org> 3.4.5-9mdv2009.0
+ Revision: 259370
- rebuild

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 3.4.5-8mdv2009.0
+ Revision: 247245
- rebuild

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 3.4.5-6mdv2008.1
+ Revision: 136445
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - buildrequires X11-devel instead of XFree86-devel

* Fri Sep 07 2007 Anssi Hannula <anssi@mandriva.org> 3.4.5-6mdv2008.0
+ Revision: 82070
- drop prereq
- rebuild for new soname of tcl

* Fri Jun 22 2007 Thierry Vignaud <tv@mandriva.org> 3.4.5-5mdv2008.0
+ Revision: 43196
- fix build with tcl-8.5
- fix group
- fix group


* Wed Jan 04 2006 Erwan Velu <erwan@seanodes.com> 3.4.5-4mdk
- Using mkrel
- Removing uggly %%post I made, using profile.d/pvm.sh

* Wed Jan 04 2006 Oden Eriksson <oeriksson@mandriva.com> 3.4.5-3mdk
- rebuilt against new net-snmp with new major (10)

* Wed Jan 04 2006 Oden Eriksson <oeriksson@mandriva.com> 3.4.5-2mdk
- rebuilt against soname aware deps (tcl/tk)
- fix deps
- added one gcc4 patch by debian (P4)

* Tue Mar 29 2005 Erwan Velu <erwan@seanodes.com> 3.4.5-1mdk
- 3.4.5
- Cleaning arch LINUXX86_64 -> LINUX64
- Fixing Buildrequires
- TODO: Removing crappy bashrc workaround

* Thu Sep 23 2004 Olivier Blin <blino@mandrake.org> 3.4.4-26mdk
- do not erase content of the PATH environment variable

* Fri Feb 27 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 3.4.4-25mdk
- Fix some DIRM (distlint)

* Wed Feb 25 2004 Erwan Velu <erwan@mandrakesoft.com> 3.4.4-24mdk
- Rebuild

* Thu Feb 19 2004 Erwan Velu <erwan@mandrakesoft.com> 3.4.4-23mdk
- Rebuild against latest tcl/tk

* Wed Jun 18 2003 Erwan Velu <erwan@mandrakesoft.com> 3.4.4-22mdk
- Enabling x86_64

* Thu Jun 12 2003 Antoien Ginies <aginies@mandrakesoft.com> 3.4.4-21mdk
- fix user pb when installing

* Tue Jan 28 2003 Lenny Cartier <lenny@mandrakesoft.com> 3.4.4-20mdk
- rebuild

* Thu Jan 16 2003 Erwan Velu <erwan@mandrakesoft.com> 3.4.4-19mdk
- Rebuild for new glibc

* Thu Jan 09 2003 Erwan Velu <erwan@mandrakesoft.com> 3.4.4-18mdk
- IA64 Support

* Thu Dec 12 2002 Clic-dev <clic-dev-public@mandrakesoft.com> 3.4.4-17mdk
- Fixing wrong right & files in libdevel (Thx to Olivier Lobry)
- Fixing buildrequires
- Fixing missing files

* Mon Aug 26 2002 Erwan Velu <erwan@mandrakesoft.com> 3.4.4-16mdk
- Rebuild

* Tue Aug 06 2002 Antoine Ginies <aginies@mandrakesoft.com> 3.4.4-15mdk
- build with gcc 3.2

* Wed Jul 10 2002 Erwan Velu <erwan@mandrakesoft.com> 3.4.4-14mdk
- Changing exports from /etc/profile to /etc/bashc

* Tue Jul 09 2002 Erwan Velu <erwan@mandrakesoft.com> 3.4.4-13mdk
- Rebuild

* Thu Jul 04 2002 Erwan Velu <erwan@mandrakesoft.com> 3.4.4-12mdk
- Re-enabling rsh support
- Adding group write right to /var/run/pvm3

* Fri Jun 28 2002 Erwan Velu <erwan@mandrakesoft.com> 3.4.4-11mdk
- Fixing update mode (thx to Oden Eriksson)

* Fri Jun 28 2002 Erwan Velu <erwan@mandrakesoft.com> 3.4.4-10mdk
- Removing autostartup of pvm service

* Tue Jun 25 2002 Antoine Ginies <aginies@mandrakesoft.com> 3.4.4-9mdk
- set PVM environement in /etc/profile

* Thu Jun 06 2002 Erwan Velu <erwan@mandrakesoft.com> 3.4.4-8mdk
- Fixing pvm user id
- Fixing package architecture

* Thu Apr 11 2002 Erwan Velu <erwan@mandrakesoft.com> 3.4.4-7mdk
- Fixing genpubkey script

* Tue Apr 09 2002 Erwan Velu <erwan@mandrakesoft.com> 3.4.4-6mdk
- Fixing missing dependencies on openssh
- Autogenerate ssh public key 
- Adding null password to pvm user
- Adding userdel in postun
- Adding script for distributing ssh public key 
- Changing group attribution

* Mon Apr 08 2002 Erwan Velu <erwan@mandrakesoft.com> 3.4.4-5mdk
- Fixing PVM_ROOT export
- Moving libs in devel package

* Thu Mar 07 2002 Erwan Velu <erwan@mandrakesoft.com> 3.4.4-4mdk
- Final rebuild

* Tue Mar 05 2002 Erwan Velu <erwan@mandrakesoft.com> 3.4.4-3mdk
- Adding .bash_profile and .bashrc for user pvm
- Changing rsh to ssh
- Unset export PVM* in pvmd.init : unused before a "daemon --user"
- Fixing stupid arch problems in spec file

* Mon Mar 04 2002 Erwan Velu <erwan@mandrakesoft.com> 3.4.4-2mdk
- Including xpvm as subpackage

* Fri Mar 01 2002 Erwan Velu <erwan@mandrakesoft.com> 3.4.4-1mdk
- First build
- Cleaning spec



Revision 1.30  2001/11/12 16:41:53  wiget
typo

Revision 1.29  2001/11/12 16:02:33  kloczek
- merge translations from CNV and adapterized spec.

Revision 1.28  2001/11/12 15:57:54  wiget
updated to 3.4.4

Revision 1.27  2001/11/12 15:07:38  wiget
fine grained architecture selection

Revision 1.26  2001/11/12 14:31:20  wiget
release 24
PVM_ROOT moved to /usr/lib/pvm3
DEFBINDIR moved to PVM_ROOT/bin/PVM_ARCH

Revision 1.25  2001/10/03 16:40:31  filon
- added using pvm macro in requires

Revision 1.24  2001/06/30 07:28:22  agaran
added m4 to buildrequires (no need to rebuild,nor $rel++)

Revision 1.23  2001/04/14 12:04:57  qboosh
- back commented out scripts and init file - see NOTE
  please don't uncomment it unless you change pvm behaviour
- removed "man fix" - man package was broken, now is fixed
- use %%rpmcflags, added pl translations
- release 23

Revision 1.22  2001/01/25 20:03:47  misiek
Massive attack. We use -O0 instead -O flags while debug enabled.

Revision 1.21  2001/01/05 19:23:17  dobrek
- Added pvm-book.ps to examples subpackage.

Revision 1.20  2001/01/03 23:59:11  kloczek
- uncomment %%post/%%preun svcripts,
- release 22 (for allow upgrade from RH),
- merged RH vaargfix patch,
- added URL.

Revision 1.19  2001/01/03 21:41:12  qboosh
- update to 3.4.3
- updated noenv patch

Revision 1.18  2000/12/27 14:09:35  kloczek
- adapterized and few cosmetics.

Revision 1.17  2000/12/26 21:05:20  qboosh
- Release 4:
- devel and examples subpackages
- examples to %%{_examplesdir}, not %%{_docdir}
- fix manuals
- moved xpvm to separate package (xpvm)
- setting PVM_ROOT no longer needed

Revision 1.16  2000/12/23 00:48:46  michuz
- changed %%{!?debug:...}%%{?debug...} to %%{?debug:...}%%{!?debug...}
  (now it's more C like)

Revision 1.15  2000/12/21 20:43:19  qboosh
- Release 3:
- added xpvm (as subpackage)
- BuildRequires
- fixed links
- PVM_ROOT, XPVM_ROOT variables setting (through /etc/profile.d)

Revision 1.14  2000/11/01 18:42:49  dobrek
- Realase=2
- A lot of changes. in install and files. It seams that everything can
  be keept in placec which are in agreement with FHS.
- Now tested only on i386. But soon the AXP version will apear.
- pvmd.init added.

Revision 1.13  2000/05/02 21:23:16  baggins
- fixed version, minor cleanup

Revision 1.12  2000/04/01 11:15:36  zagrodzki
- changed all BuildRoot definitons
- removed all applnkdir defs
- changed some prereqs/requires
- removed duplicate empty lines

Revision 1.11  2000/03/28 16:55:05  baggins
- translated kloczkish into english

Revision 1.10  1999/07/18 14:53:24  baggins
- fixed bogus Group: field

Revision 1.9  1999/07/12 23:06:13  kloczek
- added using CVS keywords in %%changelog (for automating them).

