# """ Этот код запускается один раз, для создания кнопок в БД"""

# import sqlite3

# # # Устанавливаем соединение с базой данных
# connection = sqlite3.connect('buttons_db/database.db')
# cursor = connection.cursor()

# # Создаем таблицу create_menu
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS create_menu (
# type_menu TEXT NOT NULL,
# order_num INTEGER,
# btn_name TEXT NOT NULL,
# btn_callback TEXT NOT NULL
# )
# ''')

# cursor.execute('INSERT INTO create_menu (type_menu, order_num, btn_name, btn_callback) VALUES (?, ?, ?, ?)', ('main', 1, '➕ Новый ученик', 'new_student')),
# cursor.execute('INSERT INTO create_menu (type_menu, order_num, btn_name, btn_callback) VALUES (?, ?, ?, ?)', ('main', 2, "💸 Оплата", 'payment')),
# cursor.execute('INSERT INTO create_menu (type_menu, order_num, btn_name, btn_callback) VALUES (?, ?, ?, ?)', ('main', 3, "🥶 Зоморозка", 'cold')),

# cursor.execute('INSERT INTO create_menu (type_menu, order_num, btn_name, btn_callback) VALUES (?, ?, ?, ?)', ('new_student', 1, "Пн • Ср • Пт", 'mwf')),
# cursor.execute('INSERT INTO create_menu (type_menu, order_num, btn_name, btn_callback) VALUES (?, ?, ?, ?)', ('new_student', 2, "Вт • Чт • Сб", 'tts')),
# cursor.execute('INSERT INTO create_menu (type_menu, order_num, btn_name, btn_callback) VALUES (?, ?, ?, ?)', ('new_student', 3, "Пн ••• Пт", 'ed')),
# cursor.execute('INSERT INTO create_menu (type_menu, order_num, btn_name, btn_callback) VALUES (?, ?, ?, ?)', ('new_student', 4, "🔙 Назад", 'main')),

# cursor.execute('INSERT INTO create_menu (type_menu, order_num, btn_name, btn_callback) VALUES (?, ?, ?, ?)', ('pay',1, '◀️ Предыдущий абонемент', "previous")),
# cursor.execute('INSERT INTO create_menu (type_menu, order_num, btn_name, btn_callback) VALUES (?, ?, ?, ?)', ('pay', 2, '🔙 Назад',  'main'))

# cursor.execute('INSERT INTO create_menu (type_menu, order_num, btn_name, btn_callback) VALUES (?, ?, ?, ?)', ('cold', 1,  '🌬 Заморозить', 'freeze'))
# cursor.execute('INSERT INTO create_menu (type_menu, order_num, btn_name, btn_callback) VALUES (?, ?, ?, ?)', ('cold', 2,  '❄️ Массовая заморозка', 'bulk_freezing'))
# cursor.execute('INSERT INTO create_menu (type_menu, order_num, btn_name, btn_callback) VALUES (?, ?, ?, ?)', ('cold', 3,  '🔙 Назад', 'main'))

# cursor.execute('INSERT INTO create_menu (type_menu, order_num, btn_name, btn_callback) VALUES (?, ?, ?, ?)', ('payment', 1,  '⏭ Продолжить', 'continue'))
# cursor.execute('INSERT INTO create_menu (type_menu, order_num, btn_name, btn_callback) VALUES (?, ?, ?, ?)', ('payment', 1,  '🧨 Продолжить в долг', 'continue'))
# cursor.execute('INSERT INTO create_menu (type_menu, order_num, btn_name, btn_callback) VALUES (?, ?, ?, ?)', ('payment', 2,  '🆕 Новая дата', 'new_date'))
# cursor.execute('INSERT INTO create_menu (type_menu, order_num, btn_name, btn_callback) VALUES (?, ?, ?, ?)', ('payment', 3,  '🔙 Назад','main'))



# # # Сохраняем изменения и закрываем соединени
# connection.commit()
# connection.close()


## cursor.execute('UPDATE create_menu SET age = ? WHERE username = ?', (29, 'newuser'))