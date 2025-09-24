import asyncio
import json

# Public in-memory store (easy to import in tests)
todos = []

def add_task(task: str):
    if not task:
        raise ValueError("Empty task")
    todos.append(task)
    return {"status": "Task added", "task": task}

def list_tasks():
    return todos.copy()

def delete_task(task: str):
    if task in todos:
        todos.remove(task)
        return {"status": "Task deleted", "task": task}
    raise KeyError("Task not found")

async def handle_request(reader, writer):
    addr = writer.get_extra_info('peername')
    # Serve line-delimited JSON-RPC
    while True:
        data = await reader.readline()
        if not data:
            break
        text = data.decode().strip()
        if not text:
            continue
        try:
            request = json.loads(text)
            req_id = request.get("id")
            method = request.get("method")
            params = request.get("params", {})

            response = {"jsonrpc": "2.0", "id": req_id}

            try:
                if method == "add_task":
                    task = params.get("task")
                    result = add_task(task)
                    response["result"] = result

                elif method == "list_tasks":
                    response["result"] = {"tasks": list_tasks()}

                elif method == "delete_task":
                    task = params.get("task")
                    result = delete_task(task)
                    response["result"] = result

                else:
                    response["error"] = {"code": -32601, "message": "Method not found"}

            except Exception as e:
                response["error"] = {"code": -32000, "message": str(e)}

        except Exception as e:
            response = {"jsonrpc": "2.0", "id": None,
                        "error": {"code": -32700, "message": f"Parse error: {e}"}}

        writer.write((json.dumps(response) + "\n").encode())
        await writer.drain()

    try:
        writer.close()
        await writer.wait_closed()
    except:
        pass

async def main():
    server = await asyncio.start_server(handle_request, "0.0.0.0", 8765)
    print("✅ MCP Todo Server running on 0.0.0.0:8765")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutdown")

