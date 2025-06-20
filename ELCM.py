import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Employee Data Processor (CSV)", layout="wide")
st.title("Employee Data Processor (CSV)")

uploaded_file = st.file_uploader("Upload Employee Data CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Read CSV with correct encoding
        df = pd.read_csv(uploaded_file, encoding='latin1')
        
        # Rest of your code...
        required_columns = [
            'Employee Code', 'Name Of Employee', 'Employement Status',
            'Employee Type', 'Location Name', 'Date of Joining',
            'Department 1.0', 'Location Code', 'Location City'
        ]
        
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            st.error(f"Missing columns in data: {', '.join(missing_cols)}")
        else:
            df = df[required_columns].copy()
            
            oct1_2024 = datetime(2024, 10, 1)
            df['Date of Joining'] = pd.to_datetime(df['Date of Joining'])
            df['New join / movment'] = df['Date of Joining'].apply(
                lambda x: 'New Join' if x > oct1_2024 else 'Movement'
            )
            
            df['AMD / Out side AMD'] = df['Location City'].apply(
                lambda x: 'AMD' if str(x).strip().lower() == 'ahmedabad' else 'Out side AMD'
            )
            
            df['Old GCC / New GCC'] = df['Department 1.0'].apply(
                lambda x: 'Old GCC' if str(x).strip().upper() in ['ABEX', 'GDGC'] else 'New GCC'
            )
            
            st.success("Data processed successfully!")
            st.dataframe(df)
            
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
    st.info("Please upload a CSV file to get started")
