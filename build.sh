#!/bin/bash
# Read version from parent directory
VERSION=$(grep -oP '(?<=version=).*' ../version)

# mkdir -p ../docker_data/grafana/provisioning
# cp -r -u ../grafana/dashboards ../docker_data/grafana/provisioning/dashboards
# cp -r -u ../grafana/datasources ../docker_data/grafana/provisioning/datasources

# mkdir -p ../docker_data/grafana/data
# cp -r -f ../grafana/dashboards ../docker_data/grafana/data/dashboards
# cp -r -f ../grafana/datasources ../docker_data/grafana/data/datasources

docker build --no-cache -t maxo99/weatherflow-collector:${VERSION} -t maxo99/weatherflow-collector:latest  .
# docker push maxo99/weatherflow-collector:latest

# rm -r -f ./grafana/*