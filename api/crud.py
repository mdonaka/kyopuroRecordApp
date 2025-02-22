from fastapi import FastAPI
import mysql.connector

app = FastAPI()

db_config = {
    'user': 'admin',
    'password': '*19991123Oy',
    'host': 'database-1.cy0pswpd42h6.ap-northeast-1.rds.amazonaws.com',
    'database': 'my_schema'
}

@app.on_event("startup")
async def startup_db_client():
    # MySQLクライアントを初期化
    app.db_connection = mysql.connector.connect(**db_config)
    app.db_cursor = app.db_connection.cursor()

@app.on_event("shutdown")
async def shutdown_db_client():
    # アプリケーションの終了時にMySQLクライアントをクローズ
    app.db_cursor.close()
    app.db_connection.close()

@app.get("/getUserInfo/{userName}")
async def getUserInfo(userName:str):
    try:
        # テーブルのデータを取得
        query = "SELECT * FROM user_info where user_name = %s"
        app.db_cursor.execute(query,(userName,))
        data = app.db_cursor.fetchall()
        return {"data": data}
    except Exception as e:
        return {"error": str(e)}


@app.get("/getUserInfo/")
async def getAllUserInfo():
    try:
        # テーブルのデータを取得
        query = "SELECT * FROM user_info"
        app.db_cursor.execute(query)
        data = app.db_cursor.fetchall()
        return {"data": data}
    except Exception as e:
        return {"error": str(e)}
    