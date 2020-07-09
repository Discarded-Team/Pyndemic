# Intenral API

This is the list of possible requests that can be sent to a launched game programmatically, and possible responses that can be received.

All requests and responses are dict-like objects with a required string field `"type"`.

Possible request type values are:

- empty
- check
- command
- message
- termination

Possible values for the response type are:

- empty
- message
- termination

---

## Request syntax

### Empty request

Syntax:

```python
{
    "type": "empty"
}
```

Empty requests suppose to do nothing with the game and the only possible response is also empty.

### Check request

**Warning: this request type is under development and its functionality may change.**

Syntax:

```python
{
    "type": "check"
}
```

Requests the current game state information. The response has a "message" type with `"game_data"` field included.

### Message request

**Warning: this request type is under development and is not functional.**

Syntax:

```python
{
    "type": "message",
    "message": "Any string-type message"
}
```

Sends a text message to the game engine. The response type may variate.

### Termination request

Syntax:

```python
{
    "type": "termination"
}
```

Requests the game end. This must be the final request, and no requests can be sent after this one. The response type is also "termination" and may contain the `"message"` field with final messages from the game.


### Command request

This type of request serves to send various gameplay commands representing player actions in the real game. The `"command"` string field is required in the request. The additional `"args"` field must be specified for some types of action. The following examples show the syntax of currently supported game actions.

* Pass:
  ```python
  {
      "type": "command",
      "command": "pass"
  }
  ```

* Standard move:
  ```python
  {
      "type": "command",
      "command": "move",
      "args" : {
          "destination": "London"
      }
  }
  ```

* Direct flight:
  ```python
  {
      "type": "command",
      "command": "fly",
      "args" : {
          "destination": "London"
      }
  }
  ```

* Charter flight:
  ```python
  {
      "type": "command",
      "command": "charter",
      "args" : {
          "destination": "London"
      }
  }
  ```

* Shuttle flight:
  ```python
  {
      "type": "command",
      "command": "shuttle",
      "args" : {
          "destination": "London"
      }
  }
  ```

* Building a laboratory:
  ```python
  {
      "type": "command",
      "command": "build"
  }
  ```

* Treat action:
  ```python
  {
      "type": "command",
      "command": "treat",
      "args" : {
          "colour": "Red"
      }
  }
  ```

* Cure a disease:
  ```python
  {
      "type": "command",
      "command": "cure",
      "args" : {
          "cards": ["Five", "Evenly", "Colored", "Player", "Cards"]
      }
  }
  ```

* Share a card:
  ```python
  {
      "type": "command",
      "command": "share",
      "args" : {
          "card": "London",
          "player": "Bravo"
      }
  }
  ```

The response is a "message" response with messages emitted during the command execution (if it does not fail). Also, the resulting game state information is included in the `"game_data"` field.

---

## Response syntax

### Empty response

This response does not contain any meaningful things.

Syntax:

```python
{
    "type": "empty"
}
```

### Message response

This response is used as a standard response for the majority of requests. It contains a `"message"` field with a text message from the game engine and may contain some other fields depending on details of the preceding request.

Syntax:

```python
{
    "type": "message",
    "message": "Something happened in the game."
}
```

### Termination response

This response is sent if any game-level exception is raised that means the rule-based game ending. And, obviously, this is the response for a termination request. May contain unnecessary `"message"` field.

Syntax:

```python
{
    "type": "termination",
    "message": "This game is ended."
}
```
