from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

'''
create html to create new WebSocket for connecting with the server socket
'''
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var username = prompt("Enter your name:"); // Prompt the user for their user ID
            document.querySelector("#ws-id").textContent = username;
            var ws = new WebSocket(`ws://localhost:8000/ws/${username}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


class ConnectionManager:
    #defining socket events
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    
    #connect event
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    #disconnect event
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    #send message from client
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    #send message each client
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(f"{message}")


manager = ConnectionManager()


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket)
    await manager.send_personal_message(f"{username}", websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{username}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{username} left the chat")