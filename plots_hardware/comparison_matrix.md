# Comparison Matrix Heatmap

## Mục đích
Biểu đồ heatmap này visualize **tất cả metrics cùng lúc** trong một ma trận màu, giúp dễ dàng so sánh điểm mạnh/yếu của từng tracker.

## Cấu Trúc Heatmap
- **Rows**: 4 trackers (CSRT, OSTrack, SiamRPN++, DiMP)
- **Columns**: 7 metrics quan trọng
- **Color**: 
  - 🔵 **Blue (low value)** = GOOD for robotics
  - 🔴 **Red (high value)** = BAD for robotics

## Metrics Được Normalize

Tất cả metrics được normalize về scale 0-1:
- **0 (Blue)** = Best value
- **1 (Red)** = Worst value

**Normalization rule**:
- **FPS**: Higher is better → Inverted (1 - value/max)
- **Others**: Lower is better → Direct (value/max)

---

## Đọc Heatmap

### FPS (Column 1)
**Inverted scale**: Blue = High FPS (good)

| Tracker   | Color | Value | Interpretation |
|-----------|-------|-------|----------------|
| OSTrack   | 🔵 Blue | ~0.4 | Highest FPS (62.5) - good |
| SiamRPN++ | 🟡 Yellow | ~0.6 | Medium FPS (38.5) - OK |
| DiMP      | 🟠 Orange | ~0.7 | Lower FPS (32.3) - acceptable |
| CSRT      | 🔴 Red | ~1.0 | Lowest FPS (25.0) - but sufficient |

**CSRT analysis**:
- ⚠️ Red cho FPS (low) NHƯNG 25 FPS vẫn đủ
- Trade-off acceptable cho stability

---

### Latency (Column 2)
**Direct scale**: Blue = Low latency (good)

| Tracker | Color | Value | Interpretation |
|---------|-------|-------|----------------|
| OSTrack | 🔵 Blue | ~0.4 | Lowest avg latency (17ms) - good |
| SiamRPN++ | 🟢 Green | ~0.6 | Medium latency (27ms) - OK |
| DiMP | 🟡 Yellow | ~0.75 | Higher latency (32ms) - acceptable |
| CSRT | 🔴 Red | ~1.0 | Highest latency (41ms) - but predictable |

**CSRT analysis**:
- ⚠️ Red cho latency NHƯNG variance thấp bù lại
- 41ms stable > 17ms unstable

---

### P95 Latency (Column 3)
**Direct scale**: Blue = Low P95 (good)

Similar pattern to average latency
- CSRT: 🔴 Red (~49ms) but **close to mean** = consistent
- OSTrack: 🔵 Blue (~30ms) but **far from mean** = outliers

---

### Latency Variance (Column 4) ⭐ MOST IMPORTANT
**Direct scale**: Blue = Low variance (good)

| Tracker | Color | Value | Interpretation |
|---------|-------|-------|----------------|
| **CSRT** | **🔵 BLUE** | **0.14** | **BEST - Lowest variance (9)** ✅ |
| SiamRPN++ | 🟡 Yellow | ~0.56 | Medium variance (36) |
| DiMP | 🟠 Orange | ~0.77 | High variance (49) |
| OSTrack | 🔴 RED | 1.0 | WORST - Highest variance (64) ❌ |

**CSRT THẮNG ÁP ĐẢO**:
- ✅ **Darkest blue** = Predictable nhất
- ✅ 7x tốt hơn OSTrack
- ✅ **Critical metric** cho robotics

---

### CPU % (Column 5)
**Direct scale**: Blue = Low CPU (good)

| Tracker | Color | Value | Interpretation |
|---------|-------|-------|----------------|
| OSTrack | 🔵 Blue | ~0.4 | Lowest CPU (23.8%) - good |
| SiamRPN++ | 🟢 Green | ~0.5 | Medium CPU (28.8%) - OK |
| DiMP | 🟡 Yellow | ~0.55 | Medium CPU (31.4%) - OK |
| CSRT | 🟠 Orange | ~0.58 | Higher CPU (32.6%) - acceptable |

**CSRT analysis**:
- ⚠️ Orange (không thấp nhất) NHƯNG
- 32% vẫn để lại 68% cho tasks khác
- Không cần GPU bù lại ✅

---

### RAM MB (Column 6) ⭐ CRITICAL
**Direct scale**: Blue = Low RAM (good)

| Tracker | Color | Value | Interpretation |
|---------|-------|-------|----------------|
| **CSRT** | **🔵 BLUE** | **~0.3** | **BEST - Lowest RAM (152MB)** ✅ |
| DiMP | 🟡 Yellow | ~0.56 | Medium RAM (286MB) |
| SiamRPN++ | 🟠 Orange | ~0.61 | Higher RAM (315MB) |
| OSTrack | 🔴 RED | 1.0 | WORST - Highest RAM (515MB) ❌ |

**CSRT THẮNG ÁP ĐẢO**:
- ✅ **Darkest blue** = Nhẹ nhất
- ✅ 3.4x nhẹ hơn OSTrack
- ✅ Chạy được Pi 1-2GB RAM

---

### GPU % (Column 7) ⭐ CRITICAL
**Direct scale**: Blue = Low GPU (good)

| Tracker | Color | Value | Interpretation |
|---------|-------|-------|----------------|
| **CSRT** | **🔵 BLUE (0%)** | **0.0** | **PERFECT - No GPU needed** ✅ |
| SiamRPN++ | 🟠 Orange | ~0.65 | Needs GPU (30.7%) |
| DiMP | 🟠 Orange | ~0.81 | Needs GPU (38.5%) |
| OSTrack | 🔴 RED | 1.0 | WORST - Heavy GPU (47.2%) ❌ |

**CSRT THẮNG TUYỆT ĐỐI**:
- ✅ **Perfect blue (0)** = No GPU
- ✅ Rẻ hơn $1000
- ✅ Tiết kiệm điện
- ✅ Mobile-friendly

---

## Pattern Recognition

### CSRT Row Pattern
```
🔴 🔴 🔴 | 🔵 🟠 🔵 🔵
FPS Lat P95| Var CPU RAM GPU
```

**Interpretation**:
- Left side (Performance): 🔴 Red → Lower raw performance
- Right side (Efficiency): 🔵 Blue → **Superior efficiency**
- **Trade-off**: Sacrifice some speed for stability & efficiency

---

### OSTrack Row Pattern
```
🔵 🔵 🔵 | 🔴 🔵 🔴 🔴
FPS Lat P95| Var CPU RAM GPU
```

**Interpretation**:
- Left side (Performance): 🔵 Blue → High raw performance
- Right side (Efficiency): 🔴 Red → **Poor efficiency**
- **Trade-off**: Fast but unstable & resource-hungry

---

## Visual Summary

### Best for Robotics Pattern (CSRT)
```
Prefer: 🔵 🔵 🔵 in columns 4, 6, 7
        ↓  ↓  ↓
      Var RAM GPU
```
→ **Stability & Efficiency > Raw Speed**

### Bad for Robotics Pattern (OSTrack)
```
Red flags: 🔴 🔴 🔴 in columns 4, 6, 7
           ↓  ↓  ↓
         Var RAM GPU
```
→ **Fast but unreliable & expensive**

---

## Scoring by Color Count

### Blue (Good) Count:
- **CSRT**: 3 blues (Variance, RAM, GPU) ✅
- OSTrack: 3 blues (FPS, Latency, CPU) but wrong metrics ❌
- SiamRPN++: 0 blues
- DiMP: 0 blues

### Red (Bad) Count for Critical Metrics (Var, RAM, GPU):
- **CSRT**: 0 reds in critical metrics ✅
- OSTrack: 3 reds in critical metrics ❌
- Others: 2+ reds

---

## Decision Matrix

### For Robotics (Priority: Var > RAM > GPU > others)
```
              Var  RAM  GPU  | Score
CSRT:         🔵   🔵   🔵   | ✅✅✅ BEST
SiamRPN++:    🟡   🟠   🟠   | ⚠️⚠️⚠️
DiMP:         🟠   🟡   🟠   | ⚠️⚠️⚠️  
OSTrack:      🔴   🔴   🔴   | ❌❌❌ WORST
```

### For Desktop/Research (Priority: FPS > Latency > others)
```
              FPS  Lat  P95  | Score
OSTrack:      🔵   🔵   🔵   | ✅✅✅ BEST
SiamRPN++:    🟡   🟢   🟢   | ✅⚠️
DiMP:         🟠   🟡   🟡   | ⚠️⚠️
CSRT:         🔴   🔴   🔴   | ❌❌❌ WORST
```

---

## Kết Luận

### Heatmap Chứng Minh:

1. **CSRT**: Blue in RIGHT metrics (Var, RAM, GPU)
   - ✅ Optimized for **deployment constraints**
   - ✅ Trade performance for **reliability**

2. **OSTrack**: Blue in WRONG metrics (FPS, Latency)
   - ❌ Optimized for **benchmark numbers**
   - ❌ Ignores **real-world constraints**

3. **Color pattern reveals philosophy**:
   - CSRT: **Engineering for production** 🔧
   - OSTrack: **Research for papers** 📄

## Critical Insight

> **Heatmap shows:**
> - Context matters: Blue ≠ always better
> - **CSRT blues** = Important metrics (Var, RAM, GPU)
> - **OSTrack blues** = Less critical (FPS, Latency)
> - For robotics: **Right blues > More blues**

→ **CSRT has blues where it counts!**
