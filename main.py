import psycopg2
from psycopg2 import sql
import config as cf

def insert_db():
    # Kết nối đến cơ sở dữ liệu PostgreSQL
    conn = psycopg2.connect(
        dbname=cf.POSTGRES_DB,
        user=cf.POSTGRES_USER,
        password=cf.POSTGRES_PASSWORD,
        host=cf.POSTGRES_HOST,
        port="5432"
    )

    # Tạo một đối tượng cursor để thực hiện các thao tác SQL
    cursor = conn.cursor()

    # Dữ liệu mẫu
    students_data = [
        ('11','John', 'Doe', '2000-01-01'),
        ('12','Jane', 'Smith', '1999-02-15'),
        ('13','Emily', 'Jones', '2001-05-22'),
        ('14','Michael', 'Brown', '1998-09-30'),
        ('15','Sarah', 'Davis', '2002-12-10')
    ]

    # Chèn dữ liệu mẫu vào bảng Students
    insert_query = '''
    INSERT INTO Students (studentid, FirstName, LastName, BirthDate)
    VALUES (%s, %s, %s, %s)
    '''

    for student in students_data:
        cursor.execute(insert_query, student)

    # Lưu các thay đổi
    conn.commit()

    # Truy vấn dữ liệu để kiểm tra
    cursor.execute('SELECT * FROM Students')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    # Đóng kết nối
    cursor.close()
    conn.close()

if __name__ == '__main__':
    insert_db()
