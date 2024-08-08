import psycopg2
from psycopg2 import OperationalError
import config as cf
import time
def test_connection():
    # Cấu hình kết nối đến PostgreSQL
    # noinspection PyInterpreter,PyPackageRequirements
    conn_params = {
        'dbname': cf.POSTGRES_DB,
        'user':  cf.POSTGRES_USER,
        'password': cf.POSTGRES_PASSWORD,
        'host': cf.POSTGRES_HOST,  # Ví dụ: 'localhost'
        'port': '5432'   # Ví dụ: '5432'
    }
    try:
        # Tạo kết nối đến cơ sở dữ liệu
        conn = psycopg2.connect(**conn_params)
        print("Kết nối thành công!")
        conn.close()
    except OperationalError as e:
        print(f"Lỗi kết nối: {e}")

if __name__ == "__main__":
    test_connection()