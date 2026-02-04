# Hardware Comparison Overview

## Mục đích
Biểu đồ này so sánh trực tiếp 6 metrics quan trọng của 4 trackers để đánh giá khả năng triển khai trên phần cứng hạn chế.

## Các Metrics Được So Sánh

### 1. **Average FPS (Throughput)**
- **Kết quả**: OSTrack thắng (62.5 FPS) > SiamRPN++ (38.5) > DiMP (32.3) > CSRT (25.0)
- **Phân tích**: 
  - CSRT có FPS thấp nhất NHƯNG vẫn **đủ cho robot** (threshold ~20 FPS)
  - FPS cao hơn không quan trọng nếu không ổn định

### 2. **Average Latency** 
- **Kết quả**: OSTrack thấp nhất (16.7ms) < SiamRPN++ < DiMP < CSRT (41.2ms)
- **Phân tích**:
  - CSRT có latency cao hơn NHƯNG vẫn trong ngưỡng acceptable (<50ms)
  - Quan trọng hơn là **variance thấp** (xem metric 3)

### 3. **Latency Variance** ⭐ MOST IMPORTANT
- **Kết quả**: CSRT **THẮNG ÁP ĐẢO** (9) << SiamRPN++ (36) << DiMP (49) << OSTrack (64)
- **Tại sao CSRT thắng**:
  - Variance thấp = **Predictable** = Critical cho real-time control
  - OSTrack có variance **7x cao hơn** = Không tin cậy được
  - Robot cần biết chính xác thời gian response, không chấp nhận bất ngờ

### 4. **CPU Usage**
- **Kết quả**: OSTrack thấp nhất (23.8%) < DiMP < CSRT (32.6%)
- **Phân tích**:
  - CSRT cao hơn một chút NHƯNG không cần GPU bù lại
  - CPU 32% vẫn để lại 68% cho tasks khác (navigation, planning, etc.)

### 5. **RAM Usage** ⭐ CRITICAL FOR EMBEDDED
- **Kết quả**: CSRT **THẮNG** (152MB) << DiMP (286MB) << SiamRPN++ (315MB) << OSTrack (515MB)
- **Tại sao CSRT thắng**:
  - **3.4x nhẹ hơn** OSTrack
  - Chạy được trên Raspberry Pi 4 (1-2GB RAM)
  - Modern trackers cần 512MB+ chỉ cho tracker, không đủ RAM cho OS + apps khác

### 6. **GPU Usage** ⭐ CRITICAL FOR COST & POWER
- **Kết quả**: CSRT **THẮNG TUYỆT ĐỐI** (0%) << SiamRPN++ (30.7%) < DiMP (38.5%) < OSTrack (47.2%)
- **Tại sao CSRT thắng**:
  - **Không cần GPU** = Không cần phần cứng đắt ($1000+)
  - **Tiết kiệm điện**: 2-5W (CPU) vs 15-30W (GPU)
  - **Phù hợp battery-powered robots**: Drone, AGV mobile

## Kết Luận

### CSRT Thắng Vì:
1. ✅ **Latency Variance thấp nhất** → Predictable, reliable
2. ✅ **RAM nhẹ nhất** → Chạy trên embedded devices
3. ✅ **Không cần GPU** → Rẻ, tiết kiệm điện, mobile-friendly
4. ✅ **FPS & Latency đủ dùng** → Đáp ứng requirements robot

### Modern Trackers (OSTrack, SiamRPN++, DiMP) Thua Vì:
1. ❌ **Latency variance cao** → Unpredictable, không đáng tin
2. ❌ **Cần RAM nhiều** → Không chạy được Pi, Jetson Nano entry
3. ❌ **Cần GPU** → Đắt, tốn điện, không phù hợp mobile
4. ❌ **Overkill performance** → FPS cao không cần thiết nếu variance cao

## Trade-off Analysis
CSRT trade **một chút performance** (FPS thấp hơn) để đổi lấy:
- **Stability** (variance thấp)
- **Efficiency** (RAM nhẹ, không GPU)
- **Cost** (phần cứng rẻ hơn 20x)
- **Reliability** (fail predictably)

→ **Perfect trade-off cho robotics deployment!**
