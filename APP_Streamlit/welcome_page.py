# welcome_page.py
import streamlit as st

def show_welcome_page():
    st.title("Welcome to PacePerfect")
    st.header("Your Personal Running Guide")

    # Add an image or icon
    st.image("running_logo.png", width=200)

    st.write("Discover PacePerfect, the app that tailors personalized run recommendations without the need for costly gadgets or coaches. Drawing insights from millions of athletes, our collaborative filtering model analyzes your running history and goals to design training runs that enhance speed and minimize the risk of injury. ")
    
    st.write("With a data-driven and budget-friendly approach, embrace the power of PacePerfect and take your running journey to new heights!")

 # Add a testimonial or quote
    st.write("> \"PacePerfect helped me improve my running pace and endurance. Highly recommended!\" - Matt Pitz, Marathon Runner")
    st.write("> \"I'm not a runner and had no idea where to start, PacePerfect helped me create a plan in no time. This is great!\" - Ria Mahajan, New Runner")


    # Add an FAQ section (example with collapsible sections)
    st.subheader("Frequently Asked Questions (FAQs):")
    with st.expander("How does PacePerfect personalize training runs?"):
        st.write("PacePerfect employs a collaborative filtering model to examine your running history and objectives, offering personalized recommendations derived from insights obtained from fellow athletes.")
    
    with st.expander("Can I use PacePerfect for free?"):
        st.write("Yes, PacePerfect is free to get you started on your running journey")
    
    # Add contact information
    st.subheader("Contact Us:")
    st.write("For support or inquiries, please email us at support@paceperfect.com ")


 # Use Markdown to customize the appearance of the "Get Started" message
    st.markdown("<p style='font-size: 24px; font-weight: bold; color: #0080FF;'>To get started, please click below:</p>", unsafe_allow_html=True)

