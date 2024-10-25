CREATE_GROUP_TABLE = """
CREATE TABLE IF NOT EXISTS groups (
id INTEGER PRIMARY KEY AUTOINCREMENT,
group_id INTEGER NOT NULL,
user_id INTEGER NOT NULL,
group_name VARCHAR(255) NOT NULL
);
"""

CREATE_FAVORITE_GROUP = """
CREATE TABLE IF NOT EXISTS favorite (
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
group_id INTEGER NOT NULL
)
"""

INSERT_GROUP = """INSERT INTO groups (group_id, user_id, group_name) VALUES (?, ?, ?)"""

INSERT_FAVORITE = """INSERT INTO favorite (user_id, group_id) VALUES (?, ?)"""

UPDATE_FAVORITE = """UPDATE favorite SET group_id = ? WHERE user_id = ?"""

SELECT_USER_GROUPS = """SELECT group_id, group_name FROM groups WHERE user_id = ?"""

SELECT_USER_FAVORITE = """
SELECT g.group_id, g.group_name FROM favorite as f 
JOIN groups as g 
ON f.group_id = g.group_id
WHERE f.user_id = ?
"""