from distutils.log import info
from operator import mod
import streamlit as st
import numpy as np
import pandas as pd
import pickle
from PIL import Image


def main():
    st.title("Cardiograma")

    with open(r"model.pickle", "rb") as input_file:
        model= pickle.load(input_file)    

    with st.form(key="myform"):
        st.write("Fill in the form below:")
        st_slope_up = st.selectbox("ST segment slope up?:", ["", "Yes", "No"])
        chest_pain_type = st.selectbox("Chest pain type Asymptomatic:", ["", "Yes", "No"])
        sex = st.selectbox("Sex of the patient:", ["", "Male", "Female"])

        submit = st.form_submit_button('Submit')

        if submit:
            if st_slope_up != "" and chest_pain_type != "" and sex != "":
                ChestPainType_ASY = st_slope_up == "Yes"
                ST_Slope_Up = chest_pain_type == "Yes"
                Sex = sex == "Male"

                r = {
                    'ChestPainType_ASY':[ChestPainType_ASY],
                    'ST_Slope_Up':[ST_Slope_Up],
                    'Sex':[Sex]
                }

                df = pd.DataFrame(r)
                df['ChestPainType_ASY'] = df['ChestPainType_ASY'].astype(int)
                df['ST_Slope_Up'] = df['ST_Slope_Up'].astype(int)
                df['Sex'] = df['Sex'].astype(int)

                proba = model.predict_proba(df)
                result = np.round(proba[:, 1] * 100, 2)

                st.write(f"### Probability of heart disease {result} %")
            else: st.error("All fields are required!")

if __name__ == '__main__':

    st.set_page_config(page_title="Cardiograma", page_icon="💗",
        layout="wide", initial_sidebar_state="expanded")

    hide_menu_style = """
            <style>
            #MainMenu {visibility: hidden;}
            </style>
            """
    st.markdown(hide_menu_style, unsafe_allow_html=True)

    image = Image.open('logo.png')

    st.sidebar.image(image)
    main()
    st.sidebar.markdown("""## Attention: This is just a didactic project on the use of Artificial Intelligence. The results presented here have NO scientific proof!!!""")
    st.markdown("""## Attention: This is just a didactic project on the use of Artificial Intelligence. The results presented here have NO scientific proof!!!""")
