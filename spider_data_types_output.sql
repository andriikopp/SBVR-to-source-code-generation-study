CREATE TABLE `product` (
	`product_id` int NOT NULL AUTO_INCREMENT,
	`title` varchar(255) NOT NULL,
	`description` varchar(255) NULL,
	`image` varchar(255) NULL,
	`price` varchar(255) NOT NULL,
	`amount` real NOT NULL,
	`votes` int NULL,
	`rating` varchar(255) NULL,
	PRIMARY KEY (`product_id`)
);

CREATE TABLE `category` (
	`category_id` int NOT NULL AUTO_INCREMENT,
	`title` varchar(255) NOT NULL,
	`description` varchar(255) NULL,
	`image` varchar(255) NULL,
	PRIMARY KEY (`category_id`)
);

CREATE TABLE `brand` (
	`brand_id` int NOT NULL AUTO_INCREMENT,
	`title` varchar(255) NOT NULL,
	`image` varchar(255) NULL,
	`description` varchar(255) NULL,
	`origin_country` varchar(255) NOT NULL,
	PRIMARY KEY (`brand_id`)
);

ALTER TABLE `product` ADD `brand_id` int AFTER `product_id`;
ALTER TABLE `product` ADD FOREIGN KEY (`brand_id`) REFERENCES `brand` (`brand_id`);

ALTER TABLE `product` ADD `category_id` int AFTER `product_id`;
ALTER TABLE `product` ADD FOREIGN KEY (`category_id`) REFERENCES `category` (`category_id`);

