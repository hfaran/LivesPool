**This documentation is automatically generated.**

# /api/game/creategame

    Content-Type: application/json

## POST
### Input
```json
{
    "required": [
        "player_names", 
        "nbpp"
    ], 
    "type": "object", 
    "properties": {
        "player_names": {
            "type": "array"
        }, 
        "password": {
            "type": "string"
        }, 
        "nbpp": {
            "type": "number"
        }
    }
}
```
### Output
```json
{
    "type": "object", 
    "properties": {
        "game_id": {
            "type": "string"
        }
    }
}
```


POST the required parameters to create a new game

* `nbpp`: Number of balls per player
* `password`: Password for the game; only the gamemaster should have access to this as it allows updates to the game
* `player_names`: List of player names that will join the game






# /api/game/sinkball

    Content-Type: application/json

## POST
### Input
```json
{
    "required": [
        "ball", 
        "password", 
        "game_id"
    ], 
    "type": "object", 
    "properties": {
        "game_id": {
            "type": "string"
        }, 
        "password": {
            "type": "string"
        }, 
        "ball": {
            "type": "number"
        }
    }
}
```
### Output
```json
{
    "type": "object", 
    "properties": {
        "game_id": {
            "type": "string"
        }
    }
}
```


POST the required parameters to register the pocketing of a ball

* `ball`: The ball that was pocketed
* `game_id`: The full game_id of the game for which to register
* `password`: Password for the game; must be provided in order to update the game






# /api/player/createplayer

    Content-Type: application/json

## POST
### Input
```json
{
    "required": [
        "name"
    ], 
    "type": "object", 
    "properties": {
        "name": {
            "type": "string"
        }
    }
}
```
### Output
```json
{
    "type": "object", 
    "properties": {
        "name": {
            "type": "string"
        }
    }
}
```


POST the required parameters to permanently register a new player

* `name`: Username of the player


