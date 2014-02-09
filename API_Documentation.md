**This documentation is automatically generated.**

# /api/auth/login

    Content-Type: application/json

## POST
### Input
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


POST the required credentials to get back a cookie

* `name`: Username
* `password`: Password






# /api/game/creategame

    Content-Type: application/json

## POST
### Input
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


POST the required parameter to create a new game; only the owner of a room can make this request

* `nbpp`: Number of balls per player






# /api/game/sinkball

    Content-Type: application/json

## POST
### Input
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
### Output
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






# /api/player/player

    Content-Type: application/json

## POST
### Input
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
* `password`: Password for future logins



## GET
### Input
```json
null
```
### Output
```json
{
    "type": "object"
}
```


GET to retrieve player info






# /api/room/createroom

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
        "password": {
            "type": "string"
        }, 
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


POST the required parameters to create a new room

* `name`: Name of the room
* `password`: (Optional) Password to the room if you wish to keep entry restricted to players who know the password






# /api/room/joinroom

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
        "password": {
            "type": "string"
        }, 
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


POST the required parameters to create a new room

* `name`: Name of the room
* `password`: (Optional) Password to the room if it has one






# /api/room/leaveroom

    Content-Type: application/json

## DELETE
### Input
```json
null
```
### Output
```json
{
    "type": "string"
}
```


DELETE to leave current room






# /api/room/listrooms

    Content-Type: application/json

## GET
### Input
```json
null
```
### Output
```json
{
    "type": "array"
}
```


GET to receive list of rooms






# /api/room/retireroom

    Content-Type: application/json

## DELETE
### Input
```json
null
```
### Output
```json
{
    "type": "string"
}
```


DELETE to delete current room (if you are the owner)


