#!/usr/bin/env python3
"""Materialize the skill's canonical preview without network dependencies."""
import argparse
import json
from pathlib import Path

def prepare(output_dir: Path, fragment_dir: Path) -> dict:
    skill = Path(__file__).resolve().parents[1]
    fragment = (skill / "assets" / "preview.html").read_text(encoding="utf-8")
    output_dir.mkdir(parents=True, exist_ok=True)
    fragment_dir.mkdir(parents=True, exist_ok=True)
    fragment_path = fragment_dir / "web-interactions-preview.html"
    page_path = output_dir / "网页交互效果预览.html"
    if fragment_path.resolve() == (skill / "assets" / "preview.html").resolve():
        raise ValueError("Choose an output directory outside the canonical skill asset.")
    fragment_path.write_text(fragment, encoding="utf-8")
    css = """
    :root{color-scheme:light dark;--font-size-base:14px;--background:#fff;--foreground:#202724;--card:#f2f5f3;--card-foreground:#202724;--primary:#243f35;--primary-foreground:#fff;--secondary:#e3eae6;--secondary-foreground:#263b32;--muted:#eef2ef;--muted-foreground:#52665a;--border:#c9d5ce;--blue:#227b66;--viz-series-1:#227b66;--accent:#e7f0eb;--accent-foreground:#20392c;--ring:#227b66}
    @media(prefers-color-scheme:dark){:root{--background:#181d1a;--foreground:#edf4ee;--card:#232c27;--card-foreground:#edf4ee;--primary:#d9eee0;--primary-foreground:#18271c;--secondary:#34473b;--secondary-foreground:#edf4ee;--muted:#23322a;--muted-foreground:#b4c7ba;--border:#4c6254;--blue:#71c4a6;--viz-series-1:#71c4a6;--accent:#334a3b;--accent-foreground:#e5f3e9;--ring:#71c4a6}}
    *{box-sizing:border-box}body{margin:0;background:var(--background);color:var(--foreground);font:400 14px/1.5 system-ui,-apple-system,'PingFang SC',sans-serif}main{max-width:1040px;margin:32px auto;padding:0 24px}h1,h2,h3,p{margin:0;font-weight:500}h2{font-size:20px}h3{font-size:15px}.text-small{font-size:12px}.text-muted{color:var(--muted-foreground)}.tabular-nums{font-variant-numeric:tabular-nums}.card{padding:16px;border:1px solid var(--border);border-radius:12px;background:var(--card);color:var(--card-foreground)}.btn{font:inherit;padding:8px 12px;min-height:38px;background:transparent;color:var(--foreground);border:1px solid var(--border);border-radius:7px;text-align:left;cursor:pointer;white-space:normal;overflow-wrap:anywhere}.btn:hover{background:var(--accent);color:var(--accent-foreground)}.btn-primary,.btn[aria-pressed=true]{background:var(--primary);color:var(--primary-foreground);border-color:var(--primary)}.btn:focus-visible,input:focus-visible,textarea:focus-visible,summary:focus-visible{outline:3px solid var(--ring);outline-offset:3px}.viz-controls{display:flex;align-items:center;flex-wrap:wrap;gap:10px}.form-check{display:flex;align-items:center;gap:8px}.form-check-input{accent-color:var(--primary)}.form-label{display:block;margin-bottom:6px}.form-range{width:100%;accent-color:var(--primary)}.form-control{font:inherit;width:100%;border:1px solid var(--border);background:var(--background);color:var(--foreground);border-radius:6px;padding:10px}.cursor-interaction{cursor:pointer}summary{cursor:pointer}details>*+*{margin-top:10px}@media(pointer:coarse){.btn{min-height:44px}.form-control{font-size:16px}}@media(max-width:480px){main{margin:16px auto;padding:0 12px}}
    """
    document = "<!doctype html><html lang=\"zh-CN\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>网页交互效果预览</title><style>" + css + "</style></head><body><main>" + fragment + "</main></body></html>"
    page_path.write_text(document, encoding="utf-8")
    return {"fragment": str(fragment_path.resolve()), "standalone": str(page_path.resolve()), "effects": 28}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--fragment-dir", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(prepare(args.output_dir, args.fragment_dir), ensure_ascii=False))
