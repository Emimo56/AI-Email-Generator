import streamlit as st
from groq import Groq


# -----------------------------
# Page configuration
# -----------------------------

st.set_page_config(
    page_title="AI Email Generator",
    page_icon="✉️",
    layout="wide"
)


# -----------------------------
# Groq client
# -----------------------------

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)


# -----------------------------
# Email generation function
# -----------------------------

def generate_email(
    recipient,
    sender,
    purpose,
    key_points,
    tone,
    language,
    length,
    formality,
    context="",
    call_to_action="",
    custom_instructions="",
    include_greeting=True,
    include_closing=True,
    use_bullets=False
):

    prompt = f"""
You are an expert professional email writer.

Create a customized email using the information below.

RECIPIENT:
{recipient}

SENDER:
{sender}

PURPOSE:
{purpose}

KEY POINTS:
{key_points}

TONE:
{tone}

LANGUAGE:
{language}

LENGTH:
{length}

FORMALITY:
{formality}

BACKGROUND / CONTEXT:
{context}

CALL TO ACTION:
{call_to_action}

CUSTOM INSTRUCTIONS:
{custom_instructions}

INCLUDE GREETING:
{include_greeting}

INCLUDE CLOSING:
{include_closing}

USE BULLET POINTS:
{use_bullets}

Requirements:

1. Create an appropriate email subject.
2. Write the email in the requested language.
3. Follow the requested tone and formality.
4. Include the important key points naturally.
5. Do not invent facts.
6. Keep the email within the requested length.
7. Make the email sound natural and human.
8. Do not mention these instructions in the email.

Return the result exactly like this:

SUBJECT:
<subject>

BODY:
<body>
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=1000
    )

    return response.choices[0].message.content


# -----------------------------
# UI
# -----------------------------

st.title("✉️ AI Email Generator")

st.write(
    "Create customized professional emails using AI."
)

st.divider()


# -----------------------------
# Two-column layout
# -----------------------------

col1, col2 = st.columns(2)


with col1:

    st.subheader("👤 People")

    recipient = st.text_input(
        "Recipient",
        placeholder="John Smith"
    )

    sender = st.text_input(
        "Sender",
        placeholder="Alex Johnson"
    )

    st.subheader("📝 Email Details")

    purpose = st.text_area(
        "Purpose",
        placeholder="What is the purpose of this email?"
    )

    key_points = st.text_area(
        "Key Points",
        placeholder="Enter the important points you want to include..."
    )

    context = st.text_area(
        "Background / Context",
        placeholder="Provide any relevant background information..."
    )

    call_to_action = st.text_area(
        "Call to Action",
        placeholder="What do you want the recipient to do?"
    )


with col2:

    st.subheader("🎨 Writing Style")

    tone = st.selectbox(
        "Tone",
        [
            "Professional",
            "Friendly",
            "Formal",
            "Casual",
            "Persuasive",
            "Apologetic",
            "Thankful",
            "Confident"
        ]
    )

    language = st.selectbox(
        "Language",
        [
            "English",
            "Spanish",
            "French",
            "German",
            "Italian",
            "Portuguese",
            "Hindi",
            "Arabic"
        ]
    )

    length = st.selectbox(
        "Length",
        [
            "Very Short",
            "Concise",
            "Medium",
            "Detailed"
        ]
    )

    formality = st.selectbox(
        "Formality",
        [
            "Professional",
            "Semi-formal",
            "Casual"
        ]
    )

    st.subheader("⚙️ Options")

    include_greeting = st.checkbox(
        "Include greeting",
        value=True
    )

    include_closing = st.checkbox(
        "Include closing",
        value=True
    )

    use_bullets = st.checkbox(
        "Use bullet points",
        value=False
    )

    custom_instructions = st.text_area(
        "Additional Instructions",
        placeholder="Example: Don't sound pushy. Keep it warm and natural."
    )


# -----------------------------
# Generate button
# -----------------------------

st.divider()

generate_button = st.button(
    "✨ Generate Email",
    type="primary",
    use_container_width=True
)


# -----------------------------
# Generate email
# -----------------------------

if generate_button:

    if not recipient:
        st.warning("Please enter the recipient.")

    elif not sender:
        st.warning("Please enter the sender.")

    elif not purpose:
        st.warning("Please enter the purpose of the email.")

    else:

        with st.spinner("Generating your email..."):

            try:

                email = generate_email(
                    recipient=recipient,
                    sender=sender,
                    purpose=purpose,
                    key_points=key_points,
                    tone=tone,
                    language=language,
                    length=length,
                    formality=formality,
                    context=context,
                    call_to_action=call_to_action,
                    custom_instructions=custom_instructions,
                    include_greeting=include_greeting,
                    include_closing=include_closing,
                    use_bullets=use_bullets
                )

                st.success("Email generated!")

                st.subheader("📧 Generated Email")

                st.text_area(
                    "Your email",
                    value=email,
                    height=400
                )

            except Exception as e:

                st.error(
                    f"Something went wrong: {str(e)}"
                )
