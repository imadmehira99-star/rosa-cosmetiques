import os
import json
from flask import Flask, render_template, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# تهيئة الاتصال بـ Firebase بشكل مرن
db = None
try:
    if not firebase_admin._apps:
        # 1. البحث عن مفتاح Firebase داخل متغيرات بيئة Render
        env_creds = os.environ.get('FIREBASE_CREDENTIALS')
        if env_creds:
            cred_dict = json.loads(env_creds)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            print("✅ تم الاتصال بـ Firebase عبر Render Environment Variable")
        else:
            # 2. البحث عن ملف JSON محلي على الجهاز
            json_files = [f for f in os.listdir('.') if f.endswith('.json') and any(k in f.lower() for k in ['firebase', 'admin', 'cosmetic'])]
            if json_files:
                cred = credentials.Certificate(json_files[0])
                firebase_admin.initialize_app(cred)
                print(f"✅ تم الاتصال بـ Firebase عبر الملف المحلي: {json_files[0]}")
            else:
                print("⚠️ لم يتم العثور على مفتاح Firebase!")

    if firebase_admin._apps:
        db = firestore.client()
except Exception as e:
    print(f"❌ خطأ في تهيئة Firebase: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_product', methods=['GET'])
def get_product():
    barcode = request.args.get('barcode', '').strip()
    if not barcode:
        return jsonify({'success': False, 'message': 'الباركود فارغ'}), 400

    if not db:
        return jsonify({'success': False, 'message': 'السيرفر غير متصل بـ Firebase'}), 500

    try:
        # البحث بـ Document ID
        doc = db.collection('products').document(barcode).get()
        if doc.exists:
            return jsonify({'success': True, 'product': doc.to_dict()})

        # البحث داخل حقل barcode
        query = db.collection('products').where('barcode', '==', barcode).limit(1).stream()
        for p in query:
            return jsonify({'success': True, 'product': p.to_dict()})

        return jsonify({'success': False, 'message': 'المنتج غير موجود'})

    except Exception as e:
        print(f"Firestore Error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)