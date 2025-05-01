"""
Storylane Demo Assistant App

This Streamlit app integrates with Storylane dashboards and provides a
chatbot interface to interact with Product Knowledge Agent.
"""

import os
import json
import time
import asyncio
import streamlit as st
from dotenv import load_dotenv
import pandas as pd
from PIL import Image
from io import BytesIO
import requests
import numpy as np
import sounddevice as sd
import queue
import speech_recognition as sr
import scipy.io.wavfile
from text_to_speech import initialize_tts_engine, speak_text, stop_speaking
from realtime_voice_agent import listen_and_transcribe_once



# My original imports
from mock_demo_services import StorylaneDemoService
from product_knowledge_agent import ProductKnowledgeAgent

# Load environment variables (API keys)
load_dotenv()

# Retrieve API keys
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")  # Optional

# Storylane demo links
STORYLANE_LINKS = {
    "dashboard": "https://app.storylane.io/share/filcrnbzfr0i?page_id=412f5a03-66bf-4d00-b752-b34b6886908b",
    "security": "https://app.storylane.io/share/filcrnbzfr0i?page_id=86c995a2-bf4a-442b-9125-e758be1e0748",
    "alerts": "https://app.storylane.io/share/filcrnbzfr0i?page_id=9f19ef20-2c1a-46ca-b85f-740b7d236412",
    "enforcement": "https://app.storylane.io/share/filcrnbzfr0i?page_id=d4555711-e77c-494d-bbd2-eece331ac63f",
    "inventory": "https://app.storylane.io/share/filcrnbzfr0i?page_id=321f5c3f-4042-4c60-b415-18a0655d4f89",
    "api": "https://app.storylane.io/share/filcrnbzfr0i?page_id=86c995a2-bf4a-442b-9125-e758be1e0748"
}

# Section descriptions for context
SECTION_DESCRIPTIONS = {
    "dashboard": "Overview of the main dashboard and key features",
    "security": "Configuration of security policies and compliance standards",
    "alerts": "Alert management, notifications, and remediation workflows",
    "enforcement": "Policy enforcement and automated remediation capabilities",
    "inventory": "Asset inventory and resource management across cloud environments",
    "api": "API capabilities and integration options with other tools"
}

# Function to get company logo
def get_company_logo(company="broadcom"):
    try:
        if company == "paloalto":
            url = "https://www.paloaltonetworks.com/content/dam/pan/en_US/images/logos/brand/primary-company-logo/PANW_Parent_Brand_Primary_Logo_RGB.png"
        else:  # Default to Broadcom
            url = "https://www.thesoftwarereport.com/wp-content/uploads/2018/12/carbon-black-logo.png"
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img
    except:
        # Return None if logo can't be fetched
        return None

# Initialize session state
def init_session_state():
    # Initialize chat history if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
        
    # Initialize current section if it doesn't exist
    if 'current_section' not in st.session_state:
        st.session_state.current_section = "dashboard"

        
    # Initialize knowledge agent if it doesn't exist
    if 'knowledge_agent' not in st.session_state:
        if not anthropic_api_key:
            st.error("Anthropic API key not found. Please set the ANTHROPIC_API_KEY environment variable.")
            st.stop()
            
        product_type = st.session_state.get('product_type', 'carbon_black')
        st.session_state.knowledge_agent = ProductKnowledgeAgent(
            anthropic_api_key=anthropic_api_key,
            openai_api_key=openai_api_key,
            product_type=product_type
        )

    if 'tts_engine' not in st.session_state:
        st.session_state.tts_engine = initialize_tts_engine()

# App title and setup
st.set_page_config(
    page_title="Storylane Demo Assistant",
    page_icon="🔒",
    layout="wide"
)

# Initialize
init_session_state()

# Sidebar with logo and navigation
with st.sidebar:
    # Display logo
    product_selection = st.radio(
        "Select Product",
        ["Carbon Black"],
        index=0,
        key="product_radio"
    )
    
    # Update product type based on selection
    if product_selection == "Carbon Black":
        if st.session_state.get('product_type') != 'carbon_black':
            st.session_state.product_type = 'carbon_black'
            if 'knowledge_agent' in st.session_state:
                # Reinitialize knowledge agent with new product
                st.session_state.knowledge_agent = ProductKnowledgeAgent(
                    anthropic_api_key=anthropic_api_key,
                    openai_api_key=openai_api_key,
                    product_type='carbon_black'
                )
    else:
        if st.session_state.get('product_type') != 'prisma_cloud':
            st.session_state.product_type = 'prisma_cloud'
            if 'knowledge_agent' in st.session_state:
                # Reinitialize knowledge agent with new product
                st.session_state.knowledge_agent = ProductKnowledgeAgent(
                    anthropic_api_key=anthropic_api_key,
                    openai_api_key=openai_api_key,
                    product_type='prisma_cloud'
                )
    
    logo = get_company_logo("broadcom" if product_selection == "Carbon Black" else "paloalto")
    if logo:
        st.image(logo, width=200)
    
    st.title("Demo Assistant")
    
    # Navigation for Storylane sections
    st.header("Demo Navigation")
    section_options = list(STORYLANE_LINKS.keys())
    section_names = [s.capitalize() for s in section_options]
    
    selected_section = st.selectbox(
        "Select Demo Section",
        range(len(section_options)),
        format_func=lambda i: section_names[i],
        key="section_selectbox"
    )
    
    # Update current section when selection changes
    if st.session_state.current_section != section_options[selected_section]:
        st.session_state.current_section = section_options[selected_section]
    
    # Add some information about the current section
    st.info(SECTION_DESCRIPTIONS[st.session_state.current_section])

    st.markdown("---")
    enable_voice = st.checkbox("🎙️ Enable Voice Assistant", value=False)
    enable_tts = st.checkbox("🔊 Enable TTS (Read Answers Aloud)", value=False)

    if st.button("🛑 Stop Speaking"):
        stop_speaking()

    
    # Clear chat history
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()
    
    # Add information about the assistant
    with st.expander("About the Assistant"):
        st.write("""
        This demo assistant combines:
        
        1. Storylane demo visuals
        2. An AI-powered product knowledge chatbot
        3. Voice integrated
        
        Ask any questions about the product during the demo!
        """)

# Main content area with Storylane iframe and chat interface
st.title(f"{product_selection} Demo Assistant")

# Create two columns - one for Storylane, one for chat
storylane_col, chat_col = st.columns([2, 1])

with storylane_col:
    st.subheader("Demo Visualization")
    
    # Get the current Storylane URL
    current_url = STORYLANE_LINKS[st.session_state.current_section]
    
    # Display the Storylane iframe
    st.components.v1.iframe(
        current_url, 
        height=600, 
        scrolling=True
    )

with chat_col:
    st.subheader("Product Assistant")

    # Scrollable chat container with fixed height
    st.markdown("""
        <style>
        .chat-box {
            height: 540px;
            overflow-y: scroll;
            border: 1px solid #CCC;
            padding: 10px;
            border-radius: 8px;
            background-color: #f9f9f9;
            scroll-behavior: smooth;
        }
        .chat-msg {
            margin-bottom: 10px;
        }
        .chat-msg.user {
            font-weight: bold;
            color: #0a84ff;
        }
        .chat-msg.assistant {
            color: #333;
        }
        </style>
        """, unsafe_allow_html=True)

    chat_html = "<div class='chat-box'>"

    for message in st.session_state.chat_history:
        role = message["role"]
        content = message["content"]
        css_class = "user" if role == "user" else "assistant"
        chat_html += f"<div class='chat-msg {css_class}'>{role.capitalize()}: {content}</div>"

    chat_html += "</div>"

    st.markdown(chat_html, unsafe_allow_html=True)

    # Chat input
    user_input = st.chat_input("Ask a question about the product...")

    if user_input:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Get response from knowledge agent
        section_context = f"The user is currently looking at the {st.session_state.current_section} section of {product_selection}. "
        section_context += SECTION_DESCRIPTIONS[st.session_state.current_section]
        enhanced_query = f"{section_context}\n\nUser question: {user_input}"

        with st.spinner("Thinking..."):
            response = st.session_state.knowledge_agent.get_response(enhanced_query)

        # Append assistant response
        st.session_state.chat_history.append({"role": "assistant", "content": response})

        if enable_tts:
            speak_text(response, st.session_state.tts_engine)

        st.rerun()  # Rerun the app so new message is visible
    
    if enable_voice:
        st.subheader("🎙️ Voice Assistant Active")
        if st.button("🎤 Start Voice Query (Real-Time)"):
            with st.spinner("Listening..."):
                user_voice_query = listen_and_transcribe_once(duration_sec=5)
            st.success(f"Recognized: {user_voice_query}")

            st.session_state.chat_history.append({"role": "user", "content": user_voice_query})
            with st.spinner("Thinking based on your Voice Query..."):
                response = st.session_state.knowledge_agent.get_response(user_voice_query)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            if enable_tts:
                speak_text(response)
            st.rerun()

    

# Footer
st.markdown("---")
st.caption("Created by Ganesh Krishnan")