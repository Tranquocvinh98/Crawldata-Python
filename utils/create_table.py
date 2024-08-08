import psycopg2
from psycopg2 import sql
import config as cf

def create_table_data(table_name="data"):
    # Kết nối đến cơ sở dữ liệu PostgreSQL
    conn = psycopg2.connect(
        dbname=cf.POSTGRES_DB,
        user=cf.POSTGRES_USER,
        password=cf.POSTGRES_PASSWORD,
        host=cf.POSTGRES_HOST,
        port="5432"
    )
    cursor = conn.cursor()
    # Câu lệnh SQL kiểm tra bảng có tồn tại hay không
    check_table_exists_query = sql.SQL("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = {table}
        )
    """).format(table=sql.Literal(table_name))
    # Thực hiện câu lệnh kiểm tra
    cursor.execute(check_table_exists_query)
    table_exists = cursor.fetchone()[0]
    # Nếu bảng không tồn tại, tạo bảng mới
    if not table_exists:
        create_table_query = f"""
            CREATE TABLE {table_name} (
                id SERIAL,
                dataField VARCHAR(500),
                dataset VARCHAR(100),
                type VARCHAR(50),
                coverage FLOAT,
                userCount INT,
                alphaCount INT,
                region VARCHAR(50),
                delay INT,
                universe VARCHAR(50),
                update_time TIMESTAMP default current_timestamp,
                PRIMARY KEY (id, dataField)
            )
        """
        cursor.execute(create_table_query)
        conn.commit()
        print(f"Bảng {table_name} đã được tạo.")
    else:
        print(f"Bảng {table_name} đã tồn tại.")
    # Đóng kết nối
    cursor.close()
    conn.close()
