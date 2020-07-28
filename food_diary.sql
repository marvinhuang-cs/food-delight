CREATE TABLE "User" (
  "id" int PRIMARY KEY,
  "email" string UNIQUE NOT NULL,
  "username" string UNIQUE NOT NULL,
  "password" string NOT NULL,
  "full_name" string NOT NULL
);

CREATE TABLE "Food" (
  "id" int PRIMARY KEY,
  "calories" int NOT NULL,
  "servings" int,
  "meal" string
);

CREATE TABLE "User_Food" (
  "user_id" int,
  "food_id" int,
  "total_calories" int,
  PRIMARY KEY ("user_id", "food_id")
);

ALTER TABLE "User" ADD FOREIGN KEY ("id") REFERENCES "User_Food" ("user_id");

ALTER TABLE "User_Food" ADD FOREIGN KEY ("food_id") REFERENCES "Food" ("id");

