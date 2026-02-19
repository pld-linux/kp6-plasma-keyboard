#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.6.0
%define		qtver		6.10.0
%define		kpname		plasma-keyboard

Summary:	Plasma Keyboard
Name:		kp6-%{kpname}
Version:	6.6.0
Release:	3
License:	LGPL v2.1+
Group:		X11/Applications
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	0ab280ccc8e3fd92da9fdad445834963
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6VirtualKeyboard-devel >= %{qtver}
BuildRequires:	Qt6WaylandClient-devel >= %{qtver}
BuildRequires:	cmake >= 3.16.0
BuildRequires:	gettext-tools
BuildRequires:	kf6-extra-cmake-modules >= 6.22.0
BuildRequires:	kf6-kcmutils-devel >= 6.22.0
BuildRequires:	kf6-kconfig-devel >= 6.22.0
BuildRequires:	kf6-kcoreaddons-devel >= 6.23.0
BuildRequires:	kf6-ki18n-devel >= 6.22.0
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	wayland-devel >= 1.2
BuildRequires:	wayland-protocols >= 1.19
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	kp5-%{kpname} < 6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
The plasma-keyboard is a virtual keyboard based on [Qt Virtual
Keyboard](https://doc.qt.io/qt-6/qtvirtualkeyboard-overview.html)
designed to integrate in Plasma.

It wraps Qt Virtual Keyboard in a window, and uses the input-method-v1
Wayland protocol to communicate with the compositor to function as an
input method.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database_post

%postun
/sbin/ldconfig
%update_desktop_database_postun

%files -f %{kpname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/plasma-keyboard
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_plasmakeyboard.so
%dir %{_libdir}/qt6/qml/QtQuick/VirtualKeyboard/Styles/Breeze
%{_libdir}/qt6/qml/QtQuick/VirtualKeyboard/Styles/Breeze/breezestyle.qmltypes
%{_libdir}/qt6/qml/QtQuick/VirtualKeyboard/Styles/Breeze/kde-qmlmodule.version
%{_libdir}/qt6/qml/QtQuick/VirtualKeyboard/Styles/Breeze/libbreezestyle.so
%{_libdir}/qt6/qml/QtQuick/VirtualKeyboard/Styles/Breeze/qmldir
%{_libdir}/qt6/qml/QtQuick/VirtualKeyboard/Styles/Breeze/style.qml
%{_libdir}/qt6/qml/org/kde/plasma/keyboard
%{_desktopdir}/kcm_plasmakeyboard.desktop
%{_desktopdir}/org.kde.plasma.keyboard.desktop
%{_datadir}/metainfo/org.kde.plasma.keyboard.metainfo.xml
%{_datadir}/plasma/keyboard
