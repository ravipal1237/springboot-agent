import os, re, subprocess, time
from typing import List, Tuple

FENCE = re.compile(r"```(\w+)([^\n`]*)\n(.*?)```", re.DOTALL)

def run(cmd: List[str], cwd: str = None) -> Tuple[int, str, str]:
    proc = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = proc.communicate()
    return proc.returncode, out, err

def write(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def safe_rel(rel: str) -> bool:
    return not(rel.startswith('/') or '..' in rel.replace('..','__'))

def apply_fenced_drops(text: str, repo_root: str):
    if not text:
        return
    for m in FENCE.finditer(text):
        _lang, header, body = m.groups()
        pm = re.search(r"path\s*=\s*([^\s`]+)", header)
        if not pm:
            continue
        rel = pm.group(1).strip()
        if not safe_rel(rel):
            continue
        target = os.path.join(repo_root, rel)
        write(target, body.strip() + "\n")

def tail(s: str, n: int = 8000) -> str:
    return s[-n:] if s else s

def ts():
    return time.strftime('%Y-%m-%d %H:%M:%S')
