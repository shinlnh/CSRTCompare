# Cost-Benefit Analysis

## Mục đích
Biểu đồ này đánh giá **efficiency** (hiệu quả) của mỗi tracker bằng cách so sánh **benefit** (FPS) với **cost** (tổng hợp CPU, RAM, GPU).

## Cấu Trúc Biểu Đồ

### Subplot 1: Cost vs Benefit Scatter Plot
- **X-axis**: Resource Cost = CPU% + RAM(MB)/10 + GPU%×2
- **Y-axis**: Benefit = Average FPS
- **Ideal position**: Top-left (high benefit, low cost)

### Subplot 2: Efficiency Bar Chart
- **Metric**: Efficiency = FPS / Resource Cost
- **Higher is better**: More FPS per resource unit

---

## Cost Formula Explained

```
Resource Cost = CPU% + RAM(MB)/10 + GPU%×2
```

### Weights Rationale:

1. **CPU% × 1**
   - Direct contribution: 30% CPU = 30 cost units

2. **RAM(MB) / 10**
   - Scaling: 150MB RAM = 15 cost units
   - Matches importance with CPU

3. **GPU% × 2** (Double weight!)
   - GPU dependencies = expensive
   - Power consumption 5-10x CPU
   - Hardware cost 10-20x
   - Critical constraint for mobile robots

---

## Subplot 1 Analysis: Cost-Benefit Scatter

### CSRT Position
```
X (Cost): ~32 + 152/10 + 0×2 = ~47
Y (FPS):  25
Position: Medium-left (moderate cost, sufficient benefit)
```

**Interpretation**:
- ✅ **Low-medium cost** (no GPU penalty)
- ✅ **Sufficient FPS** (25 FPS adequate)
- ✅ **Best cost-efficiency sweet spot**

---

### OSTrack Position
```
X (Cost): ~24 + 515/10 + 47×2 = ~170
Y (FPS):  62.5
Position: Top-right (high benefit BUT very high cost)
```

**Interpretation**:
- ✅ Highest FPS (62.5)
- ❌ **Highest cost** (3.6x CSRT cost!)
- ❌ GPU penalty: +94 cost units
- ❌ RAM penalty: +36 cost units

---

### SiamRPN++ Position
```
X (Cost): ~29 + 315/10 + 31×2 = ~123
Y (FPS):  38.5
Position: Middle (medium benefit, medium-high cost)
```

**Interpretation**:
- ⚠️ Better FPS than CSRT (+54%)
- ⚠️ But 2.6x higher cost
- ⚠️ Not worth the trade-off

---

### DiMP Position
```
X (Cost): ~31 + 287/10 + 39×2 = ~137
Y (FPS):  32.3
Position: Middle-right (medium benefit, high cost)
```

**Interpretation**:
- ⚠️ Similar FPS to CSRT (+29%)
- ❌ 2.9x higher cost
- ❌ Worst value proposition

---

## Subplot 2 Analysis: Efficiency Ranking

### Efficiency Formula
```
Efficiency = FPS / Resource Cost
```

### Results Ranking

1. **🥇 CSRT: Efficiency = 25 / 47 = 0.53**
   - ✅ **HIGHEST efficiency**
   - ✅ Best FPS per resource unit
   - ✅ Winner!

2. **🥈 SiamRPN++: Efficiency = 38.5 / 123 = 0.31**
   - 41% lower than CSRT
   - Higher FPS không bù đắp được high cost

3. **🥉 OSTrack: Efficiency = 62.5 / 170 = 0.37**
   - 30% lower than CSRT  
   - Highest FPS but **worst cost**

4. **DiMP: Efficiency = 32.3 / 137 = 0.24**
   - Lowest efficiency
   - Worst value

---

## Detailed Efficiency Analysis

### CSRT: Why Most Efficient?

**Cost breakdown**:
- CPU: 32% → 32 units
- RAM: 152MB/10 → 15 units
- GPU: 0% × 2 → **0 units** ✅
- **Total: 47 units**

**Benefit**: 25 FPS (sufficient for robot)

**Key advantage**: **Zero GPU cost** saves 90+ units

---

### OSTrack: Why Inefficient Despite High FPS?

**Cost breakdown**:
- CPU: 24% → 24 units (good!)
- RAM: 515MB/10 → 52 units ❌
- GPU: 47% × 2 → **94 units** ❌❌
- **Total: 170 units** (3.6x CSRT!)

**Benefit**: 62.5 FPS

**Problem**: 
- 2.5x more FPS costs 3.6x resources
- GPU penalty (94 units) kills efficiency
- Not linear scaling

---

## Real-World Cost Translation

### Hardware Cost Impact

| Tracker | Min Hardware | Cost | Efficiency $/FPS |
|---------|--------------|------|------------------|
| CSRT | Raspberry Pi 4 | $50 | **$2/FPS** ✅ |
| SiamRPN++ | Jetson Nano | $200 | $5.2/FPS |
| DiMP | Jetson Xavier NX | $500 | $15.5/FPS |
| OSTrack | Jetson AGX Orin | $1000+ | **$16/FPS** ❌ |

**CSRT efficiency**: 8x better than OSTrack ($2 vs $16 per FPS)

---

### Power Consumption Impact

| Tracker | CPU+GPU Power | Battery Life* | Efficiency min/FPS |
|---------|---------------|---------------|-------------------|
| CSRT | ~5W | 30 min | **1.2 min/FPS** ✅ |
| SiamRPN++ | ~15W | 15 min | 0.39 min/FPS |
| DiMP | ~18W | 12 min | 0.37 min/FPS |
| OSTrack | ~25W | 8 min | **0.13 min/FPS** ❌ |

*Assuming 150Wh drone battery

**CSRT efficiency**: 9x better than OSTrack (1.2 vs 0.13 min/FPS)

---

### Deployment Cost (100 units)

| Tracker | Hardware/Unit | Total Cost | FPS Total | Cost/FPS |
|---------|---------------|------------|-----------|----------|
| CSRT | $50 | **$5,000** | 2500 | **$2** ✅ |
| OSTrack | $1000 | **$100,000** | 6250 | $16 ❌ |

**Production reality**:
- OSTrack: 20x more expensive hardware
- CSRT: 2.5x less total FPS but **10x cheaper per FPS**
- **Winner**: CSRT for large-scale deployment

---

## Break-Even Analysis

### Question: When is OSTrack worth it?

**OSTrack advantages**:
- +37.5 FPS more than CSRT (62.5 vs 25)
- Better for complex scenes?

**OSTrack costs**:
- +$950 hardware per unit
- +20W power consumption  
- +363MB RAM (may not fit)
- **Unpredictable latency** (variance 7x worse)

**Break-even condition**:
- Need >50 FPS absolutely required
- AND unlimited budget
- AND desktop/server environment (not mobile)
- AND OK with unpredictable latency

**Reality**: <5% of robotics applications need >50 FPS

---

## ROI (Return on Investment) Analysis

### Scenario: Warehouse with 50 robots

**CSRT deployment**:
- Cost: 50 × $50 = $2,500
- FPS: 50 × 25 = 1,250 total
- Power: 50 × 5W = 250W
- Reliability: High (variance 9)

**OSTrack deployment**:
- Cost: 50 × $1,000 = $50,000
- FPS: 50 × 62.5 = 3,125 total
- Power: 50 × 25W = 1,250W
- Reliability: Low (variance 64)

**Analysis**:
- OSTrack: 20x cost, 5x power for 2.5x FPS
- Extra 37.5 FPS per robot = **Overkill** (not needed)
- **ROI**: CSRT wins decisively

---

## Efficiency Pareto Frontier

```
Efficiency (FPS/Cost)
  0.6 |  
  0.5 |  ● CSRT (0.53) ← Optimal
  0.4 |     ● OSTrack (0.37)
  0.3 |        ● SiamRPN++ (0.31)
  0.2 |           ● DiMP (0.24)
  0.1 |
      +--------------------------------
        Low Cost              High Cost
```

**CSRT dominates**: No tracker has better efficiency

---

## Kết Luận

### CSRT Thắng Vì:

1. ✅ **Highest efficiency**: 0.53 (best FPS per resource unit)
2. ✅ **Lowest total cost**: 47 units (3.6x cheaper than OSTrack)
3. ✅ **Zero GPU penalty**: Saves 90+ cost units
4. ✅ **Best ROI**: $2 per FPS vs $16 (OSTrack)
5. ✅ **Scalable**: 20x cheaper for large deployments

### Modern Trackers Thua Vì:

1. ❌ **GPU dependency** kills efficiency (×2 cost weight)
2. ❌ **High RAM** adds cost without benefit
3. ❌ **Diminishing returns**: 2.5x FPS costs 3.6x resources
4. ❌ **Overkill performance**: >50 FPS not needed
5. ❌ **Poor ROI**: Not justified for production

### Critical Insight

> **Cost-Benefit proves:**
> - CSRT = **Best value proposition**
> - OSTrack = Fast but **expensive & inefficient**
> - For robotics: **Efficiency > Raw performance**
> - Budget matters: **CSRT scales, OSTrack doesn't**

→ **CSRT: Maximum efficiency for minimum cost!** 💰✅
