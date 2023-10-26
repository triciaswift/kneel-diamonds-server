CREATE TABLE `Metals`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `metal` NVARCHAR(160) NOT NULL,
    `price` NUMERIC(6,2) NOT NULL
);

CREATE TABLE `Styles`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `style` NVARCHAR(160) NOT NULL,
    `price` NUMERIC(6,2) NOT NULL
);

CREATE TABLE `Sizes`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `carets` NUMERIC(3,2) NOT NULL,
    `price` NUMERIC(6,2) NOT NULL
);

CREATE TABLE `Orders` (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  metalId INTEGER NOT NULL,
  styleId INTEGER NOT NULL,
  sizeId INTEGER NOT NULL,
  timestamp DATETIME DEFAULT CURRENT_DATE,
  FOREIGN KEY (metalId) REFERENCES `Metal`(id),
  FOREIGN KEY (styleId) REFERENCES `Styles`(id),
  FOREIGN KEY (sizeId) REFERENCES `Sizes`(id)
);

INSERT INTO `Metals` (id, metal, price) VALUES
(null, 'Sterling Silver', 12.42),
(null, '14K Gold', 736.4),
(null, '24K Gold', 1258.9),
(null, 'Platinum', 795.45),
(null,'Palladium', 1241);

INSERT INTO `Styles` (id, style, price) VALUES
(null, 'Classic', 500),
(null, 'Modern', 710),
(null, 'Vintage', 965);

INSERT INTO `Sizes` (id, carets, price) VALUES
(null, 0.5, 405),
(null, 0.75, 782),
(null, 1, 1470),
(null, 1.5, 1997),
(null, 2, 3638);


INSERT INTO `Orders` (id, metalId, styleId, sizeId) VALUES
(null, 1, 3, 3),
(null, 3, 1, 2),
(null, 1, 1, 1),
(null, 1, 1, 2),
(null, 1, 1, 3),
(null, 1, 1, 3),
(null, 2, 2, 1),
(null, 4, 3, 1),
(null, 3, 2, 2),
(null, 1, 4, 2),
(null, 1, 3, 2),
(null, 1, 1, 2),
(null, 1, 3, 1),
(null, 5, 2, 1),
(null, 1, 4, 1);



SELECT 
    s.id, 
    s.carets, 
    s.price 
FROM Sizes s;