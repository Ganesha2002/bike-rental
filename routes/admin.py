from datetime import datetime
from functools import wraps

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from app import db

from models.user import User
from models.bike import Bike
from models.booking import Booking

from aws.s3_upload import upload_image


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


def admin_required(view_function):

    @wraps(view_function)
    @login_required
    def wrapped_view(*args, **kwargs):

        if current_user.role != "admin":

            flash(
                "Access denied. Admin only.",
                "danger"
            )

            return redirect(
                url_for("bikes.home")
            )

        return view_function(*args, **kwargs)

    return wrapped_view


# --------------------------------------------------
# ADMIN DASHBOARD
# --------------------------------------------------

@admin_bp.route("/")
@admin_required
def dashboard():

    total_users = User.query.filter_by(
        role="user"
    ).count()

    total_bookings = Booking.query.count()

    total_revenue = db.session.query(
        db.func.coalesce(
            db.func.sum(Booking.total_price),
            0
        )
    ).scalar()

    bookings = Booking.query.order_by(
        Booking.id.desc()
    ).all()

    total_bikes = Bike.query.count()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_bookings=total_bookings,
        total_revenue=total_revenue,
        total_bikes=total_bikes,
        bookings=bookings
    )


# --------------------------------------------------
# BIKE MANAGEMENT
# --------------------------------------------------

@admin_bp.route("/bikes")
@admin_required
def manage_bikes():

    bikes = Bike.query.order_by(
        Bike.id.desc()
    ).all()

    return render_template(
        "admin_bikes.html",
        bikes=bikes
    )


# --------------------------------------------------
# ADD BIKE
# --------------------------------------------------

@admin_bp.route("/bikes/add", methods=["POST"])
@admin_required
def add_bike():

    name = request.form.get(
        "name",
        ""
    ).strip()

    price_text = request.form.get(
        "price",
        "0"
    )

    cc = request.form.get(
        "cc",
        ""
    ).strip()

    bike_type = request.form.get(
        "type",
        ""
    ).strip()

    description = request.form.get(
        "description",
        ""
    ).strip()

    image = request.files.get("image")

    if not name or not price_text or not cc or not bike_type:

        flash(
            "Please fill all required fields.",
            "danger"
        )

        return redirect(
            url_for("admin.manage_bikes")
        )

    try:

        price = float(price_text)

        if price <= 0:
            raise ValueError

    except ValueError:

        flash(
            "Please enter a valid price.",
            "danger"
        )

        return redirect(
            url_for("admin.manage_bikes")
        )

    image_url = None

    if image and image.filename:

        image_url = upload_image(image)

        if not image_url:

            flash(
                "Image upload failed.",
                "danger"
            )

            return redirect(
                url_for("admin.manage_bikes")
            )

    bike = Bike(
        name=name,
        price=price,
        image_url=image_url,
        cc=cc,
        bike_type=bike_type,
        description=description
    )

    db.session.add(bike)
    db.session.commit()

    flash(
        "Bike added successfully.",
        "success"
    )

    return redirect(
        url_for("admin.manage_bikes")
    )


# --------------------------------------------------
# EDIT BIKE
# --------------------------------------------------

@admin_bp.route(
    "/bikes/edit/<int:bike_id>",
    methods=["POST"]
)
@admin_required
def edit_bike(bike_id):

    bike = Bike.query.get_or_404(bike_id)

    bike.name = request.form.get(
        "name",
        bike.name
    ).strip()

    bike.cc = request.form.get(
        "cc",
        bike.cc
    ).strip()

    bike.bike_type = request.form.get(
        "type",
        bike.bike_type
    ).strip()

    bike.description = request.form.get(
        "description",
        bike.description
    ).strip()

    price_text = request.form.get(
        "price",
        str(bike.price)
    )

    try:

        price = float(price_text)

        if price <= 0:
            raise ValueError

        bike.price = price

    except ValueError:

        flash(
            "Invalid price.",
            "danger"
        )

        return redirect(
            url_for("admin.manage_bikes")
        )

    image = request.files.get("image")

    if image and image.filename:

        image_url = upload_image(image)

        if image_url:

            bike.image_url = image_url

        else:

            flash(
                "New image upload failed.",
                "danger"
            )

            return redirect(
                url_for("admin.manage_bikes")
            )

    db.session.commit()

    flash(
        "Bike updated successfully.",
        "success"
    )

    return redirect(
        url_for("admin.manage_bikes")
    )


# --------------------------------------------------
# DELETE BIKE
# --------------------------------------------------

@admin_bp.route(
    "/bikes/delete/<int:bike_id>",
    methods=["POST"]
)
@admin_required
def delete_bike(bike_id):

    bike = Bike.query.get_or_404(bike_id)

    existing_booking = Booking.query.filter_by(
        bike_id=bike.id
    ).filter(
        Booking.status.in_(
            ["Pending", "Confirmed"]
        )
    ).first()

    if existing_booking:

        flash(
            "This bike has active bookings and cannot be deleted.",
            "warning"
        )

        return redirect(
            url_for("admin.manage_bikes")
        )

    db.session.delete(bike)
    db.session.commit()

    flash(
        "Bike deleted successfully.",
        "success"
    )

    return redirect(
        url_for("admin.manage_bikes")
    )


# --------------------------------------------------
# BOOKING MANAGEMENT
# --------------------------------------------------

@admin_bp.route("/bookings")
@admin_required
def manage_bookings():

    bookings = Booking.query.order_by(
        Booking.id.desc()
    ).all()

    return render_template(
        "admin_bookings.html",
        bookings=bookings
    )


# --------------------------------------------------
# UPDATE BOOKING
# --------------------------------------------------

@admin_bp.route(
    "/bookings/update/<int:booking_id>",
    methods=["POST"]
)
@admin_required
def update_booking(booking_id):

    booking = Booking.query.get_or_404(
        booking_id
    )

    status = request.form.get(
        "status",
        booking.status
    )

    start_date_text = request.form.get(
        "start_date"
    )

    end_date_text = request.form.get(
        "end_date"
    )

    if not start_date_text or not end_date_text:

        flash(
            "Start date and end date are required.",
            "danger"
        )

        return redirect(
            url_for("admin.manage_bookings")
        )

    try:

        start_date = datetime.strptime(
            start_date_text,
            "%Y-%m-%d"
        ).date()

        end_date = datetime.strptime(
            end_date_text,
            "%Y-%m-%d"
        ).date()

    except ValueError:

        flash(
            "Invalid date.",
            "danger"
        )

        return redirect(
            url_for("admin.manage_bookings")
        )

    if end_date < start_date:

        flash(
            "End date cannot be before start date.",
            "danger"
        )

        return redirect(
            url_for("admin.manage_bookings")
        )

    bike = Bike.query.get(
        booking.bike_id
    )

    if bike:

        days = (
            end_date - start_date
        ).days + 1

        booking.total_price = (
            days * bike.price
        )

    booking.start_date = start_date

    booking.end_date = end_date

    booking.status = status

    db.session.commit()

    flash(
        "Booking updated successfully.",
        "success"
    )

    return redirect(
        url_for("admin.manage_bookings")
    )