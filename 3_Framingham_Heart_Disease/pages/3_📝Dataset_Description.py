import streamlit as st
import pandas as pd
from streamlit_extras.colored_header import colored_header 
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from st_aggrid.shared import GridUpdateMode

# Data for the table
def make_dcs():
    data = {
        "Column": [
            "male", 
            "age", 
            "education", 
            "currentSmok", 
            "cigsPerDay", 
            "BPMeds", 
            "prevalentStroke", 
            "prevalentHyp", 
            "diabetes", 
            "totChol", 
            "sysBP", 
            "diaBP", 
            "BMI", 
            "heartRate", 
            "glucose", 
            "TenYearCHD"
        ],
        "Description": [
            "Patient Gender Binary (1 = Male, 0 = Female)", 
            "Patient age.", 
            "Patient education level.", 
            "Smoker or not Binary (1 = Yes, 0 = No)", 
            "Number of smoking cigars per day", 
            "Blood Pressure Medications.", 
            "Whether the individual has had a stroke previously Binary (1 = Yes, 0 = No)", 
            "Whether the individual has prevalent hypertension (high blood pressure) Binary (1 = Yes, 0 = No)", 
            "Whether the individual has diabetes. Binary (1 = Yes, 0 = No)", 
            "`Total Cholesterol` The total cholesterol level in the blood", 
            "`Systolic Blood Pressure` The pressure in the arteries when the heart beats", 
            "`Diastolic Blood Pressure` The pressure in the arteries when the heart is at rest between beats.", 
            "`Body Mass Index` A measure of body fat based on height and weight, calculated as weight (kg) / height (m)^2.", 
            "Heartbeats per minute.", 
            "The blood glucose level", 
            "`Ten-Year Coronary Heart Disease Risk` The estimated risk of developing CHD over the next ten years"
        ]
    }

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # colored_header(
    # label="Dataset Description",
    # description="This is a description",
    # color_name="violet-70"
    # )

    st.header('Dataset Description', divider='blue')
    st.markdown("> #### The \"Framingham\" heart disease dataset includes over 4,240 records, 16 columns and 15 attributes. The goal of the dataset is to predict whether the patient has 10-year risk of future (CHD) coronary heart disease:")
    st.subheader('Columns Description', divider='blue')
    # st.write("Notebooks by notebook name:")

    gd = GridOptionsBuilder.from_dataframe(df)
    # gd.configure_pagination(enabled=True)
    # gd.configure_column("Upvotes", header_name="Upvotes",minWidth=50,groupable=True,aggFunc="sum")
    # gd.configure_column("URL", header_name="URL",minWidth=500,groupable=True,)
    # gd.configure_column("Notebook Title", header_name="Notebook Title",minWidth=400,groupable=True,)
    # gd.configure_column("Owner", header_name="Owner",minWidth=150,groupable=True,pivot=True, )
    gd.configure_default_column(
                    filter=True,autoSize=True,
                    resizable=True,
                    headerStyle={'textAlign': 'right', 'fontSize': '16px', 'fontWeight': 'bold', 'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f0f0f0', 'color': 'black'},  # Styling for header
                    cellStyle={'textAlign': 'left', 'fontSize': '16px', 'fontWeight': 'bold', 'fontFamily': 'Arial, sans-serif',}
                    )


    # gd.configure_side_bar()
    # gd.configure_selection(selection_mode="multiple",use_checkbox=True)
    gridoptions = gd.build()


    # Display the custom CSS
    grid_table = AgGrid(df.reset_index(),gridOptions=gridoptions,
                update_mode=GridUpdateMode.MODEL_CHANGED | GridUpdateMode.SELECTION_CHANGED,
                height = 800,
                allow_unsafe_jscode=True,
                enable_enterprise_modules = True,
                theme = 'alpine',)






if __name__ == "__main__":

    logo_path = "./p.png"  # Replace with the path to your logo image
    st.sidebar.image(logo_path, use_column_width=True)
    make_dcs()

    st.header('Notebook Link [Click Here]( https://github.com/Dataclin-Operations/Framingham_Heart_Disease/blob/main/Framingham_Heart_Disease_EDA.ipynb)', divider='blue')
#     html_code = '''
# <h2>Select option to stratify chart with</h2>
# <a href="https://github.com/Dataclin-Operations/Framingham_Heart_Disease/blob/main/Framingham_Heart_Disease_EDA.ipynb" 
# style="font-size: 30px;">Link</a>
# '''

#     st.markdown(html_code, unsafe_allow_html=True)
#     st.divider()
#     st.header('', divider='blue')
#     html_code = '''
# <hr style="border: 2px solid blue;">
# '''

#     st.header('Select option to stratify chart with\n[Link](https://github.com/Dataclin-Operations/Framingham_Heart_Disease/blob/main/Framingham_Heart_Disease_EDA.ipynb)', divider=None)
#     st.markdown(html_code, unsafe_allow_html=True)