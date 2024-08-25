import streamlit as st
import anthropic  # Ensure you have the correct API client library
api_key = st.secrets["claude-api-key"]
def generate_meal_plan(api_key, fasting_sugar, pre_meal_sugar, post_meal_sugar, dietary_preferences):
    # Initialize the client with the provided API key
    client = anthropic.Client(api_key=api_key)
    
    # Construct the prompt
    prompt = (
        "You are a helpful assistant that provides personalized meal plans based on health data.\n\n"
        "Human:\n"
        f"Fasting Sugar Level: {fasting_sugar} mg/dL\n"
        f"Pre-Meal Sugar Level: {pre_meal_sugar} mg/dL\n"
        f"Post-Meal Sugar Level: {post_meal_sugar} mg/dL\n"
        f"Dietary Preferences: {dietary_preferences}\n\n"
        "Assistant:\n"
        "Please generate a personalized meal plan including suggestions for breakfast, lunch, dinner, and snacks."
    )
    
    try:
        # Create the completion request with correct parameters
        response = client.completions.create(
            model="claude-1.3",  # Replace with the correct model name if needed
            prompt=prompt,
            max_tokens_to_sample=1000  # Adjust as needed
        )
        
        # Extract the text of the completion
        response_content = response.completion.strip()
        
        # Format the response content into paragraphs
        formatted_response = response_content.replace("\n", "\n\n")
        
    except Exception as e:
        formatted_response = f"An error occurred: {str(e)}"
    
    return formatted_response

# Streamlit app
st.title('GLUCO Guide')

# Short description of the app
st.write("""
*Welcome to GLUCO Guide!*

GLUCO Guide is designed to help diabetic patients manage their dietary needs by providing personalized meal plans. Simply enter your fasting, pre-meal, and post-meal sugar levels along with any dietary preferences you may have. Based on your inputs, GLUCO Guide will generate a meal plan tailored to your needs, helping you maintain stable blood sugar levels while enjoying a variety of nutritious and delicious meals.
""")

# Sidebar inputs
st.sidebar.header('Enter Your Details')


# Inputs for sugar levels and dietary preferences
fasting_sugar = st.sidebar.number_input('Fasting Sugar Level (mg/dL)', min_value=0, max_value=300, value=100)
pre_meal_sugar = st.sidebar.number_input('Pre-Meal Sugar Level (mg/dL)', min_value=0, max_value=300, value=100)
post_meal_sugar = st.sidebar.number_input('Post-Meal Sugar Level (mg/dL)', min_value=0, max_value=300, value=100)
dietary_preferences = st.sidebar.text_input('Dietary Preferences (e.g., vegetarian, low-carb)')

# Generate meal plan based on user input
if st.sidebar.button('Generate Meal Plan'):
    if api_key:  # Check if API key is provided
        meal_plan = generate_meal_plan(api_key, fasting_sugar, pre_meal_sugar, post_meal_sugar, dietary_preferences)
        
        # Display meal plan
        st.header('Your Personalized Meal Plan')
        st.markdown(meal_plan)  # Using markdown to maintain formatting
    else:
        st.error('Please provide your API Key to generate a meal plan.')

# Footer
st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        <p>&copy; 2024 GLUCO Guide. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)
