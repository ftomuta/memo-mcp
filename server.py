from mcp.server.fastmcp import FastMCP
from pymongo import MongoClient
import random

# Initialize MCP and MongoDB
mcp = FastMCP("Pro-Gamer-Tracker")
client = MongoClient("mongodb://localhost:27017/") # Or your Atlas URI
db = client.game_records
players = db.players

class player:
    username: str
    xp: int
    level: int
    strength: int
    vitality: int
    intelligence: int

    def __init__(self, name: str):
        self.vitality = 10
        self.strength = 0
        self.intelligence = 0
        self.level = 1
        self.username = name
        self.xp = 0

    def get_max_health(self):
        return self.vitality * (10 + (level/2))

    def gain_exp(self, opponent: player, random_number: int):
        self.xp += max(opponent.level - self.level, 1) + intelligence
        while xp >= 100 + (50 * level):
            xp -= 100 + 50 * level
            level += 1
            match random_number:
                case 1:
                    strength += 2
                case 2:
                    intelligence += 2
                case _:
                    vitality += 2

    def calculate_damage(self, random_number: int):
        return (random_number * (self.level/2)) + self.strength

@mcp.tool()
def get_player(username: str) -> dict:
    """Retrieves a player's full NoSQL document."""
    player = players.find_one({"username": username}, {"_id": 0})
    return player if player else {"error": "Player not found"}

@mcp.tool()
def add_new_player(username: str) -> str:
    """Inserts a new player document with default values."""
    if players.find_one({"username": username}):
        return "Error: Player already exists."
    players.insert_one(player(username))
    return f"Success! Player {username} has been added."

@mcp.tool()
def level_up_player(username: str, new_level: int) -> str:
    """Updates the player level in the database."""
    players.update_one({"username": username}, {"$set": {"level": new_level, "xp": 0}})
    return f"Success! {username} is now level {new_level}."

@mcp.tool()
def get_leaderboard() -> list:
    """Retrieves the top 10 players sorted by level."""
    leaderboard = list(players.find({}, {"_id": 0, "username": 1, "level": 1}).sort("level", -1).limit(10))
    return leaderboard

@mcp.tool()
def duel_players(player1: str, player2: str) -> str:
    """Simulates a duel between two players until one reaches 2 HP or below."""
    p1 = player(players.find_one({"username": player1}))
    p2 = player(players.find_one({"username": player2}))
    if not p1 or not p2:
        return "One or both players not found"
    
    hp1 = p1.get_max_health()
    hp2 = p2.get_max_health()
    winner = ""
    
    while hp1 > 2 and hp2 > 2:
        hp2 -= p1.calculate_damage(random.random_number(0,10))
        hp1 -= p2.calculate_damage(random.random_number(0,10))

    if (hp2 >= hp1): 
        p2.gain_exp(p1, random.random_number(1,3))
        winner = player2

    if (hp1 >= hp2):
        p1.gain_exp(p2, random.random_number(1,3))
        if winner != "":
            winner = "draw"
        else:
         winner = player1

    players.replace_one({"username": player1}, player1)
    players.replace_one({"username": player2}, player2)
    
    return f"Duel result: {winner} wins. {player1} HP: {hp1}, {player2} HP: {hp2}"

@mcp.resource( "player://{username}" )
def player_profile(username: str) -> dict:
    """Returns a player's profile data."""
    player = players.find_one({"username": username}, {"_id": 0})
    return player if player else {"error": "Player not found"}

if __name__ == "__main__":
    mcp.run()
