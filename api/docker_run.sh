docker stop kt_sim & docker rm kt_sim
docker run -v /$(pwd):/work --rm -it -p 5000:5000 --name kt_sim kt_sim
