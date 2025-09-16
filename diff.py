import os, zipfile, shutil, subprocess, difflib, pathlib, argparse, logging

# ---------------- Logger Setup ----------------
def setup_logger(logfile="jar_diff.log"):
    logger = logging.getLogger("JarDiff")
    logger.setLevel(logging.DEBUG)

    # Console handler (INFO only)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch_formatter = logging.Formatter("[%(levelname)s] %(message)s")
    ch.setFormatter(ch_formatter)

    # File handler (DEBUG for detailed trace)
    fh = logging.FileHandler(logfile, mode="w", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    fh.setFormatter(fh_formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger

logger = setup_logger()

# ---------------- Core Functions ----------------
def unzip_jar(jar, outdir):
    logger.info(f"Unzipping {jar} -> {outdir}")
    shutil.rmtree(outdir, ignore_errors=True)
    os.makedirs(outdir, exist_ok=True)
    with zipfile.ZipFile(jar, 'r') as z:
        z.extractall(outdir)
    logger.debug(f"Extracted {len(z.namelist())} files from {jar}")

def collect_files(base):
    result = []
    for root, _, files in os.walk(base):
        for f in files:
            if f.endswith(".class"):
                result.append(os.path.relpath(os.path.join(root, f), base))
    logger.info(f"Collected {len(result)} .class files from {base}")
    return sorted(result)

def javap(class_rel, base):
    fqcn = class_rel[:-6].replace("/", ".")
    cmd = ["javap", "-p", "-c", "-s", "-classpath", base, fqcn]
    logger.debug(f"Running javap on {fqcn}")
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.stderr:
        logger.warning(f"javap warning for {fqcn}: {proc.stderr.strip()}")
    return proc.stdout.splitlines()

def decompile_cfr(class_rel, base, cfr_jar="cfr.jar"):
    path = os.path.join(base, class_rel)
    logger.debug(f"Decompiling with CFR: {path}")
    cmd = ["java", "-jar", cfr_jar, path, "--silent", "--comments", "false"]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.stderr:
        logger.warning(f"CFR warning for {class_rel}: {proc.stderr.strip()}")
    return proc.stdout.splitlines()

def diff_files(class_rel, old_base, new_base, report_dir, mode, cfr_jar):
    logger.info(f"Diffing {class_rel} in {mode} mode")
    if os.path.exists(os.path.join(old_base, class_rel)):
        old_txt = javap(class_rel, old_base) if mode=="bytecode" else decompile_cfr(class_rel, old_base, cfr_jar)
    else:
        old_txt = []
        logger.debug(f"Missing in OLD: {class_rel}")

    if os.path.exists(os.path.join(new_base, class_rel)):
        new_txt = javap(class_rel, new_base) if mode=="bytecode" else decompile_cfr(class_rel, new_base, cfr_jar)
    else:
        new_txt = []
        logger.debug(f"Missing in NEW: {class_rel}")

    diff_html = difflib.HtmlDiff().make_file(old_txt, new_txt, "OLD/"+class_rel, "NEW/"+class_rel)
    outpath = os.path.join(report_dir, class_rel.replace("/", "_")+".html")
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(diff_html)
    return pathlib.Path(outpath).name

def build_index(report_dir, files, links):
    logger.info("Building index.html")
    html = ["<html><head><style>",
            "ul{list-style:none;} li{margin-left:20px;} .folder{font-weight:bold;cursor:pointer;}",
            "iframe{border:1px solid #ccc;}",
            "</style>",
            "<script>",
            "function toggle(e){var ul=e.nextElementSibling;ul.style.display=(ul.style.display=='none'?'block':'none');}",
            "</script>",
            "</head><body><h1>JAR Diff Report</h1><ul>"]

    tree = {}
    for f, link in zip(files, links):
        parts = f.split("/")
        node = tree
        for p in parts[:-1]:
            node = node.setdefault(p, {})
        node[parts[-1]] = link

    def render(node):
        html.append("<ul>")
        for k, v in sorted(node.items()):
            if isinstance(v, dict):
                html.append(f"<li class='folder' onclick='toggle(this)'>{k}</li>")
                render(v)
            else:
                html.append(f"<li><a href='{v}' target='right'>{k}</a></li>")
        html.append("</ul>")

    render(tree)
    html.append("</ul><iframe name='right' width='100%' height='800px'></iframe></body></html>")
    with open(os.path.join(report_dir, "index.html"), "w") as f:
        f.write("\n".join(html))

def main(oldjar, newjar, report_dir, mode, cfr_jar):
    old_unzip, new_unzip = "old_unzipped", "new_unzipped"
    unzip_jar(oldjar, old_unzip)
    unzip_jar(newjar, new_unzip)

    files = sorted(set(collect_files(old_unzip)) | set(collect_files(new_unzip)))
    os.makedirs(report_dir, exist_ok=True)

    links = []
    for f in files:
        links.append(diff_files(f, old_unzip, new_unzipped, report_dir, mode, cfr_jar))

    build_index(report_dir, files, links)
    logger.info(f"✅ Report generated: {report_dir}/index.html")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Beyond Compare–style JAR diff")
    parser.add_argument("oldjar", help="Path to old JAR")
    parser.add_argument("newjar", help="Path to new JAR")
    parser.add_argument("--mode", choices=["bytecode","source"], default="bytecode", help="Diff mode")
    parser.add_argument("--cfr", default="cfr.jar", help="Path to CFR jar (if mode=source)")
    parser.add_argument("--out", default="report", help="Report output dir")
    parser.add_argument("--log", default="jar_diff.log", help="Log file path")
    args = parser.parse_args()

    # Reset logger with custom file
    global logger
    logger = setup_logger(args.log)

    main(args.oldjar, args.newjar, args.out, args.mode, args.cfr)
