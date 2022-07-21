import sqlite3

domains = ["youtube.com", "netflix.com", "reddit.com", "primevideo.com"]

# Connect to the db
con = sqlite3.connect(
    "/Users/flo/Library/Application Support/Firefox/Profiles/7jm6hb9a.dev-edition-default/cookies.sqlite"
)
cur = con.cursor()

# Delete all cookies
for domain in domains:
    print(f"Deleting {domain} ...")
    target = "%" + domain + "%"
    cur.execute("DELETE FROM moz_cookies WHERE host LIKE ?;", [target])

# Save and close the db
con.commit()
con.close()
