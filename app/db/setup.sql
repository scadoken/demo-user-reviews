create table business (
	id varchar(20),
	alias varchar(100),
	name varchar(100),
	review_count int,
	rating numeric(3,2),
	address1 varchar(100),
	address2 varchar(100),
	city varchar(100),
	zip5 varchar(5),
	state varchar(2),
	phone varchar(15),
	_update_dt date,
	CONSTRAINT pk_business PRIMARY KEY(id)
);

create table review (
	business_id varchar(20) references business(id),
	user_id varchar(50),
	user_name varchar(100),
	create_dt date,
	stars int,
	txt varchar(5000),
	_update_dt date,
	
	CONSTRAINT pk_review PRIMARY KEY(business_id, user_id, create_dt)
);
