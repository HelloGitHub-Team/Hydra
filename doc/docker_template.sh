#!/bin/bash

function build {
    docker build -t $@:latest .
}

function up {
   docker run \
        --name $@ \
        --mount  type=volume,src=hydra,dst=xxx
        --restart=always \
        --add-host xxx:xxx \
        -d $@:latest
}

function down {
    docker rm -f -v $@
}

function log {
    docker logs -f $@
}

function sh {
    docker exec -it $@ bash
}

function main {
    Command=$1
    shift
    case "${Command}" in
        build)  build $@ ;;
        up)     up $@ ;;
        down)   down $@ ;;
        log)    log $@ ;;
        sh)     sh $@ ;;
        *)      echo "Usage: $0 {build|up|down|log|sh}" ;;
    esac
}

main $@