# Emulador Óptico 
# Networking Digital Twin Environment - CNETLAB 

Epic: Emulador Óptico

#### Prerequisites

- Linux OS Environment (Ubuntu 20.04 LTS)
- Python 3.7
- XTerm (# sudo apt-get install xterm)
- Pip3 (# sudo apt install python3-pip )
- PyYaml (# pip3 install pyYAML)
- Virtualenv
- [Docker-CE](https://docs.docker.com/get-docker/)


Then, download the CNetLab code from gitlab.

    $ git clone https://git.rnp.br/cnar/sdn-multicamada/emulacao/emulador-optico.git

Enter the _'/emulador-optico'_ directory, create a virtual python environment (virtualenv) and configure to perform the experiment with _'sudo'_ privileges, as shown below:

    $ cd emulador-optico
    $ virtualenv emul -p python3
    $ source emul/bin/activate
    $ pip3 install pyyaml
    $ python3.7 setup.py install

#### How to run experiments on CNetLab

Enter in _'cnetlab/tests/'_ and choose the experiment which you want to run. The code must be run with  root or 'sudo' privileges.

- [Test with Cassini](docs/optical.md)
- [Test with Stratum](docs/stratum.md)
