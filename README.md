Собираем контейнер:
  docker build -t eltex-controller:latest .
Запускаем контейнер:
  sudo docker run --restart -d -p 80:8005 eltex-controller
