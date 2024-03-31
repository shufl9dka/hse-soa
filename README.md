# hse-soa

Евдокимов Роман Николаевич, БПМИ2110, Социальная сеть

### Запуск всего на одной машине:

Запустить СУБД и сервис можно так:
```
$ docker-compose up --build
```

Для очистки контейнеров, сборок и томов можно использовать `docker-compose down -v`

### Ручки сервиса Client API:

Запросы к ручкам можно делать так:

#### Регистрация
```
$ curl -X POST -H "Content-Type: application/json" -d '{"username":"shufl9dka", "password":"c00l_pa$$w0rd"}' http://localhost:5000/api/user/register

{"status":"ok","message":"User registered successfully"}
```

#### Авторизация
```
$ curl -X POST -H "Content-Type: application/json" -d '{"username":"shufl9dka", "password":"c00l_pa$$w0rd"}' http://localhost:5000/api/user/auth

{"status":"ok","message":"Successful auth","token":"eyJhbG...ci"}
```

#### Изменение полей

Нужно взять `TOKEN` как `"token"` из ответа ручки `/api/user/auth`

```
$ TOKEN=eyJhbG...ci
$ curl -X POST -H "Content-Type: application/json" -H "Authorization: $TOKEN" -d '{"first_name":"Raman", "birthdate":"2004-03-29"}' http://localhost:5000/api/user/update
```