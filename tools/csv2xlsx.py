import pandas as pd
import os


def generate_risk_xlsx(
    csv_path: str = "02-Matrices/risk_matrix.csv",
    output_path: str = "docs/reports/risk_matrix.xlsx",
) -> None:
    """
    Reads the risk matrix CSV, calculates Risk (P*I), and exports the data to an Excel file.
    """
    try:
        # 1. Read the CSV file
        df = pd.read_csv(csv_path, sep=",")

        # 2. Basic Data Cleaning (ensure proper types for calculation)
        df["Probability"] = pd.to_numeric(df["Probability"], errors="coerce")
        df["Impact"] = pd.to_numeric(df["Impact"], errors="coerce")

        # 3. Recalculate Risk
        df["Risk"] = df["Probability"] * df["Impact"]

        # 4. Sort the DataFrame by Risk (descending) and Impact (descending)
        df = df.sort_values(by=["Risk", "Impact"], ascending=[False, False])

        # 5. Export to Excel
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        df.to_excel(output_path, index=False, sheet_name="Risk_Matrix")

        print(f"\nSUCCESS: Risk matrix processed and saved to: {output_path}")
        print(f"   Total risks processed: {len(df)}")
        print("   Top 3 Risks (Score):")
        print(df[["ID", "Asset", "Risk"]].head(3).to_markdown(index=False))

    except FileNotFoundError:
        print(f"ERROR: CSV file not found at {csv_path}. Please ensure the file exists.")
    except Exception as e:
        print(f"ERROR during Excel generation: {e}")


if __name__ == "__main__":
    generate_risk_xlsx()
