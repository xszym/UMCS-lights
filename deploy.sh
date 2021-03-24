#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

(
  cd "$DIR/.."

  ssh -i $ID_RSA -o StrictHostKeyChecking=no $SERVER_USER@$SERVER_IP -p $SERVER_SSH_PORT <<-EOF
    cd ~/UMCS-lights
    git pull
    docker login -u gitlab-ci-token -p $CI_BUILD_TOKEN $CI_REGISTRY
    docker-compose pull
    docker-compose stop
    docker-compose rm -f
    docker-compose -f docker-compose.prod.yml up -d
EOF
)