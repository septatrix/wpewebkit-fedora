## NOTE: Lots of files in various subdirectories have the same name (such as
## "LICENSE") so this short macro allows us to distinguish them by using their
## directory names (from the source tree) as prefixes for the files.
%global add_to_license_files() \
        mkdir -p _license_files ; \
cp -p %1 _license_files/$(echo '%1' | sed -e 's!/!.!g')

Name:           wpewebkit
Version:        2.38.0
Release:        1%{?dist}
Summary:        A WebKit port optimized for low-end devices

License:        LGPLv2 and BSD
URL:            https://www.%{name}.org/
Source0:        https://wpewebkit.org/releases/%{name}-%{version}.tar.xz

Patch0:         fix-user-style-sheet.patch

BuildRequires: atk-devel at-spi2-atk-devel
BuildRequires: bison
BuildRequires: cairo-devel
BuildRequires: cmake
BuildRequires: egl-wayland-devel
BuildRequires: flex
BuildRequires: clang
BuildRequires: gi-docgen
BuildRequires: gnutls-devel
BuildRequires: gperf
BuildRequires: gstreamer1-devel
BuildRequires: gstreamer1-plugins-bad-free-devel
BuildRequires: gstreamer1-plugins-base-devel
BuildRequires: harfbuzz-devel
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: libatomic
BuildRequires: libepoxy-devel
BuildRequires: libicu-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libsoup-devel
BuildRequires: libwebp-devel
BuildRequires: libwpe-devel
BuildRequires: libxslt-devel
BuildRequires: mesa-libEGL-devel
BuildRequires: mesa-libgbm-devel
BuildRequires: ninja-build
BuildRequires: openjpeg2-devel
BuildRequires: perl(English)
BuildRequires: perl(File::Copy::Recursive)
BuildRequires: perl-File-Find
BuildRequires: perl(FindBin)
BuildRequires: perl(JSON::PP)
BuildRequires: perl(lib)
BuildRequires: perl(Switch)
BuildRequires: python3
BuildRequires: ruby
BuildRequires: rubygem-json
BuildRequires: rubygems
BuildRequires: sqlite-devel
BuildRequires: systemd-devel
BuildRequires: wayland-devel
BuildRequires: wayland-protocols-devel
BuildRequires: woff2-devel
BuildRequires: wpebackend-fdo-devel
BuildRequires: bubblewrap
BuildRequires: libgcrypt-devel
BuildRequires: libseccomp-devel
BuildRequires: xdg-dbus-proxy
BuildRequires: lcms2-devel
Requires: atk
Requires: at-spi2-atk

%description
WPE allows embedders to create simple and performant systems based on
Web platform technologies. It is designed with hardware acceleration
in mind, leveraging common 3D graphics APIs for best performance.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries, build data, and header
files for developing applications that use %{name}

%prep
%autosetup -p1 -n wpewebkit-%{version}

%build
# Increase the DIE limit so our debuginfo packages could be size optimized.
# Decreases the size for x86_64 from ~5G to ~1.1G.
# https://bugzilla.redhat.com/show_bug.cgi?id=1456261
%global _dwz_max_die_limit 250000000

# The _dwz_max_die_limit is being overridden by the arch specific ones from the
# redhat-rpm-config so we need to set the arch specific ones as well - now it
# is only needed for x86_64.
%global _dwz_max_die_limit_x86_64 250000000

# This package fails to build with LTO due to undefined symbols.  LTO
# was disabled in openSUSE as well, but with no real explanation why
# beyond the undefined symbols.  It really shold be investigated further.
# Disable LTO
%define _lto_cflags %{nil}

# Decrease debuginfo even on ix86 because of:
# https://bugs.webkit.org/show_bug.cgi?id=140176
%ifarch s390x %{arm} %{ix86} %{power64} %{mips}
# Decrease debuginfo verbosity to reduce memory consumption even more
%global optflags %(echo %{optflags} | sed 's/-g /-g1 /')
%endif

%cmake \
  -DCMAKE_C_COMPILER=clang \
  -DCMAKE_CXX_COMPILER=clang++ \
  -DPORT=WPE \
  -DCMAKE_BUILD_TYPE=Release \
  -DENABLE_MINIBROWSER=ON \
  -DUSE_SOUP2=ON \
  -DENABLE_DOCUMENTATION=OFF \
  -DENABLE_INTROSPECTION=OFF \
  -GNinja


# Show the build time in the status
export NINJA_STATUS="[%f/%t][%e] "
%cmake_build

%install
%cmake_install

# Finally, copy over and rename various files for %license inclusion
%add_to_license_files Source/JavaScriptCore/disassembler/zydis/LICENSE-zydis.txt
%add_to_license_files Source/JavaScriptCore/disassembler/zydis/LICENSE-zycore.txt
%add_to_license_files Source/WebCore/LICENSE-LGPL-2
%add_to_license_files Source/WebCore/LICENSE-APPLE
%add_to_license_files Source/WebCore/LICENSE-LGPL-2.1
%add_to_license_files Source/WTF/LICENSE-libc++.txt
%add_to_license_files Source/WTF/wtf/dtoa/LICENSE
%add_to_license_files Source/WTF/LICENSE-LLVM.txt
%add_to_license_files Source/WTF/icu/LICENSE
%add_to_license_files Source/WebInspectorUI/UserInterface/External/Esprima/LICENSE
%add_to_license_files Source/WebInspectorUI/UserInterface/External/CodeMirror/LICENSE
%add_to_license_files Source/WebInspectorUI/UserInterface/External/three.js/LICENSE
%add_to_license_files Source/WebInspectorUI/UserInterface/External/CSSDocumentation/LICENSE
%add_to_license_files Source/ThirdParty/gtest/LICENSE
%add_to_license_files Source/ThirdParty/ANGLE/src/libANGLE/renderer/vulkan/shaders/src/third_party/ffx_spd/LICENSE
%add_to_license_files Source/ThirdParty/ANGLE/src/third_party/ceval/LICENSE
%add_to_license_files Source/ThirdParty/ANGLE/src/third_party/volk/LICENSE.md
%add_to_license_files Source/ThirdParty/ANGLE/src/third_party/libXNVCtrl/LICENSE
%add_to_license_files Source/ThirdParty/ANGLE/src/common/third_party/smhasher/LICENSE
%add_to_license_files Source/ThirdParty/ANGLE/src/common/third_party/xxhash/LICENSE
%add_to_license_files Source/ThirdParty/ANGLE/src/tests/test_utils/third_party/LICENSE
%add_to_license_files Source/ThirdParty/ANGLE/LICENSE
%add_to_license_files Source/ThirdParty/ANGLE/third_party/proguard/LICENSE
%add_to_license_files Source/ThirdParty/ANGLE/third_party/turbine/LICENSE
%add_to_license_files Source/ThirdParty/ANGLE/third_party/bazel/LICENSE
%add_to_license_files Source/ThirdParty/ANGLE/third_party/colorama/LICENSE
%add_to_license_files Source/ThirdParty/ANGLE/third_party/android_system_sdk/LICENSE
%add_to_license_files Source/ThirdParty/ANGLE/third_party/r8/LICENSE
%add_to_license_files Source/ThirdParty/ANGLE/tools/flex-bison/third_party/m4sugar/LICENSE
%add_to_license_files Source/ThirdParty/ANGLE/tools/flex-bison/third_party/skeletons/LICENSE
%add_to_license_files Source/ThirdParty/ANGLE/util/windows/third_party/StackWalker/LICENSE

%files
%{_bindir}/WPEWebDriver
%{_libdir}/libWPEWebKit-1.0.so.3
%{_libdir}/libWPEWebKit-1.0.so.3.*
%{_libexecdir}/wpe-webkit-1.0
%{_libdir}/wpe-webkit-1.0
%doc NEWS
%license _license_files/*ThirdParty*
%license _license_files/*WebCore*
%license _license_files/*WebInspectorUI*
%license _license_files/*WTF*
%license _license_files/*JavaScriptCore*

%files devel
%{_includedir}/wpe-webkit-1.0
%{_libdir}/libWPEWebKit-1.0.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Sat Sep 24 2022 Philippe Normand <philn@igalia.com> - 2.38.0-7
- 2.38, with patch to fix generated user style sheets.

* Sat Sep 24 2022 Philippe Normand <philn@igalia.com> - 2.38.0-6
- 2.38, fresh off the oven. Build attempt #6

* Sat Sep 24 2022 Philippe Normand <philn@igalia.com> - 2.38.0-5
- 2.38, fresh off the oven. Build attempt #5

* Sat Sep 24 2022 Philippe Normand <philn@igalia.com> - 2.38.0-4
- 2.38, fresh off the oven. Build attempt #4

* Fri Sep 16 2022 Philippe Normand <philn@igalia.com> - 2.38.0-3
- 2.38, fresh off the oven. Build attempt #3

* Fri Sep 16 2022 Philippe Normand <philn@igalia.com> - 2.38.0-2
- 2.38, fresh off the oven. Build attempt #2

* Fri Sep 16 2022 Philippe Normand <philn@igalia.com> - 2.38.0-1
- 2.38, fresh off the oven. Build attempt #1

* Fri Aug 26 2022 Philippe Normand <philn@igalia.com> - 2.36.7-1
- Guess what, new version

* Wed Aug 10 2022 Philippe Normand <philn@igalia.com> - 2.36.6-1
- New version

* Sun Jul 31 2022 Philippe Normand <philn@igalia.com> - 2.36.5-1
- New version

* Thu Jul 07 2022 Philippe Normand <philn@igalia.com> - 2.36.4-1
- New version

* Sat May 28 2022 Philippe Normand <philn@igalia.com> - 2.36.3-1
- New version

* Wed May 18 2022 Philippe Normand <philn@igalia.com> - 2.36.2-1
- New version

* Sun May 01 2022 Philippe Normand <philn@igalia.com> - 2.36.1-1
- New version

* Sun Mar 27 2022 Philippe Normand <philn@igalia.com> - 2.36.0-1
- New version

* Fri Mar 25 2022 Philippe Normand <philn@igalia.com> - 2.34.6-1
- New version

* Fri Feb 11 2022 Philippe Normand <philn@igalia.com> - 2.34.5-1
- New version

* Tue Jan 21 2022 Philippe Normand <philn@igalia.com> - 2.34.4-1
- New version

* Tue Jan 04 2022 Philippe Normand <philn@igalia.com> - 2.34.3-1
- New version

* Wed Nov 24 2021 Philippe Normand <philn@igalia.com> - 2.34.2-1
- New version

* Tue Oct 26 2021 Philippe Normand <philn@igalia.com> - 2.34.1-1
- New version

* Sat Oct 09 2021 Philippe Normand <philn@igalia.com> - 2.32.4-1
- New version

* Sat Jul 24 2021 Philippe Normand <philn@igalia.com> - 2.32.3-1
- New version

* Tue Jul 13 2021 Philippe Normand <philn@igalia.com> - 2.32.2-1
- New version

* Sat May 22 2021 Philippe Normand <philn@igalia.com> - 2.32.1-1
- New version

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.26.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Sep 28 2019 Chris King <bunnyapocalypse@protonmail.org> - 2.26.1-1
- New version, added atk/bubblewrap libs for build, removed crypto patch as its
  no longer needed. Also, sobump.

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.24.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 20 2019 Chris King <bunnyapocalypse@protonmail.org> - 2.24.2-1
- New version

* Fri Apr 19 2019 Chris King <bunnyapocalypse@protonmail.org> - 2.24.1-1
- New version

* Wed Mar 27 2019 Chris King <bunnyapocalypse@protonmail.org> - 2.24.0-1
- New version

* Tue Mar 19 2019 Chris King <bunnyapocalypse@protonmail.org> - 2.22.5-1
- New version

* Sat Feb 09 2019 Chris King <bunnyapocalypse@protonmail.org> - 2.22.4-1
- New version and removing patches that were upstreamed in this version

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.21.92-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 24 2019 Pete Walter <pwalter@fedoraproject.org> - 2.21.92-3
- Rebuild for ICU 63

* Fri Sep 21 2018 Chris King <bunnyapocalypse@protonmail.org> - 2.21.92-2
- Adding another patch so the package properly installs

* Fri Sep 14 2018 Chris King <bunnyapocalypse@protonmail.org> - 2.21.92-1
- Adding some patches to fix failing builds

* Mon Sep 10 2018 Chris King <bunnyapocalypse@protonmail.org> - 2.21.92-1
- Soname bump and version update

* Tue Jul 17 2018 Chris King <bunnyapocalypse@fedoraproject.org> - 2.21.2-1
- Initial RPM package.
