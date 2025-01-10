from flask import Flask, render_template, request, redirect, url_for
from mysql import connector

app = Flask(__name__)

db = connector.connect(
    host='localhost',
    user='root',
    passwd='',
    database='db_rentalps',
)

if db.is_connected():
    print('Open connection successful')

@app.route('/')
def halaman_awal():
    cur = db.cursor()
    cur.execute("SELECT * FROM rental")
    hasil = cur.fetchall()
    cur.close()
    return render_template('rental.html', hasil=hasil)

@app.route('/tambah/')
def tambah_data():
    return render_template('tambah.html')

@app.route('/proses_tambah/', methods=['POST'])
def proses_tambah():
    nama = request.form['nama']
    playstation = request.form['PlayStation']
    waktu = request.form['waktu']
    cur = db.cursor()
    cur.execute("SELECT * FROM rental WHERE nama = %s", (nama,))
    existing_rental = cur.fetchone()
    cur.close()
    if existing_rental:
        return render_template('tambah.html', error="Nama sudah ada. Mohon gunakan nama yang berbeda.")
    cur = db.cursor()
    cur.execute(
        'INSERT INTO rental (nama, PlayStation, waktu) VALUES (%s, %s, %s)',
        (nama, playstation, waktu)
    )
    db.commit()
    cur.close()
    return redirect(url_for('halaman_awal'))

@app.route('/ubah/<nama>', methods=['GET'])
def ubah_data(nama):
    cur = db.cursor()
    cur.execute('SELECT * FROM rental WHERE nama=%s', (nama,))
    hasil = cur.fetchone()
    cur.close()
    if hasil:
        return render_template('ubah.html', hasil=[hasil])
    else:
        return redirect(url_for('halaman_awal'))

@app.route('/proses_ubah/', methods=['POST'])
def proses_ubah():
    nama_ori = request.form['nama_ori']
    nama = request.form['nama']
    playstation = request.form['PlayStation']
    waktu = request.form['waktu']
    cur = db.cursor()
    sql = "UPDATE rental SET nama=%s, PlayStation=%s, waktu=%s WHERE nama=%s"
    values = (nama, playstation, waktu, nama_ori)
    cur.execute(sql, values)
    db.commit()
    cur.close()
    return redirect(url_for('halaman_awal'))

@app.route('/hapus/<nama>', methods=['GET'])
def hapus_data(nama):
    cur = db.cursor()
    cur.execute('DELETE FROM rental WHERE nama=%s', (nama,))
    db.commit()
    cur.close()
    return redirect(url_for('halaman_awal'))

if __name__ == '__main__':
    app.run(debug=True)
