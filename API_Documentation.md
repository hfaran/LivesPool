**This documentation is automatically generated.**

**Output schemas only represent `data` and not the full output; see output examples and the JSend specification.**

# /api/auth/login

    Content-Type: application/json

## POST
### Input Schema
```json
{
    "required": [
        "name", 
        "password"
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



POST the required credentials to get back a cookie

* `name`: Username
* `password`: Password






# /api/game/creategame

    Content-Type: application/json

## POST
### Input Schema
```json
{
    "required": [
        "nbpp", 
        "password", 
        "room_name"
    ], 
    "type": "object", 
    "properties": {
        "room_name": {
            "type": "string"
        }, 
        "room_password": {
            "type": "string"
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



POST the required parameters to create a new game

* `nbpp`: Number of balls per player
* `password`: Password for the game; only the gamemaster should have access to this as it allows updates to the game
* `room_name`: Room from which this game is being created
* `room_password`: (Required only if room is passworded) Password for the room from which this game is being created






# /api/game/sinkball

    Content-Type: application/json

## POST
### Input Schema
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



POST the required parameters to register the pocketing of a ball

* `ball`: The ball that was pocketed
* `game_id`: The full game_id of the game for which to register
* `password`: Password for the game; must be provided in order to update the game






# /api/player/player

    Content-Type: application/json

## POST
### Input Schema
```json
{
    "required": [
        "name", 
        "password"
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



POST the required parameters to permanently register a new player

* `name`: Username of the player
* `password`: Password for future logins



## GET
### Input Schema
```json
null
```

### Output Schema
```json
{
    "type": "object"
}
```



GET with following query parameters to retrieve player info

* `username`: Username of the player






# /api/room/createroom

    Content-Type: application/json

## POST
### Input Schema
```json
{
    "required": [
        "name", 
        "owner"
    ], 
    "type": "object", 
    "properties": {
        "owner": {
            "type": "string"
        }, 
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
* `password`: (Optional) Password to the room if you wish to keep entry restricted to players who know the password
* `owner`: Name of the player creating the room






# /api/room/joinroom

    Content-Type: application/json

## POST
### Input Schema
```json
{
    "required": [
        "name", 
        "player"
    ], 
    "type": "object", 
    "properties": {
        "player": {
            "type": "string"
        }, 
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
* `player`: Name of player joining the room






# /api/room/listrooms

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



GET to receive list of rooms


