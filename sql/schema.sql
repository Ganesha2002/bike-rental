CREATE DATABASE IF NOT EXISTS bike_rental;

USE bike_rental;


-- =========================================
-- USERS TABLE
-- =========================================

CREATE TABLE IF NOT EXISTS users (

    id INT AUTO_INCREMENT PRIMARY KEY,

    full_name VARCHAR(100) NOT NULL,

    email VARCHAR(120) NOT NULL UNIQUE,

    password VARCHAR(255) NOT NULL,

    role VARCHAR(20) NOT NULL DEFAULT 'user',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);


-- =========================================
-- BIKES TABLE
-- =========================================

CREATE TABLE IF NOT EXISTS bikes (

    id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(100) NOT NULL,

    price DECIMAL(10,2) NOT NULL,

    image_url VARCHAR(500),

    cc VARCHAR(50),

    bike_type VARCHAR(50),

    description TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);


-- =========================================
-- BOOKINGS TABLE
-- =========================================

CREATE TABLE IF NOT EXISTS bookings (

    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    bike_id INT NOT NULL,

    start_date DATE NOT NULL,

    end_date DATE NOT NULL,

    total_price DECIMAL(10,2) NOT NULL,

    status VARCHAR(30) NOT NULL DEFAULT 'Pending',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_booking_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_booking_bike
        FOREIGN KEY (bike_id)
        REFERENCES bikes(id)
        ON DELETE CASCADE

);


-- =========================================
-- SAMPLE BIKES
-- =========================================

INSERT INTO bikes
(name, price, image_url, cc, bike_type, description)
VALUES

(
    'Royal Enfield Classic 350',
    1200.00,
    NULL,
    '349 CC',
    'Manual',
    'Comfortable motorcycle suitable for city and highway rides.'
),

(
    'Yamaha MT-15',
    900.00,
    NULL,
    '155 CC',
    'Manual',
    'Sporty motorcycle with excellent handling.'
),

(
    'Honda Activa 6G',
    500.00,
    NULL,
    '109.5 CC',
    'Auto',
    'Easy and economical scooter for city travel.'
),

(
    'KTM Duke 200',
    1000.00,
    NULL,
    '199.5 CC',
    'Manual',
    'Performance-oriented street motorcycle.'
);