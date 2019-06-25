Собираем контейнер:
  docker build -t eltex-controller:latest .
Запускаем контейнер:
  sudo docker run  -d -p 1234:8005 --restart always eltex-controller
