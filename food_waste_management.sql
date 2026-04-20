CREATE DATABASE food_waste_management;
USE food_waste_management;
CREATE TABLE providers (
    Provider_ID INT PRIMARY KEY,
    Name VARCHAR(255),
    Type VARCHAR(100),
    Address VARCHAR(255),
    City VARCHAR(100),
    Contact VARCHAR(50)
);

CREATE TABLE receivers (
    Receiver_ID INT PRIMARY KEY,
    Name VARCHAR(255),
    Type VARCHAR(100),
    City VARCHAR(100),
    Contact VARCHAR(50)
);

CREATE TABLE food_listings (
    Food_ID INT PRIMARY KEY,
    Food_Name VARCHAR(100),
    Quantity INT,
    Expiry_Date DATE,
    Provider_ID INT,
    Provider_Type VARCHAR(100),
    Location VARCHAR(100),
    Food_Type VARCHAR(50),
    Meal_Type VARCHAR(50)
);

CREATE TABLE claims (
    Claim_ID INT PRIMARY KEY,
    Food_ID INT,
    Receiver_ID INT,
    Status VARCHAR(50),
    Timestamp DATETIME
);


CREATE TABLE providers (
Provider_ID INT PRIMARY KEY,
Name VARCHAR(255),
Type VARCHAR(100),
City VARCHAR(100),
Contact VARCHAR(50)
);

SELECT City, COUNT(*) AS total_providers
FROM providers
GROUP BY City
ORDER BY total_providers DESC;

SELECT City, COUNT(*) AS total_receivers
FROM receivers
GROUP BY City
ORDER BY total_receivers DESC;

SELECT Type, COUNT(*) AS provider_count
FROM providers
GROUP BY Type
ORDER BY provider_count DESC;

SELECT Name, City, Contact
FROM providers
WHERE City = 'New Jessica';

SELECT SUM(Quantity) AS total_food_quantity
FROM food_listings;

SELECT Location, COUNT(*) AS food_count
FROM food_listings
GROUP BY Location
ORDER BY food_count DESC;

SELECT Food_Type, COUNT(*) AS total
FROM food_listings
GROUP BY Food_Type
ORDER BY total DESC;

SELECT Food_ID, COUNT(*) AS total_claims
FROM claims
GROUP BY Food_ID
ORDER BY total_claims DESC;

SELECT f.Provider_ID, COUNT(*) AS successful_claims
FROM claims c
JOIN food_listings f ON c.Food_ID = f.Food_ID
WHERE c.Status = 'Completed'
GROUP BY f.Provider_ID
ORDER BY successful_claims DESC;

SELECT Status,
COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims) AS percentage
FROM claims
GROUP BY Status;

SELECT Receiver_ID, AVG(f.Quantity) AS avg_food_claimed
FROM claims c
JOIN food_listings f ON c.Food_ID = f.Food_ID
GROUP BY Receiver_ID
ORDER BY avg_food_claimed DESC;

SELECT f.Meal_Type, COUNT(*) AS total_claims
FROM claims c
JOIN food_listings f ON c.Food_ID = f.Food_ID
GROUP BY f.Meal_Type
ORDER BY total_claims DESC;

SELECT Provider_ID, SUM(Quantity) AS total_donated_food
FROM food_listings
GROUP BY Provider_ID
ORDER BY total_donated_food DESC;

SELECT Food_Name, Expiry_Date, Quantity
FROM food_listings
WHERE Expiry_Date <= CURDATE() + INTERVAL 2 DAY
ORDER BY Expiry_Date;

SELECT Receiver_ID, COUNT(*) AS total_claims
FROM claims
GROUP BY Receiver_ID
ORDER BY total_claims DESC;