CREATE TABLE Tags(
    id int NOT NULL AUTO_INCREMENT,
    tag1 varchar(255),
    tag2 varchar(255),
    pet_id int,
    PRIMARY KEY (id),
    FOREIGN KEY (pet_id) REFERENCES Pets(id)
);

CREATE TABLE Photos(
    id int NOT NULL AUTO_INCREMENT,
    photo1 varchar(255),
    photo2 varchar(255),
    pet_id int,
    PRIMARY KEY (id),
    FOREIGN KEY (pet_id) REFERENCES Pets(id)
);

CREATE TABLE Pets (
    id int NOT NULL AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    status varchar(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE Users(
    id int NOT NULL AUTO_INCREMENT,
    username varchar(255) NOT NULL UNIQUE,
    firstName varchar(255) NOT NULL,
    lastName varchar(255) NOT NULL,
    email varchar(255) NOT NULL,
    password varchar(255) NOT NULL,
    phone int,
    PRIMARY KEY (id)
);
CREATE TABLE Orders(
    id int NOT NULL AUTO_INCREMENT,
    pet_id int,
    quantity int,
    shipDate date,
    complete varchar(255),
    status varchar(255),
    user_id int,
    PRIMARY KEY (id)
);
