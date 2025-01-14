from flask import Flask, request, jsonify

app = Flask(__name__)

# Data Mahasiswa (sebagai database sementara)
data_mahasiswa = []
id_counter = 1


@app.before_request
def log_request():
    print(f"Request: {request.method} {request.path}")

# GET: Mendapatkan semua data mahasiswa
@app.route('/mahasiswa', methods=['GET'])
def get_mahasiswa():
    return jsonify(data_mahasiswa), 200

# POST: Menambahkan data mahasiswa baru
@app.route('/mahasiswa', methods=['POST'])
def tambah_mahasiswa():
    global id_counter
    data = request.get_json()
    if not data.get('nama') or not data.get('nim') or not data.get('jurusan') or not data.get('semester'):
        return jsonify({"error": "Data tidak lengkap"}), 400
    
    nim = 23830900
    mahasiswa = {
        "id": id_counter,
        "nama": data['nama'],
        "nim": nim,
        "jurusan": data['jurusan'],
        "semester": data['semester']
    }
    data_mahasiswa.append(mahasiswa)
    id_counter += 1
    nim += 1
    return jsonify(mahasiswa), 201

# PUT: Memperbarui data mahasiswa berdasarkan ID
@app.route('/mahasiswa/<int:id_mahasiswa>', methods=['PUT'])
def perbarui_mahasiswa(id_mahasiswa):
    data = request.get_json()
    mahasiswa = next((m for m in data_mahasiswa if m['id'] == id_mahasiswa), None)
    if not mahasiswa:
        return jsonify({"error": "Mahasiswa tidak ditemukan"}), 404

    mahasiswa['nama'] = data.get('nama', mahasiswa['nama'])
    mahasiswa['nim'] = data.get('nim', mahasiswa['nim'])
    mahasiswa['jurusan'] = data.get('jurusan', mahasiswa['jurusan'])
    mahasiswa['semester'] = data.get('semester', mahasiswa['semester'])
    return jsonify(mahasiswa), 200

# DELETE: Menghapus data mahasiswa berdasarkan ID
@app.route('/mahasiswa/<int:id_mahasiswa>', methods=['DELETE'])
def hapus_mahasiswa(id_mahasiswa):
    global data_mahasiswa
    mahasiswa = next((m for m in data_mahasiswa if m['id'] == id_mahasiswa), None)
    if not mahasiswa:
        return jsonify({"error": "Mahasiswa tidak ditemukan"}), 404

    data_mahasiswa = [m for m in data_mahasiswa if m['id'] != id_mahasiswa]
    return jsonify({"message": "Mahasiswa berhasil dihapus"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=2004)
