# $Id$
# Authority: dag
# Upstream: Dag Wieers <dag@wieers.com>

%{?dist: %{expand: %%define %dist 1}}

%{?rh7:%define _with_python15 1}
%{?el2:%define _with_python15 1}

Summary: Versatile vmstat, iostat and ifstat replacement
Name: dstat
Version: 0.5.6
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
Dstat is a versatile replacement for vmstat, iostat and ifstat. Dstat
overcomes some of the limitations and adds some extra features.

Dstat allows you to view all of your system resources instantly,
you can eg. compare disk usage in combination with interrupts from
your IDE controller, or compare the network bandwidth numbers
directly with the disk throughput (in the same interval).

Dstat also cleverly gives you the most detailed information in
columns and clearly indicates in what magnitude and unit the output
is displayed. Less confusion, less mistakes.

Dstat is also unique in letting you aggregate block device throughput
for a certain diskset or network bandwidth for a group of interfaces,
ie. you can see the throughput for all the block devices that make up
a single filesystem or storage system.

You can customize your dstat output from /etc/dstat.conf and you can
write your own dstat modules to plug into the dstat output.

Dstat's output, in its current form, is not very useful to be post-
processed by other tools. It's mostly meant for allowing humans to
interprete real-time data as easy as possible.

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
%doc AUTHORS ChangeLog COPYING README* TESTS TODO
#%doc *.conf
%doc %{_mandir}/man1/dstat.1*
#%config(noreplace) %{_sysconfdir}/dstat.conf
%{_bindir}/dstat

%changelog
* Thu Dec 02 2004 Dag Wieers <dag@wieers.com> - 0.5.6-1
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
