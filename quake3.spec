Summary:	Quake3 for Linux
Summary(pl):	Quake3 dla Linuksa
Name:		quake3
Version:	1.32b
%define		_subver	3
Release:	3
Vendor:		id Software
License:	Q3A EULA, PB EULA
Group:		Applications/Games
Source0:	ftp://ftp.idsoftware.com/idstuff/quake3/linux/linuxq3apoint-%{version}-%{_subver}.x86.run
# Source0-md5:	c71fdddccb20e8fc393d846e9c61d685
Source1:	q3ded.init
Source2:	q3ded.sysconfig
Source3:	%{name}.png
Source4:	%{name}.desktop
Source5:	%{name}-smp.desktop
URL:		http://www.idsoftware.com/
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-common = %{version}-%{release}
Requires:	OpenGL
Requires:	psmisc
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		_noautoreqdep	libGL.so.1 libGLU.so.1
%define		_gamedir	/opt/quake3

%description
Quake 3 for Linux.

%description -l pl
Quake 3 dla linuksa.

%package server
Summary:	Quake3 server
Summary(pl):	Serwer Quake3
Group:		Applications/Games
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-common = %{version}-%{release}
Requires:	screen

%description server
Quake3 server.

%description server -l pl
Serwer Quake3.

%package smp
Summary:	Quake3 for SMP
Summary(pl):	Quake3 dla SMP
Group:		Applications/Games
Requires:	%{name}-common = %{version}-%{release}

%description smp
Quake3 for multi processor machine.

%description smp -l pl
Quake3 dla maszyny wieloprocesorowej.

%package common
Summary:	Common files for quake3
Summary(pl):	Pliki wspólne dla quake3
Group:		Applications/Games
Obsoletes:	quake3-single

%description common
Common files for quake3 server and player game.

%description common -l pl
Pliki wspólne quake3 dla serwera i trybu gracza.

%prep
%setup -qcT
sh %{SOURCE0} --tar xf

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig} \
	$RPM_BUILD_ROOT{%{_gamedir}/{baseq3,pb/{,htm}},%{_bindir}} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/q3ded
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/q3ded
install %{SOURCE3} $RPM_BUILD_ROOT%{_pixmapsdir}
install %{SOURCE4} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop
install %{SOURCE5} $RPM_BUILD_ROOT%{_desktopdir}/%{name}-smp.desktop
install baseq3/* $RPM_BUILD_ROOT%{_gamedir}/baseq3
install bin/Linux/x86/* $RPM_BUILD_ROOT%{_gamedir}
install pb/*.so $RPM_BUILD_ROOT%{_gamedir}/pb
install pb/htm/*.htm $RPM_BUILD_ROOT%{_gamedir}/pb/htm

cat << EOF > $RPM_BUILD_ROOT%{_bindir}/quake3
#!/bin/sh
cd %{_gamedir}
./quake3.x86
EOF
cat << EOF > $RPM_BUILD_ROOT%{_bindir}/quake3-smp
#!/bin/sh
cd %{_gamedir}
./quake3-smp.x86
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post common
if [ "$1" = "1" ]; then
echo ""
echo "You need to copy pak0.pk3 from your Quake3 CD into %{_gamedir}/baseq3/."
echo "Or if you have got a Windows installation of Q3 make a symlink to save space."
echo ""
fi

%post server
/sbin/chkconfig --add q3ded
if [ -f /var/lock/subsys/q3ded ]; then
	/etc/rc.d/init.d/q3ded restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/q3ded start\" to start Quake3 server"
fi

%preun server
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/q3ded ]; then
		/etc/rc.d/init.d/q3ded stop 1>&2
	fi
	/sbin/chkconfig --del q3ded
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_gamedir}/quake3.x86
%attr(755,root,root) %{_bindir}/quake3
%{_desktopdir}/quake3.desktop

%files common
%defattr(644,root,root,755)
%doc Q3A_EULA.txt README-linux.txt pb/PB_EULA.txt
%dir %{_gamedir}
%{_gamedir}/baseq3
%dir %{_gamedir}/pb
%{_gamedir}/pb/htm
%attr(755,root,root) %{_gamedir}/pb/*.so
%{_pixmapsdir}/quake3.png

%files server
%defattr(644,root,root,755)
%attr(755,root,root) /etc/rc.d/init.d/q3ded
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/q3ded
%attr(755,root,root) %{_gamedir}/q3ded

%files smp
%defattr(644,root,root,755)
%attr(755,root,root) %{_gamedir}/quake3-smp.x86
%attr(755,root,root) %{_bindir}/quake3-smp
%{_desktopdir}/quake3-smp.desktop
