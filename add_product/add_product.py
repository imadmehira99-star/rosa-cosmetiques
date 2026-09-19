import os
import sys
import tkinter as tk
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials, firestore

# تحديد المسار الحالي للتطبيق سواء كود عادي أو exe
if getattr(sys, 'frozen', False):
  base_path = sys._MEIPASS
  current_dir = os.path.dirname(sys.executable)
else:
  current_dir = os.path.dirname(os.path.abspath(__file__))

# البحث عن ملف الـ JSON في نفس مجلد التشغيل
json_files = [f for f in os.listdir(current_dir) if f.endswith('.json')]

if not json_files:
  root = tk.Tk()
  root.withdraw()
  messagebox.showerror(
      'خطأ في الاتصال',
      'لم يتم العثور على ملف مفتاح Firebase (.json) في مجلد البرنامج!',
  )
  sys.exit()

# تهيئة Firebase
if not firebase_admin._apps:
  cred_path = os.path.join(current_dir, json_files[0])
  cred = credentials.Certificate(cred_path)
  firebase_admin.initialize_app(cred)

db = firestore.client()


# دالة إضافة المنتج إلى قاعدة البيانات
def save_product():
  barcode = entry_barcode.get().strip()
  name_ar = entry_name_ar.get().strip()
  name_fr = entry_name_fr.get().strip()
  price = entry_price.get().strip()
  desc_ar = entry_desc_ar.get().strip()
  desc_fr = entry_desc_fr.get().strip()

  if not barcode or not name_ar or not price:
    messagebox.showerror(
        'خطأ',
        'يرجى ملء الحقول الإجبارية (الباركود، الاسم بالعربية، والسعر على الأقل)',
    )
    return

  try:
    price_val = float(price)
  except ValueError:
    messagebox.showerror('خطأ', 'السعر يجب أن يكون رقماً صحيحاً أو عشرياً')
    return

  try:
    db.collection('products').document(barcode).set({
        'barcode': barcode,
        'name_ar': name_ar,
        'name_fr': name_fr,
        'price': price_val,
        'description_ar': desc_ar,
        'description_fr': desc_fr,
    })
    messagebox.showinfo('نجاح', 'تم إضافة المنتج بنجاح إلى النظام! 🔥')

    entry_barcode.delete(0, tk.END)
    entry_name_ar.delete(0, tk.END)
    entry_name_fr.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    entry_desc_ar.delete(0, tk.END)
    entry_desc_fr.delete(0, tk.END)
    entry_barcode.focus()

  except Exception as e:
    messagebox.showerror('خطأ', f'حدث خطأ أثناء الحفظ: {e}')


def on_barcode_enter(event):
  entry_name_ar.focus()


# تصميم الواجهة
root = tk.Tk()
root.title('Rosa Cosmétiques - نظام إدارة المخزون')
root.geometry('450x660')
root.config(bg='#121212')

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
    text='لوحة إضافة المنتجات (جاهز لقارئ الباركود)',
    font=('Segoe UI', 10),
    bg='#121212',
    fg='#b3b3b3',
).pack(pady=2)

card_frame = tk.Frame(
    root, bg='#1e1e1e', highlightbackground='#ff4d4d', highlightthickness=1
)
card_frame.pack(fill='both', expand=True, padx=25, pady=5)


def create_field(parent, label_text):
  tk.Label(
      parent,
      text=label_text,
      font=('Segoe UI', 9, 'bold'),
      bg='#1e1e1e',
      fg='#ffffff',
      anchor='w',
  ).pack(fill='x', padx=20, pady=(10, 2))
  entry = tk.Entry(
      parent,
      font=('Segoe UI', 11),
      bg='#2c2c2c',
      fg='#ffffff',
      insertbackground='white',
      relief='flat',
      highlightbackground='#444444',
      highlightcolor='#ff4d4d',
      highlightthickness=1,
  )
  entry.pack(fill='x', padx=20, ipady=4)
  return entry


entry_barcode = create_field(card_frame, 'الباركود (Barcode) - امسح هنا:')
entry_barcode.bind('<Return>', on_barcode_enter)

entry_name_ar = create_field(card_frame, 'الاسم بالعربية:')
entry_name_fr = create_field(card_frame, 'الاسم بالفرنسية (Nom):')
entry_price = create_field(card_frame, 'السعر (دج):')
entry_desc_ar = create_field(card_frame, 'الوصف بالعربية:')
entry_desc_fr = create_field(card_frame, 'الوصف بالفرنسية (Description FR):')

btn_save = tk.Button(
    root,
    text='حفظ المنتج في النظام 💾',
    font=('Segoe UI', 11, 'bold'),
    bg='#cc0000',
    fg='white',
    activebackground='#ff1a1a',
    activeforeground='white',
    relief='flat',
    cursor='hand2',
    command=save_product,
)
btn_save.pack(pady=20, padx=25, fill='x', ipady=6)

entry_barcode.focus()

root.mainloop()