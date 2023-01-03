USE MEDICO;
SET FOREIGN_KEY_CHECKS=0;

-- Table: user


DROP TABLE IF EXISTS user;



CREATE TABLE user (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	username VARCHAR(16) NOT NULL, 
	password_hash VARCHAR(128), 
	fullname VARCHAR(64) NOT NULL, 
	dob DATE NOT NULL, 
	sex VARCHAR(1) NOT NULL, 
	blood VARCHAR(3), 
	reference VARCHAR(64), 
	email VARCHAR(64), 
	address VARCHAR(64), 
	admin SMALLINT NOT NULL, 
	active SMALLINT NOT NULL, 
	author INTEGER, 
	created_at DATETIME, 
	modified_at DATETIME, 
	avatar VARCHAR(128), analysis TEXT, case_photo_1 VARCHAR(128), case_photo_2 VARCHAR(128), case_photo_3 VARCHAR(128), case_photo_4 VARCHAR(128), 
	CONSTRAINT pk_user PRIMARY KEY (id), 
	CONSTRAINT uq_user_username UNIQUE (username), 
	CONSTRAINT uq_user_email UNIQUE (email), 
	CONSTRAINT fk_user_author_user FOREIGN KEY(author) REFERENCES user (id)
);


-- Table: prescription
DROP TABLE IF EXISTS prescription;
CREATE TABLE prescription (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	note TEXT, 
	prescription TEXT, 
	patient_id INTEGER, 
	author INTEGER, 
	created_at DATETIME, 
	modified_at DATETIME, 
	follow_up_date DATE, 
	CONSTRAINT pk_prescription PRIMARY KEY (id), 
	CONSTRAINT fk_prescription_author_user FOREIGN KEY(author) REFERENCES user (id), 
	CONSTRAINT fk_prescription_patient_id_user FOREIGN KEY(patient_id) REFERENCES user (id)
);



-- Table: conversation
DROP TABLE IF EXISTS conversation;
CREATE TABLE conversation (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	conversation VARCHAR(128), 
	`read` SMALLINT, 
	patient_id INTEGER, 
	author INTEGER, 
	created_at DATETIME, 
	modified_at DATETIME, 
	admin_id INTEGER, 
	CONSTRAINT pk_conversation PRIMARY KEY (id), 
	CONSTRAINT fk_conversation_author_user FOREIGN KEY(author) REFERENCES user (id), 
	CONSTRAINT fk_conversation_patient_id_user FOREIGN KEY(patient_id) REFERENCES user (id), 
	CONSTRAINT fk_conversation_admin_id_user FOREIGN KEY(admin_id) REFERENCES user (id)
);

-- Table: medicine
DROP TABLE IF EXISTS medicine;
CREATE TABLE medicine (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	short_name VARCHAR(128), 
	medicine VARCHAR(128), 
    potency VARCHAR(128), 
	author INTEGER, 
	created_at DATETIME, 
	modified_at DATETIME, 
	CONSTRAINT pk_medicine PRIMARY KEY (id), 
	CONSTRAINT fk_medicine_author_user FOREIGN KEY(author) REFERENCES user (id), 
	CONSTRAINT uq_medicine_medicine UNIQUE (medicine), 
	CONSTRAINT uq_medicine_short_name UNIQUE (short_name)
);


INSERT INTO `user`
(
username, 
password_hash,
fullname, 
dob, 
sex, 
blood, 
admin, 
active, 
author
)
VALUES
(
'root', 
'sha256$9BKqwnG8UDTSVJHc$d46b6bde118980d83b6b538448e948ed41c60aee5ddd30368cfe7ac20a82d875', 
'Sys Admin', 
'1983-12-31', 
'M', 
'B+',
1, 
1, 
1
);