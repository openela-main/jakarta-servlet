%bcond_with bootstrap

Name:           jakarta-servlet
Version:        5.0.0
Release:        10%{?dist}
Summary:        Server-side API for handling HTTP requests and responses
# most of the project is EPL-2.0 or GPLv2 w/exceptions,
# but some files still have Apache-2.0 license headers:
# https://github.com/eclipse-ee4j/servlet-api/issues/347
License:        (EPL-2.0 or GPLv2 with exceptions) and ASL 2.0
URL:            https://github.com/eclipse-ee4j/servlet-api
BuildArch:      noarch

Source0:        https://github.com/eclipse-ee4j/servlet-api/archive/%{version}-RELEASE/servlet-api-%{version}.tar.gz

BuildRequires:  maven-local
%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
%endif

Provides:       glassfish-servlet-api = %{version}-%{release}

%description
Jakarta Servlet defines a server-side API for handling HTTP requests
and responses.

%{?javadoc_package}

%prep
%setup -q -n servlet-api-%{version}-RELEASE

# remove unnecessary dependency on parent POM
%pom_remove_parent . api

# do not build specification documentation
%pom_disable_module spec

# Copy to old package name
# TODO: Remove when all dependencies are migrated from javax.servlet to jakarta.servlet
cp -pr api/src/main/java/jakarta api/src/main/java/javax
sed -i -e 's/jakarta\./javax./g' $(find api/src/main/java/javax -name *.java)
%pom_xpath_replace pom:instructions/pom:Export-Package \
  '<Export-Package>jakarta.servlet.*,javax.servlet.*;version="4.0.0"</Export-Package>' api

# do not install useless parent POM
%mvn_package jakarta.servlet:servlet-parent __noinstall

# remove unnecessary maven plugins
%pom_remove_plugin -r :formatter-maven-plugin
%pom_remove_plugin -r :impsort-maven-plugin
%pom_remove_plugin -r :maven-enforcer-plugin
%pom_remove_plugin -r :maven-javadoc-plugin
%pom_remove_plugin -r :maven-source-plugin

# add maven artifact coordinate aliases for backwards compatibility
%mvn_alias jakarta.servlet:jakarta.servlet-api \
    javax.servlet:javax.servlet-api \
    javax.servlet:servlet-api

# add compat symlink for packages constructing the classpath manually
%mvn_file :{*} %{name}/@1 glassfish-servlet-api

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%license LICENSE.md NOTICE.md
%doc README.md

%changelog
* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 5.0.0-10
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Wed Jun 09 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0.0-9
- Rebuild to workaround DistroBaker issue

* Tue Jun 08 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0.0-8
- Bootstrap Maven for CentOS Stream 9

* Wed May 26 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0.0-7
- Re-add provides on glassfish-servlet-api

* Mon May 17 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0.0-6
- Bootstrap build
- Non-bootstrap build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Aug 20 2020 Mat Booth <mat.booth@redhat.com> - 5.0.0-4
- Correct mvn_file macro invokation

* Wed Aug 19 2020 Fabio Valentini <decathorpe@gmail.com> - 5.0.0-3
- Add compat symlink for packages constructing the classpath manually.

* Wed Aug 19 2020 Mat Booth <mat.booth@redhat.com> - 5.0.0-2
- Also ship the API in the old javax namespace to aid transition

* Thu Aug 13 2020 Fabio Valentini <decathorpe@gmail.com> - 5.0.0-1
- Initial package renamed from glassfish-servlet-api.

