#!/bin/bash
# Script to install: docker.io, docker-compose, com.visualstudio.code-oss, pgadmin4, nvm, nodejs, npm and yarn for development of scanhub on Linux Mint (version 21.3 based on Ubuntu jammy)
# For the installation of pgadmin4 the pgadmin.org repository and keys are added to the system according to https://www.pgadmin.org/download/pgadmin-4-apt/.
# The installation of nvm works by downloading and executing a bash script according to https://nodejs.org/en/download/package-manager
# Adds the current linux user to the docker group.

#
# Regular installs with apt and flatpak
#
sudo apt -y install docker.io
sudo apt -y install docker-compose-v2
sudo flatpak install com.visualstudio.code-oss

#
# Installation of nvm, nodejs, npm and yarn 
# Need nvm to install nodejs in newer version than Linux Mint supports with apt.
# Copied from https://nodejs.org/en/download/package-manager
#
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash     # install nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
nvm install 20          # install nodejs 20
npm install -g yarn     # install yarn with npm to get latest version

#
# Installation of pgadmin.org repository and key as well as pgadmin4 itself.
# Copied from https://www.pgadmin.org/download/pgadmin-4-apt/ but replaced $(lsb_release -cs) with jammy for Linux Mint 21.3 which is based on Ubuntu jammy according to https://linuxmint.com/download_all.php
# 
# Install the public key for the pgadmin.org repository:
curl -fsS https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo gpg --dearmor -o /usr/share/keyrings/packages-pgadmin-org.gpg
# Create the repository configuration file:
sudo sh -c 'echo "deb [signed-by=/usr/share/keyrings/packages-pgadmin-org.gpg] https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/jammy pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list && apt update'
# Install for desktop mode only:
sudo apt -y install pgadmin4-desktop

#
# Add user to docker group to avoid the need for sudo on every docker command.
#
sudo usermod -aG docker $(id --user --name)

#
# Final instructions to the user.
#
echo
echo Please reboot or at least logout and login again to make the new docker group for your linux user effective.
echo Afterwards you should be good to go and may start the development with:
echo ./development-launcher.sh --full-rebuild
echo You need to add a first user to the scanhub database "(db-scanhub)". Find details to connect to the database in docker-compose.yml and data for an example user Max with password letmein in defaultuser.txt
echo Good luck! Viel Erfolg!
