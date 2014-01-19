**This documentation is automatically generated.**

# /api/game/creategame

    Content-Type: application/json

## POST
### Input
```
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
```
{
    "type": "object", 
    "properties": {
        "game_id": {
            "type": "string"
        }
    }
}
```







# /api/game/sinkball

    Content-Type: application/json

## POST
### Input
```
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
```
{
    "type": "object", 
    "properties": {
        "game_id": {
            "type": "string"
        }
    }
}
```



