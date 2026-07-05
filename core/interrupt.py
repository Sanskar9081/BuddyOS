import threading

_interrupted = False
_lock = threading.Lock()
_active_processes = []

INTERRUPT_KEYWORDS = [
    "stop buddy",
    "buddy stop",
    "cancel",
    "abort",
    "never mind",
    "nevermind",
    "hold on"
]

def check_for_interrupt_words(text: str) -> bool:
    t = text.lower()
    return any(w in t for w in INTERRUPT_KEYWORDS)

def set_interrupt(value: bool):
    global _interrupted
    with _lock:
        _interrupted = value
        if value:
            # Try to forcefully kill any registered processes (e.g. subprocesses)
            for p in list(_active_processes):
                try:
                    p.terminate()
                except Exception:
                    pass
            _active_processes.clear()

def is_interrupted() -> bool:
    with _lock:
        return _interrupted

def check_interrupt():
    """Call this periodically in long-running tasks."""
    if is_interrupted():
        raise InterruptedError("Task was interrupted by the user.")

def register_process(p):
    """Register a subprocess.Popen object to be killed on interrupt."""
    with _lock:
        if p not in _active_processes:
            _active_processes.append(p)

def unregister_process(p):
    with _lock:
        if p in _active_processes:
            _active_processes.remove(p)
