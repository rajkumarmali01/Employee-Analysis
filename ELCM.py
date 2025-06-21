import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Employee Data Processor", layout="wide")
st.title("Employee Data with Seating Details")

# Upload main employee data
main_file = st.file_uploader("Upload Main Employee Data CSV", type=["csv"], key="main")
seating_file = st.file_uploader("Upload Seating Details CSV", type=["csv"], key="seating")

if main_file is not None:
    try:
        # Read main CSV
        df_main = pd.read_csv(main_file, encoding='latin1')
        
        # Required columns for main data
        required_columns = [
            'Employee Code', 'Name of Employee', 'Employment Status',
            'Employee Type', 'Location Name', 'Date of Joining',
            'Department 1.0', 'Location Code', 'Location City'
        ]
        
        # Check for missing columns
        missing_cols = [col for col in required_columns if col not in df_main.columns]
        if missing_cols:
            st.error(f"Missing columns in main data: {', '.join(missing_cols)}")
        else:
            df_main = df_main[required_columns].copy()
            
            # Process date column
            oct1_2024 = datetime(2024, 10, 1)
            df_main['Date of Joining'] = pd.to_datetime(df_main['Date of Joining'], errors='coerce')
            df_main['New join / movment'] = df_main['Date of Joining'].apply(
                lambda x: 'New Join' if pd.notnull(x) and x > oct1_2024 else 'Movement'
            )
            
            # Process location column
            df_main['Ahmedabad / Out side Ahmedabad'] = df_main['Location City'].apply(
                lambda x: 'Ahmedabad' if str(x).strip().lower() == 'ahmedabad' else 'Out side Ahmedabad'
            )
            
            # Process department column
            df_main['Department 1.0'] = df_main['Department 1.0'].astype(str).str.strip().str.upper()
            df_main['Old GCC / New GCC'] = df_main['Department 1.0'].apply(
                lambda x: 'Old GCC' if any(d in x for d in ['ABEX - GCC', 'GROUP DATA GOVERNANCE AND CONTROL - GCC']) 
                else 'New GCC'
            )
            
            # Process seating details if uploaded
            if seating_file is not None:
                try:
                    df_seating = pd.read_csv(seating_file, encoding='latin1')
                    
                    # Required seating columns
                    seating_columns = [
                        'Employee ID ', 'Building Name ', 'Floor', 
                        'Wing', 'WS Number ', 'WS Type '
                    ]
                    
                    # Check for missing seating columns
                    missing_seating = [col for col in seating_columns if col not in df_seating.columns]
                    if missing_seating:
                        st.warning(f"Missing columns in seating data: {', '.join(missing_seating)}")
                    else:
                        # Select only required seating columns
                        df_seating = df_seating[seating_columns].copy()
                        
                        # Merge seating details with main data
                        df_merged = pd.merge(
                            df_main,
                            df_seating,
                            left_on='Employee Code',
                            right_on='Employee ID',
                            how='left'
                        )
                        
                        # Drop the duplicate 'Employee ID' column after merge
                        df_merged = df_merged.drop(columns=['Employee ID'], errors='ignore')
                        
                        # Show merged data
                        st.success("Data processed with seating details!")
                        st.dataframe(df_merged)
                        
                        # Download merged data
                        csv = df_merged.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Download Data with Seating Details",
                            data=csv,
                            file_name="employee_data_with_seating.csv",
                            mime="text/csv"
                        )
                        # Set df_main to merged for display
                        df_main = df_merged
                
                except Exception as e:
                    st.error(f"Error processing seating file: {str(e)}")
            
            # If no seating file uploaded, show main data
            if seating_file is None:
                st.success("Data processed successfully!")
                st.dataframe(df_main)
                
                csv = df_main.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Processed Data",
                    data=csv,
                    file_name="processed_employee_data.csv",
                    mime="text/csv"
                )
            
    except Exception as e:
        st.error(f"Error processing main file: {str(e)}")
else:
    st.info("Please upload the main employee data CSV file to get started")
