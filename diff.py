import zipfile
import os
import subprocess
import difflib
from pathlib import Path

CFR_JAR = "/path/to/cfr.jar"   # download from https://github.com/leibnitz27/cfr

def extract_jar(jar_path, extract_to):
    with zipfile.ZipFile(jar_path, 'r') as jar:
        jar.extractall(extract_to)

def decompile_class(class_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    subprocess.run([
        "java", "-jar", CFR_JAR,
        class_path, "--outputdir", output_dir, "--silent", "true"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def collect_classes(base_dir, decompiled_dir):
    file_map = {}
    for root, _, files in os.walk(base_dir):
        for f in files:
            if f.endswith(".class"):
                rel_path = os.path.relpath(os.path.join(root, f), base_dir)
                java_rel = rel_path.replace(".class", ".java")
                class_file = os.path.join(root, f)
                java_file = os.path.join(decompiled_dir, java_rel)

                # Decompile
                out_dir = os.path.dirname(java_file)
                decompile_class(class_file, out_dir)

                if os.path.exists(java_file):
                    with open(java_file, "r", errors="ignore") as jf:
                        content = jf.readlines()
                else:
                    content = []

                file_map[java_rel.replace("\\", "/")] = content
    return file_map

def compare_jars_code(jar1, jar2, report_file="jar_code_diff_report.html"):
    dir1, dir2 = "jar1_classes", "jar2_classes"
    decompiled1, decompiled2 = "jar1_java", "jar2_java"

    os.makedirs(dir1, exist_ok=True)
    os.makedirs(dir2, exist_ok=True)
    os.makedirs(decompiled1, exist_ok=True)
    os.makedirs(decompiled2, exist_ok=True)

    extract_jar(jar1, dir1)
    extract_jar(jar2, dir2)

    files1 = collect_classes(dir1, decompiled1)
    files2 = collect_classes(dir2, decompiled2)

    all_files = sorted(set(files1.keys()) | set(files2.keys()))

    # Counters
    identical_count = 0
    modified_count = 0
    only_in_jar1 = 0
    only_in_jar2 = 0

    rows = []

    for f in all_files:
        src1 = files1.get(f)
        src2 = files2.get(f)

        if src1 is None:
            only_in_jar2 += 1
            status = f"<span class='missing'>Only in {jar2} ✘</span>"
        elif src2 is None:
            only_in_jar1 += 1
            status = f"<span class='missing'>Only in {jar1} ✘</span>"
        else:
            if src1 == src2:
                identical_count += 1
                status = "<span class='identical'>Identical ✓</span>"
            else:
                modified_count += 1
                diff_file = f"diff_{f.replace('/', '_')}.html"
                diff_html = difflib.HtmlDiff().make_file(
                    src1, src2, fromdesc=jar1, todesc=jar2
                )
                os.makedirs("diffs", exist_ok=True)
                with open(os.path.join("diffs", diff_file), "w", encoding="utf-8") as df:
                    df.write(diff_html)
                status = f"<span class='different'>Modified ≠</span> (<a href='diffs/{diff_file}'>View Diff</a>)"

        rows.append(f"<tr><td>{f}</td><td>{status}</td></tr>")

    # HTML Output
    html = ["<html><head><style>",
            "table {border-collapse: collapse; width: 100%; font-family: monospace;}",
            "td, th {border: 1px solid #999; padding: 4px;}",
            ".identical {color: green; font-weight: bold;}",
            ".different {color: orange; font-weight: bold;}",
            ".missing {color: red; font-weight: bold;}",
            ".summary {margin-bottom: 20px; padding: 10px; border: 1px solid #999; width: 40%;}",
            "</style></head><body>",
            f"<h2>JAR Code Diff Report</h2><p>Comparing: <b>{jar1}</b> vs <b>{jar2}</b></p>"]

    # Summary Dashboard
    html.append("<div class='summary'><h3>Summary</h3><ul>")
    html.append(f"<li class='identical'>Identical: {identical_count}</li>")
    html.append(f"<li class='different'>Modified: {modified_count}</li>")
    html.append(f"<li class='missing'>Only in {jar1}: {only_in_jar1}</li>")
    html.append(f"<li class='missing'>Only in {jar2}: {only_in_jar2}</li>")
    html.append("</ul></div>")

    # File-level table
    html.append("<table><tr><th>Class</th><th>Status</th></tr>")
    html.extend(rows)
    html.append("</table></body></html>")

    with open(report_file, "w", encoding="utf-8") as f:
        f.write("\n".join(html))

    print(f"Code diff report generated: {report_file}")


if __name__ == "__main__":
    compare_jars_code("old.jar", "new.jar")
