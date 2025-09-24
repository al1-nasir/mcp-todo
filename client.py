import socket, json

def send(req: dict, host="127.0.0.1", port=8765):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall((json.dumps(req) + "\n").encode())
    resp = b''
    # read single response (server writes one line)
    while True:
        part = s.recv(4096)
        if not part:
            break
        resp += part
        if b'\n' in part:
            break
    s.close()
    return json.loads(resp.decode().strip())

if __name__ == "__main__":
    print(send({"jsonrpc":"2.0","id":1,"method":"add_task","params":{"task":"Buy milk"}}))
    print(send({"jsonrpc":"2.0","id":2,"method":"list_tasks"}))
    print(send({"jsonrpc":"2.0","id":3,"method":"delete_task","params":{"task":"Buy milk"}}))
    print(send({"jsonrpc":"2.0","id":4,"method":"list_tasks"}))

