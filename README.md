<p align="right">
  <img alt="" src="https://i.ibb.co/Lpk3tgK/c3-removebg-preview.png" width="300">
</p>

### Курсовая №5
[> ТЗ тут <](https://www.notion.so/skyengpublic/5-1006b67899fb4ce1bd97668c09352453)

`Позволяет загрузить тестовые данные в базу и сделать по ним выборку согласно ТЗ`

***Старт***

Win -> `python main.py`

Linux -> `python3 main.py`

***ENV***

> необходимо прописать константы для подключения к базе данных Postgres и передавать ([тут](https://github.com/bbt-t/c5/blob/9b246ef64bf45d3fdf5129eab08d6b1096b26719/dump/dump_vacancies.py#L78C18-L78C18) и [тут](https://github.com/bbt-t/c5/blob/1bf8c273de3dc7b674361996f9aee20e8b74aac2/main.py#L16C24-L16C27)) атрибут конфига

из env's (по умолчанию):
```HOST``` ```PG_PORT``` ```POSTGRES_DB``` ```POSTGRES_USER``` ```POSTGRES_PASSWORD```


из файла `.env` (должен находиться в корне проекта, пример смотри тут -> [example_env_file](https://github.com/bbt-t/c5/blob/dev/.example_env)) - передавать атрибут конфига `.file`
