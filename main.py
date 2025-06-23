import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from user_input import get_user_input
from road_features import RoadFeatures
from weather_conditions import WeatherConditions

groq_api_key = st.secrets["GROQ_API_KEY"]
llm = ChatGroq(api_key=groq_api_key, model="llama-3.1-8b-instant")

road = RoadFeatures()
weather = WeatherConditions(road.latitude, road.longitude)
weather.fetch_weather()

bms_data = {"soc": 85, "voltage": 400, "current": 200}
tpms_penalty = 0.05

prompt_template = """
You are an assistant that predicts the electric vehicle (EV) driving range based on real-time data.

You are given:
- Slope: {slope} degrees
- Curvature: {curvature}
- Slope penalty: {slope_penalty}
- Curvature penalty: {curvature_penalty}
- Temperature: {temperature}°C
- Wind speed: {wind_speed} m/s
- Weather penalty: {weather_penalty}
- Tire pressure penalty: {tpms_penalty}
- State of Charge (SOC): {soc}%
- Voltage: {voltage} V
- Current: {current} A

Based on this data and user’s query, estimate the current EV range, and warn if any conditions are severely impacting it.
Respond clearly and helpfully.

User's Question:
{query}

Answer:
"""

prompt = ChatPromptTemplate.from_template(prompt_template)
chain = LLMChain(prompt=prompt, llm=llm)

st.title("EV Range Predictor (Voice Enabled)")

if st.button("Ask About Your EV Range"):
    with st.spinner("Listening to your question..."):
        query = get_user_input()

    if query.strip():
        st.info(f"You said: {query}")
        with st.spinner("Calculating prediction..."):
            features = road.get_features()
            weather_penalty = weather.get_weather_penalty()

            inputs = {
                "slope": features["slope"],
                "curvature": features["curvature"],
                "slope_penalty": features["slope_penalty"],
                "curvature_penalty": features["curvature_penalty"],
                "temperature": weather.get_temperature(),
                "wind_speed": weather.get_wind_speed(),
                "weather_penalty": weather_penalty,
                "tpms_penalty": tpms_penalty,
                "soc": bms_data["soc"],
                "voltage": bms_data["voltage"],
                "current": bms_data["current"],
                "query": query,
            }

            response = chain.run(inputs)
            st.success("🔍 Estimated Result:")
            st.write(response)
    else:
        st.warning("Didn't catch your voice. Please try again.")
