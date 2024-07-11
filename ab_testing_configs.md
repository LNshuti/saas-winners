
## **Objective:**
To understand which of the two buttons (indicators) users are more likely to click and use for longer times on the app.

### Summary

- **Objective:** Compare click-through rates and usage time for SMA vs. MACD buttons.
- **Test Groups:** 2 (Button A: SMA, Button B: MACD)
- **Key Metrics:** CTR, Average usage time
- **Traffic Allocation:** 50% SMA, 50% MACD
- **Significance Level:** 0.05
- **Power:** 0.8
- **Minimum Sample Size:** 3837 users per group
- **Test Duration:** 30 days

### **Number of test groups:**
2 (Button A: SMA, Button B: MACD)

### Key Metrics

- Click-through rate (CTR) for each button
- Average usage time of each button

### Expected Conversion Rates

**Current conversion rate (baseline) and expected lift:**
- Baseline CTR for Button A (SMA): 10%
- Expected CTR for Button A (SMA): 12%
- Baseline CTR for Button B (MACD): 10%
- Expected CTR for Button B (MACD): 12%

### **Significance level (alpha) and power (1-beta):**
- Significance level: 0.05
- Power: 0.8

### **Traffic allocation between the test groups:**
- 50% to Button A (SMA)
- 50% to Button B (MACD)

### **Planned duration of the test:**
- 30 days

-
### Sample Size Calculation

We calculate the sample size for each group to detect the expected change in CTR with the given significance level and power. We use a sample size calculator for proportions.

**Sample Size Calculation Formula:**
\[ n = \frac{{(Z_{\alpha/2} + Z_{\beta})^2 \times [p_1(1 - p_1) + p_2(1 - p_2)]}}{{(p_1 - p_2)^2}} \]

Where:
- \( Z_{\alpha/2} \) = Z-value for the desired significance level (1.96 for 0.05)
- \( Z_{\beta} \) = Z-value for the desired power (0.84 for 0.8)
- \( p_1 \) = baseline conversion rate (10% or 0.10)
- \( p_2 \) = expected conversion rate (12% or 0.12)

Plugging in the values:
\[ n = \frac{{(1.96 + 0.84)^2 \times [0.10(1 - 0.10) + 0.12(1 - 0.12)]}}{{(0.12 - 0.10)^2}} \]
\[ n = \frac{{(2.8)^2 \times [0.10 \times 0.90 + 0.12 \times 0.88]}}{{(0.02)^2}} \]
\[ n = \frac{{7.84 \times [0.09 + 0.1056]}}{{0.0004}} \]
\[ n = \frac{{7.84 \times 0.1956}}{{0.0004}} \]
\[ n = \frac{{1.534464}}{{0.0004}} \]
\[ n = 3836.16 \]

