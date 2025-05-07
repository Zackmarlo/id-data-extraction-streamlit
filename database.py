import sqlite3

# ✅ اسم قاعدة البيانات
DB_PATH = "egypt_id_data.db"

# ✅ إنشاء الاتصال بقاعدة البيانات
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ✅ إنشاء الجدول إذا لم يكن موجودًا
cursor.execute("""
CREATE TABLE IF NOT EXISTS id_cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    family_name TEXT,
    number TEXT,
    birth TEXT,
    city TEXT,
    state TEXT,
    neighborhood TEXT,
    date TEXT,
    code TEXT,
    image TEXT
)
""")
conn.commit()

# ✅ دالة لحفظ البيانات في القاعدة
def save_to_db(fields: dict):
    cursor.execute("""
        INSERT INTO id_cards (
            name, family_name, number, birth, city, state, neighborhood, date, code, image
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        fields.get("name", ""),
        fields.get("family name", ""),
        fields.get("number", ""),
        fields.get("birth", ""),
        fields.get("city", ""),
        fields.get("state", ""),
        fields.get("neighborhood", ""),
        fields.get("date", ""),
        fields.get("code", ""),
        fields.get("image", ""),
    ))
    conn.commit()
    print("✅ تم حفظ البيانات في قاعدة البيانات بنجاح.")

# ✅ مثال لتجربة الدالة
sample_fields = {
    "name": "أحمد",
    "family name": "حسين",
    "number": "29804150102875",
    "birth": "15/04/1998",
    "city": "الزقازيق",
    "state": "الشرقية",
    "neighborhood": "حي ثان",
    "date": "01/01/2023",
    "code": "12345",
    "image": "photo_base64_or_url"
}

save_to_db(sample_fields)

# ✅ يمكنك أيضًا استعراض البيانات لاحقًا:
for row in cursor.execute("SELECT * FROM id_cards"):
    print(row)

# ❌ لا تنسَ إغلاق الاتصال عند الانتهاء
conn.close()