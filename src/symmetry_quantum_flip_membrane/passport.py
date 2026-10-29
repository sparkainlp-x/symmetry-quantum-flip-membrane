"""Evidence passport: SHA-256 seal over canonical JSON.

The seal changes if any recorded result, seed, parameter, or version
changes. It proves only that the recorded JSON is the one sealed, not
that any claim about the real world is true.
"""
import hashlib
import json

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))

def seal(obj):
    return hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()
