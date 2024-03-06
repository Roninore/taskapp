create table "session" (
    "id" varchar(256) primary key,
    "user_id" int not null,
    "ip" varchar(15),
    "user_agent" varchar(256),
    "is_active" boolean not null,
    "created_timestamp" timestamp not null default (now() at time zone 'utc')
);

create table "user" (
    "id" serial primary key,
    "username" varchar(32) not null,
    "full_name" varchar(128) not null,
    "password_encrypted" varchar(128) not null,
    "role" int not null default(0),
    "created_timestamp" timestamp not null default (now() at time zone 'utc')
);
create unique index "user__username__unique_idx" on "user" ("username");

create table "task" (
    "id" serial primary key,
    "caption" varchar(128) not null,
    "text" text not null default(''),
    "created_by" int not null,
    "state" varchar(16) not null default('not_started'),
    "edited_timestamp" timestamp not null default (now() at time zone 'utc'),
    "created_timestamp" timestamp not null default (now() at time zone 'utc')
);

create table "task_performer" (
    "id" serial primary key,
    "user_id" int not null,
    "task_id" int not null,
    "created_timestamp" timestamp not null default (now() at time zone 'utc')
);
create unique index "task_performer__user_id__task_id__unique_idx" on "task_performer" ("user_id", "task_id");


