Summary:	Quake3 for Linux
Summary(pl):	Quake3 dla Linuksa
Name:		quake3
Version:	1.32b
%define		_subver	3
Release:	0.2
Vendor:		id Software
License:	Q3A EULA, PB EULA
Group:		Applications/Games
Source0:	ftp://ftp.idsoftware.com/idstuff/quake3/linux/linuxq3apoint-%{version}-%{_subver}.x86.run
# Source0-md5:	c71fdddccb20e8fc393d846e9c61d685
Source1:	http://www.evenbalance.com/downloads/pbweb.x86
# Source1-md5:	cb4baff8cf481915d87fa4da23294e8e
Source2:	q3ded.init
Source3:	q3ded.sysconfig
URL:		http://www.idsoftware.com/
Requires(post,preun):	/sbin/chkconfig
Requires:	screen
Requires:	OpenGL
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		_noautoreqdep	libGL.so.1 libGLU.so.1
%define		_gamedir	/opt/quake3

%description
"The most important PC game ever."

%description -l pl
"Najwa¿niejsza gra wszechczasów na PC."

%prep
%setup -qcT
sh %{SOURCE0} --tar xf

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig},%{_gamedir}/{,baseq3,pb/{,htm}}}

install %{SOURCE1} $RPM_BUILD_ROOT%{_gamedir}/
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/q3ded
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/q3ded
install baseq3/* $RPM_BUILD_ROOT%{_gamedir}/baseq3/
install bin/Linux/x86/* $RPM_BUILD_ROOT%{_gamedir}/
install pb/*.so $RPM_BUILD_ROOT%{_gamedir}/pb/
install pb/htm/*.htm $RPM_BUILD_ROOT%{_gamedir}/pb/htm/

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add q3ded
echo ""
echo "You need to copy pak0.pk3 from your Quake3 CD into %{_gamedir}/baseq3/."
echo "Or if you have got a Windows installation of Q3 make a symlink to save space."
echo ""

%preun
if [ "$1" = "0" ]; then
    /sbin/chkconfig --del q3ded
fi

%files
%defattr(644,root,root,755)
%doc Q3A_EULA.txt README-linux.txt pb/PB_EULA.txt
%attr(754,root,root) /etc/rc.d/init.d/q3ded
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/q3ded
%dir %{_gamedir}
%{_gamedir}/baseq3
%dir %{_gamedir}/pb
%{_gamedir}/pb/htm
%attr(755,root,root) %{_gamedir}/pb/*.so
%attr(755,root,root) %{_gamedir}/pbweb.x86
%attr(754,root,games) %{_gamedir}/q3ded
%attr(754,root,games) %{_gamedir}/quake3*x86
