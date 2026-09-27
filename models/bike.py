from app import db


class Bike(db.Model):

    __tablename__ = "bikes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    image_url = db.Column(
        db.String(500)
    )

    cc = db.Column(
        db.String(50)
    )

    bike_type = db.Column(
        db.String(50)
    )

    description = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def __repr__(self):

        return (
            f"<Bike {self.name}>"
        )