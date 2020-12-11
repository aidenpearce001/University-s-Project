CREATE DATABASE final;
USE final;

CREATE TABLE restaurant2(
	id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    address VARCHAR(255) NOT NULL,
    openTime VARCHAR(10),
    closeTime VARCHAR(10),
    priceRange VARCHAR(100)
);

CREATE TABLE style(
	id INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_id INT REFERENCES restaurant(id),
    style VARCHAR(20)
);

CREATE TABLE menu(
	id INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_id INT REFERENCES restaurant(id),
    menu VARCHAR(20)
);

CREATE TABLE services(
	id INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_id INT REFERENCES restaurant(id),
    air_condition VARCHAR(10),
    take_away VARCHAR(10),
    wifi VARCHAR(10),
    outside_sit VARCHAR(10),
	car_park VARCHAR(10),
    private_room VARCHAR(10),
    free_park VARCHAR(10),
    smoking VARCHAR(10),
    football VARCHAR(10),
    live_music VARCHAR(10)
);

CREATE TABLE evaluation(
    id INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_id INT REFERENCES restaurant(id),
    quality_point VARCHAR(10), 
    spacial_point VARCHAR(10), 
    price_point VARCHAR(10), 
    location_point VARCHAR(10)
);