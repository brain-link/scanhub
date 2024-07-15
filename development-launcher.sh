#!/bin/bash
# Script to launch scanhub and the development tools. It shuts down scanhub after exiting the development session.
# It starts the scanhub containers, except the frontend container, which is started with this script directly. It also starts firefox, pgadmin4 and vscode (flatpack), which need to be installed.
# Use option --full-rebuild on first install, after making changes to the base container, after installing libraries or when changing other structural aspects.
cd $(dirname $0)

echo
echo scanhub: git status
git status

if [ "$1" == --full-rebuild ]
then
    echo
    echo Do full rebuild.
    cd services/base/
    echo services/base/: docker build -t scanhub-base .
    docker build -t scanhub-base .
    cd ../..
    echo
    echo docker-compose build --build-arg BASE_IMG=scanhub-base:latest
    docker-compose build --build-arg BASE_IMG=scanhub-base:latest
fi

echo
sed 308,321s/^/#/ -i docker-compose.yml    # add line comment to start of lines 308 to 321. This allows for faster development by disabling the frontend container and running the frontend directly with this script.
echo docker-compose up -d
docker-compose up -d

if [ "$1" == --full-rebuild ]
then
    cd scanhub-ui
    echo
    echo rm -r .parcel-cache
    rm -r .parcel-cache
    echo scanhub-ui/: yarn install --check-files
    yarn install --check-files
    echo
    echo Wait 10 seconds for backend containers to start
    sleep 10
    echo scanhub-ui/: yarn generate-all-clients
    yarn generate-all-clients
    cd ..
    echo
    echo git status
    git status
fi

echo
echo starting firefox in 15 seconds
echo starting pgadmin4 in 2 seconds
echo starting vscode for scanhub in 2 seconds
sleep 15 && firefox localhost:3000 &
sleep 2 && /usr/pgadmin4/bin/pgadmin4 >> /dev/null 2>&1 &
sleep 2 && /usr/bin/flatpak run --branch=stable --arch=x86_64 --command=code-oss --file-forwarding com.visualstudio.code-oss --unity-launch @@ . @@ >> /dev/null 2>&1

echo
cd scanhub-ui
echo scanhub-ui/: yarn start
echo To stop, press Ctrl-C, wait for parcel to rebuild, press Ctrl-C again, wait for complete shutdown!
yarn start
cd ..

echo
echo scanhub: docker-compose down
docker-compose down
sed 308,321s/^#// -i docker-compose.yml    # remove possible line comments at start of lines 308 to 321. Enable frontend container again.

echo
echo until next time!
