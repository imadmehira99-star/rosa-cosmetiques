from flask import Flask, render_template, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)
app.json.ensure_ascii = False

# الربط باستخدام اسم المفتاح الحقيقي المكتمل
cred = credentials.Certificate("cosmeticstore-98acc-firebase-adminsdk-fbsvc-6465d8febd.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/product/<barcode>')
def get_product(barcode):
    try:
        doc_ref = db.collection('products').document(barcode)
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            return jsonify({
                "success": True,
                "name_ar": data.get("name_ar", "-"),
                "name_fr": data.get("name_fr", "-"),
                "price": str(data.get("price", "-")),
                "description": data.get("description", "-")
            })
        return jsonify({"success": False, "message": "المنتج غير موجود في قاعدة البيانات"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)