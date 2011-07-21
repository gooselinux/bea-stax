# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support 1

Summary:        Streaming API for XML
URL:            http://dev2dev.bea.com/technologies/stax/index.jsp
Source0:        http://dist.codehaus.org/stax/distributions/stax-src-1.2.0_rc1-dev.zip
# XXX: 
# since libgcj already includes classes in javax.xml.stream.events.* which 
# are not api compliant with those in the api jar, the build fails in gcj 
# unless added to bootclasspath
Patch0:         %{name}-ecj-bootclasspath.patch
Name:           bea-stax
Version:        1.2.0
Release:        0.5.rc1.2%{?dist}
Epoch:          0
License:        ASL 2.0 and ASL 1.1
Group:          Development/Libraries/Java
%if ! %{gcj_support}
BuildArch:      noarch
%endif

BuildRequires:          jpackage-utils >= 0:1.6
BuildRequires:          ant
BuildRequires:          xerces-j2,xalan-j2
Requires:               jpackage-utils >= 0:1.6
Requires:       %{name}-api = %{epoch}:%{version}-%{release}

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if %{gcj_support}
BuildRequires:          java-gcj-compat-devel
Requires(post):         java-gcj-compat
Requires(postun):       java-gcj-compat
%endif

%description
The Streaming API for XML (StAX) is a groundbreaking 
new Java API for parsing and writing XML easily and 
efficiently. 

%package api
Summary:        The StAX API
Group:          Development/Documentation
Requires:               jpackage-utils >= 0:1.6
%if %{gcj_support}
BuildRequires:          java-gcj-compat-devel
Requires(post):         java-gcj-compat
Requires(postun):       java-gcj-compat
%endif

%description api
%{summary}

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Documentation
Requires:               jpackage-utils >= 0:1.6

%description javadoc
%{summary}

%prep
%setup -q -c -n %{name}-%{version}
%{__sed} -i 's/\r//' ASF2.0.txt
%if %{gcj_support}
%patch0 -b .bak
%endif

%build
export CLASSPATH=`pwd`/build/stax-api-1.0.jar
ant all javadoc

%install
rm -rf $RPM_BUILD_ROOT

# jar
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}
install -p -m 0644 build/stax-api-1.0.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-api-%{version}.jar
install -p -m 0644 build/stax-1.2.0_rc1-dev.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-ri-%{version}.jar
ln -s %{name}-api-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-api.jar
ln -s %{name}-ri-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-ri.jar

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr build/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post api
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%postun api
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%post
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%postun
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%defattr(-,root,root,-)
%doc ASF2.0.txt
%{_javadir}/%{name}-ri-%{version}.jar
%{_javadir}/%{name}-ri.jar

%if %{gcj_support}
%dir %attr(-,root,root) %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/bea-stax-ri-1.2.0.jar.*
%endif

%files api
%defattr(-,root,root,-)
%doc ASF2.0.txt
%{_javadir}/%{name}-api-%{version}.jar
%{_javadir}/%{name}-api.jar

%if %{gcj_support}
%dir %attr(-,root,root) %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/bea-stax-api-1.2.0.jar.*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/*

%changelog
* Mon Jan 11 2010 Andrew Overholt <overholt@redhat.com> 1.2.0-0.5.rc1.2
- Fix gcj_support macro usage
- Add ASL 1.1 to License as XmlReader is 1.1 and included in final JAR

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0:1.2.0-0.5.rc1.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.0-0.5.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.0-0.4.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.2.0-0.3.rc1
- drop repotag
- fix license

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.2.0-0.2.rc1.2jpp.1
- Autorebuild for GCC 4.3

* Mon Feb 12 2007 Vivek Lakshmanan <vivekl@redhat.com> 0:1.2.0-0.1.rc1.2jpp.1.fc7
- Use new naming convention
- Add ASF2.0.txt as doc for api and main package
- Remove post/postun magic for javadoc
- Add BR on ant, xerces-j2 and xalan-j2
- Add conditional patch to make the package build under ecj/gcj

* Wed Jan 18 2006 Fernando Nasser <fnasser@redhat.com> 0:1.2.0-0.rc1.2jpp
- First JPP 1.7 build

* Wed Jan 18 2006 Deepak Bhole <dbhole@redhat.com> 0:1.2.0-0.rc1.1jpp
- Change source zip, and build the ri jars
- Use setup macro in prep
- First version all under APL
- New package name
- Demo still not yet available under the APL; will be in an update

* Tue Apr 26 2005 Fernando Nasser <fnasser@redhat.com> 0:1.0-2jpp_2rh
- First Red Hat build

* Wed Oct 20 2004 David Walluck <david@jpackage.org> 0:1.0-2jpp
- fix build

* Thu Sep 09 2004 Ralph Apel <r.apel at r-apel.de> 0:1.0-1jpp
- First JPackage build 
- Note: there is a stax project starting at codehaus
