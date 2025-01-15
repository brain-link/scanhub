-- Create the User table if it does not exist
CREATE TABLE IF NOT EXISTS user (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    salt VARCHAR(255) NOT NULL,
    access_token VARCHAR(255) NOT NULL,
    last_activity_unixtime INT NOT NULL
);

-- Insert default user
INSERT INTO user (username, first_name, last_name, email, role, password_hash, salt, access_token, last_activity_unixtime)
VALUES (
    'Max',
    'Maximillian',
    'Mustermann',
    'mustermail@mail.de',
    'admin',
    'fee296a374f7d8d105fc93bb3b87b7e4cdc81e8421d45e51e0e4c1a3b3e696f9',
    'de863377c864747810505dc65ca308cec37ea4dd50d68a65a2aef71f6625b2ec64a76c9fef2ba840c0a3af7bbb732c6b2f6f68070518d00f0e3279ee55477783979fb92a83873bc82244b2b949570695e999a57c595b88c09d355327af9cc4b8eb1b0f7284f64d87932990befe8859d75fc0b0a65eee0d725a7e564f20081a195157876c97acbfe72528e5a5ec671000d5ce4537b86e345553bf24ede536cfc111b7f6f3ab1ccc5d33d22e7d44989a2f693b9f95c03bb5fe07d0bc75eb0a44754f8484388db46f64c1b7d172184ba6b5428c8b263dcf2cfae30b72cf56587e4fd43c177bd21d0c3d8fb82f908c98e46ea63a6bbab1d7777a04657940fc214e31751ef9cae58db39ad91d3c50c448e982164260fe8d47a2936f46db5d1e32150ca04880f2f95f290123b0d77d8c24c8baa974f99fde21754af4797bd22ee195685952df94352cc716fa79c112505ba6ff5962443bd76947043bbfd09badf2471fefe3a518b725d5168496a138039258fce5eda37e4052a127d4d18ac7d1d8208b813d28605fb6554e9227a258e937d0f4808078c0a59e1ce86992a4b09e103f35815176c72acadeed98f26bbdfb2e425595b739fdb2c39afcedc4ffbc2b656d07ecbcdd2722ffb2ca24d41cd8871c804bbc52acb88823542024f76a0e88ea8089b375d6b72012af81c422b5d41a5e87cac38f5dc00104009c7a83a4f62620933841b3ca2ce2ea4c7d4862b46a0ac4cd0603efa3dc01543b259a361d13e5afdadb6c474c96a7778853e2fbb98f88cf9987a27671a3424661197dffd0fc0b2c73435af3be9472241b1e6dcb3bb5066812bf0bfd35027f68419030f972c5307306ee80eed29702335052de3370ba74afb27050f75f58a9891c8a50c17d5d658e2d95f46b4dbea056fdedbfbbc92b63efa76f89b8600f48d8899c98da65a6e8fab120312c12eb2ae5bb95db43e44a543e02fe2b87ad8f66d253d0b1d48ca5343074a1164adfedd372645f6df86ff64c9a80a145584161068e6613292d77d86698b94ce6a8571aaa162991d30d365800af912c6549ba83fab63ea3bfca82c6a487c4a8ea735a59f360bb624a9f4386e6747cc1297cc2a693e77059f592391ba38200995cfb7cc27fd253bb5d49170025c1b13c83236e3985fdbc80901dbb840e6ac9f64dd847790bbc9b1b2324af3fa289e5c469b989627a470a04a4d9439eead5432e972336a6ef45414cb9df61ff23f2d41bc980b4553a73738e942db44b53fee7184e791fb3e0bfbcc5faf342c0bf75c5c1a3d674d05c1e9d193903a35b858860f1d95e2c69acaaea42b09a9c2195e473c707602306f9c53b923311293770b33010bafc0446bbaea9cca979b96699f44982630a8455c40f4208d56f5729bc3863c9ef2eaa6b079867445606806c83ac0dc9cc51a39583efb7b4efda2f96c05edeb3',
    '',
    ''
);