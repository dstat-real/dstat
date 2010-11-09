prefix = /usr
datadir = $(prefix)/share
mandir = $(datadir)/man

template = dagit.ott

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

%.html: %.txt
	asciidoc $<

%.1.xml: %.1.txt
	asciidoc -b docbook -d manpage $<

%.1: %.1.xml
	@xmlto man $<

%.xml: %.txt
	asciidoc -b docbook -d article -o $@ $<

%.htm: %.txt
	asciidoc -s -b html4 -d article -o $@ $<

%.xhtml: %.txt
	asciidoc -s -b xhtml11 -d article -o $@ $<

%.tmp.odt: %.xml
#»··-make -C /home/dag/home-made/docbook2odf/ dag-cv
	docbook2odf -f --params generate.meta=0 -o $@ $<

%.odt: $(template) %.tmp.odt
	unoconv -f odt -t $(template) -o $@ $<
