from sqlalchemy import create_engine, text

# Замените на ваши данные для подключения
DATABASE_URL = "postgresql://postgres:postgres@localhost/booking"

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    # Удаляем таблицу с версиями миграций
    conn.execute(text("DROP TABLE IF EXISTS alembic_version CASCADE"))
    conn.commit()
    print("✅ Таблица alembic_version удалена")

print("Теперь можно запускать: alembic revision --autogenerate -m 'initial migration'")




#
#
# openapi_examples={
#     "1":{"summary": "Сочи",
#          "value": {
#             "title": "",
#             "description": "",
#             "price": "",
#             "quantity":"",
#          }
#     },
#     "2":{"summary": "Дубай",
#          "value": {
#             "title": "Отель Rich у фонтана",
#             "location": "Дубай, ул. Шейха, 5",
#          }
#     }
# })