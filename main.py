from pathlib import Path

import numpy as np

csv_path = Path(__file__).with_name("orders.csv")

order_dtype = np.dtype([
    ("order_id", "i8"),
    ("customer", "U50"),
    ("city", "U30"),
    ("product", "U50"),
    ("quantity", "i4"),
    ("unit_price", "f8"),
    ("discount", "f8"),
    ("is_paid", "?"),
    ("is_delivered", "?"),
])

orders = np.genfromtxt(
    csv_path,
    delimiter=",",
    names=True,
    dtype=order_dtype,
    encoding="utf-8-sig",
    ndmin=1,
)

print(f"Прочитано замовлень: {len(orders)}")

print("\n Перші 100 замовлень")
print(", ".join(orders.dtype.names))
print(orders[:100])

unit_prices = orders["unit_price"]

print("\n Ціни за одиницю товару")
with np.printoptions(threshold=unit_prices.size):
    print(unit_prices)

print(f"Мінімальна ціна: {unit_prices.min():.2f} грн")
print(f"Максимальна ціна: {unit_prices.max():.2f} грн")
print(f"Середня ціна: {unit_prices.mean():.2f} грн")

summary_fields = [
    "order_id",
    "customer",
    "city",
    "quantity",
    "unit_price",
    "is_paid",
]

order_summary = orders[summary_fields].copy()

print("\nСкорочені дані про замовлення")
print(", ".join(order_summary.dtype.names))

with np.printoptions(threshold=order_summary.size):
    print(order_summary)

order_totals = (
    orders["quantity"] * unit_prices * (1 - orders["discount"] / 100)
)

print("\n Звіт про замовлення")

for order, total in zip(orders, order_totals):
    paid = "Так" if order["is_paid"] else "Ні"
    delivered = "Так" if order["is_delivered"] else "Ні"

    print(
        f"Замовлення №{order['order_id']} | Покупець: {order['customer']} | "
        f"Місто: {order['city']} | Товар: {order['product']} | "
        f"Кількість: {order['quantity']} | Сума: {total:.2f} грн | "
        f"Оплачено: {paid} | Доставлено: {delivered}"
    )

unpaid_mask = ~orders["is_paid"]

total_amount = order_totals.sum()
unpaid_count = np.count_nonzero(unpaid_mask)
unpaid_amount = order_totals[unpaid_mask].sum()

print("\n Підсумки")
print(f"Загальна вартість усіх замовлень: {total_amount:.2f} грн")
print(f"Кількість неоплачених замовлень: {unpaid_count}")
print(f"Загальна вартість неоплачених замовлень: {unpaid_amount:.2f} грн")