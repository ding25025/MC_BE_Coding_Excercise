import threading
import pymysql


def get_db():
    return pymysql.connect(
        host="localhost",
        port=3306,
        user="user",
        password="test",
        database="task",
        connect_timeout=31536000,
        cursorclass=pymysql.cursors.DictCursor,
    )


def get_cursor(connection):
    """get db cursor."""
    try:
        print("connection==")
        # connection = get_db()
        connection.ping(True)
        db_Info = connection.get_host_info()

        print("DB Version:" + db_Info)

    except pymysql.OperationalError as error:
        connection.ping(True)
        # connection.reconnect()
        print("connection Error" + error)
    finally:
        cursor = connection.cursor()
    return cursor


def query_sql(sql, val):
    """query sql function."""
    try:
        connection = get_db()
        lock = threading.Lock()
        cursor = get_cursor(connection)
        if val == "":
            lock.acquire()
            cursor.execute(sql)
            lock.release()
        else:
            lock.acquire()
            cursor.execute(sql, val)
            lock.release()
        record = cursor.fetchall()
        cursor.close()
        # connection.close()
        print("目前資料：", record)
        if len(record) > 0:
            msg = record
        else:
            msg = record

    except pymysql.Error as error:
        msg = ""
        cursor.close()
        connection.close()
        print(error)

    return msg


def insert_sql(sql, val):
    """insert sql function."""
    try:
        connection = get_db()
        lock = threading.Lock()
        cursor = get_cursor(connection)
        lock.acquire()
        cursor.execute(sql, val)
        connection.commit()
        lock.release()
        print(cursor.lastrowid, ": record inserted.")
        record = cursor.lastrowid
        cursor.close()
        # connection.close()
        # print("目前資料：", record)
        msg = record

    except pymysql.Error as error:
        msg = ""
        cursor.close()
        connection.close()
        print(error)
    return msg


def update_sql(sql, val):
    """update sql function."""
    try:
        connection = get_db()
        lock = threading.Lock()
        cursor = get_cursor(connection)
        lock.acquire()
        cursor.execute(sql, val)
        connection.commit()
        lock.release()
        print(cursor.rowcount, ": record updated.")
        record = cursor.rowcount
        cursor.close()
        # connection.close()
        # print("目前資料：", record)
        msg = record

    except pymysql.Error as error:
        msg = ""
        cursor.close()
        connection.close()
        print(error)
    return msg
