import os
import firebase_admin
from firebase_admin import credentials, firestore

# البحث التلقائي عن ملف الـ JSON في المجلد الحالي
json_files = [f for f in os.listdir() if f.endswith(".json")]

if not json_files:
  print("❌ خطأ: لم يتم العثور على ملف الـ JSON في المجلد!")
  exit()

# استخدام اسم الملف الحقيقي الذي تم العثور عليه تلقائياً
cred_file = json_files[0]
print(f"📂 تم العثور على ملف المفتاح: {cred_file}")

cred = credentials.Certificate(cred_file)
firebase_admin.initialize_app(cred)

# جلب وعرض المنتجات من قاعدة البيانات
db = firestore.client()
docs = db.collection("products").stream()

print("\n--- 📦 قائمة منتجات متجر مستحضرات التجميل ---")
for doc in docs:
  product = doc.to_dict()
  print(f"🔹 ID المستند: {doc.id}")
  print(f"الباركود: {product.get('barcode')}")
  print(f"الاسم بالعربية: {product.get('name_ar')}")
  print(f"الاسم بالفرنسية: {product.get('name_fr')}")
  print(f"السعر: {product.get('price')} دج")
  print(f"الوصف: {product.get('description')}")
  print("-" * 45)