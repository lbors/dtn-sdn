# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2020 National Network for Education and Research (RNP)        +
#                                                                              +
#     Licensed under the Apache License, Version 2.0 (the "License");          +
#     you may not use this file except in compliance with the License.         +
#     You may obtain a copy of the License at                                  +
#                                                                              +
#         http://www.apache.org/licenses/LICENSE-2.0                           +
#                                                                              +
#     Unless required by applicable law or agreed to in writing, software      +
#     distributed under the License is distributed on an "AS IS" BASIS,        +
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. +
#     See the License for the specific language governing permissions and      +
#     limitations under the License.                                           +
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import sys

from setuptools.command.install import install
import subprocess
import yaml


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        install.run(self)
        # self.install_models()
        self.install_requeriments()

    def exec_cmd(self, cmd):
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            output = p.stdout.readline()
            if output == '' or p.poll() is not None:
                break
            if output:
                print(output.decode("utf-8").strip())

    def install_models(self):
        with open("models.yaml") as file:
            models = yaml.load(file, Loader=yaml.FullLoader)
            for model, image in models['Models'].items():
                print("Installing model {} with image {}".format(model, image))
                cmd = "/usr/bin/docker pull {}".format(image)
                self.exec_cmd(cmd)

    def install_requeriments(self):
        with open("requirements.txt") as file:
            #required = file.read().splitlines()
            for modules in file.readlines():
                #print("Installing module {}".format(modules))
                cmd = "pip3 install {}".format(modules)
                self.exec_cmd(cmd)

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='cnetlab',
    version='0.1',
    packages=find_packages(),
    url='https://git.rnp.br/cnar/sdn-multicamada/emulacao/emulador-optico.git',
    license='APACHE 2',
    author='Fernando Farias',
    author_email='fernando.farias@rnp.br',
    description='Network emulator as part of SDN-Multilayer project from RNP',
    install_requires=required,
    cmdclass={
        'install': PostInstallCommand,
    },
    classifiers=[
        'Development Status :: 0.1 - Release',
        'License :: OSI Approved :: APACHE2 License',
        'Programming Language :: Python :: 3.8',
        'Topic :: SDN-NG :: Network Emulator',
    ]
)
