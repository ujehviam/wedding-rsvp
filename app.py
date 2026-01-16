from flask import (
    Flask, render_template, request,
    redirect, url_for, flash, send_file
)
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import io
import csv

# -------------------- LOAD ENV --------------------

load_dotenv()

# -------------------- APP CONFIG --------------------

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# PostgreSQL connection string
# Example:
# postgresql://user:password@localhost:5432/wedding_rsvp
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# -------------------- DB INIT --------------------

db = SQLAlchemy(app)

# -------------------- MODEL --------------------

class Guest(db.Model):
    __tablename__ = "guest"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Guest {self.email}>"

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

        # Check for duplicate email
        if Guest.query.filter_by(email=email).first():
            flash(
                "You have already indicated your attendance. Thank you 💍",
                "info"
            )
            return redirect(url_for("index"))

        guest = Guest(
            name=name,
            email=email,
            category=category
        )

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
    app.run(debug=True)

