import re

def extract_records(lines):
    """
    Groups EDI lines into logical records based on the S5 segment.
    Returns a list of records, where each record is a list of lines.
    """
    records = []
    current = []

    for line in lines:
        line = line.strip()
        if line.startswith("S5^"):  # Start of a new record
            if current:
                records.append(current)
            current = [line]
        else:
            current.append(line)

    if current:
        records.append(current)

    return records


def find_po_value(record):
    """
    Extracts the PO value from an L11 segment ending with ^PO~
    """
    for line in record:
        if line.startswith("L11^") and line.endswith("^PO~"):
            parts = line.split("^")
            if len(parts) >= 3:
                return parts[1]  # The PO value
    return None


def is_problematic_po(po):
    """
    Applies multiple heuristics to detect dangerous PO values.
    """
    if po is None:
        return False

    # Rule 1: Starts with PO-
    if po.startswith("PO-"):
        return True

    # Rule 2: Contains multiple hyphens with trailing letters
    if re.match(r".+-\d+-[A-Za-z]+$", po):
        return True

    # Rule 3: Contains spaces
    if " " in po:
        return True

    # Rule 4: Too long
    if len(po) > 20:
        return True

    # Rule 5: Contains characters outside safe set
    if not re.match(r"^[A-Za-z0-9\-/]+$", po):
        return True

    return False


def main():
    print("Enter the path to the EDI text file:")
    input_path = input("> ").strip()

    print("Enter the path for the output report file:")
    output_path = input("> ").strip()

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    records = extract_records(lines)

    print(f"\nFound {len(records)} records. Scanning for potential problems...\n")

    flagged = []

    for idx, record in enumerate(records, start=1):
        po = find_po_value(record)
        if is_problematic_po(po):
            flagged.append((idx, po, record))

    # Write results to output file
    try:
        with open(output_path, "w", encoding="utf-8") as out:
            out.write("EDI Problem Record Report\n")
            out.write("=========================\n\n")

            if not flagged:
                out.write("No problematic records detected.\n")
            else:
                for idx, po, record in flagged:
                    out.write(f"Record #{idx}\n")
                    out.write(f"PO Value: {po}\n")
                    out.write("Record Lines:\n")
                    for line in record:
                        out.write("  " + line + "\n")
                    out.write("\n")

        print(f"Scan complete. Results written to:\n{output_path}")

    except Exception as e:
        print(f"Error writing output file: {e}")


if __name__ == "__main__":
    main()