## Importando arquivos locais para dentro do container utilizando mongoimport

docker cp books.json mongo_db:/tmp/books.json
  
  
docker exec mongo_db mongoimport -d books -c books_collection --file /tmp/books.json
