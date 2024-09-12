#!/bin/bash
# Script to launch scanhub, run all tests and shut scanhub down again.
# Use option --full-rebuild after making changes to the base container, after installing libraries or when changing other structural aspects.
cd $(dirname $0)
cd ..

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
    echo docker-compose --profile with-frontend build --build-arg BASE_IMG=scanhub-base:latest
    docker-compose --profile with-frontend build --build-arg BASE_IMG=scanhub-base:latest
fi

echo
echo docker-compose --profile with-frontend up --detach
docker-compose --profile with-frontend up --detach

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


cd tests

cd services/exam-manager
source .env/bin/activate
pytest
deactivate

cd ..


echo
echo scanhub: docker-compose --profile with-frontend down
docker-compose --profile with-frontend down

echo
echo run_all_tests.sh is done, bye!
