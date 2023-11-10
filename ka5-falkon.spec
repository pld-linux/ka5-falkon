#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	23.08.3
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		falkon
Summary:	A KDE web browser
Name:		ka5-%{kaname}
Version:	23.08.3
Release:	1
License:	GPL v3+
Group:		X11/Applications
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	8063afbf57fe1898e4a001ef54ac150c
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= 5.15.2
BuildRequires:	Qt5DBus-devel >= 5.15.2
BuildRequires:	Qt5Gui-devel >= 5.15.2
BuildRequires:	Qt5Network-devel >= 5.15.2
BuildRequires:	Qt5Positioning-devel >= 5.15
BuildRequires:	Qt5PrintSupport-devel
BuildRequires:	Qt5Qml-devel >= 5.15.9
BuildRequires:	Qt5Quick-devel >= 5.15.9
BuildRequires:	Qt5Sql-devel
BuildRequires:	Qt5WebChannel-devel
BuildRequires:	Qt5WebEngine-devel >= 5.15.0
BuildRequires:	Qt5Widgets-devel >= 5.15.2
BuildRequires:	Qt5X11Extras-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-devel
BuildRequires:	kf5-extra-cmake-modules >= 5.78.0
BuildRequires:	kf5-karchive-devel
BuildRequires:	kf5-kauth-devel >= 5.105.0
BuildRequires:	kf5-kcodecs-devel >= 5.105.0
BuildRequires:	kf5-kcompletion-devel >= 5.105.0
BuildRequires:	kf5-kconfig-devel >= 5.105.0
BuildRequires:	kf5-kconfigwidgets-devel >= 5.105.0
BuildRequires:	kf5-kcoreaddons-devel >= 5.105.0
BuildRequires:	kf5-kcrash-devel >= 5.78.0
BuildRequires:	kf5-ki18n-devel
BuildRequires:	kf5-kio-devel >= 5.78.0
BuildRequires:	kf5-kitemviews-devel >= 5.105.0
BuildRequires:	kf5-kjobwidgets-devel >= 5.105.0
BuildRequires:	kf5-kservice-devel >= 5.105.0
BuildRequires:	kf5-kwallet-devel >= 5.78.0
BuildRequires:	kf5-kwidgetsaddons-devel >= 5.105.0
BuildRequires:	kf5-kxmlgui-devel >= 5.105.0
BuildRequires:	kf5-purpose-devel >= 5.78.0
BuildRequires:	kf5-solid-devel >= 5.105.0
BuildRequires:	libgnome-keyring-devel
BuildRequires:	libxcb-devel
BuildRequires:	ninja
BuildRequires:	openssl-devel
BuildRequires:	python3-devel
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	qt5-linguist
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{name}-data = %{version}-%{release}
ExcludeArch:	x32
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Falkon is a KDE web browser. It uses QtWebEngine rendering engine.

%description -l pl.UTF-8
Falkon jest przedglądarką www KDE korzystającą z silnika
QtWebEngine.

%package data
Summary:	Data files for %{kaname}
Summary(pl.UTF-8):	Dane dla %{kaname}
Group:		X11/Applications
BuildArch:	noarch

%description data
Data files for %{kaname}.

%description data -l pl.UTF-8
Dane dla %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

rm -rf $RPM_BUILD_ROOT%{_kdedocdir}/{el,ko,sr,zh_CN}
%find_lang %{kaname} --all-name --with-kde --with-qm

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/falkon
%{_libdir}/libFalkonPrivate.so.*.*.*
%ghost %{_libdir}/libFalkonPrivate.so.3
%dir %{_libdir}/qt5/plugins/falkon
%attr(755,root,root) %{_libdir}/qt5/plugins/falkon/AutoScroll.so
%attr(755,root,root) %{_libdir}/qt5/plugins/falkon/FlashCookieManager.so
%attr(755,root,root) %{_libdir}/qt5/plugins/falkon/GnomeKeyringPasswords.so
%attr(755,root,root) %{_libdir}/qt5/plugins/falkon/GreaseMonkey.so
%attr(755,root,root) %{_libdir}/qt5/plugins/falkon/KDEFrameworksIntegration.so
%attr(755,root,root) %{_libdir}/qt5/plugins/falkon/MouseGestures.so
%attr(755,root,root) %{_libdir}/qt5/plugins/falkon/PIM.so
%attr(755,root,root) %{_libdir}/qt5/plugins/falkon/StatusBarIcons.so
%attr(755,root,root) %{_libdir}/qt5/plugins/falkon/TabManager.so
%attr(755,root,root) %{_libdir}/qt5/plugins/falkon/VerticalTabs.so

%files data -f %{kaname}.lang
%defattr(644,root,root,755)
%{_desktopdir}/org.kde.falkon.desktop
%{bash_compdir}/falkon
%{_datadir}/falkon
%{_iconsdir}/hicolor/128x128/apps/falkon.png
%{_iconsdir}/hicolor/16x16/apps/falkon.png
%{_iconsdir}/hicolor/256x256/apps/falkon.png
%{_iconsdir}/hicolor/32x32/apps/falkon.png
%{_iconsdir}/hicolor/48x48/apps/falkon.png
%{_iconsdir}/hicolor/64x64/apps/falkon.png
%{_iconsdir}/hicolor/scalable/apps/falkon.svg
%{_datadir}/metainfo/org.kde.falkon.appdata.xml
