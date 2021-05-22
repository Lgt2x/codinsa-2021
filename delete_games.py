from src.io import Connection

with open('token', 'r') as f:
    conn = Connection(f.readline())
    conn.deleteGames()