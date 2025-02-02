docker pull whmi/dl_ai_one_container
docker run -p 80:80 -p 5432:5432 -p 8000:8000 --name dl_ai_container whmi/dl_ai_one_container