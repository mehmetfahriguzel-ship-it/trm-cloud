import pandas as pd
from jinja2 import Template
from datetime import datetime, timezone
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True, parents=True)

# ----- ÖRNEK VERİ -----
products = [
    {"sku": "SKU-A", "name": "Ürün A", "price": 199.90, "commission": 0.18},
    {"sku": "SKU-B", "name": "Ürün B", "price": 89.90,  "commission": 0.22},
    {"sku": "SKU-C", "name": "Ürün C", "price": 349.00, "commission": 0.15},
    {"sku": "SKU-D", "name": "Ürün D", "price": 59.90,  "commission": 0.28},
    {"sku": "SKU-E", "name": "Ürün E", "price": 129.00, "commission": 0.12},
]
df = pd.DataFrame(products)
df["estimated_commission_try"] = (df["price"] * df["commission"]).round(2)

csv_path = REPORTS / "TRM_REPORT_PRETTY.csv"
df.to_csv(csv_path, index=False, encoding="utf-8")

html_tpl = Template("""
<!doctype html><meta charset="utf-8">
<title>TRM Günlük Özet</title>
<style>
body{font-family:Arial, sans-serif;margin:24px}
table{border-collapse:collapse;width:100%;margin-top:16px}
th,td{border:1px solid #ddd;padding:8px;text-align:left}
th{background:#f2f2f2} tfoot td{font-weight:bold}
</style>
<h1>TRM Günlük Özet</h1>
<small>Oluşturulma: {{ created_at }}</small>
<table>
<thead><tr><th>SKU</th><th>Ürün</th><th>Fiyat (₺)</th><th>Komisyon</th><th>Tahmini Komisyon (₺)</th></tr></thead>
<tbody>
{% for r in rows %}
<tr><td>{{r.sku}}</td><td>{{r.name}}</td><td>{{'%.2f'|format(r.price)}}</td><td>{{'%.0f%%'|format(r.commission*100)}}</td><td>{{'%.2f'|format(r.estimated_commission_try)}}</td></tr>
{% endfor %}
</tbody>
<tfoot><tr><td colspan="4">Toplam Tahmini Komisyon</td><td>{{'%.2f'|format(total)}}</td></tr></tfoot>
</table>
""")

now = datetime.now(timezone.utc).astimezone()
html = html_tpl.render(
    created_at=now.strftime('%Y-%m-%d %H:%M %Z'),
    rows=df.to_dict(orient="records"),
    total=float(df["estimated_commission_try"].sum()),
)
(REPORTS / "latest_v1_2_summary.html").write_text(html, encoding="utf-8")
print("[TRM] Raporlar yazıldı:", csv_path, "ve latest_v1_2_summary.html")
