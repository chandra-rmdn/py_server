from flask import Flask, request, jsonify

app = Flask(__name__)

data_mahasiswa = []
id_counter = 1
nim = 830900

@app.before_request
def log_request():
    print(f"Request: {request.method} {request.path}")

@app.route('/', methods=['GET'])
def get_mahasiswa():
    return jsonify(data_mahasiswa), 200

@app.route('/', methods=['POST'])
def tambah_mahasiswa():
    global id_counter
    global nim
    data = request.get_json()
    if not data.get('nama') or not data.get('jurusan') or not data.get('semester'):
        return jsonify({}), 400
    
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

@app.route('/<int:id_mahasiswa>', methods=['PUT'])
def perbarui_mahasiswa(id_mahasiswa):
    data = request.get_json()
    mahasiswa = next((m for m in data_mahasiswa if m['id'] == id_mahasiswa), None)
    if not mahasiswa:
        return jsonify({}), 404

    mahasiswa['nama'] = data.get('nama', mahasiswa['nama'])
    mahasiswa['jurusan'] = data.get('jurusan', mahasiswa['jurusan'])
    mahasiswa['semester'] = data.get('semester', mahasiswa['semester'])
    return jsonify(mahasiswa), 200

@app.route('/<int:id_mahasiswa>', methods=['DELETE'])
def hapus_mahasiswa(id_mahasiswa):
    global data_mahasiswa
    mahasiswa = next((m for m in data_mahasiswa if m['id'] == id_mahasiswa), None)
    if not mahasiswa:
        return jsonify({}), 404

    data_mahasiswa = [m for m in data_mahasiswa if m['id'] != id_mahasiswa]
    return jsonify({}), 200

if __name__ == '__main__':
    app.run(debug=True, port=2004)
