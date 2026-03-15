# 113restaurantdatabase
My app tracks restaurants in pittsburgh (although there is nothing stopping it from being generalized to greater areas other than the fact that there's no database columns pertaining to city, state, country, etc. -- only neighborhood in pittsburgh.

id INTEGER
name TEXT
neighborhood TEXT
cuisine TEXT
rating INTEGER
visited TEXT

just open app.py and run it. only sqlite3 is needed. the CLI tells the user exactly how to run each CRUD operation, which is just by inputting a number. from there, users are prompted to input text or integers to create, read, update, or delete.
