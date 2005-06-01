# $Id$
# Authority: dag
# Upstream: Dag Wieers <dag@wieers.com>

%{?dist: %{expand: %%define %dist 1}}

%{?rh7:%define _with_python15 1}
%{?el2:%define _with_python15 1}

Summary: Versatile resource statistics tool
Name: dstat
Version: 0.6.1
Release: 1
License: GPL
Group: System Environment/Base
URL: http://dag.wieers.com/home-made/dstat/

Packager: Dag Wieers <dag@wieers.com>
Vendor: Dag Apt Repository, http://dag.wieers.com/apt/

Source: http://dag.wieers.com/home-made/dstat/dstat-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch: noarch
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

Dstat is unique in letting you aggregate block device throughput for
a certain diskset or networkset, ie. you can see the throughput for
all the block devices that make up a single filesystem or storage
system.

You can write your own dstat plugins to monitor whatever you like in
just a few minutes based on provided examples and a little bit of
Python knowledge.

Dstat's output by default is designed for being interpreted by humans
in real-time, however the new CSV output allows you to store CSV
output in detail to a file to be imported later into Gnumeric or Excel
to generate graphs.

%prep
%setup

%build

%install
%{__rm} -rf %{buildroot}
%makeinstall

%{?_with_python15:%{__install} -D -m0755 dstat15 %{buildroot}%{_bindir}/dstat}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING README* TODO examples/ *.conf
%doc %{_mandir}/man1/dstat.1*
#%config(noreplace) %{_sysconfdir}/dstat.conf
%{_bindir}/dstat
%{_datadir}/dstat/

%changelog
* Tue May 31 2005 Dag Wieers <dag@wieers.com> - 0.6.1-1
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
