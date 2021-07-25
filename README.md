1. Clone this project
2. Start a virtual machine of python
```shell
python -m venv env
```
3. install dependencies
```shell
pip install -r .\requirement.txt
```
4. Runserver
```shell
python manage.py runserver [ip:port]
```

5. Data info
EDUCA			Householders' highest level of education	0-6
0: Không
1: Tiểu học
2: Trung học cơ sở
3: Trung học phổ thông
4: Đại học
5: Cao học
WK_STAT			Work status					1-5
1: Công nhân
2: Nhân viên văn phòng
3: Nông nghiệp
4: Kinh doanh
5: Không
NUM_MEM			Number of member				0-20
RES_TYPE		Description of residence			0-19
0-9: Nông thôn
10-19: Thành thị
Đánh giá tăng dần theo mức độ đông đúc của dân cư
INCOME			Household income				1-6
1: Trợ cấp
2: Dưới 5 triệu
2: 5-10
3: 10-20
4: 20-50
5: 50-500
6: 500tr+
Label			Daily electricity usage	per device		0-24
Số giờ trung bình sử dụng trong ngày trên mỗi thiết bị