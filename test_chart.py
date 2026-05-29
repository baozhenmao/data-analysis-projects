import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('C:/Users/30905/Desktop/Superstore.csv', encoding='latin1')

discount_bins = [-0.01, 0, 0.2, 0.4, 0.6, 0.8, 1]
discount_labels = ['0%', '0-20%', '20-40%', '40-60%', '60-80%', '80-100%']
df['Discount_Range'] = pd.cut(df['Discount'], bins=discount_bins, labels=discount_labels)

# 修复：确保每个区间都有值（没有订单的区间填0）
loss_rate_by_discount = []
for label in discount_labels:
    group = df[df['Discount_Range'] == label]
    if len(group) > 0:
        loss_rate = len(group[group['Profit'] < 0]) / len(group) * 100
        print(f"折扣 {label}：订单数 {len(group)}，亏损率 {loss_rate:.1f}%")
    else:
        loss_rate = 0
        print(f"折扣 {label}：订单数 0，亏损率 0%")
    loss_rate_by_discount.append(loss_rate)

# 画图
plt.figure(figsize=(8, 5))
plt.plot(discount_labels, loss_rate_by_discount, marker='o', linewidth=2, markersize=8)
plt.xlabel('折扣区间')
plt.ylabel('亏损率（%）')
plt.title('折扣区间与亏损率的关系')
plt.grid(True, alpha=0.3)
for i, v in enumerate(loss_rate_by_discount):
    plt.text(i, v + 2, f'{v:.0f}%', ha='center', fontsize=10)
plt.tight_layout()
plt.savefig('C:/Users/30905/Desktop/折扣与亏损率.png', dpi=150)
plt.show()
print("\n✓ 图表已保存：折扣与亏损率.png")