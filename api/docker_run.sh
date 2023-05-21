docker stop kt_sim_api & docker rm kt_sim_api
docker run -v /$(pwd):/work --rm -it -p 5000:5000 --name kt_sim_api kt_sim_api
