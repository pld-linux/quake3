# TODO:
#		- init script for the dedicated server.
#
Summary:	Quake3 for Linux
Summary(pl):	Quake3 dla Linuksa
Name:		quake3
Version:	1.32b
%define		_subver	3
Release:	0.1
Vendor:		id Software
License:	Q3A EULA, PB EULA
Group:		Applications/Games
Source0:	ftp://ftp.idsoftware.com/idstuff/quake3/linux/linuxq3apoint-%{version}-%{_subver}.x86.run
# Source0-md5:	c71fdddccb20e8fc393d846e9c61d685
URL:		http://www.idsoftware.com/games/quake/quake3-arena/
#Requires:	screen
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
install -d $RPM_BUILD_ROOT%{_gamedir}/{,baseq3,pb/{,htm}}

install baseq3/* $RPM_BUILD_ROOT%{_gamedir}/baseq3/
install pb/*.so $RPM_BUILD_ROOT%{_gamedir}/pb/
install pb/htm/*.htm $RPM_BUILD_ROOT%{_gamedir}/pb/htm/
install bin/Linux/x86/* $RPM_BUILD_ROOT%{_gamedir}/

%clean
rm -rf $RPM_BUILD_ROOT

%post
echo "You need to copy pak0.pk3 from your Quake3 CD into %{_gamedir}/baseq3/."
echo "Or if you have got a Windows installation of Q3 make a symlink to save space."

%files
%defattr(644,root,root,755)
%doc Q3A_EULA.txt README-linux.txt pb/PB_EULA.txt Docs/PunkBuster
%dir %{_gamedir}
%{_gamedir}/baseq3
%dir %{_gamedir}/pb
%{_gamedir}/pb/htm
%attr(755,root,root) %{_gamedir}/pb/*.so
%attr(754,root,games) %{_gamedir}/quake3*x86
