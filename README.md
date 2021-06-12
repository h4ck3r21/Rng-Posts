# touch typing battle program
epic

## Disconnection
```mermaid
sequenceDiagram;
    autonumber
    participant Browser1
    participant Server
    participant Browser2
    
    Browser1 ->> Browser1: close Browser
    Browser1 -x Server: disconnect
    Server ->> Browser2: check online<br>(broadcast)
    Browser2 ->> Server: online
    Server ->> Server: rebuild the users list<br>based on replies
    Server ->> Browser2: new users list
    
```
        
