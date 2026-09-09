"""MCP Server for Double Ratchet Skill."""
import json
import sys
from client import DoubleRatchetSession

def main():
    sessions = {}
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "tools/list":
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": [{
                            "name": "ratchet_encrypt",
                            "description": "Encrypt message and advance forward-secret ratchet state",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "session_id": {"type": "string"},
                                    "shared_secret": {"type": "string"},
                                    "message": {"type": "string"}
                                },
                                "required": ["session_id", "message"]
                            }
                        }]
                    }
                }
            elif method == "tools/call":
                args = params.get("arguments", {})
                sid = args["session_id"]
                if sid not in sessions:
                    sessions[sid] = DoubleRatchetSession(args.get("shared_secret", "DEFAULT_SECRET"))
                out = sessions[sid].encrypt_and_ratchet(args["message"])
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(out)}]}
                }
            else:
                res = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            print(json.dumps(res), flush=True)
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err), flush=True)

if __name__ == "__main__":
    main()
