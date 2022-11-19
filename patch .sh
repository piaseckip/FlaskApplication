pushd chess-openings-helmcharts
export VERSION=$1
yq -i '.image.tag = strenv(VERSION)' ./app/values.yaml
yq -i '.image.tag = strenv(VERSION)' ./app/charts/flask-app/values.yaml
git add -A
git commit -m "App version changed to ${1}"
git push http://jenkins:$2@35.178.81.143/piaseckip/Portfolio_App_repo.git
popd 