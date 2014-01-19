**This documentation is automatically generated.**

# /api/handlers/creategame

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
            "type": "list"
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
    "type": "string"
}
```



