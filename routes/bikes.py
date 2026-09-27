from flask import Blueprint, render_template, request
from models.bike import Bike

bikes_bp = Blueprint("bikes", __name__)


@bikes_bp.route("/")
def home():

    bikes = Bike.query.order_by(Bike.id.desc()).all()

    return render_template(
        "index.html",
        bikes=bikes
    )


@bikes_bp.route("/bikes")
def bikes():

    search = request.args.get("search", "").strip()

    if search:

        bikes = Bike.query.filter(
            Bike.name.ilike(f"%{search}%")
        ).order_by(Bike.id.desc()).all()

    else:

        bikes = Bike.query.order_by(Bike.id.desc()).all()

    return render_template(
        "bikes.html",
        bikes=bikes,
        search=search
    )


@bikes_bp.route("/bike/<int:bike_id>")
def bike_details(bike_id):

    bike = Bike.query.get_or_404(bike_id)

    return render_template(
        "bike_details.html",
        bike=bike
    )