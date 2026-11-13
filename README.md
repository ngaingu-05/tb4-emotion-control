# Điều khiển TurtleBot 4 bằng biểu cảm khuôn mặt

Node webcam dùng OpenCV + FER 22.5.1 để nhận diện sáu lớp `happy`, `sad`, `neutral`,
`angry`, `surprise`, `fear`, hiển thị nhãn/confidence và phát lệnh vận tốc ROS 2.
Mỗi biểu cảm phải xuất hiện ổn định qua hai lần nhận diện mới kích hoạt. Hành vi
chạy có thời hạn; nhận diện neutral, không thấy mặt, lỗi camera hoặc lỗi mô hình
đều dừng và xóa hành vi đang chạy.

| Biểu cảm | Hành động | Thời lượng / vận tốc đặt |
| --- | --- | --- |
| Happy | Cung cong trái | 4 s, v=0.10 m/s, ω=0.30 rad/s |
| Sad | Cung cong phải | 4 s, v=0.10 m/s, ω=-0.30 rad/s |
| Neutral | Dừng | 0 m/s |
| Angry | Lùi nhẹ | 1.5 s, v=-0.08 m/s |
| Surprise | Quay tại chỗ một vòng | 2π/0.50 s, ω=0.50 rad/s |
| Fear | Tiến nhẹ | 1.5 s, v=0.08 m/s |

## Lấy package và build mô phỏng

Đặt repo trong thư mục `src` của workspace ROS 2 Jazzy:

```bash
cd ~/turtlebot4
git clone https://github.com/ngaingu-05/tb4-emotion-control.git src/tb4_emotion_control
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install --packages-select tb4_emotion_control
source install/setup.bash
```

Không cần cài TensorFlow để chạy mô phỏng với biểu cảm giả. Để nhận diện webcam
thật, cài stack CPU tùy chọn trong virtualenv:

```bash
cd ~/turtlebot4
python3 -m venv --system-site-packages .venv-emotion
.venv-emotion/bin/python -m pip install -r src/tb4_emotion_control/requirements-ai.txt
.venv-emotion/bin/python -m pip install --no-deps fer==22.5.1
```

## Chạy

Đảm bảo robot đã bật, dùng đúng camera, và không có Nav2/teleop hay node khác
đang phát `/cmd_vel`.

```bash
cd ~/turtlebot4
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch tb4_emotion_control emotion.launch.py
```

Chọn camera khác bằng `camera:=1`. Nếu thiết bị đích nhận `geometry_msgs/Twist`
thay vì Jazzy `geometry_msgs/TwistStamped`, đặt `stamped:=false`. Có thể chỉnh
ngưỡng confidence, tần suất nhận diện và tắt cửa sổ bằng tham số ROS:

```bash
ros2 launch tb4_emotion_control emotion.launch.py camera:=1 confidence:=0.55 inference_period:=0.5 show_window:=false
```

Nhấn `q` trong cửa sổ webcam hoặc `Ctrl-C` để dừng. Các hành vi là lệnh vận tốc
vòng hở, nên quãng đường và góc quay thực tế thay đổi theo pin, mặt sàn và tải.
Thử ở vùng trống, tốc độ thấp; camera cần thấy rõ một khuôn mặt. Chương trình
chỉ phát zero khi nhận diện neutral/mất mặt/lỗi hoặc kết thúc node; cần bảo đảm
robot có timeout vận tốc downstream nếu tiến trình bị kill đột ngột.

## Chạy mô phỏng Gazebo + RViz

Mô phỏng dùng Gazebo Harmonic, TurtleBot 4 standard, RViz và đồng hồ mô phỏng.
Để khởi chạy cả mô phỏng, demo đợi đến khi action undock hoàn tất rồi mới chạy
biểu cảm Happy giả. Lệnh này không cần cài mô hình FER:

```bash
cd ~/turtlebot4
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch tb4_emotion_control demo.launch.py mock_emotion:=happy python:=/usr/bin/python3
```

Chờ Gazebo/RViz hiện robot và node báo đã sẵn sàng. Demo chọn camera 0; có thể
đổi bằng `camera:=1`. Muốn nhận diện thật, bỏ `mock_emotion:=happy` sau khi cài
stack `requirements-ai.txt`; launch sẽ dùng `.venv-emotion/bin/python` mặc định.
Có thể chỉ khởi động simulator bằng
`ros2 launch tb4_emotion_control simulation.launch.py`; simulator để robot trên
dock, nên gửi `ros2 action send_goal /undock irobot_create_msgs/action/Undock '{}'`
trước khi chạy node điều khiển riêng.
