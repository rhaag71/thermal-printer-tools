#
# Makefile for Rollo CUPS printer driver
#
# Copyright © 2020-2024 by Nelu LLC.
#
# This program is free software.  Distribution and use rights are outlined in
# the file "COPYING".
#


# POSIX makefile...
.POSIX:


# Version number
ROLLO_VERSION	=	1.8.4


# Programs and options...
CC		=	gcc
CFLAGS		=	-fPIC -march=x86-64 -mtune=generic -O2 -pipe -fno-plt -fexceptions         -Wp,-D_FORTIFY_SOURCE=3 -Wformat -Werror=format-security         -fstack-clash-protection -fcf-protection         -fno-omit-frame-pointer -mno-omit-leaf-frame-pointer -I/usr/include/p11-kit-1 -D_REENTRANT $(CPPFLAGS) $(OPTIM) $(WARNINGS)
CPPFLAGS	=	 -D__USE_MISC -D_GNU_SOURCE
INSTALL		=	/home/dev/src/aur/rollo-printer/src/rollo-cups-driver-1.8.4/install-sh
LDFLAGS		=	-fPIE -pie -Wl,-O1 -Wl,--sort-common -Wl,--as-needed -Wl,-z,relro -Wl,-z,now          -Wl,-z,pack-relative-relocs -Wl,-z,relro,-z,now $(OPTIM)
LIBS		=	 -lcups
OPTIM		=	 -g -Os
RM		=	/usr/bin/rm -f
SHELL		=	/bin/sh
WARNINGS	=	-Wall -Wunused -Wno-char-subscripts -Wno-deprecated-declarations -Wno-format-truncation -Wno-format-y2k -Wno-switch -Wno-unused-result


# Directories...
CUPS_DATADIR	=	/usr/share/cups
CUPS_SERVERBIN	=	/usr/lib/cups

BUILDROOT       =       $(DSTROOT)$(RPM_BUILD_ROOT)$(DESTDIR)


# Rules...
.SILENT:
.SUFFIXES: .c .h .o
.c.o:
	echo Compiling $<...
	$(CC) $(CFLAGS) -c -o $@ $<


# Targets...
OBJS	=	\
		rastertorollo.o \
		rollo-dither.o
TARGETS	=	\
		rastertorollo


# Resource files...
PPDS	 =	\
		rollo-x1038.ppd


# Make everything...
all:		$(TARGETS)


# Clean everything...
clean:
	echo Removing generated files...
	$(RM) $(OBJS) $(TARGETS) clang.log cppcheck.log


# Really clean everything
distclean:	clean
	$(RM) config.status config.log Makefile


# Update dependencies...
depend:


# Install everything...
install:	$(TARGETS)
	echo Creating $(BUILDROOT)$(CUPS_SERVERBIN)/filter...
	$(INSTALL) -d -m 755 $(BUILDROOT)$(CUPS_SERVERBIN)/filter
	$(INSTALL) -c -m 755 rastertorollo $(BUILDROOT)$(CUPS_SERVERBIN)/filter
	echo Creating $(BUILDROOT)$(CUPS_DATADIR)/model...
	$(INSTALL) -d -m 755 $(BUILDROOT)$(CUPS_DATADIR)/model
	for file in $(PPDS); do \
		$(INSTALL) -c -m 644 $$file $(BUILDROOT)$(CUPS_DATADIR)/model; \
	done


# rastertorollo
rastertorollo:	$(OBJS)
	echo Linking $@...
	$(CC) $(LDFLAGS) -o $@ $(OBJS) $(LIBS)


# Scan code with the Clang static analyzer <https://clang-analyzer.llvm.org>
clang:
	echo "clang $(CPPFLAGS) --analyze ..."
	clang $(CPPFLAGS) --analyze $(OBJS:.o=.c) 2>clang.log
	rm -rf $(OBJS:.o=.plist)
	@test -s clang.log && (echo ""; echo "Errors detected:"; echo ""; cat clang.log; exit 1) || exit 0


# Scan code with Cppcheck <http://cppcheck.sourceforge.net>
cppcheck:
	echo "cppcheck $(CPPFLAGS) --template=gcc --addon=cert.py --suppress=cert-MSC24-C --suppress=cert-EXP05-C --suppress=cert-API01-C ... 2>cppcheck.log"
	cppcheck $(CPPFLAGS) --template=gcc --addon=cert.py --suppress=cert-MSC24-C --suppress=cert-EXP05-C --suppress=cert-API01-C $(OBJS:.o=.c) 2>cppcheck.log
	@test -s cppcheck.log && (echo ""; echo "Errors detected:"; echo ""; cat cppcheck.log; exit 1) || exit 0


# Dependencies
$(OBJS): Makefile rollo-dither.h
$(TARGETS): Makefile
