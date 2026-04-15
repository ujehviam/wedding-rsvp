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

        existing_guest = Guest.query.filter_by(email=email).first()

        if existing_guest:
            return redirect(url_for(
                "success",
                name=existing_guest.name,
                category=existing_guest.category
            ))

        guest = Guest(name=name, email=email, category=category)
        db.session.add(guest)
        db.session.commit()

        return redirect(url_for("success", name=name, category=category))

    return render_template("index.html")


@app.route("/success")
def success():
    name = request.args.get("name")
    category = request.args.get("category")
    return render_template("success.html", name=name, category=category)


# -------------------- ACCESS CARD --------------------

@app.route("/card/<name>")
def generate_card(name):
    try:
        category = request.args.get("category", "")

        name = name.upper()
        category = category.upper()

        # Load image
        img_path = os.path.join("static", "images", "access-card.jpg")
        image = Image.open(img_path)

        draw = ImageDraw.Draw(image)

        # Load font
        font_path = os.path.join("static", "fonts", "Zikketica.ttf")

        try:
            name_font = ImageFont.truetype(font_path, 30)
            category_font = ImageFont.truetype(font_path, 20)
        except:
            name_font = ImageFont.load_default()
            category_font = ImageFont.load_default()

        image_width, image_height = image.size

        # -------- NAME --------
        name_bbox = draw.textbbox((0, 0), name, font=name_font)
        name_width = name_bbox[2] - name_bbox[0]
        name_height = name_bbox[3] - name_bbox[1]

        x_name = (image_width - name_width) / 2
        y_name = int(image_height * 0.68)

        draw.text((x_name, y_name), name, fill="#3b2f2f", font=name_font)

        # -------- CATEGORY (BELOW NAME) --------
        cat_bbox = draw.textbbox((0, 0), category, font=category_font)
        cat_width = cat_bbox[2] - cat_bbox[0]
        cat_height = cat_bbox[3] - cat_bbox[1]

        x_cat = (image_width - cat_width) / 2
        y_cat = y_name + name_height + 10  # spacing below name

        draw.text((x_cat, y_cat), category, fill="#3b2f2f", font=category_font)

        # Save image
        img_io = io.BytesIO()
        image.save(img_io, "PNG")
        img_io.seek(0)

        return send_file(img_io, mimetype="image/png")

    except Exception as e:
        print("ERROR generating card:", e)
        return f"Error generating card: {e}", 500


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