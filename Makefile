name = dstat
version = $(shell awk '/^Version: / {print $$2}' $(name).spec)

prefix = /usr
sysconfdir = /etc
bindir = $(prefix)/bin
datadir = $(prefix)/share
mandir = $(datadir)/man

.PHONY: all install docs clean

all: docs
	@echo "Nothing to be build."

docs:
	$(MAKE) -C docs docs

install:
#	-[ ! -f $(DESTDIR)$(sysconfdir)/dstat.conf ] && install -D -m0644 dstat.conf $(DESTDIR)$(sysconfdir)/dstat.conf
	install -Dp -m0755 dstat $(DESTDIR)$(bindir)/dstat
	install -d -m0755 $(DESTDIR)$(datadir)/dstat/
	install -Dp -m0755 dstat $(DESTDIR)$(datadir)/dstat/dstat.py
	install -Dp -m0644 plugins/dstat_*.py $(DESTDIR)$(datadir)/dstat/
#	install -d -m0755 $(DESTDIR)$(datadir)/dstat/examples/
#	install -Dp -m0755 examples/*.py $(DESTDIR)$(datadir)/dstat/examples/
	install -Dp -m0644 docs/dstat.1 $(DESTDIR)$(mandir)/man1/dstat.1

docs-install:
	$(MAKE) -C docs install

clean:
	rm -f dstat15.tr examples/*.pyc plugins/*.pyc
	$(MAKE) -C docs clean

dist: clean
	$(MAKE) -C docs dist
	svn list -R | pax -d -w -x ustar -s ,^,$(name)-$(version)/, | bzip2 >../$(name)-$(version).tar.bz2

rpm: dist
	rpmbuild -tb --clean --rmsource --rmspec --define "_rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm" --define "_rpmdir ../" ../$(name)-$(version).tar.bz2

srpm: dist
	rpmbuild -ts --clean --rmsource --rmspec --define "_rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm" --define "_srcrpmdir ../" ../$(name)-$(version).tar.bz2
