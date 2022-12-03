create table if not exists users (
  id integer primary key autoincrement,
  name text not null unique,
  password text not null,
  privileges int not null
);

create table if not exists posts (
  id integer primary key autoincrement,
  author text not null,
  content text not null,
  visible integer not null
);

drop table if exists logs;
create table if not exists logs (
  id integer primary key autoincrement,
  type text not null,
  src_ip text not null,
  resource text not null,
  user_agent text not null,
  time timestamp not null default current_timestamp
);
