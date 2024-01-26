import pymysql


def get_db():
    """db connection information"""
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


def task_list():
    """Get task list"""
    sql = "SELECT * from task"
    msg = query_sql(sql, "")
    return msg


def insert_task_cmd(name):
    """Insert a task"""
    sql = "INSERT INTO task (name) VALUES (%s)"
    val = [(name)]
    return insert_sql(sql, val)


def update_task_cmd(task_id, name, status):
    """Update a task"""
    try:
        sql = "Update task Set name=%s,status=%s where id=%s"
        val = (name, status, task_id)
        msg = update_sql(sql, val)
    except pymysql.Error as error:
        msg = {"result": error}
    return msg


def delete_task_cmd(task_id):
    """Delete a task"""
    try:
        sql = "Delete From task where id=%s"
        val = [(task_id)]
        msg = delete_sql(sql, val)

    except pymysql.Error as error:
        msg = {"result": error}
    return msg


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
        if cursor.rowcount == 0:
            msg = {"result": "Record is not exist!"}
        else:
            msg = {"result": record}

    except pymysql.Error as error:
        msg = ""
        cursor.close()
        connection.close()
        print(error)
    return msg


def delete_sql(sql, val):
    """delete sql function."""
    try:
        connection = get_db()
        cursor = get_cursor(connection)
        cursor.execute(sql, val)
        connection.commit()
        # Check if any records were deleted
        if cursor.rowcount == 0:
            msg = {"result": "Record is not exist!"}
        else:
            msg = {"result": f"{cursor.rowcount} record(s) deleted."}

    except pymysql.Error as error:
        msg = {"result": f"Error: {error}"}

    finally:
        cursor.close()
        connection.close()

    return msg
