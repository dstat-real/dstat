prefix = /usr
sysconfdir = /etc
bindir = $(prefix)/bin
mandir = $(datadir)/man

all: install

install:
#	-[ ! -f $(DESTDIR)$(sysconfdir)/dstat.conf ] && install -D -m0644 dstat.conf $(DESTDIR)$(sysconfdir)/dstat.conf
	install -D -m0755 dstat $(DESTDIR)$(bindir)/dstat
