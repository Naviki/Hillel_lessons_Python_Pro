create table storage(id SERIAL primary key,
	name varchar(30) not null,
	address varchar (50)
);

create table goods(id SERIAL primary key,
	name varchar (70),
	price int not null,
	quantity int not null,
	storage_id int references storage(id)
);

insert into storage (name, address)
	values ('FTS', 'Kyiv, Mykhaila Hryshka Street, 7');

insert into storage (name, address)
	values ('DBD', 'Odesa, Pryvozna Street, 14');

insert into storage (name, address)
	values ('STH', 'Lviv, Tarasa Shevchenka, 3');

insert into goods (name, price, quantity, storage_id)
	values
		('T-shirt', 15, 8, 1),
		('Jeans', 30, 1, 2),
		('Dress', 12, 30, 2),
		('Hoodie', 20, 7, 3),
		('Skirt', 15, 8, 3),
		('Sweater', 70, 21, 1),
		('Pants', 99, 51, 2),
		('Blouse', 36, 40, 1),
		('Jacket', 45, 4, 3),
		('Shorts', 45, 7, 3);

select * from goods;

update goods
	set quantity = quantity + 5
	where name = 'Dress';

delete from goods where storage_id=3;

explain analyse select * from goods where name='Dress';

create index goods_name_idx on goods(name);