from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import login_required, current_user

from app import db
from models.bike import Bike
from models.booking import Booking


booking_bp = Blueprint("booking", __name__)


@booking_bp.route("/book/<int:bike_id>", methods=["GET", "POST"])
@login_required
def book_bike(bike_id):

    bike = Bike.query.get_or_404(bike_id)

    if request.method == "POST":

        start_date_text = request.form.get("start_date")
        end_date_text = request.form.get("end_date")

        if not start_date_text or not end_date_text:

            flash("Please select both dates.", "danger")

            return redirect(
                url_for("booking.book_bike", bike_id=bike.id)
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

            flash("Invalid date format.", "danger")

            return redirect(
                url_for("booking.book_bike", bike_id=bike.id)
            )

        if end_date < start_date:

            flash(
                "End date cannot be before start date.",
                "danger"
            )

            return redirect(
                url_for("booking.book_bike", bike_id=bike.id)
            )

        days = (end_date - start_date).days + 1

        total_price = days * bike.price

        booking = Booking(
            user_id=current_user.id,
            bike_id=bike.id,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price,
            status="Pending"
        )

        db.session.add(booking)
        db.session.commit()

        flash(
            "Bike booking submitted successfully.",
            "success"
        )

        return redirect(
            url_for("booking.my_bookings")
        )

    return render_template(
        "booking.html",
        bike=bike
    )


@booking_bp.route("/my-bookings")
@login_required
def my_bookings():

    bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Booking.id.desc()
    ).all()

    return render_template(
        "my_bookings.html",
        bookings=bookings
    )


@booking_bp.route("/cancel/<int:booking_id>", methods=["POST"])
@login_required
def cancel_booking(booking_id):

    booking = Booking.query.get_or_404(booking_id)

    if booking.user_id != current_user.id:

        flash(
            "You are not authorized to cancel this booking.",
            "danger"
        )

        return redirect(
            url_for("booking.my_bookings")
        )

    if booking.status in ["Completed", "Cancelled"]:

        flash(
            "This booking cannot be cancelled.",
            "warning"
        )

        return redirect(
            url_for("booking.my_bookings")
        )

    booking.status = "Cancelled"

    db.session.commit()

    flash(
        "Booking cancelled successfully.",
        "success"
    )

    return redirect(
        url_for("booking.my_bookings")
    )