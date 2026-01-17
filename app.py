from flask import (
    Flask, render_template, request,
    redirect, url_for, flash, send_file
)
import io
import csv
import os

from db import db, init_db
from models import Guest

# -------------------- APP SETUP --------------------

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-only-secret")

# -------------------- DB INIT --------------------

init_db(app)

# -------------------- ROUTES --------------------

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        category = request.form.get("category", "").strip()

        if not name or not email or not category:
            flash("All fields are required", "error")
            return redirect(url_for("index"))

        if Guest.query.filter_by(email=email).first():
            flash(
                "You have already indicated your attendance. Thank you 💍",
                "info"
            )
            return redirect(url_for("index"))

        guest = Guest(name=name, email=email, category=category)
        db.session.add(guest)
        db.session.commit()

        return redirect(url_for("success"))

    return render_template("index.html")

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/download")
def download():
    guests = Guest.query.order_by(Guest.id.asc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Name", "Email", "Category"])

    for guest in guests:
        writer.writerow([guest.name, guest.email, guest.category])

    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode("utf-8")),
        mimetype="text/csv",
        as_attachment=True,
        download_name="wedding_guests.csv"
    )

# -------------------- ENTRY POINT --------------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", debug=True)
