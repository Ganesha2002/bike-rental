import os


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "change-this-secret-key"
    )

    # ==========================
    # MySQL RDS Configuration
    # ==========================

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ==========================
    # AWS S3 Configuration
    # ==========================

    AWS_REGION = os.getenv(
        "AWS_REGION",
        "ap-south-1"
    )

    S3_BUCKET = os.getenv(
        "S3_BUCKET"
    )

    MAX_CONTENT_LENGTH = (
        10 * 1024 * 1024
    )  # 10MB Upload Limit