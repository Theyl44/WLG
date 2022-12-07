#!/bin/bash
id_container=`cat running_docker`
docker stop $id_container
