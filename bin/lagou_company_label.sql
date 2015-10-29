create table `lagou_company_label`(
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `position_id` int(11) not null default '0',
    `label` varchar(64) not null default ''
);
