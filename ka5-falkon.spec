#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	24.01.95
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		falkon
Summary:	A KDE web browser
Name:		ka5-%{kaname}
Version:	24.01.95
Release:	0.1
License:	GPL v3+
Group:		X11/Applications
Source0:	https://download.kde.org/unstable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	6619725c89b4835b8de8ff4a0c1f24e2
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= 5.15.2
BuildRequires:	Qt6DBus-devel >= 5.15.2
BuildRequires:	Qt6Gui-devel >= 5.15.2
BuildRequires:	Qt6Network-devel >= 5.15.2
BuildRequires:	Qt6Positioning-devel >= 5.15
BuildRequires:	Qt6PrintSupport-devel
BuildRequires:	Qt6Qml-devel >= 5.15.9
BuildRequires:	Qt6Quick-devel >= 5.15.9
BuildRequires:	Qt6Sql-devel
BuildRequires:	Qt6WebChannel-devel
BuildRequires:	Qt6WebEngine-devel >= 5.15.0
BuildRequires:	Qt6Widgets-devel >= 5.15.2
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-devel
BuildRequires:	kf6-extra-cmake-modules >= 5.78.0
BuildRequires:	kf6-karchive-devel
BuildRequires:	kf6-kauth-devel >= 5.105.0
BuildRequires:	kf6-kcodecs-devel >= 5.105.0
BuildRequires:	kf6-kcompletion-devel >= 5.105.0
BuildRequires:	kf6-kconfig-devel >= 5.105.0
BuildRequires:	kf6-kconfigwidgets-devel >= 5.105.0
BuildRequires:	kf6-kcoreaddons-devel >= 5.105.0
BuildRequires:	kf6-kcrash-devel >= 5.78.0
BuildRequires:	kf6-ki18n-devel
BuildRequires:	kf6-kio-devel >= 5.78.0
BuildRequires:	kf6-kitemviews-devel >= 5.105.0
BuildRequires:	kf6-kjobwidgets-devel >= 5.105.0
BuildRequires:	kf6-kservice-devel >= 5.105.0
BuildRequires:	kf6-kwallet-devel >= 5.78.0
BuildRequires:	kf6-kwidgetsaddons-devel >= 5.105.0
BuildRequires:	kf6-kxmlgui-devel >= 5.105.0
BuildRequires:	kf6-purpose-devel >= 5.78.0
BuildRequires:	kf6-solid-devel >= 5.105.0
BuildRequires:	libgnome-keyring-devel
BuildRequires:	libxcb-devel
BuildRequires:	ninja
BuildRequires:	openssl-devel
BuildRequires:	python3-devel
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	qt6-linguist
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
%dir %{_libdir}/qt6/plugins/falkon
%attr(755,root,root) %{_libdir}/qt6/plugins/falkon/AutoScroll.so
%attr(755,root,root) %{_libdir}/qt6/plugins/falkon/FlashCookieManager.so
%attr(755,root,root) %{_libdir}/qt6/plugins/falkon/GnomeKeyringPasswords.so
%attr(755,root,root) %{_libdir}/qt6/plugins/falkon/GreaseMonkey.so
%attr(755,root,root) %{_libdir}/qt6/plugins/falkon/KDEFrameworksIntegration.so
%attr(755,root,root) %{_libdir}/qt6/plugins/falkon/MouseGestures.so
%attr(755,root,root) %{_libdir}/qt6/plugins/falkon/PIM.so
%attr(755,root,root) %{_libdir}/qt6/plugins/falkon/StatusBarIcons.so
%attr(755,root,root) %{_libdir}/qt6/plugins/falkon/TabManager.so
%attr(755,root,root) %{_libdir}/qt6/plugins/falkon/VerticalTabs.so

%files data -f %{kaname}.lang
%defattr(644,root,root,755)
%{_desktopdir}/org.kde.falkon.desktop
%{bash_compdir}/falkon
%{_datadir}/falkon
%{_iconsdir}/hicolor/*x*/apps/falkon.png
%{_iconsdir}/hicolor/scalable/apps/falkon.svg
%{_datadir}/metainfo/org.kde.falkon.appdata.xml
