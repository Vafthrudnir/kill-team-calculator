docker stop kt_sim & docker rm kt_sim
docker run -v /$(pwd):/work --rm -it --name kt_sim kt_sim
