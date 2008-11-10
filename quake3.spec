
%define	_dataver	1.32b3
%define	_snap	20081110
%define	_rel	1
Summary:	Quake3 for Linux
Summary(de.UTF-8):	Quake3 für Linux
Summary(pl.UTF-8):	Quake3 dla Linuksa
Name:		quake3
Version:	1.35
Release:	0.%{_snap}.%{_rel}
License:	GPL v2
Group:		Applications/Games
Source0:	%{name}-%{_snap}.tar.bz2
# Source0-md5:	65ed9787590bc043412c38b69c2c8521
Source2:	q3ded.init
Source3:	q3ded.sysconfig
Source4:	%{name}.desktop
Source5:	%{name}-smp.desktop
Patch0:		%{name}-QUAKELIBDIR.patch
Patch1:		%{name}-alpha.patch
URL:		http://ioquake3.org/
BuildRequires:	OpenAL-devel
BuildRequires:	OpenGL-devel
BuildRequires:	SDL-devel
BuildRequires:	libvorbis-devel
BuildRequires:	rpmbuild(macros) >= 1.268
#BuildRequires:	speex-devel
Requires:	%{name}-common = %{version}-%{release}
Requires:	OpenGL
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# source has been fixed to work without those
%define		filterout_c	-fwrapv -fno-strict-aliasing -fsigned-char

%define		specflags	-ffast-math -funroll-loops -fomit-frame-pointer -fno-strict-aliasing
%define		x86_flags	-falign-loops=2 -falign-jumps=2 -falign-functions=2 -fstrength-reduce
%define		specflags_ia32	%{x86_flags}
%define		specflags_x86_64 %{x86_flags}
%define		specflags_amd64	%{x86_flags}
%define		specflags_ia32e	%{x86_flags}
%define		_noautoreqdep	libGL.so.1 libGLU.so.1

%description
Quake 3 for Linux.

%description -l de.UTF-8
Quake 3 für Linux.

%description -l pl.UTF-8
Quake 3 dla Linuksa.

%package server
Summary:	Quake3 server
Summary(de.UTF-8):	Quake3 Server
Summary(pl.UTF-8):	Serwer Quake3
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

%description server -l de.UTF-8
Quake3 Server.

%description server -l pl.UTF-8
Serwer Quake3.

%package smp
Summary:	Quake3 for SMP
Summary(de.UTF-8):	Quake3 für SMP
Summary(pl.UTF-8):	Quake3 dla SMP
Group:		Applications/Games
Requires:	%{name}-common = %{version}-%{release}

%description smp
Quake3 for multi processor machine.

%description smp -l de.UTF-8
Quake3 für Multiprocessor Rechner.

%description smp -l pl.UTF-8
Quake3 dla maszyny wieloprocesorowej.

%package common
Summary:	Common files for Quake3
Summary(de.UTF-8):	Gemeinsame Dateien für Quake3
Summary(pl.UTF-8):	Pliki wspólne dla Quake3
Group:		Applications/Games
Requires(triggerpostun):	/usr/sbin/groupdel
Requires(triggerpostun):	/usr/sbin/userdel
Requires:	quake3-data >= %{_dataver}-1
Obsoletes:	quake3-single

%description common
Common files for Quake3 server and player game.

%description common -l de.UTF-8
Gemeinsame Dateien für den Quake3 Server und das Spiel.

%description common -l pl.UTF-8
Pliki wspólne Quake3 dla serwera i trybu gracza.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1

%build
cat << 'EOF' > Makefile.local
BUILD_STANDALONE= 0
BUILD_CLIENT	= 1
# smp broken
BUILD_CLIENT_SMP= 0
BUILD_SERVER	= 1
BUILD_GAME_SO	= 1
BUILD_GAME_QVM	= 0
BUILD_MISSIONPACK= 1
USE_OPENAL	= 1
USE_OPENAL_DLOPEN = 0
USE_CURL	= 1
USE_CURL_DLOPEN = 0
USE_CODEC_VORBIS = 1
USE_MUMBLE	= 1
USE_VOIP	= 1
USE_INTERNAL_SPEEX = 1
USE_LOCAL_HEADERS = 0
GENERATE_DEPENDENCIES = 0

DEFAULT_BASEDIR = %{_datadir}/games/%{name}

override OPTIMIZE = %{rpmcflags} \
	-DQUAKELIBDIR=\\\"%{_libdir}/%{name}\\\"

# vim spec bug: "

override CC = %{__cc}
override LDFLAGS = %{rpmldflags}
override BR = rel

EOF

%{__make} release

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig} \
	$RPM_BUILD_ROOT{%{_bindir},%{_datadir}/games/%{name}/baseq3} \
	$RPM_BUILD_ROOT%{_libdir}/%{name}/{baseq3,missionpack} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}} \
	$RPM_BUILD_ROOT/var/games/quake3

install rel/ioquake3.* $RPM_BUILD_ROOT%{_bindir}/%{name}
#install rel/ioquake3-smp.* $RPM_BUILD_ROOT%{_bindir}/%{name}-smp
install rel/ioq3ded.* $RPM_BUILD_ROOT%{_bindir}/q3ded

install rel/baseq3/*.so $RPM_BUILD_ROOT%{_libdir}/%{name}/baseq3
install rel/missionpack/*.so $RPM_BUILD_ROOT%{_libdir}/%{name}/missionpack

install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/q3ded
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/q3ded
install misc/%{name}.svg $RPM_BUILD_ROOT%{_pixmapsdir}
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
%{_pixmapsdir}/quake3.svg
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

%if 0
%files smp
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/quake3-smp
%{_desktopdir}/quake3-smp.desktop
%endif
