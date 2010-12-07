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
BuildRequires:	tcl tcl-devel tk tk-devel
Requires: 	initscripts >= 5.54, bash >= 2, shadow-utils, openssh-server, openssh-clients
BuildRoot: 	%{_tmppath}/%name-buildroot

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
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_pvm_root}/lib/%{_pvm_arch}
mkdir -p $RPM_BUILD_ROOT/var/run/pvm3
mkdir -p $RPM_BUILD_ROOT%{_pvm_root}/conf

install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir},%{_pvm_root}/conf,%{_docdir}/%{name}} \
	$RPM_BUILD_ROOT/%{name}/{examples,gexamples,hoster,misc,tasker,xep} \
	$RPM_BUILD_ROOT{%{_mandir}/man{1,3},/etc/rc.d/init.d,%{_sbindir}} \
	$RPM_BUILD_ROOT/%{_sysconfdir}/profile.d

install %{SOURCE1}  $RPM_BUILD_ROOT/etc/rc.d/init.d/pvm
install lib/%{_pvm_arch}/{pvm,pvmgs} $RPM_BUILD_ROOT%{_pvm_root}/lib/%{_pvm_arch}
install lib/%{_pvm_arch}/pvmd3 $RPM_BUILD_ROOT%{_pvm_root}/lib/%{_pvm_arch}
install lib/pvm		$RPM_BUILD_ROOT%{_pvm_root}
install lib/debugger	$RPM_BUILD_ROOT%{_pvm_root}/lib
install lib/debugger2	$RPM_BUILD_ROOT%{_pvm_root}/lib
install lib/pvmgetarch	$RPM_BUILD_ROOT%{_pvm_root}/lib
install lib/pvmtmparch	$RPM_BUILD_ROOT%{_pvm_root}/lib
install lib/aimk	$RPM_BUILD_ROOT%{_pvm_root}/lib
install lib/pvmd	$RPM_BUILD_ROOT%{_pvm_root}/lib
install conf/%{_pvm_arch}.def $RPM_BUILD_ROOT%{_pvm_root}/conf
install include/{fpvm3,pvm3,pvmproto,pvmtev}.h $RPM_BUILD_ROOT%{_includedir}
install lib/%{_pvm_arch}/lib*.a $RPM_BUILD_ROOT%{pvmlib}
install man/man1/* $RPM_BUILD_ROOT%{_mandir}/man1
install man/man3/* $RPM_BUILD_ROOT%{_mandir}/man3
install %{SOURCE5} $RPM_BUILD_ROOT%{_pvm_root}/.bashrc
install %{SOURCE6} $RPM_BUILD_ROOT%{_pvm_root}
install %{SOURCE7} $RPM_BUILD_ROOT%{_pvm_root}
install %{SOURCE8} $RPM_BUILD_ROOT%{_pvm_root}
install -m 755 %{SOURCE9} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
touch $RPM_BUILD_ROOT%{_pvm_root}/pvmhosts

# Examples
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}/source
mv $RPM_BUILD_DIR/pvm3/examples $RPM_BUILD_ROOT%{_docdir}/%{name}/source
mv $RPM_BUILD_DIR/pvm3/gexamples $RPM_BUILD_ROOT%{_docdir}/%{name}/source
mv $RPM_BUILD_DIR/pvm3/hoster $RPM_BUILD_ROOT%{_docdir}/%{name}/source
mv $RPM_BUILD_DIR/pvm3/misc $RPM_BUILD_ROOT%{_docdir}/%{name}/source
mv $RPM_BUILD_DIR/pvm3/tasker $RPM_BUILD_ROOT%{_docdir}/%{name}/source
mv $RPM_BUILD_DIR/pvm3/xep $RPM_BUILD_ROOT%{_docdir}/%{name}/source
install %{SOURCE2}  $RPM_BUILD_ROOT%{_docdir}/%{name}/pvm-book.ps
gzip -9nf $RPM_BUILD_ROOT%{_docdir}/%{name}/pvm-book.ps

#xpvm
install -d $RPM_BUILD_ROOT/usr/X11R6/bin
install -m 0755 $RPM_BUILD_DIR/%{xpvmpath}/src/%{_pvm_arch}/xpvm %{buildroot}%{_bindir}
LIBDIR=/usr/X11R6/lib/xpvm
install -d -m 755 $RPM_BUILD_ROOT$LIBDIR
install -d -m 755 $RPM_BUILD_ROOT$LIBDIR/src
install -d -m 755 $RPM_BUILD_ROOT$LIBDIR/src/xbm
install -d -m 755 $RPM_BUILD_ROOT$LIBDIR/src/help
install -m 0644 $RPM_BUILD_DIR/%{xpvmpath}/*.tcl $RPM_BUILD_ROOT$LIBDIR
install -m 0644 $RPM_BUILD_DIR/%{xpvmpath}/src/xbm/*.xbm $RPM_BUILD_ROOT$LIBDIR/src/xbm
install -m 0644 $RPM_BUILD_DIR/%{xpvmpath}/src/help/*.help $RPM_BUILD_ROOT$LIBDIR/src/help
install -m 0644 $RPM_BUILD_DIR/%{xpvmpath}/README .
install -m 0644 %{SOURCE4} .


%clean
rm -rf $RPM_BUILD_ROOT

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
%dir %{_pvm_root}
%dir %{_pvm_root}/lib
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

