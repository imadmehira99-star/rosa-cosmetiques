import os
import sys
import tkinter as tk
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials, firestore

# تحديد المسار الحالي للتطبيق سواء كود عادي أو exe
if getattr(sys, 'frozen', False):
  current_dir = os.path.dirname(sys.executable)
else:
  current_dir = os.path.dirname(os.path.abspath(__file__))

# البحث عن ملف الـ JSON
json_files = [f for f in os.listdir(current_dir) if f.endswith('.json')]

if not json_files:
  root = tk.Tk()
  root.withdraw()
  messagebox.showerror('خطأ', 'لم يتم العثور على ملف Firebase (.json)!')
  sys.exit()

# تهيئة Firebase
if not firebase_admin._apps:
  cred_path = os.path.join(current_dir, json_files[0])
  cred = credentials.Certificate(cred_path)
  firebase_admin.initialize_app(cred)

db = firestore.client()


# دالة البحث عن المنتج بواسطة الباركود
def search_product(event=None):
  barcode = entry_barcode.get().strip()

  if not barcode:
    return

  try:
    doc_ref = db.collection('products').document(barcode)
    doc = doc_ref.get()

    if doc.exists:
      data = doc.to_dict()

      # تحديث الواجهة بالبيانات
      lbl_name_ar_val.config(text=data.get('name_ar', '-'))
      lbl_name_fr_val.config(text=data.get('name_fr', '-'))
      lbl_price_val.config(text=f"{data.get('price', 0):,.2f} دج")
      lbl_desc_ar_val.config(text=data.get('description_ar', '-'))
      lbl_desc_fr_val.config(text=data.get('description_fr', '-'))
      lbl_status.config(text='✅ تم العثور على المنتج', fg='#00ff66')
    else:
      # إعادة ضبط الحقول إذا لم يوجد المنتج
      clear_display()
      lbl_status.config(text='❌ المنتج غير موجود في النظام', fg='#ff3333')

    # تحديد النص بالكامل ليكون جاهزاً للمسح التالي فوراً
    entry_barcode.select_range(0, tk.END)

  except Exception as e:
    messagebox.showerror('خطأ', f'حدث خطأ أثناء البحث: {e}')


def clear_display():
  lbl_name_ar_val.config(text='-')
  lbl_name_fr_val.config(text='-')
  lbl_price_val.config(text='-')
  lbl_desc_ar_val.config(text='-')
  lbl_desc_fr_val.config(text='-')


# إنشاء الواجهة الرسومية
root = tk.Tk()
root.title('Rosa Cosmétiques - شاشة الاستعلام والأسعار')
root.geometry('480x620')
root.config(bg='#121212')

# الهيدر
header_frame = tk.Frame(root, bg='#121212')
header_frame.pack(fill='x', pady=15)

tk.Label(
    header_frame,
    text='🌹 ROSA COSMÉTIQUES 🌹',
    font=('Segoe UI', 16, 'bold'),
    bg='#121212',
    fg='#ff4d4d',
).pack()
tk.Label(
    header_frame,
    text='شاشة البحث والاستعلام السريع عن الأسعار',
    font=('Segoe UI', 10),
    bg='#121212',
    fg='#b3b3b3',
).pack(pady=2)

# إدخال الباركود
search_frame = tk.Frame(root, bg='#1e1e1e', padx=15, pady=15)
search_frame.pack(fill='x', padx=20, pady=5)

tk.Label(
    search_frame,
    text='امسح الباركود هنا:',
    font=('Segoe UI', 10, 'bold'),
    bg='#1e1e1e',
    fg='#ffffff',
).pack(anchor='w')

entry_barcode = tk.Entry(
    search_frame,
    font=('Segoe UI', 14, 'bold'),
    bg='#2c2c2c',
    fg='#ffffff',
    insertbackground='white',
    relief='flat',
    highlightbackground='#ff4d4d',
    highlightthickness=1,
)
entry_barcode.pack(fill='x', pady=5, ipady=4)
entry_barcode.bind('<Return>', search_product)

lbl_status = tk.Label(
    search_frame,
    text='جاهز لقراءة الباركود...',
    font=('Segoe UI', 9),
    bg='#1e1e1e',
    fg='#888888',
)
lbl_status.pack(anchor='w', pady=2)

# بطاقة عرض تفاصيل المنتج
card_frame = tk.Frame(
    root, bg='#1e1e1e', highlightbackground='#333333', highlightthickness=1
)
card_frame.pack(fill='both', expand=True, padx=20, pady=10)


def create_info_row(parent, title):
  frame = tk.Frame(parent, bg='#1e1e1e')
  frame.pack(fill='x', padx=15, pady=6)
  tk.Label(
      frame,
      text=title,
      font=('Segoe UI', 9),
      bg='#1e1e1e',
      fg='#aaaaaa',
      anchor='w',
  ).pack(fill='x')
  val_lbl = tk.Label(
      frame,
      text='-',
      font=('Segoe UI', 11, 'bold'),
      bg='#1e1e1e',
      fg='#ffffff',
      anchor='w',
      justify='left',
  )
  val_lbl.pack(fill='x')
  return val_lbl


lbl_name_ar_val = create_info_row(card_frame, 'الاسم بالعربية:')
lbl_name_fr_val = create_info_row(card_frame, 'الاسم بالفرنسية:')

# إبراز السعر بلون وحجم أكبر
price_frame = tk.Frame(card_frame, bg='#2a1515', padx=10, pady=8)
price_frame.pack(fill='x', padx=15, pady=10)
tk.Label(
    price_frame,
    text='السعر للمستهلك:',
    font=('Segoe UI', 9, 'bold'),
    bg='#2a1515',
    fg='#ff4d4d',
).pack(anchor='w')
lbl_price_val = tk.Label(
    price_frame,
    text='- دج',
    font=('Segoe UI', 18, 'bold'),
    bg='#2a1515',
    fg='#ff4d4d',
)
lbl_price_val.pack(anchor='w')

lbl_desc_ar_val = create_info_row(card_frame, 'الوصف بالعربية:')
lbl_desc_fr_val = create_info_row(card_frame, 'الوصف بالفرنسية:')

entry_barcode.focus()
root.mainloop()