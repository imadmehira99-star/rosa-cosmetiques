import os
import sys
import tkinter as tk
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials, firestore

# تحديد مسار العمل
if getattr(sys, 'frozen', False):
  current_dir = os.path.dirname(sys.executable)
else:
  current_dir = os.path.dirname(os.path.abspath(__file__))

# البحث عن ملف الـ JSON الخاص بـ Firebase
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


# دالة حفظ المنتج
def save_product():
  barcode = entry_barcode.get().strip()
  name_ar = entry_name_ar.get().strip()
  name_fr = entry_name_fr.get().strip()
  price = entry_price.get().strip()
  desc_ar = entry_desc_ar.get().strip()
  desc_fr = entry_desc_fr.get().strip()

  if not barcode or not name_ar or not price:
    messagebox.showerror(
        'خطأ', 'يرجى ملء الحقول الإجبارية: الباركود، الاسم بالعربية، والسعر'
    )
    return

  try:
    price_val = float(price)
  except ValueError:
    messagebox.showerror('خطأ', 'السعر يجب أن يكون رقماً صحيحاً أو عشرياً')
    return

  try:
    # استخدام الباركود كمُعرّف للمستند
    db.collection('products').document(barcode).set({
        'barcode': barcode,
        'name_ar': name_ar,
        'name_fr': name_fr,
        'price': price_val,
        'description_ar': desc_ar,
        'description_fr': desc_fr,
    })
    messagebox.showinfo('نجاح', 'تم إضافة المنتج بنجاح إلى Firebase! 🔥')

    # تفريغ الحقول
    entry_barcode.delete(0, tk.END)
    entry_name_ar.delete(0, tk.END)
    entry_name_fr.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    entry_desc_ar.delete(0, tk.END)
    entry_desc_fr.delete(0, tk.END)
    entry_barcode.focus()

  except Exception as e:
    messagebox.showerror('خطأ', f'حدث خطأ أثناء الحفظ: {e}')


# إنشاء النافذة
root = tk.Tk()
root.title('Rosa Cosmétiques - إضافة منتج جديد')
root.geometry('420x560')
root.config(bg='#121212')

# العناوين
tk.Label(
    root,
    text='🌹 ROSA COSMÉTIQUES 🌹',
    font=('Segoe UI', 14, 'bold'),
    bg='#121212',
    fg='#ff4d4d',
).pack(pady=10)
tk.Label(
    root,
    text='إضافة منتج جديد للمخزون',
    font=('Segoe UI', 10),
    bg='#121212',
    fg='#b3b3b3',
).pack()

form_frame = tk.Frame(root, bg='#1e1e1e', padx=15, pady=15)
form_frame.pack(fill='both', expand=True, padx=20, pady=15)


def add_field(parent, label_text):
  tk.Label(
      parent,
      text=label_text,
      font=('Segoe UI', 9, 'bold'),
      bg='#1e1e1e',
      fg='#ffffff',
      anchor='w',
  ).pack(fill='x', pady=(4, 2))
  entry = tk.Entry(
      parent,
      font=('Segoe UI', 10),
      bg='#2c2c2c',
      fg='#ffffff',
      insertbackground='white',
      relief='flat',
  )
  entry.pack(fill='x', ipady=3)
  return entry


entry_barcode = add_field(form_frame, 'الباركود (Barcode) *')
entry_name_ar = add_field(form_frame, 'الاسم (بالعربية) *')
entry_name_fr = add_field(form_frame, 'الاسم (بالفرنسية)')
entry_price = add_field(form_frame, 'السعر (دج) *')
entry_desc_ar = add_field(form_frame, 'الوصف (بالعربية)')
entry_desc_fr = add_field(form_frame, 'الوصف (بالفرنسية)')

btn_save = tk.Button(
    form_frame,
    text='حفظ المنتج 💾',
    font=('Segoe UI', 11, 'bold'),
    bg='#ff4d4d',
    fg='#ffffff',
    activebackground='#ff3333',
    activeforeground='#ffffff',
    relief='flat',
    cursor='hand2',
    command=save_product,
)
btn_save.pack(fill='x', pady=15, ipady=5)

entry_barcode.focus()
root.mainloop()