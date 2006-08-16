#
# Conditional build:
%bcond_with	altivec		# use altivec, no runtime detection
%bcond_without	openal		# don't use OpenAL

%define	_dataver	1.32b3
%define	_snap	20060330
Summary:	Quake3 for Linux
Summary(de):	Quake3 für Linux
Summary(pl):	Quake3 dla Linuksa
Name:		quake3
Version:	1.33
Release:	0.%{_snap}.1
License:	GPL v2
Group:		Applications/Games
Source0:	http://sparky.homelinux.org/snaps/icculus/%{name}-%{_snap}.tar.bz2
# Source0-md5:	124c35755bbb175aed010af4e6267c4e
Source2:	q3ded.init
Source3:	q3ded.sysconfig
Source4:	%{name}.desktop
Source5:	%{name}-smp.desktop
Patch0:		%{name}-gpl-Makefile-install.patch
Patch1:		%{name}-QUAKELIBDIR.patch
Patch2:		%{name}-alpha.patch
URL:		http://icculus.org/quake3/
%if %{with openal}
BuildRequires:	OpenAL-devel
%endif
BuildRequires:	OpenGL-devel
BuildRequires:	SDL-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	%{name}-common = %{version}-%{release}
Requires:	OpenGL
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-ffast-math -funroll-loops -fomit-frame-pointer -fno-strict-aliasing
%define		specflags_ia32	-falign-loops=2 -falign-jumps=2 -falign-functions=2
%if %{with altivec}
%define		specflags_ppc	-maltivec -mabi=altivec
%endif
%define		_noautoreqdep	libGL.so.1 libGLU.so.1

%description
Quake 3 for Linux.

%description -l de
Quake 3 für Linux.

%description -l pl
Quake 3 dla Linuksa.

%package server
Summary:	Quake3 server
Summary(de):	Quake3 Server
Summary(pl):	Serwer Quake3
Group:		Applications/Games
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(triggerpostun):	/usr/sbin/usermod
Requires:	%{name}-common = %{version}-%{release}
Requires:	psmisc
Requires:	rc-scripts
Requires:	screen
Provides:	group(quake3)
Provides:	user(quake3)

%description server
Quake3 server.

%description server -l de
Quake3 Server.

%description server -l pl
Serwer Quake3.

%package smp
Summary:	Quake3 for SMP
Summary(de):	Quake3 für SMP
Summary(pl):	Quake3 dla SMP
Group:		Applications/Games
Requires:	%{name}-common = %{version}-%{release}

%description smp
Quake3 for multi processor machine.

%description smp -l de
Quake3 für Multiprocessor Rechner.

%description smp -l pl
Quake3 dla maszyny wieloprocesorowej.

%package common
Summary:	Common files for Quake3
Summary(de):	Gemeinsame Dateien für Quake3
Summary(pl):	Pliki wspólne dla Quake3
Group:		Applications/Games
Requires(triggerpostun):	/usr/sbin/groupdel
Requires(triggerpostun):	/usr/sbin/userdel
Requires:	quake3-data >= %{_dataver}-1
Obsoletes:	quake3-single

%description common
Common files for Quake3 server and player game.

%description common -l de
Gemeinsame Dateien für den Quake3 Server und das Spiel.

%description common -l pl
Pliki wspólne Quake3 dla serwera i trybu gracza.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1
cat << EOF > Makefile.local
BUILD_CLIENT	= 1
BUILD_CLIENT_SMP= 1
BUILD_SERVER	= 1
BUILD_GAME_SO	= 1
BUILD_GAME_QVM	= 0
%if %{without openal}
USE_OPENAL	= 0
%endif
EOF

%build
CFLAGS="%{rpmcflags}"
CFLAGS="$CFLAGS -DDEFAULT_BASEDIR=\\\"%{_datadir}/games/%{name}\\\""
CFLAGS="$CFLAGS -DQUAKELIBDIR=\\\"%{_libdir}/%{name}\\\""
CFLAGS="$CFLAGS -Wall -Wimplicit -Wstrict-prototypes"
CFLAGS="$CFLAGS -DUSE_SDL_VIDEO=1 -DUSE_SDL_SOUND=1 $(sdl-config --cflags)"
%if %{with openal}
CFLAGS="$CFLAGS -DUSE_OPENAL=1"
%endif
CFLAGS="$CFLAGS -DNDEBUG -MMD"
%ifnarch %{ix86} %{x8664}
CFLAGS="$CFLAGS -DNO_VM_COMPILED"
%endif

%{__make} makedirs tools targets \
	B="release-%{_target}"	\
	CC="%{__cc}"		\
	CFLAGS="$CFLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig} \
	$RPM_BUILD_ROOT{%{_bindir},%{_datadir}/games/%{name}/baseq3} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}} \
	$RPM_BUILD_ROOT/var/games/quake3

%{__make} install \
	BR="release-%{_target}"	\
	BINDIR=$RPM_BUILD_ROOT%{_bindir}		\
	Q3LIBDIR=$RPM_BUILD_ROOT%{_libdir}/%{name}

install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/q3ded
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/q3ded
install code/unix/%{name}.png $RPM_BUILD_ROOT%{_pixmapsdir}
install %{SOURCE4} $RPM_BUILD_ROOT%{_desktopdir}/quake3.desktop
install %{SOURCE5} $RPM_BUILD_ROOT%{_desktopdir}/quake3-smp.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post common
if [ "$1" = "1" ]; then
	echo ""
	echo "You need to copy pak0.pk3 from your Quake3 CD into %{_datadir}/games/%{name}/baseq3/."
	echo "Or if you have got a Windows installation of Q3 make a symlink to save space."
	echo "You may place it in ~/.q3a/baseq3/ but you will have to put all pak files there (or make symlinks)."
	echo ""
fi

%pre server
%groupadd -P %{name}-server -g 38 quake3
%useradd -P %{name}-server -u 124 -d /var/games/quake3 -s /bin/sh -c "Quake ]|[ Arena" -g quake3 quake3

%post server
/sbin/chkconfig --add q3ded
%service q3ded restart "Quake3 server"

%preun server
if [ "$1" = "0" ]; then
	%service q3ded stop
	/sbin/chkconfig --del q3ded
fi

%postun server
if [ "$1" = "0" ]; then
	%userremove quake3
	%groupremove quake3
fi

%triggerpostun server -- %{name}-server < 1.33
if [ -f /var/lock/subsys/q3ded ]; then
	# server will fail because of lack of pak0.pk3
	/sbin/service q3ded stop 1>&2
fi
if [ "`getent passwd quake3 | cut -d: -f6`" = "/opt/quake3" ]; then
	/usr/sbin/usermod -d /var/games/quake3 -s /bin/sh quake3
fi

%triggerpostun common -- %{name}-common < 1.33
if [ ! -f %{_datadir}/games/%{name}/baseq3/pak0.pk3 ]; then
	# Better don't link/move automatically, /opt may be on other partition than /usr
	echo ""
	echo "Quake 3 data location has changed, link or move pak0.pk3 to %{_datadir}/games/%{name}/baseq3/."
	echo ""
fi

if [ "$1" = "0" ]; then
	%userremove quake3
	%groupremove quake3
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/quake3
%{_desktopdir}/quake3.desktop

%files common
%defattr(644,root,root,755)
%doc BUGS id-readme.txt README ChangeLog TODO
%dir %{_datadir}/games/%{name}
%dir %{_datadir}/games/%{name}/baseq3
%{_pixmapsdir}/quake3.png
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/baseq3
%dir %{_libdir}/%{name}/missionpack
%attr(755,root,root) %{_libdir}/%{name}/baseq3/*.so
%attr(755,root,root) %{_libdir}/%{name}/missionpack/*.so

%files server
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/q3ded
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/q3ded
%attr(755,root,root) %{_bindir}/q3ded
%attr(750,quake3,quake3) /var/games/quake3

%files smp
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/quake3-smp
%{_desktopdir}/quake3-smp.desktop
