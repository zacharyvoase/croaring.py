all: README.rst amalgamated

README.rst: README.md
	cat $^ | egrep -v '^\[\!' | pandoc -f markdown -t rst > $@

amalgamated: croaring-src/roaring.h croaring-src/roaring.c

croaring-src/roaring.h roaring-src/roaring.c: $@
	cd croaring-src/; ./amalgamation.sh

.PHONY: all amalgamated
