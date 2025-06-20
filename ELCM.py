import streamlit as st
import pandas as pd
from datetime import datetime

# Streamlit configuration
st.set_page_config(page_title="Employee Data Processor", layout="wide")
st.title("Employee Data Processor")

# File upload
uploaded_file = st.file_uploader("Upload Employee Data Excel Sheet", type=["xlsx", "xls"])

if uploaded_file is not None:
    # Read Excel and select columns
    try:
        df = pd.read_excel(uploaded_file)
        
        # Required columns
        required_columns = [
            'Employee Code', 'Name Of Employee', 'Employement Status',
            'Employee Type', 'Location Name', 'Date of Joining',
            'Department 1.0', 'Location Code', 'Location City'
        ]
        
        # Check for missing columns
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            st.error(f"Missing columns in data: {', '.join(missing_cols)}")
        else:
            # Filter to required columns
            df = df[required_columns].copy()
            
            # 1. New join/movement column
            oct1_2024 = datetime(2024, 10, 1)
            df['New join / movment'] = df['Date of Joining'].apply(
                lambda x: 'New Join' if pd.to_datetime(x) > oct1_2024 else 'Movement'
            )
            
            # 2. AMD/Outside AMD column
            df['AMD / Out side AMD'] = df['Location City'].apply(
                lambda x: 'AMD' if str(x).strip().lower() == 'ahmedabad' else 'Out side AMD'
            )
            
            # 3. Old GCC/New GCC column
            df['Old GCC / New GCC'] = df['Department 1.0'].apply(
                lambda x: 'Old GCC' if str(x).strip().upper() in ['ABEX', 'GDGC'] else 'New GCC'
            )
            
            # Show processed data
            st.success("Data processed successfully!")
            st.dataframe(df)
            
            # Export option
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Processed Data",
                data=csv,
                file_name="processed_employee_data.csv",
                mime="text/csv"
            )
            
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
else:
    st.info("Please upload an Excel file to get started")


