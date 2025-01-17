import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import re

# loading the saved models
bte_model = pickle.load(open('saved_models/bte_model.sav', 'rb'))
bmep_model = pickle.load(open('saved_models/bmep_model.sav', 'rb'))
brake_power_model = pickle.load(open('saved_models/brake_power_model.sav', 'rb'))

# Title and description
st.title("Engine Performance Calculator")
st.markdown(
    """
    This application calculates **Brake Thermal Efficiency (BTE)**, 
    **Brake Mean Effective Pressure (BMEP)**, and **Brake Power** 
    based on input parameters. Just provide the necessary details, 
    and let the calculator do the rest!
    """
)

# Function to parse description and extract values
def parse_description(description):
    injection_timing = int(re.search(r'injection timing of (\d+) degrees', description).group(1))
    injector_pressure = int(re.search(r'injection pressure of (\d+) bar', description).group(1))
    cl = float(re.search(r'coolant load of ([\d\.]+) units', description).group(1))
    egt = int(re.search(r'exhaust gas temperature is (\d+)°C', description).group(1))
    ve = float(re.search(r'volumetric efficiency is ([\d\.]+)%', description).group(1))
    
    temperature = 30  # Default value, adjust if needed
    return injection_timing, injector_pressure, temperature, egt, ve, cl

# Initial values
Injection_timing, Injector_pressure, Temperature, EGT, VE, CL = 27, 270, 30, 190, 77.5, 3.0

# Input section with expander
st.header("Input Description")
with st.expander("Click here to enter engine parameters"):
    description = st.text_area(
        "Enter the engine parameters in the format: '**I have an LHR engine with an injection timing of 28 degrees before TDC (Top Dead Center), an injection pressure of 230 bar, and a coolant load of 3.2 units. The exhaust gas temperature is 350°C, and the volumetric efficiency is 80%.**'"
    )

# Extract values from description
if description:
    Injection_timing, Injector_pressure, Temperature, EGT, VE, CL = parse_description(description)
elif st.button("Enter values manually"):
    st.markdown("### 🛠️ Manual Input Section")
    col1, col2 = st.columns(2)
    
    with col1:
        Injection_timing = st.number_input("Injection Timing (degrees)", min_value=0, max_value=50, value=27)
        Injector_pressure = st.number_input("Injector Pressure (bar)", min_value=100, max_value=500, value=270)
        Temperature = st.number_input("Ambient Temperature (°C)", min_value=0, max_value=50, value=30)

    with col2:
        CL = st.number_input("Coolant Load (units)", min_value=0.0, value=3.0, step=0.1)
        EGT = st.number_input("Exhaust Gas Temperature (°C)", min_value=0, value=190)
        VE = st.number_input("Volumetric Efficiency (%)", min_value=0.0, value=77.5, step=0.1)

# Feature vector for the models
features = np.array([[Injection_timing, Injector_pressure, Temperature, EGT, VE, CL]])

# Predictions with spinner and progress bar
if st.button("Calculate 🚀"):
    with st.spinner('Calculating... Please wait!'):
        st.progress(100)
        bte = bte_model.predict(features)[0]
        bmep = bmep_model.predict(features)[0]
        brake_power = brake_power_model.predict(features)[0]

    # Display results with background color effect
    st.header("📊 Results")
    st.success(f"**Brake Thermal Efficiency (BTE):** {bte:.2f} %")
    st.info(f"**Brake Mean Effective Pressure (BMEP):** {bmep:.2f} bar")
    st.success(f"**Brake Power:** {brake_power:.2f} kW")
