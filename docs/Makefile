prefix = /usr
sysconfdir = /etc
bindir = $(prefix)/bin
datadir = $(prefix)/share
mandir = $(datadir)/man

all: docs

docs: dstat.1 dstat.1.html
	echo "test"

install:
	install -Dp -m0644 dstat.1 $(DESTDIR)$(mandir)/man1/dstat.1

clean:
	rm -f dstat.1 dstat.1.xml *.html

%.html: %.txt
	asciidoc -d manpage $<

%.1: %.1.xml
	xmlto man $<

%.xml: %.txt
	asciidoc -b docbook -d manpage $<
