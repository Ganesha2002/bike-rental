from app import db


class Booking(db.Model):

    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    bike_id = db.Column(
        db.Integer,
        db.ForeignKey("bikes.id"),
        nullable=False
    )

    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    total_price = db.Column(db.Float)

    status = db.Column(
        db.String(50),
        default="Pending"
    )

    user = db.relationship(
        "User",
        backref=db.backref("bookings", lazy=True)
    )

    bike = db.relationship(
        "Bike",
        backref=db.backref("bookings", lazy=True)
    )