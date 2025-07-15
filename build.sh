#!/bin/bash
# Read version from parent directory
VERSION=$(grep -oP '(?<=version=).*' ../version)

cp -r ../grafana/dashboards ./grafana
cp -r ../grafana/provisioning ./grafana

docker build --no-cache -t maxo99/weatherflow-collector:${VERSION} -t maxo99/weatherflow-collector:latest  .
# docker push maxo99/weatherflow-collector:latest
