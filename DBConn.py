import pymysql


def get_db():
    return pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
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
        cursor = get_cursor(connection)
        if val == "":
            cursor.execute(sql)
        else:
            cursor.execute(sql, val)
        record = cursor.fetchall()
        cursor.close()
        # connection.close()
        print("目前資料：", record)
        if len(record) > 0:
            msg = {"result": record}
        else:
            msg = {"result": "No Data"}
    except pymysql.Error as error:
        msg = ""
        cursor.close()
        connection.close()
        print(error)

    return msg


def getTasks():
    sql = "SELECT * from task"

    return query_sql(sql, "")


def insertTaskCmd(name):
    sql = "INSERT INTO task (name) VALUES (%s)"
    val = [(name)]
    return insert_sql(sql, val)


def updateTaskCmd(id, name, status):
    sql = "Update task Set name=%s,status=%s where id=%s"
    val = (name, status, id)
    return update_sql(sql, val)


def deleteTaskCmd(id):
    sql = "Delete From task where id=%s"
    val = [(id)]
    return update_sql(sql, val)


def insert_sql(sql, val):
    """insert sql function."""
    try:
        connection = get_db()
        cursor = get_cursor(connection)
        cursor.execute(sql, val)
        connection.commit()

        print(cursor.lastrowid, ": record inserted.")

        # SQL query to retrieve the inserted data
        select_sql = "SELECT * FROM task WHERE id = LAST_INSERT_ID()"
        # Execute the SELECT query
        cursor.execute(select_sql)
        record = cursor.fetchone()
        cursor.close()
        # connection.close()
        # print("目前資料：", record)
        msg = {"result": record}

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
        cursor = get_cursor(connection)
        cursor.execute(sql, val)
        connection.commit()
        print(cursor.rowcount, ": record updated.")
        select_query = "SELECT * FROM task WHERE id = %s"
        print(val[0])
        select_values = (val[2],)
        cursor.execute(select_query, select_values)
        record = cursor.fetchone()

        cursor.close()
        # connection.close()
        print("目前資料：", record)
        msg = {"result": record}

    except pymysql.Error as error:
        msg = ""
        cursor.close()
        connection.close()
        print(error)
    return msg
