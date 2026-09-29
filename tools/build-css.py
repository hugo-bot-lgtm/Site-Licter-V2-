#!/usr/bin/env python3
"""Builds css/styles.min.css from css/styles.css.

styles.css stays the file you edit, comments and history included; the pages
load the built copy. Run after every change to styles.css:

    python3 tools/build-css.py

The build does three things, all without changing what renders:
  1. drops comments and whitespace;
  2. drops selectors whose classes or ids appear in no HTML or JS file
     (dead rules left behind by earlier versions of a component);
  3. drops a declaration when the very same selector, in the very same
     @media / @supports context, sets the same property again further down
     (the later one always wins, so the earlier one never shows).
"""
import re, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
src = (root / "css" / "styles.css").read_text()
sources = "\n".join(p.read_text() for p in list(root.glob("*.html")) + list((root / "js").glob("*.js")))

# ---------------------------------------------------------------- parse
css = re.sub(r"/\*.*?\*/", "", src, flags=re.S)

def parse(text, i=0):
    """[('rule', selector, body) | ('at', prelude, children|None, raw)]"""
    out = []
    n = len(text)
    while i < n:
        j = i
        while j < n and text[j] not in "{};}":
            j += 1
        if j >= n:
            break
        head = text[i:j].strip()
        if text[j] == "}":
            return out, j + 1
        if text[j] == ";":                      # @import / @charset
            if head:
                out.append(("stmt", head))
            i = j + 1
            continue
        # text[j] == "{"
        if head.startswith("@") and re.match(r"@(media|supports|layer|container)\b", head):
            children, k = parse(text, j + 1)
            out.append(("at", head, children))
            i = k
        else:
            depth, k = 1, j + 1
            while k < n and depth:
                if text[k] == "{": depth += 1
                elif text[k] == "}": depth -= 1
                k += 1
            body = text[j + 1:k - 1]
            out.append(("raw" if head.startswith("@") else "rule", head, body))
            i = k
    return out, i

tree, _ = parse(css)

# ------------------------------------------------------- 2. dead selectors
known = {}
def used(token, kind):
    key = kind + token
    if key not in known:
        ok = token in sources
        if not ok and "--" in token:            # "word--" + tone, built in JS
            ok = (token.split("--")[0] + "--") in sources
        if not ok and "__" in token and kind == ".":
            ok = False
        known[key] = ok
    return known[key]

def split_top(sel):
    parts, depth, cur = [], 0, ""
    for ch in sel:
        if ch == "(": depth += 1
        elif ch == ")": depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur); cur = ""
        else:
            cur += ch
    parts.append(cur)
    return [p.strip() for p in parts if p.strip()]

def alive(sel):
    bare = re.sub(r":(not|is|where|has)\((?:[^()]|\([^()]*\))*\)", "", sel)   # what is only a condition
    for c in re.findall(r"\.(-?[_a-zA-Z][\w-]*)", bare):
        if not used(c, "."): return False
    for c in re.findall(r"#(-?[_a-zA-Z][\w-]*)", bare):
        if not used(c, "#"): return False
    return True

dropped_sel = 0
def prune(nodes):
    global dropped_sel
    out = []
    for node in nodes:
        if node[0] == "rule":
            sels = split_top(node[1])
            keep = [s for s in sels if alive(s)]
            dropped_sel += len(sels) - len(keep)
            if keep:
                out.append(("rule", ",".join(keep), node[2]))
        elif node[0] == "at":
            kids = prune(node[2])
            if kids:
                out.append(("at", node[1], kids))
        else:
            out.append(node)
    return out

tree = prune(tree)

# ------------------------------------------------ 3. overridden declarations
def decls(body):
    out, depth, cur = [], 0, ""
    for ch in body:
        if ch == "(": depth += 1
        elif ch == ")": depth -= 1
        if ch == ";" and depth == 0:
            if cur.strip(): out.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip(): out.append(cur.strip())
    return out

dropped_decl = 0
def dedupe(nodes):
    global dropped_decl
    # later (selector, property) pairs in this same context, walking backwards
    seen = set()
    result = []
    for node in reversed(nodes):
        if node[0] == "rule":
            sel = re.sub(r"\s+", " ", node[1])
            keep = []
            for d in reversed(decls(node[2])):
                if ":" not in d:
                    keep.append(d); continue
                prop = d.split(":", 1)[0].strip().lower()
                important = "!important" in d
                key = (sel, prop)
                if key in seen and not important:
                    dropped_decl += 1
                    continue
                if not important:
                    seen.add(key)
                keep.append(d)
            keep.reverse()
            if keep:
                result.append(("rule", node[1], ";".join(keep)))
        elif node[0] == "at":
            result.append(("at", node[1], dedupe(node[2])))
        else:
            result.append(node)
    result.reverse()
    return result

tree = dedupe(tree)

# ------------------------------------------------------------ 1. print
def mini(s):
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s*([{};,>])\s*", r"\1", s)
    return s.strip()

def emit(nodes):
    out = []
    for node in nodes:
        if node[0] == "rule":
            body = ";".join(mini(re.sub(r"\s*:\s*", ":", d, count=1)) for d in decls(node[2]))
            out.append(mini(node[1]) + "{" + body + "}")
        elif node[0] == "at":
            out.append(mini(node[1]) + "{" + emit(node[2]) + "}")
        elif node[0] == "raw":
            out.append(mini(node[1]) + "{" + mini(node[2]) + "}")
        else:
            out.append(mini(node[1]) + ";")
    return "".join(out)

min_css = emit(tree)
(root / "css" / "styles.min.css").write_text(min_css + "\n")
print("styles.min.css: %d KB -> %d KB (%d dead selectors, %d overridden declarations dropped)"
      % (len(src.encode()) // 1024, len(min_css.encode()) // 1024, dropped_sel, dropped_decl))
