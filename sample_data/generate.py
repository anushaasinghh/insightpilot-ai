# Run this once to generate it
import pandas as pd, numpy as np, random
from datetime import datetime, timedelta

random.seed(42); np.random.seed(42)
products   = ["Laptop","Phone","Tablet","Monitor","Keyboard","Mouse","Headphones","Webcam"]
regions    = ["North","South","East","West"]
categories = {"Laptop":"Computing","Phone":"Mobile","Tablet":"Mobile",
              "Monitor":"Computing","Keyboard":"Accessories",
              "Mouse":"Accessories","Headphones":"Audio","Webcam":"Accessories"}

rows = []
for i in range(1000):
    product  = random.choice(products)
    date     = datetime(2024,1,1) + timedelta(days=random.randint(0,364))
    qty      = random.randint(1, 20)
    price    = {"Laptop":999,"Phone":699,"Tablet":449,"Monitor":379,
                "Keyboard":89,"Mouse":49,"Headphones":199,"Webcam":129}[product]
    rows.append({
        "date": date.strftime("%Y-%m-%d"),
        "product": product,
        "category": categories[product],
        "region": random.choice(regions),
        "quantity": qty,
        "unit_price": price,
        "revenue": round(qty * price * random.uniform(0.9,1.1), 2),
        "customer_id": f"CUST-{random.randint(1000,9999)}",
        "returned": random.random() < 0.05
    })

pd.DataFrame(rows).to_csv("sample_data/sample_sales.csv", index=False)
print("✅ Sample data created")