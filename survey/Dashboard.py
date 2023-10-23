import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="SURVEY ANALYSIS", page_icon=":chart_with_upwards_trend:",layout="wide")

st.title(" :chart_with_upwards_trend: SURVEY ANALYSIS")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

fl = st.file_uploader(":file_folder: Upload the file",type=(["csv","txt","xlsx","xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding = "ISO-8859-1")
else:
    os.chdir(r"C:\Users\RESAF\Downloads\survey analysis")
    df = pd.read_csv("Sample_survey_final.csv", encoding = "ISO-8859-1")

st.sidebar.header("Choose your filter :arrow_down_small: ")
# Create for Location
region = st.sidebar.multiselect("Region", df["Location"].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df["Location"].isin(region)]

# Create for Gender
gender = st.sidebar.multiselect("Gender", df2["Gender"].unique())
if not gender:
    df3 = df2.copy()
else:
    df3 = df2[df2["Gender"].isin(gender)]

# Create for Age
age = st.sidebar.multiselect("Age range",df3["Age Category"].unique())
if not age:
    df4 = df3.copy()
else:
    df4 = df3[df3["Age Category"].isin(age)]

# Create for Qualification
qualification = st.sidebar.multiselect("Qualification", df3['Qualification'].unique())
if not qualification:
    df5 = df4.copy()
else:
    df5 = df4[df4["Qualification"].isin(qualification)]

# Filter the data based on Region, Gender, Age and Qualification

if not region and not gender and not age and not qualification:
    filtered_df = df
elif not gender and not age and not qualification:
    filtered_df = df[df["Location"].isin(region)]
elif not region and not age and not qualification:
    filtered_df = df[df["Gender"].isin(gender)]
elif not region and not gender and not qualification:
    filtered_df = df[df['Age Category'].isin(age)]
elif region and gender:
    filtered_df = df5[df5["Location"].isin(region) & df5["Gender"].isin(gender)]
elif region and age:
    filtered_df = df5[df5["Location"].isin(region) & df5["Age Category"].isin(age)]
elif region and qualification:
    filtered_df = df5[df5["Location"].isin(region) & df5["Qualification"].isin(qualification)]
elif age and gender:
    filtered_df = df5[df5["Age Category"].isin(age) & df5["Gender"].isin(gender)]
elif qualification and gender:
    filtered_df = df5[df5["Qualification"].isin(qualification) & df5["Gender"].isin(gender)]
elif age and qualification:
    filtered_df = df5[df5["Age Category"].isin(age) & df5["Qualification"].isin(qualification)]
elif gender and age and qualification:
    filtered_df = df5[df["Gender"].isin(gender) & df5["Age Category"].isin(age) & df5["Qualification"].isin(qualification)]
elif region and age and qualification:
    filtered_df = df5[df["Location"].isin(region) & df5["age"].isin(age) & df5['Qualification'].isin(qualification)]
elif region and gender and qualification:
    filtered_df = df5[df["Location"].isin(region) & df5["Gender"].isin(gender) & df5['Qualification'].isin(qualification)]
elif region and gender and age:
    filtered_df = df5[df["Location"].isin(region) & df5["Gender"].isin(gender) & df5['Age Category'].isin(age)]
elif qualification:
    filtered_df = df5[df5["Qualification"].isin(qualification)]
else:
    filtered_df = df5[df5["Location"].isin(region) & df5["Gender"].isin(gender) & df5["Age Category"].isin(age) & df5['Qualification'].isin(qualification)]

# Calculate the number of results after applying filters
num_results = len(filtered_df)
# Display the result count in your Streamlit app
st.write(f"Number of results : {num_results}")
male_count = filtered_df[filtered_df['Gender'] == 'Male']['Gender'].count()
female_count = filtered_df[filtered_df['Gender'] == 'Female']['Gender'].count()

colm1, colm2, colm3 = st.columns((3))

# Create a Streamlit row
st.write('<div class="row">', unsafe_allow_html=True)
# Create a card for total count
with colm1:
    st.write(
        """
        <div class="col-md-4" style="border: 2px solid #FFFFFF; border-radius: 10px; padding: 10px; text-align: center;">
            <h2>Total</h2>
            <p style="font-size: 16px;">""" + str(num_results) + """</p>
        </div>
        """,
        unsafe_allow_html=True
    )
# Create a card for male count
with colm2:
    st.write(
        """
        <div class="col-md-4" style="border: 2px solid #4B8BBE; border-radius: 10px; padding: 10px; text-align: center;">
            <h2>Male</h2>
            <p style="font-size: 16px;">""" + str(male_count) + """</p>
        </div>
        """,
        unsafe_allow_html=True
    )
# Create a card for female count
with colm3:
    st.write(
        """
        <div class="col-md-4" style="border: 2px solid #FF69B4; border-radius: 10px; padding: 10px; text-align: center;">
            <h2>Female</h2>
            <p style="font-size: 16px;">""" + str(female_count) + """</p>
        </div>
        """,
        unsafe_allow_html=True
    )

col1, col2 = st.columns((2))

with col1:
    st.subheader("Demographics")
    fig = px.histogram(filtered_df, x = "Age",
                 template = "seaborn", nbins=20, title='Age Distribution')
    st.plotly_chart(fig,use_container_width=True, height = 200)

