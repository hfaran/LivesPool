**This documentation is automatically generated.**

**Output schemas only represent `data` and not the full output; see output examples and the JSend specification.**

# `/api/auth/login`

    Content-Type: application/json

## POST
### Input Schema
```json
{
    "required": [
        "username", 
        "password"
    ], 
    "type": "object", 
    "properties": {
        "username": {
            "type": "string"
        }, 
        "password": {
            "type": "string"
        }
    }
}
```

### Output Schema
```json
{
    "type": "object", 
    "properties": {
        "username": {
            "type": "string"
        }
    }
}
```



POST the required credentials to get back a cookie

* `username`: Username
* `password`: Password



## GET
### Input Schema
```json
null
```

### Output Schema
```json
{
    "type": "string"
}
```



GET to check if authenticated. Should be obvious from status code (403 vs. 200).






# `/api/auth/logout`

    Content-Type: application/json

## DELETE
### Input Schema
```json
null
```

### Output Schema
```json
{
    "type": "string"
}
```



DELETE to clear cookie for current user.






# `/api/game/ballsontable`

    Content-Type: application/json

## GET
### Input Schema
```json
null
```

### Output Schema
```json
{
    "type": "array"
}
```

### Output Example
```json
[
    2, 
    5, 
    9, 
    6
]
```



GET to receive list of balls on the table in current game






# `/api/game/creategame`

    Content-Type: application/json

## POST
### Input Schema
```json
{
    "required": [
        "nbpp"
    ], 
    "type": "object", 
    "properties": {
        "nbpp": {
            "type": "number"
        }
    }
}
```

### Output Schema
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



POST the required parameter to create a new game; only the owner of a room can make this request

* `nbpp`: Number of balls per player






# `/api/game/leavegame`

    Content-Type: application/json

## DELETE
### Input Schema
```json
null
```

### Output Schema
```json
{
    "required": [
        "game_id"
    ], 
    "type": "object", 
    "properties": {
        "game_id": {
            "type": "string"
        }
    }
}
```



DELETE to remove yourself from current game






# `/api/game/listplayers`

    Content-Type: application/json

## GET
### Input Schema
```json
null
```

### Output Schema
```json
{
    "required": [
        "gamemaster", 
        "players"
    ], 
    "type": "object", 
    "properties": {
        "players": {
            "type": "array"
        }, 
        "gamemaster": {
            "type": "string"
        }
    }
}
```

### Output Example
```json
{
    "players": [
        "Stark", 
        "Stannis", 
        "Baratheon", 
        "Tyrell", 
        "Lannister"
    ], 
    "gamemaster": "Stark"
}
```



GET to receive list of players in current game

* `players` array includes ALL players (including gamemaster)
* `gamemaster` field is useful for highlighting the gamemaster in the UI






# `/api/game/toggleball`

    Content-Type: application/json

## POST
### Input Schema
```json
{
    "required": [
        "ball"
    ], 
    "type": "object", 
    "properties": {
        "ball": {
            "type": "number"
        }
    }
}
```

### Output Schema
```json
{
    "required": [
        "game_id"
    ], 
    "type": "object", 
    "properties": {
        "game_id": {
            "type": "string"
        }, 
        "message": {
            "type": "string"
        }
    }
}
```



POST the required parameters to register the pocketing/unpocketing of a ball

* `ball`: The ball that was pocketed/unpocketed






# `/api/player/player`

    Content-Type: application/json

## POST
### Input Schema
```json
{
    "required": [
        "username", 
        "password"
    ], 
    "type": "object", 
    "properties": {
        "username": {
            "type": "string"
        }, 
        "password": {
            "type": "string"
        }
    }
}
```

### Output Schema
```json
{
    "type": "object", 
    "properties": {
        "username": {
            "type": "string"
        }
    }
}
```



POST the required parameters to permanently register a new player

* `username`: Username of the player
* `password`: Password for future logins



## GET
### Input Schema
```json
null
```

### Output Schema
```json
{
    "type": "object", 
    "properties": {
        "current_room": {
            "type": "string"
        }, 
        "orig_balls": {
            "type": "array"
        }, 
        "current_game_id": {
            "type": "string"
        }, 
        "name": {
            "type": "string"
        }, 
        "balls": {
            "type": "array"
        }
    }
}
```



GET to retrieve player info






# `/api/room/createroom`

    Content-Type: application/json

## POST
### Input Schema
```json
{
    "required": [
        "roomname"
    ], 
    "type": "object", 
    "properties": {
        "roomname": {
            "type": "string"
        }, 
        "password": {
            "type": "string"
        }
    }
}
```

### Output Schema
```json
{
    "type": "object", 
    "properties": {
        "roomname": {
            "type": "string"
        }
    }
}
```



POST the required parameters to create a new room

* `name`: Name of the room
* `password`: (Optional) Password to the room if you wish to keep entry restricted to players who know the password






# `/api/room/joinroom`

    Content-Type: application/json

## POST
### Input Schema
```json
{
    "required": [
        "name"
    ], 
    "type": "object", 
    "properties": {
        "password": {
            "type": "string"
        }, 
        "name": {
            "type": "string"
        }
    }
}
```

### Output Schema
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



POST the required parameters to create a new room

* `name`: Name of the room
* `password`: (Optional) Password to the room if it has one






# `/api/room/leaveroom`

    Content-Type: application/json

## DELETE
### Input Schema
```json
null
```

### Output Schema
```json
{
    "type": "string"
}
```



DELETE to leave current room. If the room owner leaves, the room will be deleted.






# `/api/room/listplayers`

    Content-Type: application/json

## GET
### Input Schema
```json
null
```

### Output Schema
```json
{
    "required": [
        "owner", 
        "players"
    ], 
    "type": "object", 
    "properties": {
        "owner": {
            "type": "string"
        }, 
        "players": {
            "type": "array"
        }
    }
}
```

### Output Example
```json
{
    "owner": "Stark", 
    "players": [
        "Stark", 
        "Stannis", 
        "Baratheon", 
        "Tyrell", 
        "Lannister"
    ]
}
```



GET to receive list of players in current room

* `players` array includes ALL players (including owner)
* `owner` field is useful for highlighting the room owner in the UI






# `/api/room/listrooms`

    Content-Type: application/json

## GET
### Input Schema
```json
null
```

### Output Schema
```json
{
    "type": "array"
}
```

### Output Example
```json
[
    {
        "pwd_req": true, 
        "name": "Curve"
    }, 
    {
        "pwd_req": false, 
        "name": "Cue"
    }
]
```



GET to receive list of rooms


