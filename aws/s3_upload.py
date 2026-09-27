import uuid

import boto3

from flask import current_app


ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp"
}


def allowed_file(filename):

    if "." not in filename:
        return False

    extension = filename.rsplit(
        ".",
        1
    )[1].lower()

    return extension in ALLOWED_EXTENSIONS


def upload_image(file):

    if not file or not file.filename:

        return None

    if not allowed_file(file.filename):

        return None

    extension = file.filename.rsplit(
        ".",
        1
    )[1].lower()

    filename = (
        f"bikes/{uuid.uuid4().hex}.{extension}"
    )

    try:

        s3 = boto3.client(
            "s3",
            region_name=current_app.config[
                "AWS_REGION"
            ]
        )

        s3.upload_fileobj(
            file,
            current_app.config["S3_BUCKET"],
            filename,
            ExtraArgs={
                "ContentType": file.content_type
            }
        )

        return (
            f"https://"
            f"{current_app.config['S3_BUCKET']}"
            f".s3."
            f"{current_app.config['AWS_REGION']}"
            f".amazonaws.com/"
            f"{filename}"
        )

    except Exception as e:

        print("S3 Upload Error:", e)

        return None