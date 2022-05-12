#
# Conditional build:
%bcond_without	doc	# Documentation

%define		orgname		qtwebchannel
%define		qtbase_ver		%{version}
%define		qtdeclarative_ver	%{version}
%define		qttools_ver		%{version}
%define		qtwebsockets_ver	%{version}
Summary:	The Qt5 WebChannel library
Summary(pl.UTF-8):	Biblioteka Qt5 WebChannel
Name:		qt5-%{orgname}
Version:	5.15.4
Release:	1
License:	LGPL v3 or GPL v2 or GPL v3 or commercial
Group:		X11/Libraries
Source0:	https://download.qt.io/official_releases/qt/5.15/%{version}/submodules/%{orgname}-everywhere-opensource-src-%{version}.tar.xz
# Source0-md5:	790a627fd53a94f1f779be6d5ee76cc6
URL:		https://www.qt.io/
BuildRequires:	Qt5Core-devel >= %{qtbase_ver}
BuildRequires:	Qt5Network-devel >= %{qtbase_ver}
BuildRequires:	Qt5Qml-devel >= %{qtdeclarative_ver}
BuildRequires:	Qt5Quick-devel >= %{qtdeclarative_ver}
# for examples
BuildRequires:	Qt5WebSockets-devel >= %{qtwebsockets_ver}
%if %{with doc}
BuildRequires:	qt5-assistant >= %{qttools_ver}
%endif
BuildRequires:	qt5-build >= %{qtbase_ver}
BuildRequires:	qt5-qmake >= %{qtbase_ver}
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing
%define		qt5dir		%{_libdir}/qt5

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.

This package contains Qt5 WebChannel library.

%description -l pl.UTF-8
Qt to wieloplatformowy szkielet aplikacji i interfejsów użytkownika.
Przy użyciu Qt można pisać aplikacje powiązane z WWW i wdrażać je w
systemach biurkowych, przenośnych i wbudowanych bez przepisywania kodu
źródłowego.

Ten pakiet zawiera bibliotekę Qt5 WebChannel.

%package -n Qt5WebChannel
Summary:	The Qt5 WebChannel library
Summary(pl.UTF-8):	Biblioteka Qt5 WebChannel
Group:		Libraries
Requires:	Qt5Core >= %{qtbase_ver}
Requires:	Qt5Network >= %{qtbase_ver}
Requires:	Qt5Qml >= %{qtdeclarative_ver}

%description -n Qt5WebChannel
Qt5 WebChannel library provides seamless integration of C++ and QML
applications with HTML/JavaScript clients.

%description -n Qt5WebChannel -l pl.UTF-8
Biblioteka Qt5 WebChannel udostępnia integrację aplikacji C++ i QML z
klientami w HTML-u/JavaScripcie.

%package -n Qt5WebChannel-devel
Summary:	Qt5 WebChannel library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 WebChannel - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt5Core-devel >= %{qtbase_ver}
Requires:	Qt5Network-devel >= %{qtbase_ver}
Requires:	Qt5Qml-devel >= %{qtdeclarative_ver}
Requires:	Qt5WebChannel = %{version}-%{release}

%description -n Qt5WebChannel-devel
Qt5 WebChannel library - development files.

%description -n Qt5WebChannel-devel -l pl.UTF-8
Biblioteka Qt5 WebChannel - pliki programistyczne.

%package doc
Summary:	Qt5 WebChannel documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 WebChannel w formacie HTML
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc
Qt5 WebChannel documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki Qt5 WebChannel w formacie HTML.

%package doc-qch
Summary:	Qt5 WebChannel documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 WebChannel w formacie QCH
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc-qch
Qt5 WebChannel documentation in QCH format.

%description doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt5 WebChannel w formacie QCH.

%package examples
Summary:	Qt5 WebChannel examples
Summary(pl.UTF-8):	Przykłady do biblioteki Qt5 WebChannel
Group:		X11/Development/Libraries
BuildArch:	noarch

%description examples
Qt5 WebChannel examples.

%description examples -l pl.UTF-8
Przykłady do biblioteki Qt5 WebChannel.

%prep
%setup -q -n %{orgname}-everywhere-src-%{version}

%{__sed} -i -e '1{
	s,^#!.*bin/env node,#!/usr/bin/node,
}' \
	examples/webchannel/qwclient/qwclient.js

%build
qmake-qt5
%{__make}
%{?with_doc:%{__make} docs}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%if %{with doc}
%{__make} install_docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# useless symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.so.5.??
# actually drop *.la, follow policy of not packaging them when *.pc exist
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.la

# Prepare some files list
ifecho() {
	r="$RPM_BUILD_ROOT$2"
	if [ -d "$r" ]; then
		echo "%%dir $2" >> $1.files
	elif [ -x "$r" ] ; then
		echo "%%attr(755,root,root) $2" >> $1.files
	elif [ -f "$r" ]; then
		echo "$2" >> $1.files
	else
		echo "Error generation $1 files list!"
		echo "$r: no such file or directory!"
		return 1
	fi
}
ifecho_tree() {
	ifecho $1 $2
	for f in `find $RPM_BUILD_ROOT$2 -printf "%%P "`; do
		ifecho $1 $2/$f
	done
}

echo "%defattr(644,root,root,755)" > examples.files
ifecho_tree examples %{_examplesdir}/qt5/webchannel

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt5WebChannel -p /sbin/ldconfig
%postun	-n Qt5WebChannel -p /sbin/ldconfig

%files -n Qt5WebChannel
%defattr(644,root,root,755)
%doc LICENSE.GPL3-EXCEPT README.md
# R: Core Qml
%attr(755,root,root) %{_libdir}/libQt5WebChannel.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5WebChannel.so.5
%dir %{qt5dir}/qml/QtWebChannel
# R: Core Qml
%attr(755,root,root) %{qt5dir}/qml/QtWebChannel/libdeclarative_webchannel.so
%{qt5dir}/qml/QtWebChannel/plugins.qmltypes
%{qt5dir}/qml/QtWebChannel/qmldir

%files -n Qt5WebChannel-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5WebChannel.so
%{_libdir}/libQt5WebChannel.prl
%{_includedir}/qt5/QtWebChannel
%{_pkgconfigdir}/Qt5WebChannel.pc
%{_libdir}/cmake/Qt5WebChannel
%{qt5dir}/mkspecs/modules/qt_lib_webchannel.pri
%{qt5dir}/mkspecs/modules/qt_lib_webchannel_private.pri

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtwebchannel

%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtwebchannel.qch
%endif

%files examples -f examples.files
%defattr(644,root,root,755)
# XXX: dir shared with qt5-qtbase-examples
%dir %{_examplesdir}/qt5
