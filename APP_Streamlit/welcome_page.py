# welcome_page.py
import streamlit as st

def show_welcome_page():
    st.title("Welcome to the PacePerfect")
    st.subheader("Your Personal Running Guide")

    # Add an image or icon
    st.image("running_logo.png", width=200)

    st.write("Discover PacePerfect, the app that tailors personalized run recommendations without the need for costly gadgets or coaches. Drawing insights from millions of athletes, our collaborative filtering model analyzes your running history and goals to design training runs that enhance speed and minimize the risk of injury. ")
    
    st.write("With a data-driven and budget-friendly approach, embrace the power of PacePerfect and take your running journey to new heights!")

 # Add a testimonial or quote
    st.write("> \"PacePerfect helped me improve my running pace and endurance. Highly recommended!\" - Matt Pitz, Marathon Runner")
    st.write("> \"I'm not a runner and had no idea where to start, PacePerfect helped me create a plan in no time. This is great!\" - Ria Mahajan, New Runner")


    st.write("To get started, please click Get Started:")
