prefix = /usr
sysconfdir = /etc
bindir = $(prefix)/bin
datadir = $(prefix)/share
mandir = $(datadir)/man

all:
	@echo "No build phase."

install:
#	-[ ! -f $(DESTDIR)$(sysconfdir)/dstat.conf ] && install -D -m0644 dstat.conf $(DESTDIR)$(sysconfdir)/dstat.conf
	install -Dp -m0755 dstat $(DESTDIR)$(bindir)/dstat
	install -Dp -m0644 dstat.1 $(DESTDIR)$(mandir)/man1/dstat.1
	install -d -m0755 $(DESTDIR)$(datadir)/dstat/
	install -Dp -m0755 stats/*.py $(DESTDIR)$(datadir)/dstat/
#	install -d -m0755 $(DESTDIR)$(datadir)/dstat/examples/
#	install -Dp -m0755 examples/*.py $(DESTDIR)$(datadir)/dstat/examples/

clean:
	rm -f dstat15.tr examples/*.pyc

#### Imperfect translation to dstat15
tr:
	@cat dstat | perl -p -e ' \
			next if (s|(\S+)\.center\((.+)\)\.replace\((.+), (.+)\)|string.replace(string.center($$1, $$2), $$3, $$4)|g); \
			next if (s|(.[-?] .)\.rjust\((\S+)\)|string.rjust\($$1, $$2\)|g); \
			next if (s|(. .)\.join\(l\[cpunr\+2:\]\)\.split\((.,.)\)|string.split(string.join(l[cpunr+2:], $$1), $$2)|g); \
			next if (s|self\.intmap\[(\S+)\.strip\(\)\.lower\(\)\]|self.intmap[string.strip(string.lower($$1))]|g); \
			next if (s|\((.0.) \+ (. .) \* len\((\S+)\)\)\.rjust\((\S+)\)|string.rjust($$1 + $$2 * len($$3), $$4)|g); \
			next if (s|(\S+)\.replace\((.:.), (. .)\)\.split\(\)|string.split(string.replace($$1, $$2, $$3))|g); \
			next if (s|ret\[name\.strip\(\)\.lower\(\)\]|name = string.lower(string.strip(name))\n				ret[name]|g); \
			s|(\S+)\.replace\((.+), (.+)\)|string.replace($$1, $$2, $$3)|g; \
			s|(\S+)\.rjust\((.+)\)|string.rjust($$1, $$2)|g; \
			s|(\S+)\.center\((.+)\)|string.center($$1, $$2)|g; \
			s|(\S+)\.strip\((.+)\)|string.strip($$1, $$2)|g; \
			s|(\S+)\.split\((.+)\)|string.split($$1, $$2)|g; \
			s|(\S+)\.rjust\(\)|string.rjust($$1)|g; \
			s|(\S+)\.center\(\)|string.center($$1)|g; \
			s|(\S+)\.strip\(\)|string.strip($$1)|g; \
			s|(\S+)\.split\(\)|string.split($$1)|g; \
			s|(\w+)\.lower\(\)|string.lower($$1)|g; \
			s|long\(round\(var\)|int\(round\(var\)|g; \
			s|, time$$|, time, string|g; \
		' >dstat15.tr
	@chmod a+x dstat15.tr
