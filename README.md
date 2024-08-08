## Crawl dữ liệu chứng khoán từ nền tảng Worldquant Brain
- Lưu trữ dữ liệu chứng khoán theo bộ dữ liệu và thị trường vào database để phân tích dữ liệu chứng khoán
- Database: Postgresql
- Programing Language: Python
- Deploy: Docker

### Các bước chạy Project
#### Tải project:
- `git clone https://github.com/quannm290898/WQB-Crawl-Data.git`
- `cd WQB-Crawl-Data`

#### Cài đặt môi trường
- python3 -m pip install --user virtualenv 
- python3 -m venv envs
- source envs/bin/activate
- sudo pip install --upgrade -r requirements.txt 

#### Set up .env
- Các tham số `region`, `universer`, `delay`.
- Tham số đường dẫn `path_token` để có thể truy cập được trang web Worldquant.
- Các tham số của PostgreSQl
- Các bộ dữ liệu được lựa chọn: dataset = ['analyst69', 'analyst11', 'analyst15', 'analyst39'] chỉnh sửa trong file config.py
- Lưu ý: database postgres được cài đặt thông qua file docker-compose.yml, nếu đã có database chỉnh sửa trong file docker-compose.yml

#### Chạy souce code
- Sử dụng venv: `python3 get_dataset_wq.py`
- Chạy bằng docker: `docker-compose up --build`

### Cấu trúc project
``` commandline
.
├── configs  
│   ├── token.txt   // đường dẫn đến token WQB 
├── datasets       // đường dẫn lưu trữ các dataset    
├── .gitignore  
├── .dockerignore  
├── docker-compose.yaml  
├── Dockerfile  
├── .env            // các tham số của project  
├── utils  
│   ├─ create_table.py // tạo bảng lưu trữ dữ liệu nếu chưa tồn tại
├── config.py 
├── get_dataset_wq.py  // file chính để crawl và lưu trữ dữ liệu 
├── README.md  
└── requirements.txt
```
