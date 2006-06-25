prefix = /usr
datadir = $(prefix)/share
mandir = $(datadir)/man

txttargets = $(shell echo *.txt)
htmltargets = $(patsubst %.txt, %.html, $(txttargets))

all:

dist: docs

docs: dstat.1 $(htmltargets)

install: dstat.1
	install -Dp -m0644 dstat.1 $(DESTDIR)$(mandir)/man1/dstat.1

clean:
	rm -f dstat.1 *.html *.xml

%.1.html: %.1.txt
	asciidoc -d manpage $<

%.1: %.1.xml
	xmlto man $<

%.html: %.txt
	asciidoc $<

%.1.xml: %.1.txt
	asciidoc -b docbook -d manpage $<
