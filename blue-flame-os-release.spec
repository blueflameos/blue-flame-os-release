%global release_name BlueFlameOS
%global dist_version 29

# This package defines the dist tag (see
# https://fedoraproject.org/wiki/Packaging:DistTag).
# That presents a chicken-and-egg problem if another
# system-release file (like fedora-release) is not
# installed. So, if dist is undefined, we define it
# here based on dist-version.

%{!?dist:%global dist .fc%{dist_version}}

Summary:	Blue Flame OS release files
Name:		blue-flame-os-release
Version:	29
Release:	2%{dist}
License:	MIT
Group:		System Environment/Base
Source0:	LICENSE
Source1:	README.developers
Source2:	README.BlueFlameOS-Release-Notes
Source3:	README.license
Source4:	80-server.preset
Source5:	80-workstation.preset
Source6:	85-display-manager.preset
Source7:	90-default.preset
Source8:	99-default-disable.preset
Source9:	convert-to-edition.lua
Source10:	org.gnome.shell.gschema.override
Obsoletes:	redhat-release
Provides:	redhat-release
Provides:	system-release
Provides:	system-release(%{version})

# Comment this next Requires out if we're building for a non-rawhide target
#Requires:	fedora-repos-rawhide
#Requires:	blue-flame-os-repos-rawhide
Requires:	fedora-repos(%{version})
Requires:	blue-flame-os-repos = %{version}
Obsoletes:	blue-flame-os-release-rawhide <= 21-5
BuildArch:	noarch
Conflicts:	fedora-release
Conflicts:	generic-release

%description
Blue Flame OS release files such as yum configs and various /etc/ files that
define the release. This package explicitly is a replacement for the 
trademarked release package, if you are unable for any reason to abide by the 
trademark restrictions on that release package.

%package atomichost
Summary:        Base package for Blue Flame OS Atomic-specific default configurations
Provides:	system-release-atomichost
Provides:	system-release-atomichost(%{version})
Provides:	system-release-product
Requires:	blue-flame-os-release = %{version}-%{release}

%description atomichost
Provides a base package for Blue Flame OS Atomic Host-specific configuration files to
depend on. This package explicitly is a replacement for the trademarked release 
package, if you are unable for any reason to abide by the trademark 
restrictions on that release package.

%package cloud
Summary:        Base package for Blue Flame OS Cloud-specific default configurations
Provides:	system-release-cloud
Provides:	system-release-cloud(%{version})
Provides:	system-release-product
Requires:	blue-flame-os-release = %{version}-%{release}

%description cloud
Provides a base package for Blue Flame OS Cloud-specific configuration files to
depend on.

%package server
Summary:        Base package for Blue Flame OS Server-specific default configurations
Provides:	system-release-server
Provides:	system-release-server(%{version})
Provides:	system-release-product
Requires:	blue-flame-os-release = %{version}-%{release}
Requires:	systemd
Requires:	cockpit-bridge
Requires:	cockpit-networkmanager
Requires:	cockpit-shell
Requires:	cockpit-storaged
Requires:	cockpit-ws
Requires:	openssh-server
Requires(post): systemd

%description server
Provides a base package for Blue Flame OS Server-specific configuration files to
depend on.

%package workstation
Summary:	Base package for Blue Flame OS Workstation-specific default configurations
Provides:	system-release-workstation
Provides:	system-release-workstation(%{version})
Provides:	system-release-product
Requires:	blue-flame-os-release = %{version}-%{release}
# needed for captive portal support
Requires:	NetworkManager-config-connectivity-fedora
Requires(post): /usr/bin/glib-compile-schemas
Requires(postun): /usr/bin/glib-compile-schemas

%description workstation
Provides a base package for Blue Flame OS Workstation-specific configuration files to
depend on.

%package notes
Summary:	Release Notes
License:	Open Publication
Group:		System Environment/Base
Provides:	system-release-notes = %{version}-%{release}
Conflicts:	fedora-release-notes
Conflicts:	generic-release-notes

%description notes
Blue Flame OS release notes package. This package explicitly is a replacement 
for the trademarked release-notes package, if you are unable for any reason
to abide by the trademark restrictions on that release-notes 
package. Please note that there is no actual useful content here.


%prep
%setup -c -T
cp -a %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} %{SOURCE8} %{SOURCE9} %{SOURCE10} .

%build

%install
install -d %{buildroot}/etc
echo "Blue Flame OS release %{version} (%{release_name})" > %{buildroot}/etc/fedora-release
echo "cpe:/o:blueflameos:blueflameos:%{version}" > %{buildroot}/etc/system-release-cpe

# Symlink the -release files
ln -s fedora-release $RPM_BUILD_ROOT/etc/redhat-release
ln -s fedora-release $RPM_BUILD_ROOT/etc/system-release

# Create the common os-release file
install -d $RPM_BUILD_ROOT/usr/lib/os.release.d/
cat << EOF >>$RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-fedora
NAME=Blue Flame OS
VERSION="%{version} (%{release_name})"
ID=blueflameos
ID_LIKE=fedora
VERSION_ID=%{version}
PRETTY_NAME="Blue Flame OS %{version} (%{release_name})"
ANSI_COLOR="0;34"
CPE_NAME="cpe:/o:blueflameos:blueflameos:%{version}"
HOME_URL="https://github.com/blueflameos"
SUPPORT_URL="https://github.com/blueflameos"
BUG_REPORT_URL="https://github.com/blueflameos/blueflameos/issues"
REDHAT_BUGZILLA_PRODUCT="BlueFlameOS"
REDHAT_BUGZILLA_PRODUCT_VERSION=%{bug_version}
REDHAT_SUPPORT_PRODUCT="BlueFlameOS"
REDHAT_SUPPORT_PRODUCT_VERSION=%{bug_version}
PRIVACY_POLICY_URL="http://nsa.gov"
EOF

# Create the common /etc/issue
echo "\S" > $RPM_BUILD_ROOT/usr/lib/os.release.d/issue-fedora
echo "Kernel \r on an \m (\l)" >> $RPM_BUILD_ROOT/usr/lib/os.release.d/issue-fedora
echo >> $RPM_BUILD_ROOT/usr/lib/os.release.d/issue-fedora

# Create /etc/issue.net
echo "\S" > $RPM_BUILD_ROOT/usr/lib/issue.net
echo "Kernel \r on an \m (\l)" >> $RPM_BUILD_ROOT/usr/lib/issue.net
ln -s ../usr/lib/issue.net $RPM_BUILD_ROOT/etc/issue.net

# Create os-release and issue files for the different editions

# Atomic Host - https://bugzilla.redhat.com/show_bug.cgi?id=1200122
cp -p $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-fedora \
      $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-atomichost
echo "VARIANT=\"Atomic Host\"" >> $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-atomichost
echo "VARIANT_ID=atomic.host" >> $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-atomichost
sed -i -e "s|(%{release_name})|(Atomic Host)|g" $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-atomichost

# Cloud
cp -p $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-fedora \
      $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-cloud
echo "VARIANT=\"Cloud Edition\"" >> $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-cloud
echo "VARIANT_ID=cloud" >> $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-cloud
sed -i -e "s|(%{release_name})|(Cloud Edition)|g" $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-cloud

# Server
cp -p $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-fedora \
      $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-server
echo "VARIANT=\"Server Edition\"" >> $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-server
echo "VARIANT_ID=server" >> $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-server
sed -i -e "s|(%{release_name})|(Server Edition)|g" $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-server

cp -p $RPM_BUILD_ROOT/usr/lib/os.release.d/issue-fedora \
      $RPM_BUILD_ROOT/usr/lib/os.release.d/issue-server
echo "Admin Console: https://\4:9090/ or https://[\6]:9090/" >> $RPM_BUILD_ROOT/usr/lib/os.release.d/issue-server
echo >> $RPM_BUILD_ROOT/usr/lib/os.release.d/issue-server

# Workstation
cp -p $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-fedora \
      $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-workstation
echo "VARIANT=\"Workstation Edition\"" >> $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-workstation
echo "VARIANT_ID=workstation" >> $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-workstation
sed -i -e "s|(%{release_name})|(Workstation Edition)|g" $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-workstation

# Create the symlink for /etc/os-release
# We don't create the /usr/lib/os-release symlink until %%post
# so that we can ensure that the right one is referenced.
ln -s ../usr/lib/os-release $RPM_BUILD_ROOT/etc/os-release

# Create the symlink for /etc/issue
# We don't create the /usr/lib/os-release symlink until %%post
# so that we can ensure that the right one is referenced.
ln -s ../usr/lib/issue $RPM_BUILD_ROOT/etc/issue

# Set up the dist tag macros
install -d -m 755 $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d
cat >> $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d/macros.dist << EOF
# dist macros.

%%fedora                %{dist_version}
%%dist                .fc%{dist_version}
%%fc%{dist_version}                1
EOF

# Add presets
mkdir -p $RPM_BUILD_ROOT/usr/lib/systemd/user-preset/
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/
mkdir -p $RPM_BUILD_ROOT/usr/lib/os.release.d/presets

# Default system wide
install -m 0644 85-display-manager.preset $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/
install -m 0644 90-default.preset $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/
install -m 0644 99-default-disable.preset $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/
# Fedora Server
install -m 0644 80-server.preset $RPM_BUILD_ROOT%{_prefix}/lib/os.release.d/presets/
# Fedora Workstation
install -m 0644 80-workstation.preset $RPM_BUILD_ROOT%{_prefix}/lib/os.release.d/presets/

# Override the list of enabled gnome-shell extensions for Workstation
mkdir -p $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas/
install -m 0644 org.gnome.shell.gschema.override $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas/

%post -p <lua>
%include %{_sourcedir}/convert-to-edition.lua
-- On initial installation, we'll at least temporarily put the non-product
-- symlinks in place. It will be overridden by blue-flame-os-release-$EDITION
-- %%post sections because we don't write the /usr/lib/variant file until
-- %%posttrans to avoid trumping the blue-flame-os-release-$EDITION packages.
-- This is necessary to avoid breaking systemctl scripts since they rely on
-- /usr/lib/os-release being valid. We can't wait until %%posttrans to default
-- to os-release-fedora.
if arg[2] == "0" then
    set_release(fedora)
    set_issue(fedora)
end

-- We also want to forcibly set these paths on upgrade if we are explicitly
-- set to "nonproduct"
if read_variant() == "nonproduct" then
    convert_to_edition("nonproduct", false)
end

%posttrans -p <lua>
%include %{_sourcedir}/convert-to-edition.lua
-- If we get to %%posttrans and nothing created /usr/lib/variant, set it to
-- nonproduct.
install_edition("nonproduct")

%post atomichost -p <lua>
%include %{_sourcedir}/convert-to-edition.lua
install_edition("atomichost")

%preun atomichost -p <lua>
%include %{_sourcedir}/convert-to-edition.lua
uninstall_edition("atomichost")

%post cloud -p <lua>
%include %{_sourcedir}/convert-to-edition.lua
install_edition("cloud")

%preun cloud -p <lua>
%include %{_sourcedir}/convert-to-edition.lua
uninstall_edition("cloud")

%post server -p <lua>
%include %{_sourcedir}/convert-to-edition.lua
install_edition("server")

%preun server -p <lua>
%include %{_sourcedir}/convert-to-edition.lua
uninstall_edition("server")

%post workstation -p <lua>
%include %{_sourcedir}/convert-to-edition.lua
install_edition("workstation")

%preun workstation -p <lua>
%include %{_sourcedir}/convert-to-edition.lua
uninstall_edition("workstation")

%postun workstation
if [ $1 -eq 0 ] ; then
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans workstation
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files
%defattr(-,root,root,-)
%license LICENSE README.license
%ghost /usr/lib/variant
%dir /usr/lib/os.release.d
%dir /usr/lib/os.release.d/presets
%config %attr(0644,root,root) /usr/lib/os.release.d/os-release-fedora
%ghost /usr/lib/os-release
/etc/os-release
%config %attr(0644,root,root) /etc/fedora-release
/etc/redhat-release
/etc/system-release
%config %attr(0644,root,root) /etc/system-release-cpe
%config %attr(0644,root,root) /usr/lib/os.release.d/issue-fedora
%ghost /usr/lib/issue
%config(noreplace) /etc/issue
%config %attr(0644,root,root) /usr/lib/issue.net
%config(noreplace) /etc/issue.net
%attr(0644,root,root) %{_rpmconfigdir}/macros.d/macros.dist
%dir /usr/lib/systemd/user-preset/
%dir %{_prefix}/lib/systemd/system-preset/
%{_prefix}/lib/systemd/system-preset/85-display-manager.preset
%{_prefix}/lib/systemd/system-preset/90-default.preset
%{_prefix}/lib/systemd/system-preset/99-default-disable.preset

%files atomichost
%license LICENSE
%config %attr(0644,root,root) /usr/lib/os.release.d/os-release-atomichost

%files cloud
%license LICENSE
%config %attr(0644,root,root) /usr/lib/os.release.d/os-release-cloud

%files server
%license LICENSE
%config %attr(0644,root,root) /usr/lib/os.release.d/os-release-server
%config %attr(0644,root,root) /usr/lib/os.release.d/issue-server
%ghost %{_prefix}/lib/systemd/system-preset/80-server.preset
%config %attr(0644,root,root) /usr/lib/os.release.d/presets/80-server.preset

%files workstation
%license LICENSE
%config %attr(0644,root,root) /usr/lib/os.release.d/os-release-workstation
%{_datadir}/glib-2.0/schemas/org.gnome.shell.gschema.override
%ghost %{_prefix}/lib/systemd/system-preset/80-workstation.preset
%config %attr(0644,root,root) /usr/lib/os.release.d/presets/80-workstation.preset

%files notes
%defattr(-,root,root,-)
%doc README.BlueFlameOS-Release-Notes

%changelog
* Fri Nov 16 2018 yucuf Sourani <youssef.m.sourani@gmail.com> - 29-2
- Release 2

* Fri Nov 16 2018 yucuf Sourani <youssef.m.sourani@gmail.com> - 29-1
- Initial For BlueFlameOS 29

* Mon Jul 09 2018 Adam Williamson <awilliam@redhat.com> - 29-0.2
- Server: don't require rolekit (not installable, soon to be retired)

* Mon Apr 16 2018 Tom Callaway <spot@fedoraproject.org> 29-0.1
- add ID_LIKE=fedora to os-release
- update to 29

* Wed Nov 15 2017 Tom Callaway <spot@fedoraproject.org> 28-0.3
- rework significantly to match fedora-release

* Mon Sep 25 2017 Matthew Miller <mattdm@fedoraproject.org> 28-0.2
- use dist-tag -- and define it if previously undefined

* Wed Aug 23 2017 Mohan Boddu <mboddu@redhat.com> 28-0.1
- Rawhide is now 28

* Fri Mar  3 2017 Tom Callaway <spot@fedoraproject.org> 27-0.1
- Rawhide is now 27

* Thu Aug 04 2016 Bruno Wolff III <bruno@wolff.to> - 26-0.1
- Rawhide is now 26

* Sat Mar 05 2016 Bruno Wolff III <bruno@wolff.to> - 25-0.1
- Rawhide is now 25

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 24-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 19 2016 Tom Callaway <spot@fedoraproject.org> - 24-0.3
- spec file cleanups

* Sat Aug 22 2015 Bruno Wolff III <bruno@wolff.to> - 24-0.2
- Fix typo in obsoletes

* Wed Jul 15 2015 Bruno Wolff III <bruno@wolff.to> - 24-0.1
- Rawhide is now f24

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 23-0.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Dennis Gilmore <dennis@ausil.us> - 23-0.5
- add system preset files
- drop product sub-packages

* Sat Feb 14 2015 Bruno Wolff III <bruno@wolff.to> - 23-0.4
- Fix up change log

* Sat Feb 14 2015 Bruno Wolff III <bruno@wolff.to> - 23-0.3
- Rawhide is now 23

* Tue Oct 21 2014 Tom Callaway <spot@fedoraproject.org> - 22-0.3
- add versioned provide for system-release(VERSION)

* Tue Oct 21 2014 Tom Callaway <spot@fedoraproject.org> - 22-0.2
- add productization (it is the foooooture)

* Thu Aug 07 2014 Dennis Gilmore <dennis@ausil.us> - 22-0.1
- Require fedora-repos and no longer ship repo files

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Tom Callaway <spot@fedoraproject.org> - 21-4
- license changes and clarification doc

* Sun Mar 09 2014 Bruno Wolff III <bruno@wolff.to> - 21-3
- Install dist macro into the correct directory

* Sun Jan 05 2014 Bruno Wolff III <bruno@wolff.to> - 21-2
- Work around incorrect prefix in the upstream tarball

* Sun Jan 05 2014 Bruno Wolff III <bruno@wolff.to> - 21-1
- Bump version to match current rawhide

* Sat Dec 21 2013 Bruno Wolff III <bruno@wolff.to> - 21-0.3
- Update version to 21 (which should have happened when f20 was branched)
- Changed to work with recent yum change (bug 1040607)

* Mon Dec  9 2013 Tom Callaway <spot@fedoraproject.org> - 20-1
- final release (disable rawhide dep)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 26 2013 Tom Callaway <spot@fedoraproject.org> - 20-0.1
- sync

* Wed Jun 26 2013 Tom Callaway <spot@fedoraproject.org> - 19-2
- sync to release

* Mon Mar 11 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 19-0.3
- Remove %%config from %%{_sysconfdir}/rpm/macros.*
  (https://fedorahosted.org/fpc/ticket/259).

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 19-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 19 2012 Tom Callaway <spot@fedoraproject.org> - 19-0.1
- sync to 19-0.1

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 18-0.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 10 2012 Tom Callaway <spot@fedoraproject.org> - 18-0.2
- sync with fedora-release model

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17-0.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 28 2011 Tom Callaway <spot@fedoraproject.org> - 17-0.2
- initial 17

* Fri Jul 22 2011 Tom Callaway <spot@fedoraproject.org> - 16-0.2
- require -rawhide subpackage if we're built for rawhide

* Fri May 13 2011 Tom Callaway <spot@fedoraproject.org> - 16-0.1
- initial 16

* Fri May 13 2011 Tom Callaway <spot@fedoraproject.org> - 15-1
- sync to f15 final

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 20 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 15-0.3
- sync to rawhide

* Wed Feb 24 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 14-0.2
- fix broken requires

* Wed Feb 17 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 14-0.1
- update to sync with fedora-release

* Mon Nov 16 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 12-1
- Update for F12 final

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 20 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 11.90-1
- Build for F12 collection

* Wed May 20 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 11-1
- resync with fedora-release package

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.90-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Tom "spot" Callaway <tcallawa@redhat.com> 10.90-2
- drop Requires: system-release-notes

* Thu Nov 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 10.90-1
- 10.90

* Thu Nov 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 10-1
- Bump to 10, update repos

* Mon Sep 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> 9.91-2
- add Conflicts
- further sanitize descriptions

* Mon Sep 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> 9.91-1
- initial package for generic-release and generic-release-notes
