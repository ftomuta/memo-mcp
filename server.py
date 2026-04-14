from mcp.server.fastmcp import FastMCP
from pymongo import MongoClient
import random

# Initialize MCP and MongoDB
mcp = FastMCP("Pro-Gamer-Tracker")
client = MongoClient("mongodb://localhost:27017/") # Or your Atlas URI
db = client.game_records
players = db.players

@mcp.tool()
def get_player(username: str) -> dict:
    """Retrieves a player's full NoSQL document."""
    player = players.find_one({"username": username}, {"_id": 0})
    return player if player else {"error": "Player not found"}

@mcp.tool()
def update_xp(username: str, new_xp: int) -> str:
    """Updates the player's xp in the database."""
    players.update_one({"username": username}, {"$set": {"xp": new_xp}})
    return f"Success! {username}'s xp is now {new_xp}."

@mcp.tool()
def add_new_player(username: str) -> str:
    """Inserts a new player document with default values."""
    if players.find_one({"username": username}):
        return "Error: Player already exists."
    new_player = {
        "username": username,
        "xp": 0,
        "level": 1,
        "health": 100.00,
        "strength": 10,
        "vitality": 10,
        "intelligence": 10,
        "achievements": []
    }
    players.insert_one(new_player)
    return f"Success! Player {username} has been added."

@mcp.tool()
def level_up_player(username: str, new_level: int) -> str:
    """Updates the player level in the database."""
    players.update_one({"username": username}, {"$set": {"level": new_level}})
    return f"Success! {username} is now level {new_level}."

@mcp.tool()
def add_achievement(username: str, achievement: str) -> str:
    """Pushes a new achievement into the player's history array."""
    players.update_one(
        {"username": username}, 
        {"$push": {"achievements": achievement}}
    )
    return f"Achievement unlocked: {achievement}!"

@mcp.tool()
def get_leaderboard() -> list:
    """Retrieves the top 10 players sorted by xp."""
    leaderboard = list(players.find({}, {"_id": 0, "username": 1, "xp": 1}).sort("xp", -1).limit(10))
    return leaderboard

@mcp.tool()
def duel_players(player1: str, player2: str) -> str:
    """Simulates a duel between two players until one reaches 2 HP or below."""
    p1 = players.find_one({"username": player1})
    p2 = players.find_one({"username": player2})
    if not p1 or not p2:
        return "One or both players not found"
    
    hp1 = p1["health"]
    hp2 = p2["health"]
    level1 = p1["level"]
    level2 = p2["level"]
    
    turn = 0  # 0: player1 attacks player2, 1: player2 attacks player1
    while hp1 > 2 or hp2 > 2:
        if turn == 0:
            damage = random.randint(1, 10) * (0.5 * level1)
            hp2 -= damage
            turn = 1
        else:
            damage = random.randint(1, 10) * (0.5 * level2)
            hp1 -= damage
            turn = 0
    
    if hp1 > hp2:
        winner = player1
    elif hp2 > hp1:
        winner = player2
    else:
        winner = "Draw"
    
    # Update health in database
    players.update_one({"username": player1}, {"$set": {"health": hp1}})
    players.update_one({"username": player2}, {"$set": {"health": hp2}})
    
    return f"Duel result: {winner} wins. {player1} HP: {hp1}, {player2} HP: {hp2}"

@mcp.resource( "player://{username}" )
def player_profile(username: str) -> dict:
    """Returns a player's profile data."""
    player = players.find_one({"username": username}, {"_id": 0})
    return player if player else {"error": "Player not found"}

if __name__ == "__main__":
    mcp.run()