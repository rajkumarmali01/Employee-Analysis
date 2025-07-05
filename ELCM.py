import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Employee Analysis", layout="wide")
st.title("GCC Employee Analysis 🏢 | Department X | Seating X | ⌚ Security")

# Upload files
main_file = st.file_uploader("Upload Main Employee Data CSV (ELCM)", type=["csv"], key="main")
seating_file = st.file_uploader("Upload Master Seating Data CSV", type=["csv"], key="seating")

# Main File Handling
if main_file is not None:
    try:
        df_main = pd.read_csv(main_file, encoding='latin1')
        df_main.columns = df_main.columns.str.strip()

        st.write("📋 Columns in Main Employee Data:", df_main.columns.tolist())

        required_columns = [
            'Employee Code', 'Name of Employee', 'Employment Status',
            'Employee Type', 'Location Name', 'Date of Joining',
            'Date of Separation',  # ✅ Added this column
            'Department 1.0', 'Location Code', 'Location City'
        ]
        missing_cols = [col for col in required_columns if col not in df_main.columns]
        if missing_cols:
            st.error(f"Missing columns in main data: {', '.join(missing_cols)}")
        else:
            df_main = df_main[required_columns].copy()

            # Convert dates
            df_main['Date of Joining'] = pd.to_datetime(df_main['Date of Joining'], errors='coerce')
            df_main['Date of Separation'] = pd.to_datetime(df_main['Date of Separation'], errors='coerce')

            # Derived columns
            oct1_2024 = datetime(2024, 10, 1)
            df_main['New join / movment'] = df_main['Date of Joining'].apply(
                lambda x: 'New Join' if pd.notnull(x) and x > oct1_2024 else 'Movement'
            )
            df_main['Ahmedabad / Out side Ahmedabad'] = df_main['Location City'].apply(
                lambda x: 'Ahmedabad' if str(x).strip().lower() == 'ahmedabad' else 'Out side Ahmedabad'
            )
            df_main['Department 1.0'] = df_main['Department 1.0'].astype(str).str.strip().str.upper()
            df_main['Old GCC / New GCC'] = df_main['Department 1.0'].apply(
                lambda x: 'Old GCC' if any(d in x for d in ['ABEX - GCC', 'GROUP DATA GOVERNANCE AND CONTROL - GCC'])
                else 'New GCC'
            )

            # Seating File Handling
            if seating_file is not None:
                try:
                    df_seating = pd.read_csv(seating_file, encoding='latin1')
                    df_seating.columns = df_seating.columns.str.strip()

                    st.write("🪑 Columns in Seating Data:", df_seating.columns.tolist())

                    seating_columns = [
                        'Employee ID', 'Building Name', 'Floor', 'Wing', 'WS Number', 'WS Type'
                    ]
                    missing_seating = [col for col in seating_columns if col not in df_seating.columns]
                    if missing_seating:
                        st.error(f"Missing columns in seating file: {', '.join(missing_seating)}")
                    else:
                        # Preprocess keys
                        df_main['Employee Code'] = df_main['Employee Code'].astype(str).str.strip()
                        df_seating['Employee ID'] = df_seating['Employee ID'].astype(str).str.strip()

                        # Filter required columns
                        df_seating = df_seating[seating_columns].copy()

                        # Rename for merging
                        df_seating.rename(columns={'Employee ID': 'Employee Code'}, inplace=True)

                        # Merge
                        df_merged = pd.merge(df_main, df_seating, on='Employee Code', how='left')
                        st.success("✅ Data processed with seating details!")
                        st.dataframe(df_merged)

                        csv = df_merged.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Download Data with Seating Details",
                            data=csv,
                            file_name="employee_data_with_seating.csv",
                            mime="text/csv"
                        )

                        df_main = df_merged  # Update main to merged for consistency
                except Exception as e:
                    st.error(f"❌ Error processing seating file: {str(e)}")

            # If seating file not uploaded, still show processed main file
            if seating_file is None:
                st.success("✅ Data processed successfully!")
                st.dataframe(df_main)

                csv = df_main.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Processed Data",
                    data=csv,
                    file_name="processed_employee_data.csv",
                    mime="text/csv"
                )

    except Exception as e:
        st.error(f"❌ Error processing main file: {str(e)}")

else:
    st.info("📤 Please upload the Main Employee Data CSV to get started.")