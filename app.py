from flask import (
    Flask, render_template, request,
    redirect, url_for, flash, send_file
)
import io
import csv
import os

from PIL import Image, ImageDraw, ImageFont

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

        # Redirect with name
        return redirect(url_for("success", name=name))

    return render_template("index.html")


@app.route("/success")
def success():
    name = request.args.get("name")
    return render_template("success.html", name=name)


# -------------------- ACCESS CARD GENERATION --------------------

@app.route("/card/<name>")
def generate_card(name):
    name = name.upper()

    # Load base image (your access card)
    img_path = os.path.join("static", "images", "access-card.jpg")
    image = Image.open(img_path)

    draw = ImageDraw.Draw(image)

    # Load font (make sure this file exists)
    font_path = os.path.join("static", "fonts", "arial.ttf")
    font = ImageFont.truetype(font_path, 50)

    # Get image size
    image_width, image_height = image.size

    # Calculate text width for centering
    bbox = draw.textbbox((0, 0), name, font=font)
    text_width = bbox[2] - bbox[0]

    # Center horizontally, adjust vertical position manually
    x = (image_width - text_width) / 2
    y = int(image_height * 0.45)  # adjust this to fit the red bar

    draw.text((x, y), name, fill="white", font=font)

    # Save to memory
    img_io = io.BytesIO()
    image.save(img_io, "PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png")


# -------------------- DOWNLOAD CSV --------------------

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