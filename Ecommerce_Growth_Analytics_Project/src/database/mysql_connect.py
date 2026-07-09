import pymysql
from src.config import DB_CONFIG

# 创建连接（和截图逻辑一致）
def create_conn():
    conn = pymysql.connect(**DB_CONFIG)
    return conn

# 通用读取SQL转DataFrame函数
def read_sql_data(sql):
    import pandas as pd
    conn = create_conn()
    df = pd.read_sql(sql, conn)
    conn.close()
    return df

# 测试连接
def test_connection():
    try:
        conn = create_conn()
        print("MySQL连接成功")
        conn.close()
        return True
    except Exception as e:
        print("MySQL连接失败")
        print(e)
        return False

if __name__ == "__main__":
    test_connection()