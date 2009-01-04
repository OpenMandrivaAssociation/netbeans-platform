Name:                   netbeans-platform
Version:                6.5
Release:                %mkrel 1
%define section		devel
%define source_top	%{name}-src
%define netbeansdir     %{_datadir}/netbeans

%define clusterdir      %{netbeansdir}
%define nbplatform      platform9

Summary:	NetBeans Platform for Development of Rich Client Swing Applications Wrapper
URL:		http://platform.netbeans.org
Source0:	http://download.netbeans.org/netbeans/6.5/final/zip/netbeans-6.5-200811100001-ml-platform-src.zip
Source1: 	scripts.sh

Patch0:         10-build.patch

Epoch:		0
License:	GPLv2 with exceptions or CDDL
Group:		Development/Java
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch:	noarch
BuildRequires:	java-devel >= 1.6.0
BuildRequires:	java-rpmbuild >= 0:1.5
BuildRequires:	ant >= 0:1.7.1
BuildRequires:  ant-junit >= 1.7.1
BuildRequires:  ant-nodeps >= 0:1.7.1
BuildRequires:  ant-trax >= 0:1.7.1
BuildRequires:	junit4 >= 0:4.3
BuildRequires:	swing-layout >= 0:1.0
BuildRequires:  javahelp2 >= 2.0.05
BuildRequires:  jna >= 3.0
Requires:       libnb-%{nbplatform} >= 6.5

%description
NetBeans Platform is a framework for development of 
rich client Swing applications. It contains powerful
module system and a set of modules providing various
functionalities needed for simplification of 
development of modular desktop applications.


%package -n libnb-%{nbplatform}
Summary: NetBeans Platform for Development of Rich Client Swing Applications
Group: Development/Java
Requires: 	java >= 0:1.6
Requires:	jpackage-utils >= 0:1.5
Requires:	swing-layout >= 0:1.0
Requires:	javahelp2 >= 2.0.05
Requires:       jna >= 3.0


%description -n libnb-%{nbplatform}
NetBeans Platform is a framework for development of 
rich client Swing applications. It contains powerful
module system and a set of modules providing various
functionalities needed for simplification of 
development of modular desktop applications.


%package -n libnb-%{nbplatform}-javadoc
Summary: Javadoc documentation for NetBeans Platform
Group: Development/Java
Requires:       libnb-%{nbplatform} >= 6.5

%description -n libnb-%{nbplatform}-javadoc
NetBeans Platform is a set of modules, each providing
their own APIs and working together or in a standalone
mode. This package provides one master 
javadoc to all of them.



%package -n libnb-%{nbplatform}-devel
Summary: Build harness for NetBeans Platform
Group: Development/Java
Requires:   javahelp2 >= 2.0
Requires:   libnb-%{nbplatform} >= 6.5
Provides:   netbeans-platform9-harness = 6.5
Provides:   libnb-platform9-harness = 6.5
Obsoletes:  libnb-platform7-devel
Obsoletes:  libnb-platform8-devel


%description -n libnb-%{nbplatform}-devel
Harness with build scripts and ant tasks for everyone who
build an application on top of NetBeans Platform

%prep
%{__rm} -rf netbeans-src

%setup -q -c
find . -type d | xargs -t chmod 755
find . -type f -exec chmod 644 {} ";"
find . -type f \( -iname "*.jar" -o -iname "*.zip" \) | xargs -t %{__rm} -f

LNS="%{__ln_s}"
MKDIRP="%{__mkdir_p}"
JAVADIR="%{_javadir}"
JAVADOCDIR="$RPM_BUILD_ROOT/%{_javadocdir}/netbeans-%{nbplatform}"
RMF="%{__rm} -rf"
INS="%{__cp} -r"
NBDIR="$RPM_BUILD_ROOT/%{clusterdir}"
JHJAR=javahelp2.jar
export LNS MKDIRP JAVADIR JAVADOCDIR RMF INS NBDIR JHJAR
sh -x %{SOURCE1} setup 

%patch0 -p0 -b .sav

%build

LNS="%{__ln_s}"
MKDIRP="%{__mkdir_p}"
JAVADIR="%{_javadir}"
JAVADOCDIR="$RPM_BUILD_ROOT/%{_javadocdir}/netbeans-%{nbplatform}"
RMF="%{__rm} -rf"
INS="%{__cp} -r"
NBDIR="$RPM_BUILD_ROOT/%{clusterdir}"
JHJAR=javahelp2.jar
export LNS MKDIRP JAVADIR JAVADOCDIR RMF INS NBDIR JHJAR

sh -x %{SOURCE1} build || exit 1
sh -x %{SOURCE1} build_devel || exit 1
sh -x %{SOURCE1} build_javadoc || exit 1


%install

%{__rm} -rf $RPM_BUILD_ROOT
LNS="%{__ln_s}"
MKDIRP="%{__mkdir_p}"
JAVADIR="%{_javadir}"
JAVADOCDIR="$RPM_BUILD_ROOT/%{_javadocdir}/netbeans-%{nbplatform}"
RMF="%{__rm} -rf"
INS="%{__cp} -r"
NBDIR="$RPM_BUILD_ROOT/%{clusterdir}"
JHJAR=javahelp2.jar
export LNS MKDIRP JAVADIR JAVADOCDIR RMF INS NBDIR JHJAR

%{__mkdir_p} $NBDIR

sh -x %{SOURCE1} install || exit 1
sh -x %{SOURCE1} install_devel || exit 1
sh -x %{SOURCE1} install_javadoc || exit 1


%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files

%files -n libnb-%{nbplatform}
%defattr(644,root,root,755)
%dir %{clusterdir}/%{nbplatform}/
%{clusterdir}/%{nbplatform}/*
# to prevent use of autoupdate on this directory
%{clusterdir}/%{nbplatform}/.noautoupdate

%files -n libnb-%{nbplatform}-devel
%defattr(644,root,root,755)
%dir %{clusterdir}/harness/
%{clusterdir}/harness/*
%{clusterdir}/harness/jsearch-2.0_05.jar
# to prevent use of autoupdate on this directory
%{clusterdir}/harness/.noautoupdate

%files -n libnb-%{nbplatform}-javadoc
%defattr(-,root,root)
%{_javadocdir}/netbeans-%{nbplatform}


