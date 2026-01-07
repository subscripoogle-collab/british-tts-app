import streamlit as st
import edge_tts
import asyncio
import io

# Set page title and icon
st.set_page_config(page_title="British Neural TTS", page_icon="🇬🇧")

# Title and Description
st.title("🇬🇧 British Neural TTS Maker")
st.markdown("Generate human-like British audio for your storytelling projects.")

# Voice Options
BRITISH_VOICES = {
    "Sonia (Female - Clear)": "en-GB-SoniaNeural",
    "Ryan (Male - Standard)": "en-GB-RyanNeural",
    "Libby (Female - Soft)": "en-GB-LibbyNeural",
    "Thomas (Male - Formal)": "en-GB-ThomasNeural",
    "Maisie (Child - Playful)": "en-GB-MaisieNeural"
}

# Async generation function
async def generate_audio_stream(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    audio_data = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data.write(chunk["data"])
    return audio_data

# --- The UI Layout ---
with st.container():
    # 1. Select Voice
    voice_label = st.selectbox("Choose a Voice:", list(BRITISH_VOICES.keys()))
    selected_voice_id = BRITISH_VOICES[voice_label]

    # 2. Text Input
    text_input = st.text_area("Enter your text here:", height=150, placeholder="Once upon a time in London...")

    # 3. Generate Button
    if st.button("▶ Generate Audio", type="primary"):
        if text_input.strip() == "":
            st.warning("Please enter some text first.")
        else:
            with st.spinner('Generating high-quality audio...'):
                try:
                    # Run the async function
                    audio_bytes = asyncio.run(generate_audio_stream(text_input, selected_voice_id))
                    
                    # Play Audio
                    st.audio(audio_bytes, format='audio/mp3')
                    
                    # Download Button
                    st.download_button(
                        label="💾 Download MP3",
                        data=audio_bytes,
                        file_name="british_audio.mp3",
                        mime="audio/mp3"
                    )
                    st.success("Generation complete!")
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")

# Add a footer note
st.markdown("---")
st.caption("Powered by Microsoft Edge Neural Voices | Built for Web Bay Design")