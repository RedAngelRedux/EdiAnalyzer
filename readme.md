# 📦 EDI Problem Record Detector  
### A Python utility for identifying malformed or high‑risk EDI records before import

This project provides a lightweight Python tool that scans EDI 204‑style shipment files and identifies records that may cause downstream failures in reporting tools such as Crystal Reports or Infragistics grids. It was built to solve a real production issue where certain EDI records imported cleanly into SQL Server but caused application crashes during report generation.

The detector uses a set of carefully refined heuristics based on real‑world data analysis to flag only the records that are known to cause failures — without generating noise or false positives.

---

## 🚀 Why This Tool Exists

In a logistics workflow, EDI files often contain hundreds of shipment records. While most records import cleanly, a small number may contain **PO values with structural patterns that confuse Crystal Reports’ datatype inference**, leading to:

- Report generation crashes  
- Grid binding failures  
- Hard‑to‑trace runtime exceptions  

Because the import step succeeds, the problematic records aren’t discovered until much later in the workflow — often by end users.

This tool solves that problem by **pre‑screening EDI files** and flagging only the records that match the structural patterns known to cause failures.

---

## 🧠 How It Works

The detector analyzes each EDI record, extracts the PO value from the `L11` segment, and applies a set of rules derived from extensive testing across multiple real‑world EDI files.

### ✔ A PO is flagged as problematic if:

#### **Rule A — It begins with `PO-` AND the segment after `PO-` begins with a digit**
Examples:
- `PO-005259`
- `PO-005229 Shelley`

These patterns resemble structured numeric identifiers, which Crystal Reports attempts to parse as numbers — causing crashes when other POs in the dataset are textual.

#### **Rule B — The PO does *not* start with `PO-`, but the first segment is numeric AND the PO contains two or more hyphens**
Examples:
- `4500724750-4809-III`
- `89673-NP-Centralia C`

These resemble hierarchical numeric codes, which also trigger Crystal’s numeric inference logic.

### ✔ What the tool does *not* flag:

- Free‑text POs  
- Date‑like POs  
- Simple hyphenated identifiers  
- Alphanumeric codes with letters in the first post‑hyphen segment  
- Any PO that does not match the structural patterns known to cause failures  

This ensures **high precision** and avoids false positives.

---

## 📁 Example Output

The tool generates a clean text report listing only the records that match the detection rules:

```
EDI Problem Record Report
=========================

Record #188
PO Value: PO-005259
Record Lines:
  S5^0^00~
  L11^12214K22T739251S^2I~
  L11^4K22T739^ACI~
  L11^PO-005259^PO~
  ...
```

---

## 🛠️ Usage

1. Run the script:

```
python edi_scanner.py
```

2. Enter the path to the EDI file you want to scan.

3. Enter the path where you want the output report saved.

The script will analyze the file, apply the detection rules, and write a clean, human‑readable report of any problematic records.

---

## 📂 Project Structure

```
/
├── edi_scanner.py     # Main detection script
├── README.md          # Project documentation
└── sample_data/       # (Optional) Example EDI files for testing
```

---

## 🧪 Development Notes

This tool was developed through iterative testing across multiple EDI files containing both known‑good and known‑bad records. Each detection rule was validated against:

- Confirmed crash‑inducing records  
- False positives from earlier rule versions  
- A wide variety of real‑world PO formats  

The final rule set reflects the **minimum necessary conditions** to reliably detect problematic records without over‑flagging.

---

## 🎯 Skills Demonstrated

This project highlights:

- Real‑world debugging and root‑cause analysis  
- Pattern recognition in semi‑structured data  
- Defensive programming and data validation  
- Python scripting for automation  
- Understanding of EDI formats and reporting tool behavior  
- Iterative refinement based on empirical evidence  

It’s a practical example of taking a vague production issue and turning it into a repeatable, automated solution.

---

## 📄 License

MIT License — feel free to use, modify, or extend this tool.

---

# 👤 About the Author

**Sammy Nava** is a technical consultant, systems troubleshooter, and full‑stack problem solver based in Garland, Texas. He brings a rare blend of hands‑on business leadership and deep technical capability, shaped by years of building tools, workflows, and infrastructure that keep real companies running smoothly.

Sammy’s work spans everything from Python automation and data validation to Windows application development, SQL Server workflows, and EDI processing. He has a reputation for taking messy, ambiguous problems and turning them into clean, maintainable solutions — often uncovering root causes that others overlook. His approach is methodical, evidence‑driven, and grounded in real‑world constraints.

He’s also the owner of multiple businesses, including a web agency and Texas Floors & Restoration, which gives him a practical understanding of how software impacts operations, customers, and teams. That perspective shows up in his code: clear, reliable, and built for people who depend on it.

Sammy enjoys creating tools that make life easier for others — whether that’s automating a tedious workflow, building a validation engine, or designing a clean user experience. He values clarity, maintainability, and thoughtful engineering, and he brings those values into every project he touches.

