"""db connection"""

import pymysql
import os


def get_db():
    """db connection information"""
    return pymysql.connect(
        host="localhost",
        port=3306,
        user=os.environ.get("User_KEY"),
        password=os.environ.get("Password_KEY"),
        database="task",
        connect_timeout=31536000,
        cursorclass=pymysql.cursors.DictCursor,
    )


def get_cursor(connection):
    """get db cursor."""
    try:
        print("connection==")
        connection.ping(True)
        # db_info = connection.get_host_info()
        # print("DB Version:" + db_info)

    except pymysql.OperationalError as error:
        connection.ping(True)
        # connection.reconnect()
        print("connection Error" + error)
    finally:
        if connection.cursor() is not None:
            cursor = connection.cursor()

    return cursor


def query_sql(sql, val):
    """query sql function."""
    try:
        with get_db() as connection:
            with get_cursor(connection) as cursor:
                if val == "":
                    cursor.execute(sql)
                else:
                    cursor.execute(sql, val)
                record = cursor.fetchall()
                cursor.close()
                # connection.close()
                # print("目前資料：", record)
                if len(record) > 0:
                    msg = {"result": record}
                else:
                    msg = {"result": "No Data"}
    except pymysql.Error as error:
        msg = {"result": error}
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
        with get_db() as connection:
            with get_cursor(connection) as cursor:
                cursor.execute(sql, val)
                connection.commit()
                print(cursor.lastrowid, ": record inserted.")

                # SQL query to retrieve the inserted data
                select_sql = "SELECT * FROM task WHERE id = LAST_INSERT_ID()"
                # Execute the SELECT query
                cursor.execute(select_sql)
                record = cursor.fetchone()
                msg = {"result": record}

    except pymysql.Error as error:
        msg = {"result": f"Error: {error}"}
    return msg


def update_sql(sql, val):
    """update sql function."""
    try:
        with get_db() as connection:
            with get_cursor(connection) as cursor:
                cursor.execute(sql, val)
                connection.commit()
                print(cursor.rowcount, ": record updated.")
                select_query = "SELECT * FROM task WHERE id = %s"
                print(val[0])
                select_values = (val[2],)  # Get task id
                cursor.execute(select_query, select_values)
                record = cursor.fetchone()

                if cursor.rowcount == 0:
                    msg = {"result": "Record is not exist!"}
                else:
                    msg = {"result": record}

    except pymysql.Error as error:
        msg = {"result": f"Error: {error}"}
    return msg


def delete_sql(sql, val):
    """delete sql function."""
    try:
        with get_db() as connection:
            with get_cursor(connection) as cursor:
                cursor.execute(sql, val)
                connection.commit()
                # Check if any records were deleted
                if cursor.rowcount == 0:
                    msg = {"result": "Record is not exist!"}
                else:
                    msg = {"result": f"{cursor.rowcount} record(s) deleted."}

    except pymysql.Error as error:
        msg = {"result": f"Error: {error}"}

    return msg
