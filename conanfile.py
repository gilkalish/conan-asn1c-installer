import os
from conans import AutoToolsBuildEnvironment, tools
from nxtools import NxConanFile


class Asn1cInstallerConan(NxConanFile):
    name = "asn1c"
    description = "provide asn1c compiler"
    license = "OSI-approved BSD 3-clause"
    url = "http://github.com/hoxnox/conan-asn1c-installer"
    settings = "os_build", "arch_build"
    version = "0.9.28"

    def do_source(self):
        self.retrieve("8007440b647ef2dd9fb73d931c33ac11764e6afb2437dbe638bb4e5fc82386b9",
                [
                    "vendor://vlm/asn1c/asn1c-{v}.tar.gz".format(v=self.version),
                    "https://github.com/vlm/asn1c/releases/download/v{v}/asn1c-{v}.tar.gz".format(v=self.version)
                ], "asn1c-{v}.tar.gz".format(v=self.version))


    def do_build(self):
        build_dir = "{staging_dir}/src".format(staging_dir=self.staging_dir)
        tools.untargz("asn1c-{v}.tar.gz".format(v=self.version), build_dir)
        env_build = AutoToolsBuildEnvironment(self)
        with tools.environment_append(env_build.vars):
            self.run("cd {build_dir}/asn1c-{v} && ./configure --prefix={prefix}".format(
                         v = self.version,
                         build_dir=build_dir,
                         prefix=self.package_folder))
            self.run("cd {build_dir}/asn1c-{v} && PREFIX={staging} make install".format(v =
                self.version, build_dir = build_dir, staging = self.staging_dir))

    def do_package(self):
        self.copy(pattern="bin/*", dst="", src=self.staging_dir)
        self.copy(pattern="share/asn1c/*", dst="", src=self.staging_dir)

    def do_package_info(self):
        if self.package_folder is not None:
            self.env_info.path.append(os.path.join(self.package_folder, "bin"))
            templates_dir = os.path.join(self.package_folder, "share", "asn1c")
            self.env_info.CMAKE_MODULE_PATH = templates_dir
            if not os.path.exists(templates_dir):
                raise Exception("asn1c templates dir not found: %s" % templates_dir)
