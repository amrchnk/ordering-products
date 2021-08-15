#FROM node
#
#RUN mkdir -p /usr/src/fe/
#WORKDIR /usr/src/fe/
#
#COPY . /usr/src/fe/
##RUN npm install -g npm@7.0.5
##RUN npm i
#
#EXPOSE 8080
#
#CMD ["npm" , "run","serve"]

FROM node:lts-alpine

# устанавливаем простой HTTP-сервер для статики
RUN npm install -g http-server

# делаем каталог 'app' текущим рабочим каталогом
WORKDIR /app

# копируем оба 'package.json' и 'package-lock.json' (если есть)
COPY package*.json ./

# устанавливаем зависимости проекта
RUN npm install

# копируем файлы и каталоги проекта в текущий рабочий каталог (т.е. в каталог 'app')
COPY . .

# собираем приложение для production с минификацией
RUN npm run build

EXPOSE 8080
CMD [ "http-server", "dist" ]