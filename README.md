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
```
## 🖼️ Tài nguyên hình ảnh

Game sử dụng nhiều tài nguyên hình ảnh trong thư mục `assets/`. Các tài nguyên được chia theo từng nhóm để dễ quản lý và chỉnh sửa.

### Nhân vật

Thư mục:

```txt
assets/characters/
```

Bao gồm các hình ảnh liên quan đến nhân vật chính Piko:

* Piko đứng yên
* Piko chạy
* Piko ăn mừng
* Piko dùng khiên
* Các frame animation của Piko

### Vật cản

Thư mục:

```txt
assets/obstacles/
```

Bao gồm các loại vật cản trong game:

* Khối băng bình thường
* Khối băng hư hỏng cấp 1
* Khối băng hư hỏng cấp 2
* Khối băng vỡ
* Bão tuyết / lốc tuyết dạng animation nhiều frame

Một số vật cản có thể bị bắn hỏng theo nhiều cấp độ. Khi bị phá đủ số lần, Piko có thể đi xuyên qua.

### Boss

Thư mục:

```txt
assets/boss/
```

Bao gồm hình ảnh của boss gấu Bắc Cực:

* Boss xuất hiện
* Boss chạy đuổi
* Boss ném vật thể
* Boss nhảy đánh
* Vật thể boss ném như băng đá hoặc cây

Boss ở màn 3 có nhiều trạng thái hành động khác nhau, giúp trận đấu cuối có cảm giác sinh động hơn.

### Trang trí đường chạy

Thư mục:

```txt
assets/decor/
```

Bao gồm các vật trang trí hai bên đường chạy:

* Cây
* Đá
* Băng nhọn

Các vật trang trí này không gây sát thương, chủ yếu tạo chiều sâu và làm môi trường game đẹp hơn.

### Giao diện người dùng

Thư mục:

```txt
assets/ui/
```

Bao gồm các icon và panel giao diện:

* Icon máu
* Icon xu
* Icon khiên
* Icon năng lượng
* Icon thuốc làm chậm
* Icon bom
* Panel thắng
* Panel thua
* Panel hoàn thành màn
* Hình ảnh dùng trong shop

### Cắt cảnh mở đầu

Thư mục:

```txt
assets/cutscene/
```

Bao gồm các ảnh dùng cho phần intro/cutscene mở đầu:

```txt
intro_1.png
intro_2.png
intro_3.png
intro_4.png
```

Các ảnh này được dùng để kể câu chuyện mở đầu trước khi người chơi vào menu chính.

---

## 🔊 Âm thanh

Thư mục âm thanh:

```txt
assets/sounds/
```

Các âm thanh chính trong game:

* `hit.wav`: phát khi Piko bị va chạm.
* `shield_break.wav`: phát khi khiên bị vỡ.
* `shoot.wav`: phát khi Piko bắn đạn tuyết.
* `coin.wav`: phát khi nhặt xu.
* `win.wav`: phát khi hoàn thành màn.
* `lose.wav`: phát khi thua.
* `boss_roar.wav`: phát khi boss gấu Bắc Cực xuất hiện.
* `bomb.wav`: phát khi kích hoạt bom.
* `not_enough_coin.wav`: phát khi không đủ xu để mua vật phẩm trong shop.
* `intro.wav`: âm thanh mở đầu/cắt cảnh.

Âm thanh giúp tăng cảm giác phản hồi cho người chơi, đặc biệt ở các hành động như va chạm, nhặt xu, bắn đạn và boss xuất hiện.

---

## ⚙️ Cài đặt môi trường

### 1. Clone project

```bash
git clone https://github.com/USERNAME/penguin-path.git
cd penguin-path
```

Thay `USERNAME` bằng tên tài khoản GitHub của bạn.

### 2. Tạo môi trường ảo

Trên Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Trên macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Cài thư viện

```bash
pip install -r requirements.txt
```

### 4. Chạy game

```bash
python main.py
```

---

## 📦 Requirements

Các thư viện chính cần dùng:

```txt
pygame==2.6.1
opencv-python
mediapipe
numpy
```

Trong đó:

* `pygame`: dùng để xây dựng game 2D.
* `opencv-python`: dùng để đọc camera.
* `mediapipe`: dùng để nhận diện tay.
* `numpy`: hỗ trợ xử lý dữ liệu hình ảnh và tính toán.

---

## 🧩 Công nghệ sử dụng

* **Python**: ngôn ngữ lập trình chính.
* **Pygame**: xây dựng gameplay, nhân vật, vật cản, UI và âm thanh.
* **OpenCV**: xử lý camera.
* **MediaPipe**: nhận diện bàn tay và gesture.
* **Pygame Mixer**: phát nhạc nền và hiệu ứng âm thanh.

---

## 🎯 Mục tiêu gameplay

Người chơi cần giúp Piko vượt qua các vùng băng nguy hiểm bằng cách:

1. Né vật cản.
2. Thu thập xu.
3. Quản lý máu và năng lượng.
4. Mua vật phẩm trong shop.
5. Sử dụng khiên và súng hợp lý.
6. Vượt qua boss gấu Bắc Cực ở màn cuối.

Game yêu cầu người chơi vừa phản xạ nhanh, vừa biết quản lý tài nguyên như máu, xu, năng lượng và vật phẩm.

---

## 🧠 Một số cơ chế nổi bật

### Máu không hồi giữa màn

Piko có lượng máu cố định. Máu không tự hồi khi sang màn mới.

Ví dụ: nếu màn 1 Piko còn 3 máu, khi sang màn 2 Piko vẫn chỉ có 3 máu. Người chơi cần mua hồi máu trong shop nếu muốn hồi lại.

### Năng lượng dùng chung

Súng và khiên dùng chung một thanh năng lượng.

* Bắn đạn tuyết: tốn 1 năng lượng.
* Bật khiên: tốn 5 năng lượng.

Cơ chế này buộc người chơi phải cân nhắc giữa tấn công và phòng thủ.

### Boss có vật thể ném riêng

Vật thể boss ném không xuất hiện ngay như vật cản thường. Nó bay từ tay boss ra đường trước, sau đó mới trôi về phía Piko như một vật cản.

Điều này giúp hành động ném của boss rõ ràng hơn và tạo cảm giác boss thật sự đang tấn công người chơi.

### Bão tuyết lớn

Bão tuyết có thể là một vật thể lớn chiếm cả 3 làn. Khi bão tuyết đi tới vị trí của Piko, người chơi có thể bị sát thương dù đang đứng ở bất kỳ làn nào.

### Shop giữa các màn

Sau khi hoàn thành màn chơi, người chơi có thể vào shop để mua vật phẩm bằng xu đã thu thập được.

Các vật phẩm gồm:

* Hồi máu
* Năng lượng
* Thuốc làm chậm
* Bom

Shop giúp người chơi chuẩn bị tốt hơn trước khi bước vào màn tiếp theo.

---

## 🧪 Trạng thái phát triển

Game hiện đang trong giai đoạn prototype/mở rộng tính năng.

Các phần đã có:

* Gameplay 3 làn.
* Vật cản.
* Coin.
* Shop.
* Boss.
* Cutscene mở đầu.
* Âm thanh.
* Camera hand tracking.
* UI tiếng Việt.
* Hệ thống máu.
* Hệ thống năng lượng.
* Vật phẩm hỗ trợ.

Các phần có thể phát triển thêm:

* Lưu điểm cao.
* Thêm nhiều màn chơi.
* Thêm nhiều boss.
* Thêm nâng cấp kỹ năng.
* Thêm hiệu ứng chuyển cảnh.
* Tối ưu hiệu năng.
* Đóng gói game thành file `.exe`.

---

## 🛠️ Lỗi thường gặp

### 1. Không mở được camera

Nếu terminal báo không mở được camera, game vẫn có thể chơi bằng bàn phím.

Cách kiểm tra:

* Camera có đang bị ứng dụng khác chiếm không.
* Máy có camera không.
* OpenCV đã được cài đúng chưa.
* Camera index có đúng không.

### 2. Không tìm thấy ảnh

Nếu terminal báo:

```txt
Không tìm thấy ảnh...
```

Cần kiểm tra:

* File ảnh có đúng tên không.
* File có nằm đúng thư mục `assets/...` không.
* Đuôi file có đúng là `.png`, `.jpg`, `.jpeg` không.
* Đường dẫn trong code có khớp với thư mục thật không.

### 3. Không nghe thấy âm thanh

Cần kiểm tra:

* File âm thanh có nằm trong `assets/sounds/` không.
* Tên file trong code có đúng không.
* File là `.wav` hoặc định dạng Pygame hỗ trợ.
* Âm lượng máy có bị tắt không.

### 4. Game bị đen màn hình

Cần kiểm tra:

* `pygame.display.flip()` có nằm cuối vòng lặp game không.
* Phần `draw` có chạy đúng theo `game_state` không.
* Intro/cutscene có bị `return` quá sớm không.
* Có vẽ nền mỗi frame không.

### 5. Game bị lệch giao diện sau khi đổi kích thước màn hình

Cần kiểm tra:

* Các vị trí UI có còn dùng tọa độ cứng cũ không.
* `WIDTH`, `HEIGHT`, `LANES`, `ROAD_*` trong `settings.py` đã đồng bộ chưa.
* Camera preview, HUD, shop và panel có căn theo `WIDTH // 2`, `HEIGHT // 2` chưa.

---

## 📌 Ghi chú

Đây là project game học tập và thử nghiệm, tập trung vào:

* Pygame 2D.
* Điều khiển nhân vật bằng bàn phím và camera.
* Nhận diện tay bằng MediaPipe.
* Thiết kế gameplay nhiều màn.
* Boss battle.
* Shop và item.
* Quản lý asset hình ảnh/âm thanh.
* Cắt cảnh mở đầu.
* UI tiếng Việt.

Project có thể tiếp tục mở rộng thêm nhiều tính năng mới trong tương lai.

---

## 👤 Tác giả

Project được phát triển bởi *Lại Minh Hiệp* và *Nguyễn Quang Duy*.


