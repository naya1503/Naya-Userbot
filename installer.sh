#!/usr/bin/env bash

REPO="https://github.com/naya1503/Naya-Userbot.git"
DIR="/root/naya1503"

spinner(){
    local pid=$!
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ];
    do
        for i in "Ooooo" "oOooo" "ooOoo" "oooOo" "ooooO" "oooOo" "ooOoo" "oOooo" "Ooooo"
        do
          echo -ne "\r• $i"
          sleep 0.2
        done
    done
}

clone_repo(){
    if [ ! $BRANCH ]
        then export BRANCH="main"
    fi
    if [ -d $DIR ]
        then
            echo -e $DIR "Already exists.."
            cd $DIR
            git pull
            currentbranch="$(git rev-parse --abbrev-ref HEAD)"
            if [ currentbranch != $BRANCH ]
                then
                    git checkout $BRANCH
            fi
            return
    fi
    echo -e "Cloning Naya-Userbot ${BRANCH}... "
    git clone -b $BRANCH $REPO $DIR
}

install_requirements(){
    pip install --upgrade pip
    echo -e "\n\nInstalling requirements... "
    pip3 install -q --no-cache-dir -r $DIR/requirements.txt
}

dep_install(){
    echo -e "\n\nInstalling DB Requirement..."
    if [ $MONGO_URI ]
        then
            pip3 install -q pymongo[srv]
    elif [ $DATABASE_URL ]
        then
            pip3 install -q psycopg2-binary
    elif [ $REDIS_URI ]
        then
            pip3 install -q redis hiredis
    fi
}

main(){
    (clone_repo)
    (install_requirements)
    (dep_install)
}

main
