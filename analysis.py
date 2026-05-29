# 超市销售数据分析（含可视化）
import pandas as pd
import matplotlib.pyplot as plt

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# ==================================================
# 1. 读取数据
# ==================================================
print("=" * 60)
print("超市销售数据分析报告")
print("=" * 60)

df = pd.read_csv('C:/Users/30905/Desktop/Superstore.csv', encoding='latin1')
print(f"数据规模：{df.shape[0]} 行，{df.shape[1]} 列\n")

# ==================================================
# 2. 利润分析
# ==================================================
print("=" * 60)
print("问题1：各品类的利润情况")
print("=" * 60)

category_profit = df.groupby('Category')['Profit'].sum().sort_values(ascending=False)
print(category_profit)
print()

# 图1：品类利润柱状图
plt.figure(figsize=(8, 5))
plt.bar(category_profit.index, category_profit.values, color=['green', 'blue', 'red'])
plt.xlabel('品类')
plt.ylabel('利润（美元）')
plt.title('各品类利润对比')
for i, v in enumerate(category_profit.values):
    plt.text(i, v + 1000, f'{v:.0f}', ha='center', fontsize=10)
plt.tight_layout()
plt.savefig('C:/Users/30905/Desktop/品类利润对比.png', dpi=150)
plt.show()
print("✓ 图表已保存：品类利润对比.png\n")

subcategory_profit = df.groupby('Sub-Category')['Profit'].sum().sort_values()
print("亏损最严重的5个子品类：")
print(subcategory_profit.head())
print()

# 图2：亏损子品类柱状图
plt.figure(figsize=(10, 5))
top_loss = subcategory_profit.head(5)
colors = ['red' if x < 0 else 'green' for x in top_loss.values]
plt.barh(top_loss.index, top_loss.values, color=colors)
plt.xlabel('利润（美元）')
plt.title('亏损最严重的5个子品类')
plt.tight_layout()
plt.savefig('C:/Users/30905/Desktop/亏损子品类.png', dpi=150)
plt.show()
print("✓ 图表已保存：亏损子品类.png\n")

# ==================================================
# 3. 折扣与亏损的关系
# ==================================================
print("=" * 60)
print("问题2：折扣与亏损的关系")
print("=" * 60)

loss_orders = df[df['Profit'] < 0]
print(f"亏损订单数量：{len(loss_orders)} 单")
print(f"亏损订单占比：{len(loss_orders)/len(df)*100:.2f}%")

discount_bins = [-0.01, 0, 0.2, 0.4, 0.6, 0.8, 1]
discount_labels = ['0%', '0-20%', '20-40%', '40-60%', '60-80%', '80-100%']
df['Discount_Range'] = pd.cut(df['Discount'], bins=discount_bins, labels=discount_labels)

loss_rate_by_discount = []
for label in discount_labels:
    group = df[df['Discount_Range'] == label]
    if len(group) > 0:
        loss_rate = len(group[group['Profit'] < 0]) / len(group) * 100
        loss_rate_by_discount.append(loss_rate)
        print(f"折扣 {label}：订单数 {len(group)}，亏损率 {loss_rate:.1f}%")

# 图3：折扣 vs 亏损率折线图
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
print("✓ 图表已保存：折扣与亏损率.png\n")

# ==================================================
# 4. 结论
# ==================================================
print("=" * 60)
print("分析结论汇总")
print("=" * 60)
print("1. 最赚钱的品类是：" + category_profit.index[0])
print("2. 最亏损的品类是：" + category_profit.index[-1])
print(f"3. {len(loss_orders)} 个亏损订单，占总订单的 {len(loss_orders)/len(df)*100:.1f}%")
print("4. 折扣越高，亏损率越高（特别是折扣>20%时）")
print("\n5. 业务建议：")
print("   - 控制折扣力度在20%以内，避免亏损")
print("   - 重点优化 Tables 子品类的定价策略")
print("   - Furniture 品类需要重新评估产品组合")