docker stop kt_sim_frontend & docker rm kt_sim_frontend
docker run -v /$(pwd):/work --rm -it -p 3000:3000 --name kt_sim_frontend kt_sim_frontend
