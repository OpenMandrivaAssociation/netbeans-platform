# Prevent brp-java-repack-jars from being run.
%define __jar_repack %{nil}

%define nb_             netbeans
%define nb_ver          6.7.1
%define nb_release_time 200907230233
%define nb_home         %{_datadir}/%{nb_}
%define nb_dir          %{nb_home}/%{nb_ver}

%define nb_platform_ver 10
%define nb_platform     platform%{nb_platform_ver}
%define nb_platform_dir %{nb_home}/%{nb_platform}

%define nb_harness      harness
%define nb_harness_dir  %{nb_home}/%{nb_harness}

%define nb_javadoc      javadoc
%define nb_javadoc_dir  %{_javadocdir}/%{nb_}-%{nb_platform}

%define compiler_opt    -Dbuild.compiler.deprecation=false -Dbuild.compiler.debug=false
%define jdk_opt         -Dpermit.jdk6.builds=true
%define verify_opt      -Dverify.checkout=false
%define ant_nb_opt      %{ant} %{jdk_opt} %{compiler_opt} %{verify_opt}

%define nb_javadoc_site http://bits.netbeans.org/%{nb_ver}/javadoc

%define nbbuild_platform_dir nbbuild/netbeans/%{nb_platform}
%define nbbuild_harness_dir nbbuild/netbeans/%{nb_harness}

# Prevents use of autoupdate on the specified directory.
# %1 the directory being prevented for autoupdate.
%define noautoupdate()    echo > %1/.noautoupdate

# Links the system JAR
# %1 - the sys jar
# %2 - the symlink name/path (optional)
%global lnSysJAR() %__ln_s -f %{_javadir}/%{1} %{2} && test -f %{_javadir}/%{1} ;

Name:         netbeans-platform
Version:      %{nb_ver}
Release:      %mkrel 1
Summary:      NetBeans Platform %{nb_platform_ver}
Group:        Development/Java
License:      GPLv2 with exceptions or CDDL
URL:          http://platform.netbeans.org

Source0: http://download.netbeans.org/%{nb_}/%{version}/final/zip/%{nb_}-%{version}-%{nb_release_time}-platform-src.zip

# Removes the copy actions for the windows launcher components
# (*.exe *.dll) from the o.n.bootstrup/build.xml
Patch0: %{name}-%{version}-build_bootstrap.patch
# Prevents from releasing zip files (swing-layout-1.0.3-doc.zip,
# swing-layout-1.0.3-src.zip) in the o.jdesktop.layout module
Patch1: %{name}-%{version}-properties.patch
# openjdk-javac-6-b12.jar is needed only if JDK 1.5 is used, but we use JDK 1.6
Patch2: %{name}-%{version}-javac.patch
# Avoids spam in the log if the -XX:+HeapDumpOnOutOfMemoryError option is not supported by the JVM
Patch3: %{name}-%{version}-launcher.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

BuildRequires: jpackage-utils
BuildRequires: java-devel >= 0:1.6.0
BuildRequires: ant >= 1.7.0
BuildRequires: ant-junit >= 1.7.0
BuildRequires: ant-nodeps >= 1.7.0
BuildRequires: ant-trax >= 1.7.0
BuildRequires: junit4 >= 4.5
BuildRequires: swing-layout >= 1.0
BuildRequires: javahelp2 >= 2.0.05
BuildRequires: jna >= 3.0.9
BuildRequires: cobertura >= 1.9
BuildRequires: asm2 >= 2.2.1
BuildRequires: log4j >= 1.2.9
BuildRequires: jakarta-oro >= 2.0.8
BuildRequires: jemmy >= 2.3.0.0
BuildRequires: java-rpmbuild >= 0:1.5.32

Requires: jpackage-utils
Requires: java >= 0:1.6.0
Requires: swing-layout >= 1.0
Requires: javahelp2 >= 2.0.05
Requires: jna >= 3.0.9
Obsoletes: netbeans-platform8 < 6.5

%description
The NetBeans Platform is a generic framework for Swing applications. 
It provides the services common to almost all large desktop applications: 
window management, menus, settings and storage, update management, file 
access, etc.

%package %{nb_javadoc}
Summary: Javadoc documentation for NetBeans Platform %{nb_platform_ver}
Group: Development/Java
Obsoletes: netbeans-platform8-javadoc < 6.5
%description %{nb_javadoc}
NetBeans Platform is a set of modules, each providing
their own APIs and working together or in a standalone
mode. This package provides one master 
javadoc to all of them.

%package %{nb_harness}
Summary: Build harness for NetBeans Platform %{nb_platform_ver}
Group: Development/Java
Requires: jpackage-utils
Requires: java >= 0:1.6.0
Requires: ant >= 1.7.0
Requires: %{name} = %{version}-%{release}
Requires: javahelp2 >= 2.0.05
Requires: cobertura >= 1.9
Requires: asm2 >= 2.2.1
Requires: log4j >= 1.2.9
Requires: jakarta-oro >= 2.0.8
Requires: jemmy >= 2.3.0.0
Obsoletes: netbeans-platform8-harness < 6.5
%description %{nb_harness}
Harness with build scripts and ant tasks for everyone who
build an application on top of NetBeans Platform

%prep
%setup -q -c

find . -type f \( -iname "*.jar" -o -iname "*.zip" \) | xargs -t %__rm -f
find . -type f \( -iname "*.exe" \) | xargs -t %__rm -f
find . -type f \( -iname "binaries-list" \) | xargs -t %__rm -f

# As of Java 6, JSR 223 is included in the JRE.
# Generate the stub jar file, so there is something in jsr223 API module
%__mkdir_p libs.jsr223/src/javax/script
echo "package javax.script; class empty { }" > libs.jsr223/src/javax/script/empty.java
%__mkdir_p libs.jsr223/external
jar cf libs.jsr223/external/jsr223-api.jar libs.jsr223/src/javax/script/empty.java

# To build the netbeans modules the installed jars will be used instead of pre-packaged ones
%lnSysJAR javahelp2.jar     javahelp/external/jh-2.0_05.jar
%lnSysJAR jemmy.jar         jemmy/external/jemmy-2.3.0.0.jar
%lnSysJAR jna.jar           libs.jna/external/jna-3.0.9.jar
%lnSysJAR junit4.jar        libs.junit4/external/junit-4.5.jar
%lnSysJAR swing-layout.jar  o.jdesktop.layout/external/swing-layout-1.0.3.jar
pushd apisupport.harness/external
  %lnSysJAR javahelp2.jar jsearch-2.0_05.jar
  %lnSysJAR cobertura.jar cobertura-1.9.jar
  %lnSysJAR asm2/asm2.jar      asm-2.2.1.jar
  %lnSysJAR asm2/asm2-tree.jar asm-tree-2.2.1.jar
  %lnSysJAR log4j.jar     log4j-1.2.9.jar
  %lnSysJAR oro.jar       jakarta-oro-2.0.8.jar
popd

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build

# build platform & harness
%ant_nb_opt -f nbbuild/build.xml build-platform

# build platform javadoc
%ant_nb_opt \
   -Dallmodules= \
   -Dcluster.config=platform \
   -Dconfig.javadoc.cluster=%{nb_platform} \
   -Dconfig.javadoc.netbeans=\
openide.util,openide.actions,openide.options,openide.awt,\
openide.dialogs,openide.nodes,openide.explorer,openide.filesystems,openide.modules,\
openide.text,openide.windows,openide.loaders,openide.io,queries,\
o.n.api.progress,settings,javahelp,openide.execution,\
sendopts,options.api,editor.mimelookup \
   -Djavadoc.docs.org-netbeans-api-java=%{nb_javadoc_site}/org-netbeans-api-java/ \
   -Djavadoc.docs.org-netbeans-modules-project-ant=%{nb_javadoc_site}/org-netbeans-modules-project-ant/ \
   -Djavadoc.docs.org-netbeans-modules-projectapi=%{nb_javadoc_site}/org-netbeans-modules-projectapi/ \
   -f nbbuild/build.xml build-javadoc

# clean up stub jars
%__rm -f %{nbbuild_platform_dir}/modules/ext/script-api.jar

%install
%__rm -rf %{buildroot}

# install platform
%__mkdir_p %{buildroot}%{nb_platform_dir}
%__cp -pr nbbuild/netbeans/%{nb_platform}/* %{buildroot}%{nb_platform_dir}
%noautoupdate %{buildroot}%{nb_platform_dir}

# linking the platform to the system JARs
pushd %{buildroot}%{nb_platform_dir}/modules/ext
  %lnSysJAR javahelp2.jar    jh-2.0_05.jar
  %lnSysJAR jna.jar          jna-3.0.9.jar
  %lnSysJAR junit4.jar       junit-4.5.jar
  %lnSysJAR swing-layout.jar swing-layout-1.0.3.jar
popd

# install harness
%__mkdir_p %{buildroot}%{nb_harness_dir}
%__cp -pr nbbuild/netbeans/%{nb_harness}/* %{buildroot}%{nb_harness_dir}
%noautoupdate %{buildroot}%{nb_harness_dir}

# linking the harness to the system JARs
pushd %{buildroot}%{nb_harness_dir}
  %lnSysJAR javahelp2.jar antlib/jsearch-2.0_05.jar
  %lnSysJAR jemmy.jar     modules/ext/jemmy-2.3.0.0.jar
  pushd testcoverage/cobertura
    %lnSysJAR cobertura.jar cobertura-1.9.jar
    pushd lib
      %lnSysJAR asm2/asm2.jar      asm-2.2.1.jar
      %lnSysJAR asm2/asm2-tree.jar asm-tree-2.2.1.jar
      %lnSysJAR oro.jar       jakarta-oro-2.0.8.jar
      %lnSysJAR log4j.jar     log4j-1.2.9.jar
    popd
  popd
popd

# install javadoc
%__rm -rf  nbbuild/build/javadoc/*.zip
%__mkdir_p %{buildroot}%{nb_javadoc_dir}
%__cp -pr nbbuild/build/javadoc/* %{buildroot}%{nb_javadoc_dir}

%clean
%__rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc nbbuild/licenses/CDDL-GPL-2-CP
%dir %{nb_home}/
%dir %{nb_platform_dir}/
%{nb_platform_dir}/config
%{nb_platform_dir}/core
%dir %{nb_platform_dir}/lib
%{nb_platform_dir}/lib/boot.jar
%attr(755, root, root) %{nb_platform_dir}/lib/nbexec
%{nb_platform_dir}/lib/org-openide-modules.jar
%{nb_platform_dir}/lib/org-openide-util.jar
%{nb_platform_dir}/modules
%{nb_platform_dir}/update_tracking
%{nb_platform_dir}/.noautoupdate

%files %{nb_harness}
%defattr(-,root,root,-)
%dir %{nb_harness_dir}/
%{nb_harness_dir}/antlib
%{nb_harness_dir}/config
%{nb_harness_dir}/etc
%{nb_harness_dir}/jnlp
%dir %{nb_harness_dir}/launchers
%attr(755, root, root) %{nb_harness_dir}/launchers/app.sh
%{nb_harness_dir}/modules
%{nb_harness_dir}/testcoverage
%{nb_harness_dir}/update_tracking
%doc %{nb_harness_dir}/README
%{nb_harness_dir}/build.xml
%{nb_harness_dir}/common.xml
%{nb_harness_dir}/jdk.xml
%{nb_harness_dir}/jnlp.xml
%{nb_harness_dir}/run.xml
%{nb_harness_dir}/suite.xml
%{nb_harness_dir}/tasks.jar
%{nb_harness_dir}/.noautoupdate
%{nb_harness_dir}/no-testcoverage.xml
%{nb_harness_dir}/testcoverage-suite.xml
%{nb_harness_dir}/testcoverage.xml

%files %{nb_javadoc}
%defattr(-,root,root,-)
%doc %{nb_javadoc_dir}/

