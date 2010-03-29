# $Id$
# Authority: dag
# Upstream: Dag Wieers <dag@wieers.com>

Summary: Versatile resource statistics tool
Name: dstat
Version: 0.7.1svn
Release: 1
License: GPL
Group: System Environment/Base
URL: http://dag.wieers.com/home-made/dstat/

Source: http://dag.wieers.com/home-made/dstat/dstat-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch: noarch
BuildRequires: python
Requires: python

%description
Dstat is a versatile replacement for vmstat, iostat, netstat and ifstat.
Dstat overcomes some of their limitations and adds some extra features,
more counters and flexibility. Dstat is handy for monitoring systems
during performance tuning tests, benchmarks or troubleshooting.

Dstat allows you to view all of your system resources instantly, you
can eg. compare disk usage in combination with interrupts from your
IDE controller, or compare the network bandwidth numbers directly
with the disk throughput (in the same interval). 

Dstat gives you detailed selective information in columns and clearly
indicates in what magnitude and unit the output is displayed. Less
confusion, less mistakes.

%prep
%setup

%build

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING README TODO docs/*.html docs/*.txt examples/
%doc %{_mandir}/man1/dstat.1*
%{_bindir}/dstat
%{_datadir}/dstat/

%changelog
* Tue Feb 23 2010 Dag Wieers <dag@wieers.com> - 0.7.1svn-1
- Updated to release 0.7.1svn.

* Mon Feb 22 2010 Dag Wieers <dag@wieers.com> - 0.7.1-1
- Updated to release 0.7.1.

* Wed Nov 25 2009 Dag Wieers <dag@wieers.com> - 0.7.0-1
- Updated to release 0.7.0.
- Reduce the number of paths used for importing modules. {CVE-2009-3894}

* Tue Dec 02 2008 Dag Wieers <dag@wieers.com> - 0.6.9-1
- Updated to release 0.6.9.

* Sun Aug 17 2008 Dag Wieers <dag@wieers.com> - 0.6.8-1
- Updated to release 0.6.8.

* Tue Feb 26 2008 Dag Wieers <dag@wieers.com> - 0.6.7-1
- Updated to release 0.6.7.

* Sat Apr 28 2007 Dag Wieers <dag@wieers.com> - 0.6.6-1
- Updated to release 0.6.6.

* Tue Apr 17 2007 Dag Wieers <dag@wieers.com> - 0.6.5-1
- Updated to release 0.6.5.

* Tue Dec 12 2006 Dag Wieers <dag@wieers.com> - 0.6.4-1
- Updated to release 0.6.4.

* Mon Jun 26 2006 Dag Wieers <dag@wieers.com> - 0.6.3-1
- Updated to release 0.6.3.

* Thu Mar 09 2006 Dag Wieers <dag@wieers.com> - 0.6.2-1
- Updated to release 0.6.2.

* Mon Sep 05 2005 Dag Wieers <dag@wieers.com> - 0.6.1-1
- Updated to release 0.6.1.

* Sun May 29 2005 Dag Wieers <dag@wieers.com> - 0.6.0-1
- Updated to release 0.6.0.

* Fri Apr 08 2005 Dag Wieers <dag@wieers.com> - 0.5.10-1
- Updated to release 0.5.10.

* Mon Mar 28 2005 Dag Wieers <dag@wieers.com> - 0.5.9-1
- Updated to release 0.5.9.

* Tue Mar 15 2005 Dag Wieers <dag@wieers.com> - 0.5.8-1
- Updated to release 0.5.8.

* Fri Dec 31 2004 Dag Wieers <dag@wieers.com> - 0.5.7-1
- Updated to release 0.5.7.

* Mon Dec 20 2004 Dag Wieers <dag@wieers.com> - 0.5.6-1
- Updated to release 0.5.6.

* Thu Dec 02 2004 Dag Wieers <dag@wieers.com> - 0.5.5-1
- Updated to release 0.5.5.

* Thu Nov 25 2004 Dag Wieers <dag@wieers.com> - 0.5.4-1
- Updated to release 0.5.4.
- Use dstat15 if distribution uses python 1.5.

* Sun Nov 21 2004 Dag Wieers <dag@wieers.com> - 0.5.3-1
- Updated to release 0.5.3.

* Sat Nov 13 2004 Dag Wieers <dag@wieers.com> - 0.5.2-1
- Updated to release 0.5.2.

* Thu Nov 11 2004 Dag Wieers <dag@wieers.com> - 0.5.1-1
- Updated to release 0.5.1.

* Tue Oct 26 2004 Dag Wieers <dag@wieers.com> - 0.4-1
- Initial package. (using DAR)
