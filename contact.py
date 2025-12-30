import streamlit as st


def render(colors):
    """
    Render the Contact page with social media links and contact information.

    Args:
        colors (list): Theme color palette [cyan, purple, violet, abyss, ice-blue]
    """
    # PAGE HEADER
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.95), rgba(2, 6, 23, 0.98));
            border-radius: 24px;
            padding: 48px 40px;
            width: 100%;
            margin: 0 0 48px 0;
            box-shadow:
                0 8px 40px rgba(56, 189, 248, 0.25),
                0 0 100px rgba(56, 189, 248, 0.15),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(56, 189, 248, 0.35);
            backdrop-filter: blur(12px);
            text-align: center;
        ">
        <h1 style="
            color: #38bdf8;
            margin: 0 0 16px 0;
            font-size: 3.2rem;
            font-weight: 700;
            text-shadow: 0 0 35px rgba(56, 189, 248, 0.8);
            letter-spacing: 1.5px;
        ">
            Get in Touch
        </h1>

        <h3 style="
            color: #cbd5e1;
            font-weight: 300;
            letter-spacing: 1.2px;
            margin: 0;
            font-size: 1.4rem;
            line-height: 1.6;
        ">
            Let's Connect
        </h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    # SECTION SPACING
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # CONTACT METHODS - Three Column Layout
    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown("""
        <div style="
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.88), rgba(2, 6, 23, 0.92));
            border-radius: 16px;
            padding: 40px 32px;
            border-left: 5px solid #0077b5;
            box-shadow: 0 6px 25px rgba(0, 119, 181, 0.2);
            min-height: 320px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        " onmouseover="this.style.transform='translateY(-8px)'; this.style.boxShadow='0 12px 40px rgba(0, 119, 181, 0.35)'"
           onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 6px 25px rgba(0, 119, 181, 0.2)'">
            <h3 style='
                color: #0077b5;
                margin: 0 0 16px 0;
                font-size: 1.5rem;
                font-weight: 600;
                letter-spacing: 0.5px;
            '>LinkedIn</h3>
            <p style='
                color: #cbd5e1;
                line-height: 1.8;
                font-size: 15.5px;
                margin: 0 0 20px 0;
            '>
                Connect with me professionally
            </p>
            <a href="https://www.linkedin.com/in/aditya-padmarajan/" target="_blank" style="
                color: #0077b5;
                font-weight: 600;
                text-decoration: none;
                font-size: 16px;
                padding: 10px 20px;
                border: 2px solid #0077b5;
                border-radius: 8px;
                transition: all 0.3s ease;
                display: inline-block;
            " onmouseover="this.style.backgroundColor='#0077b5'; this.style.color='#ffffff'"
               onmouseout="this.style.backgroundColor='transparent'; this.style.color='#0077b5'">
                View Profile →
            </a>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.88), rgba(2, 6, 23, 0.92));
            border-radius: 16px;
            padding: 40px 32px;
            border-left: 5px solid #333;
            box-shadow: 0 6px 25px rgba(51, 51, 51, 0.2);
            min-height: 320px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        " onmouseover="this.style.transform='translateY(-8px)'; this.style.boxShadow='0 12px 40px rgba(51, 51, 51, 0.35)'"
           onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 6px 25px rgba(51, 51, 51, 0.2)'">
            <h3 style='
                color: #ffffff;
                margin: 0 0 16px 0;
                font-size: 1.5rem;
                font-weight: 600;
                letter-spacing: 0.5px;
            '>GitHub</h3>
            <p style='
                color: #cbd5e1;
                line-height: 1.8;
                font-size: 15.5px;
                margin: 0 0 20px 0;
            '>
                Explore my projects and code
            </p>
            <a href="https://github.com/adi-padmarajan" target="_blank" style="
                color: #ffffff;
                font-weight: 600;
                text-decoration: none;
                font-size: 16px;
                padding: 10px 20px;
                border: 2px solid #ffffff;
                border-radius: 8px;
                transition: all 0.3s ease;
                display: inline-block;
            " onmouseover="this.style.backgroundColor='#ffffff'; this.style.color='#000000'"
               onmouseout="this.style.backgroundColor='transparent'; this.style.color='#ffffff'">
                Visit GitHub →
            </a>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.88), rgba(2, 6, 23, 0.92));
            border-radius: 16px;
            padding: 40px 32px;
            border-left: 5px solid #ea4335;
            box-shadow: 0 6px 25px rgba(234, 67, 53, 0.2);
            min-height: 320px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        " onmouseover="this.style.transform='translateY(-8px)'; this.style.boxShadow='0 12px 40px rgba(234, 67, 53, 0.35)'"
           onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 6px 25px rgba(234, 67, 53, 0.2)'">
            <h3 style='
                color: #ea4335;
                margin: 0 0 16px 0;
                font-size: 1.5rem;
                font-weight: 600;
                letter-spacing: 0.5px;
            '>Email</h3>
            <p style='
                color: #cbd5e1;
                line-height: 1.8;
                font-size: 15.5px;
                margin: 0 0 20px 0;
            '>
                Send me a message directly
            </p>
            <a href="mailto:aditya.padmarajan@gmail.com" style="
                color: #ea4335;
                font-weight: 600;
                text-decoration: none;
                font-size: 16px;
                padding: 10px 20px;
                border: 2px solid #ea4335;
                border-radius: 8px;
                transition: all 0.3s ease;
                display: inline-block;
            " onmouseover="this.style.backgroundColor='#ea4335'; this.style.color='#ffffff'"
               onmouseout="this.style.backgroundColor='transparent'; this.style.color='#ea4335'">
                Email Me →
            </a>
        </div>
        """, unsafe_allow_html=True)

    # SECTION SPACING
    st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)

    # CALL TO ACTION
    st.markdown("""
    <div style='
        text-align: center;
        padding: 3rem 2.5rem;
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(2, 6, 23, 0.98));
        border: 2px solid rgba(56, 189, 248, 0.5);
        border-radius: 20px;
        box-shadow:
            0 10px 40px rgba(56, 189, 248, 0.35),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        width: 100%;
        margin: 0;
    '>
        <h2 style='
            color: #38bdf8;
            margin: 0 0 20px 0;
            font-size: 2.2rem;
            font-weight: 600;
            text-shadow: 0 0 30px rgba(56, 189, 248, 0.7);
            letter-spacing: 1px;
        '>
            Let's Collaborate
        </h2>
        <p style='
            color: #cbd5e1;
            font-size: 1.15rem;
            line-height: 1.8;
            margin: 0;
            max-width: 750px;
            margin: 0 auto;
        '>
            Whether you're interested in discussing this project, exploring collaboration opportunities,
            or just want to connect, I'd love to hear from you. Feel free to reach out through any of the
            channels above!
        </p>
    </div>
    """, unsafe_allow_html=True)
