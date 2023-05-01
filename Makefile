CC = clang
#add -Wall
CFLAGS = -pedantic -Wall -std=c99 -gdwarf-4
LIBS = -lm

all: libmol.so _molecule.so molecule_wrap.c

clean:
	rm -f *.o *.so

main:
	python3 MolDisplay.py
	python3 molsql.py

libmol.so: mol.o
	$(CC) mol.o -shared -lm -o libmol.so

mol.o: mol.c mol.h
	$(CC) $(CFLAGS) -c mol.c -fpic -o mol.o

# for server
# molecule_wrap.o: molecule_wrap.c
# 	$(CC) $(CFLAGS) -c molecule_wrap.c -fpic -I/usr/include/python3.7m -o molecule_wrap.o

# _molecule.so: molecule_wrap.o libmol.so
# 	$(CC) $(CFLAGS) -shared molecule_wrap.o -L. -L/usr/include/python3.7m/config-3.7m-x86_64-linux-gnu -lpython3.7m -lmol -dymaniclib -o _molecule.so

# for local
molecule_wrap.o: molecule_wrap.c
	$(CC) $(CFLAGS) -c molecule_wrap.c -fpic -I/usr/include/python3.10 -o molecule_wrap.o
	
_molecule.so: molecule_wrap.o libmol.so
	$(CC) $(CFLAGS) -shared molecule_wrap.o -L/usr/lib/python3.10/config-3.10-x86_64-linux-gnu -lpython3.10 -L. -lmol -dymaniclib -o _molecule.so

molecule_wrap.c molecule.py: molecule.i
	swig3.0 -python molecule.i

# export LD_LIBRARY_PATH=`pwd` && export LD_LIBRARY_PATH=.
# python3 ajaxserver.py <port #>

# localhost:<port #>/ (in browser)
