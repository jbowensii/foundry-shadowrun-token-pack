#!/usr/bin/env python3
"""Build the shadowrun-token-pack Foundry module from the extracted RAR."""
import hashlib, json, re, shutil
from pathlib import Path

SCRATCH = Path(r"C:\Users\johnb\AppData\Local\Temp\claude\C--Unreal-Projects-Delving\b9950804-cf78-41c2-95b4-1416bc1f5574\scratchpad")
SRC = SCRATCH / "sr_tokens" / "Shadowrun Tokens"
MOD = SCRATCH / "shadowrun-token-pack"
MODID = "shadowrun-token-pack"
PACKSRC = SCRATCH / "pack_src"   # JSON docs for the CLI compiler

for d in (MOD, PACKSRC):
    if d.exists(): shutil.rmtree(d)
(MOD / "tokens").mkdir(parents=True)
PACKSRC.mkdir(parents=True)

ALNUM = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
def fid(seed: str) -> str:
    """Deterministic 16-char Foundry ID from a seed."""
    h = hashlib.sha256(seed.encode()).digest()
    return "".join(ALNUM[b % 62] for b in h[:16])

def safe(name: str) -> str:
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", name.strip())
    return re.sub(r"-+", "-", s).strip("-")

def pretty(stem: str) -> str:
    # "Human104-alt" -> "Human 104 alt"; "Civilian10" -> "Civilian 10"
    s = re.sub(r"(?<=[a-zA-Z])(?=\d)", " ", stem)
    s = s.replace("-", " ").replace("_", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s.title() if s.islower() else s

def category(stem: str) -> str:
    m = re.match(r"([A-Za-z ]+)", stem)
    c = (m.group(1) if m else "Other").strip().title()
    return c

MAIN_CATS = {"Human","Elf","Troll","Ork","Dwarf","Drone","Spirit"}
MOOK_CATS = {"Civilian","Security","Punk","Professional","Mage"}

sets = [("Tokens", "Runners & Metatypes", MAIN_CATS),
        ("TokenAnon's Mooks", "Mooks", MOOK_CATS)]

folders = {}   # (setlabel, cat) -> folder id
docs = []

def folder_doc(name, _id, parent=None):
    return {"_id": _id, "_key": f"!folders!{_id}", "name": name, "type": "Actor",
            "folder": parent, "sorting": "a", "color": None, "description": "",
            "flags": {}, "sort": 0}

for setdir, setlabel, cats in sets:
    top_id = fid("folder/" + setlabel)
    docs.append(folder_doc(setlabel, top_id))
    srcdir = SRC / setdir
    outsub = safe(setlabel.lower().replace(" & ", "-").replace(" ", "-"))
    (MOD / "tokens" / outsub).mkdir(parents=True, exist_ok=True)
    for png in sorted(srcdir.glob("*.png")):
        stem = png.stem
        cat = category(stem)
        if cat not in cats: cat = "Other"
        fkey = (setlabel, cat)
        if fkey not in folders:
            fid_ = fid(f"folder/{setlabel}/{cat}")
            folders[fkey] = fid_
            docs.append(folder_doc(cat, fid_, top_id))
        fname = safe(stem) + ".png"
        shutil.copy2(png, MOD / "tokens" / outsub / fname)
        img = f"modules/{MODID}/tokens/{outsub}/{fname}"
        name = pretty(stem)
        aid = fid(f"actor/{setlabel}/{stem}")
        docs.append({
            "_id": aid, "_key": f"!actors!{aid}",
            "name": name, "type": "NPC", "img": img,
            "system": {}, "items": [], "effects": [],
            "folder": folders[fkey], "sort": 0, "flags": {},
            "prototypeToken": {
                "name": name, "displayName": 0, "actorLink": False,
                "width": 1, "height": 1, "disposition": 0,
                "texture": {"src": img, "scaleX": 1, "scaleY": 1},
            },
            "ownership": {"default": 0},
        })

for d in docs:
    kind = "folder" if d["_key"].startswith("!folders!") else "actor"
    (PACKSRC / f"{kind}_{safe(d['name'])}_{d['_id']}.json").write_text(
        json.dumps(d, indent=2), encoding="utf-8")

readme_src = next(SRC.glob("*.txt"), None)
credits = readme_src.read_text(encoding="utf-8", errors="ignore") if readme_src else ""
(MOD / "CREDITS.txt").write_text(
    "Community Shadowrun token pack by ThisIsWildDog (tokens) and TokenAnon (/srg/ mooks).\n"
    "Art from Shadowrun: Returns / Dragonfall / Hong Kong (Harebrained Schemes).\n"
    "Original readme follows.\n\n" + credits, encoding="utf-8")

module_json = {
    "id": MODID,
    "title": "Shadowrun Token Pack (Community)",
    "description": "907 community-made Shadowrun tokens (ThisIsWildDog & TokenAnon) as a drag-and-drop Actor compendium plus browsable image folders. Art from the Shadowrun: Returns series. For personal use.",
    "version": "1.0.0",
    "authors": [{"name": "ThisIsWildDog & TokenAnon (packaged by John Bowens)"}],
    "compatibility": {"minimum": "13", "verified": "13"},
    "relationships": {"systems": [{"id": "shadowrun6-eden", "type": "system", "compatibility": {}}]},
    "packs": [{
        "name": "sr-tokens",
        "label": "Shadowrun Tokens (907)",
        "path": "packs/sr-tokens",
        "type": "Actor",
        "system": "shadowrun6-eden",
        "ownership": {"PLAYER": "OBSERVER", "ASSISTANT": "OWNER"}
    }],
    "media": [],
    "url": "", "manifest": "", "download": ""
}
(MOD / "module.json").write_text(json.dumps(module_json, indent=2), encoding="utf-8")

n_actors = sum(1 for d in docs if d["_key"].startswith("!actors!"))
n_folders = len(docs) - n_actors
print(f"actors: {n_actors}, folders: {n_folders}, pack src: {PACKSRC}")
print("module dir:", MOD)
