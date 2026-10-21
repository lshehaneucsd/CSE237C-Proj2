import sys
import subprocess
import re
import os
import shutil
import glob

TOP_MODULE_NAME = "cordiccart2pol"
BASE_SOURCE_DIR = "."
QUESTIONS_DIR = "questions"
OUTPUT_DIR = "out"
REPORT_NAME = f"{TOP_MODULE_NAME}_csynth.rpt"
TEST_LOG_NAME = f"{TOP_MODULE_NAME}_test.log"

def extract_metrics(vari, text):
    lat = re.search(r"Latency.*?\|\s*(\d+)\s*\|\s*(\d+)\s*\|[^|]*\|[^|]*\|\s*(\d+)\s*\|\s*(\d+)\s*\|", text, re.DOTALL)
    tot = re.search(r"\|\s*Total\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|", text)
    clk = re.search(r"\|\s*ap_clk\s*\|\s*[\d.]+\s*ns\|\s*([\d.]+)\s*ns", text)
    
    latency = lat.group(2) if lat else "NA"
    s_ii = lat.group(4) if lat else "NA"
    bram, dsp, ff, lut = (tot.group(1), tot.group(2), tot.group(3), tot.group(4)) if tot else ("NA", "NA", "NA", "NA")
    
    tp = "NA"
    if clk:
        try:
            c_val = float(s_ii) if s_ii != "NA" else (float(latency) if latency != "NA" else 0)
            if float(clk.group(1)) > 0 and c_val > 0:
                tp = f"{1000.0 / (float(clk.group(1)) * c_val):.3f}"
        except:
            pass

    return [vari, latency, s_ii, bram, dsp, lut, ff, tp]

def extract_rmse(text):
    match = re.search(r"RMSE\(R\)\s+RMSE\(Theta\)\s*\n\s*([\d.eE+-]+)\s+([\d.eE+-]+)", text)
    if match:
        return match.group(1), match.group(2)
    return "NA", "NA"

def run_question(q, varis=None):
    q_dir = os.path.join(QUESTIONS_DIR, q)
    out_dir = os.path.join(OUTPUT_DIR, q)
    os.makedirs(out_dir, exist_ok=True)

    file_pattern = rf"{re.escape(TOP_MODULE_NAME)}_(.+?)\.(h|cpp)"
    
    if not varis:
        varis = sorted(
            list({re.match(file_pattern, os.path.basename(f)).group(1) 
                  for f in glob.glob(os.path.join(q_dir, f"{TOP_MODULE_NAME}_*.*")) 
                  if re.match(file_pattern, os.path.basename(f))}),
            key=lambda x: int(x) if x.isdigit() else x
        )

    rows = [["Design", "Latency", "Sample II", "BRAM", "DSP", "LUT", "FF", "Throughput (MHz)", "RMSE (r)", "RMSE (theta)"]]
    
    for v in varis:
        # Clean up stale files before running this variant so stale metrics are not reused
        for stale in [f"{TOP_MODULE_NAME}_csynth.rpt", f"{TOP_MODULE_NAME}_test.log", f"{TOP_MODULE_NAME}_test.bin"]:
            p = os.path.join(BASE_SOURCE_DIR, stale)
            if os.path.exists(p):
                os.remove(p)

        for ext in ["h", "cpp"]:
            src = os.path.join(q_dir, f"{TOP_MODULE_NAME}_{v}.{ext}")
            dest = os.path.join(BASE_SOURCE_DIR, f"{TOP_MODULE_NAME}.{ext}")
            if os.path.exists(src):
                shutil.copy(src, dest)
            elif ext == "cpp":
                common_src = os.path.join(q_dir, f"{TOP_MODULE_NAME}.{ext}")
                if os.path.exists(common_src):
                    shutil.copy(common_src, dest)

        subprocess.run(["touch", os.path.join(BASE_SOURCE_DIR, f"{TOP_MODULE_NAME}.cpp")])
        test_out = subprocess.run(["make", "test"], cwd=BASE_SOURCE_DIR, capture_output=True, text=True)
        hls_out = subprocess.run(["make", "hls"], cwd=BASE_SOURCE_DIR, capture_output=True, text=True)
        rpt_out = subprocess.run(["make", "report"], cwd=BASE_SOURCE_DIR, capture_output=True, text=True)

        hls_log = (hls_out.stdout or "") + (hls_out.stderr or "") + \
                  (rpt_out.stdout or "") + (rpt_out.stderr or "")

        with open(os.path.join(out_dir, f"{v}_hls.log"), "w") as f:
            f.write(hls_log)

        test_log_txt = ""
        test_log_src = os.path.join(BASE_SOURCE_DIR, TEST_LOG_NAME)
        test_log_dest = os.path.join(out_dir, f"{v}_test.log")
        
        if os.path.exists(test_log_src):
            shutil.copy(test_log_src, test_log_dest)
            with open(test_log_dest, "r") as f:
                test_log_txt = f.read()
        else:
            test_log_txt = (test_out.stdout or "") + (test_out.stderr or "")
            with open(test_log_dest, "w") as f:
                f.write(test_log_txt)

        rpt_txt = ""
        rpt_src = os.path.join(BASE_SOURCE_DIR, REPORT_NAME)
        rpt_dest = os.path.join(out_dir, f"{v}.rpt")
        
        if os.path.exists(rpt_src):
            shutil.copy(rpt_src, rpt_dest)
            with open(rpt_dest, "r") as f: 
                rpt_txt = f.read()

        metrics = extract_metrics(v, hls_log + "\n" + rpt_txt)
        rmse_r, rmse_theta = extract_rmse(test_log_txt)
        metrics.extend([rmse_r, rmse_theta])
        rows.append(metrics)

    with open(os.path.join(out_dir, "_table.md"), "w") as f:
        f.write("| " + " | ".join(rows[0]) + " |\n")
        f.write("|" + "|".join(["---"] * len(rows[0])) + "|\n")
        for r in rows[1:]:
            f.write("| " + " | ".join(str(x) for x in r) + " |\n")

def main():
    q_arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    v_arg = [sys.argv[2]] if len(sys.argv) > 2 else []
    
    targets = [d for d in os.listdir(QUESTIONS_DIR) if os.path.isdir(os.path.join(QUESTIONS_DIR, d))] if q_arg == "all" else [q_arg]
    
    for t in sorted(targets):
        run_question(t, v_arg)

if __name__ == "__main__":
    main()