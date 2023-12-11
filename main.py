import sqlite3
import hashlib
import time


def calculate_hash(data, previous_hash):
    sha256 = hashlib.sha256()
    sha256.update((str(data) + str(previous_hash)).encode('utf-8'))
    return sha256.hexdigest()


def add_block(data, cursor):
    cursor.execute("SELECT hash FROM blockchain ORDER BY timestamp DESC LIMIT 1")
    previous_hash = cursor.fetchone()

    if previous_hash:
        previous_hash = previous_hash[0]
    else:
        previous_hash = '0'

    timestamp = time.time()
    hash_value = calculate_hash(data, previous_hash)

    cursor.execute("INSERT INTO blockchain (data, timestamp, hash) VALUES (?, ?, ?)",
                   (data, timestamp, hash_value))
    conn.commit()


def update_block_data(block_id, new_data, cursor):
    # Получаем существующие данные блока
    cursor.execute("SELECT hash FROM blockchain WHERE id = ?", (block_id,))
    existing_hash = cursor.fetchone()

    if existing_hash:
        # Обновляем данные блока
        cursor.execute(
            "UPDATE blockchain SET data = ? WHERE id = ?", (new_data, block_id))

        # Пересчитываем хеш блока
        updated_hash = calculate_hash(new_data, existing_hash[0])
        cursor.execute(
            "UPDATE blockchain SET hash = ? WHERE id = ?", (updated_hash, block_id))
        conn.commit()


# Подключение к базе данных
conn = sqlite3.connect('blockchain.db')
cursor = conn.cursor()

# Добавление новых блоков в базу данных
add_block('Transaction 1', cursor)
add_block('Transaction 2', cursor)

checkpoint_hashes = []
cursor.execute("SELECT hash FROM blockchain ORDER BY timestamp ASC")
for block in cursor.fetchall():
    checkpoint_hashes.append(block[0])

# Обновление данных в первом блоке
block_id_to_update = 1
new_data_for_block = 'Updated Transaction 1'
update_block_data(block_id_to_update, new_data_for_block, cursor)

is_integrity_ok = True
cursor.execute("SELECT hash FROM blockchain ORDER BY timestamp ASC")
for i, block in enumerate(cursor.fetchall()):
    if block[0] != checkpoint_hashes[i]:
        is_integrity_ok = False
        break

if is_integrity_ok:
    print("\nЦелостность данных подтверждена.")
else:
    print("\nЦелостность данных нарушена.")

# Закрытие соединения с базой данных
conn.close()

