USE squashdb;

/* CREATE SCHEMA `squashdb` DEFAULT CHARACTER SET utf8 ;*/


SET FOREIGN_KEY_CHECKS=0; 
DROP TABLE IF EXISTS `user`;
DROP TABLE IF EXISTS `usertype`;

 /* User Table */
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
    `userName` VARCHAR(45) NOT NULL,
    `firstName` VARCHAR(45) NOT NULL,
    `lastName` VARCHAR(45) NOT NULL,
    `userEmail` VARCHAR(100) DEFAULT NULL,
    `userPhoneNumber` VARCHAR(10) DEFAULT NULL,
    `password` BINARY(8) NOT NULL,
    `usertypeId` ENUM('COACH','PLAYER') NOT NULL,    
    PRIMARY KEY (`userName`),
	UNIQUE KEY `userNameID_UNIQUE` (`userName`)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8;


 /* usertype Table */
DROP TABLE IF EXISTS `usertype`;
CREATE TABLE `usertype` (
    `usertypeId` ENUM('COACH','PLAYER') NOT NULL,
    `usertype` ENUM('COACH','PLAYER') NOT NULL,
    PRIMARY KEY (`usertypeId`),
    UNIQUE KEY `usertypeId_UNIQUE` (`usertypeId`)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8;


 /* Add foreign keys and other constraints to tables in the db */
ALTER TABLE `user` usertype
	ADD FOREIGN KEY (`usertypeId`) REFERENCES `usertype`(`usertypeId`);


SET FOREIGN_KEY_CHECKS=1;