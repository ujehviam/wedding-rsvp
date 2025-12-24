from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import csv
import io

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model
class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Home page (RSVP form)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")

        if name:
            guest = Guest(name=name)
            db.session.add(guest)
            db.session.commit()
            return redirect(url_for("success"))

    return render_template("index.html")

@app.route("/success")
def success():
    return render_template("success.html")

# Download guest list as CSV
@app.route("/download")
def download():
    guests = Guest.query.all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Name"])

    for guest in guests:
        writer.writerow([guest.id, guest.name])

    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="guest_list.csv"
    )

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)