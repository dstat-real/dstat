prefix = /usr
sysconfdir = /etc
bindir = $(prefix)/bin
datadir = $(prefix)/share
mandir = $(datadir)/man

all: install

install:
#	-[ ! -f $(DESTDIR)$(sysconfdir)/dstat.conf ] && install -D -m0644 dstat.conf $(DESTDIR)$(sysconfdir)/dstat.conf
	install -D -m0755 dstat $(DESTDIR)$(bindir)/dstat
	install -D -m0644 dstat.1 $(DESTDIR)$(mandir)/man1/dstat.1
