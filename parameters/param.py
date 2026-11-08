import os 

PARAM_PORT = int(os.environ.get("PARAM_PORT", "9436"))
PARAM_FLUSH = os.environ.get("PARAM_FLUSH", "true").lower() in ("1", "true", "yes")
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "60"))
VERIFY_SSL = os.environ.get("VERIFY_SSL", "false").lower() in ("1", "true", "yes")