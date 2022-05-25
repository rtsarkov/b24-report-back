CREATE TABLE `groups` (	
	`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
	`name` VARCHAR(255),
	`bitrix_id` INT	
);
CREATE UNIQUE INDEX `bitrix_id_index` ON groups(bitrix_id);

CREATE TABLE `plan_time` (
	`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
	`group_id` INT,
	`time_s` BIGINT,
	`date_start` TIMESTAMP,
	`date_end` TIMESTAMP,
	FOREIGN KEY (group_id) REFERENCES groups(id)
);
