#!/bin/bash
# Script to launch scanhub and the development tools. It shuts down scanhub after exiting the development session.
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
    echo docker compose build --build-arg BASE_IMG=scanhub-base:latest
    docker compose build --build-arg BASE_IMG=scanhub-base:latest
fi

echo
echo docker compose up -d
docker compose up -d

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
sleep 15 && firefox localhost &
sleep 2 && /usr/pgadmin4/bin/pgadmin4 >> /dev/null 2>&1 &
sleep 2 && /usr/bin/flatpak run --branch=stable --arch=x86_64 --command=code-oss --file-forwarding com.visualstudio.code-oss --unity-launch @@ . @@ >> /dev/null 2>&1

read -p "Press enter to stop the containers."

echo
echo scanhub: docker compose down
docker compose down

echo
echo until next time!
