# 🐧 The Dark Age of Penguin / Penguin Path

**The Dark Age of Penguin** là một game phiêu lưu chạy đường băng 2D được xây dựng bằng **Python + Pygame**. Người chơi điều khiển nhân vật chim cánh cụt **Piko** vượt qua các màn chơi băng giá, né vật cản, thu thập xu, sử dụng khiên, bắn đạn tuyết, mua vật phẩm trong shop và đối đầu với boss gấu Bắc Cực ở màn 3.

Game có hỗ trợ điều khiển bằng **bàn phím** và **nhận diện tay qua camera** bằng OpenCV/MediaPipe.

---

## 🎮 Tính năng chính

### 1. Gameplay runner 3 làn
- Piko chạy trên đường băng gồm 3 làn.
- Người chơi di chuyển trái/phải để né vật cản.
- Vật cản xuất hiện theo phối cảnh xa gần.
- Bão tuyết/lốc tuyết là vật cản lớn có thể chiếm cả 3 làn.

### 2. Hệ thống máu
- Piko có 5 máu.
- Máu được hiển thị bằng biểu tượng bông tuyết.
- Máu không tự hồi khi sang màn mới.
- Nếu mất máu ở màn 1, sang màn 2 vẫn giữ lượng máu còn lại.
- Có thể hồi máu trong shop.

### 3. Hệ thống năng lượng
- Piko có tối đa 50 năng lượng.
- Bắn đạn tuyết tốn 1 năng lượng.
- Bật khiên tốn 5 năng lượng.
- Có thể mua thêm năng lượng trong shop.

### 4. Khiên bảo vệ
- Khiên giúp đỡ một lần sát thương.
- Khi va vào vật cản, khiên sẽ vỡ và biến mất.
- Khiên có cooldown riêng.
- Hiệu ứng khiên tách riêng khỏi nhân vật Piko.

### 5. Bắn đạn tuyết
- Từ màn 2 trở đi, Piko có thể bắn đạn.
- Đạn có thể phá vật cản.
- Một số vật cản có nhiều trạng thái hư hỏng.
- Khi bị bắn đủ số lần, vật cản có thể vỡ để Piko đi qua.

### 6. Hệ thống xu
- Xu xuất hiện theo từng cụm trên đường chạy.
- Mỗi cụm có nhiều xu thẳng hàng.
- Nhặt xu để mua vật phẩm trong shop.
- Có âm thanh khi nhặt xu.

### 7. Shop giữa các màn
Shop xuất hiện sau khi hoàn thành màn chơi.

Vật phẩm trong shop:
- **Hồi máu +1 HP**: hồi trực tiếp trong shop.
- **Năng lượng +10**: dùng trong trận.
- **Thuốc làm chậm**: giảm tốc độ game trong 10 giây.
- **Bom**: phá vật cản đang nhìn thấy và làm choáng boss.

### 8. Boss màn 3
Màn 3 có boss gấu Bắc Cực:
- Boss xuất hiện sau một khoảng thời gian.
- Boss nhảy vào từ bên trái.
- Boss đuổi theo Piko từ phía sau.
- Boss có thể ném băng đá/cây.
- Vật boss ném bay từ tay boss ra đường rồi trôi về phía Piko.
- Boss có kỹ năng nhảy đánh nhiều làn.
- Bom có thể làm choáng boss.

### 9. Cutscene mở đầu
Game có phần cắt cảnh mở đầu:
- Hiển thị nhiều cảnh bằng ảnh.
- Có hộp thoại tiếng Việt.
- Có âm thanh intro.
- Có thể nhấn SPACE / ENTER / ESC để bỏ qua.

### 10. Điều khiển bằng camera
Game hỗ trợ nhận diện tay:
- Di chuyển trái/phải/giữa bằng vị trí tay.
- Ký hiệu súng để bắn.
- Nắm tay để bật khiên.
- Một số gesture có thể dùng vật phẩm.

---

## 🕹️ Điều khiển

### Bàn phím

| Phím | Chức năng |
|---|---|
| `A` hoặc `←` | Sang trái |
| `D` hoặc `→` | Sang phải |
| `SPACE` | Bật khiên |
| `F` | Bắn đạn tuyết |
| `E` | Dùng vật phẩm năng lượng |
| `N` | Tiếp tục / vào shop / sang màn |
| `R` | Chơi lại |
| `ESC` | Về menu hoặc thoát |

### Camera / Hand Tracking

| Gesture | Chức năng |
|---|---|
| Tay sang trái | Di chuyển sang làn trái |
| Tay ở giữa | Di chuyển làn giữa |
| Tay sang phải | Di chuyển sang làn phải |
| Ký hiệu súng | Bắn đạn tuyết |
| Nắm tay | Bật khiên |
| Một số gesture đặc biệt | Dùng vật phẩm |

---

## 📁 Cấu trúc thư mục

```txt
penguin-path/
│
├── main.py
├── settings.py
├── player.py
├── obstacle.py
├── enemy.py
├── projectile.py
├── coin.py
├── boss.py
├── finish_line.py
├── track_effects.py
├── effects.py
├── sound_manager.py
├── camera_preview.py
├── hand_tracking.py
├── intro_cutscene.py
├── start_screen.py
├── ui.py
│
├── assets/
│   ├── characters/
│   ├── obstacles/
│   ├── boss/
│   ├── decor/
│   ├── effects/
│   ├── backgrounds/
│   ├── sounds/
│   ├── ui/
│   └── cutscene/
│
├── requirements.txt
├── README.md
└── .gitignore

🖼️ Tài nguyên hình ảnh

Game sử dụng nhiều loại ảnh trong thư mục assets/.

Nhân vật
assets/characters/

Ví dụ:

Piko idle
Piko chạy
Piko ăn mừng
Piko dùng khiên
Vật cản
assets/obstacles/

Ví dụ:

Khối băng bình thường
Khối băng hư hỏng cấp 1
Khối băng hư hỏng cấp 2
Khối băng vỡ
Bão tuyết / lốc tuyết animation nhiều frame
Boss
assets/boss/

Ví dụ:

Boss intro frame
Boss chạy đuổi
Boss ném
Boss nhảy đánh
Vật boss ném
Trang trí đường chạy
assets/decor/

Ví dụ:

Cây
Đá
Băng nhọn
UI
assets/ui/

Ví dụ:

Icon máu
Icon xu
Icon khiên
Icon năng lượng
Icon thuốc làm chậm
Icon bom
Panel thắng/thua/shop
Cutscene
assets/cutscene/

Ví dụ:

intro_1.png
intro_2.png
intro_3.png
intro_4.png
🔊 Âm thanh

Thư mục âm thanh:

assets/sounds/

Các âm thanh gợi ý:

hit.wav: khi Piko bị va chạm.
shield_break.wav: khi khiên vỡ.
shoot.wav: khi bắn.
coin.wav: khi nhặt xu.
win.wav: khi hoàn thành màn.
lose.wav: khi thua.
boss_roar.wav: khi boss xuất hiện.
bomb.wav: khi kích hoạt bom.
not_enough_coin.wav: khi không đủ xu trong shop.
intro.wav: âm thanh mở đầu.
⚙️ Cài đặt môi trường
1. Clone project
git clone https://github.com/USERNAME/penguin-path.git
cd penguin-path
2. Tạo môi trường ảo

Trên Windows:

python -m venv .venv
.venv\Scripts\activate

Trên macOS/Linux:

python3 -m venv .venv
source .venv/bin/activate
3. Cài thư viện
pip install -r requirements.txt
4. Chạy game
python main.py
📦 Requirements
pygame==2.6.1
opencv-python
mediapipe
numpy
🧩 Công nghệ sử dụng
Python: ngôn ngữ chính.
Pygame: xây dựng game 2D.
OpenCV: đọc camera.
MediaPipe: nhận diện tay.
Pygame Mixer: phát nhạc và hiệu ứng âm thanh.
🎯 Mục tiêu gameplay

Người chơi cần giúp Piko vượt qua các vùng băng nguy hiểm bằng cách:

Né vật cản.
Thu thập xu.
Quản lý máu và năng lượng.
Mua vật phẩm trong shop.
Sử dụng khiên và súng hợp lý.
Đánh bại hoặc sống sót trước boss gấu Bắc Cực.
🧠 Một số cơ chế nổi bật
Máu không hồi giữa màn

Máu được lưu qua các màn chơi. Nếu màn 1 mất máu, màn 2 sẽ tiếp tục với lượng máu còn lại.

Năng lượng dùng chung

Súng và khiên dùng chung năng lượng:

Bắn: -1 năng lượng.
Khiên: -5 năng lượng.
Boss có projectile riêng

Vật boss ném không xuất hiện ngay như vật cản thường. Nó bay từ tay boss ra đường trước, sau đó mới trôi về phía Piko như một vật cản.

Bão tuyết lớn

Bão tuyết có thể là một vật thể lớn chiếm cả 3 làn và gây sát thương nếu Piko chạm vào.

🧪 Trạng thái phát triển

Game hiện đang trong giai đoạn prototype/mở rộng tính năng.

Các phần đã có:

Gameplay 3 làn.
Vật cản.
Coin.
Shop.
Boss.
Cutscene.
Âm thanh.
Camera hand tracking.
UI tiếng Việt.

Các phần có thể phát triển thêm:

Lưu điểm cao.
Nâng cấp kỹ năng.
Thêm nhiều boss.
Thêm nhiều loại màn chơi.
Tối ưu hiệu năng.
Đóng gói game thành file .exe.
🛠️ Lỗi thường gặp
1. Không mở được camera

Nếu terminal báo không mở được camera, game vẫn có thể chơi bằng bàn phím.

Kiểm tra:

Camera có đang bị app khác chiếm không.
Đúng camera index chưa.
OpenCV đã cài chưa.
2. Không tìm thấy ảnh

Nếu terminal báo:

Không tìm thấy ảnh...

Kiểm tra:

File ảnh có đúng tên không.
File có đúng thư mục assets/... không.
Đuôi file là .png, .jpg, .wav đúng chưa.
3. Không nghe thấy âm thanh

Kiểm tra:

File âm thanh có đúng thư mục assets/sounds/ không.
Tên file trong code có khớp không.
Âm lượng máy có bị tắt không.
4. Game bị đen màn hình

Kiểm tra:

pygame.display.flip() có nằm cuối vòng lặp không.
Phần draw có chạy đúng game_state không.
Intro/cutscene có bị return sớm không.
📌 Ghi chú

Đây là project game học tập và thử nghiệm, tập trung vào:

Pygame 2D.
Điều khiển bằng camera.
Logic game nhiều màn.
Boss battle.
Shop và item.
Quản lý asset hình ảnh/âm thanh.
👤 Tác giả

Project được phát triển bởi Duy Kiên.
