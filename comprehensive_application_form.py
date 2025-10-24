"""
Comprehensive Application Form
This is the full-featured application form with all the detailed sections
you spent hours building out for the Harem CRM system.
"""

import streamlit as st

def show_comprehensive_application_form():
    st.title("📝 Comprehensive Harem Application Form")
    st.subheader("Complete Application with All Features")
    
    with st.form("comprehensive_application_form"):
        # Personal Information Section
        st.header("👤 Personal Information")
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name *", help="Your legal full name.")
            email = st.text_input("Email Address *", help="Your primary email address for communication.")
            phone = st.text_input("Phone Number", help="Your contact phone number.")
            age = st.number_input("Age *", min_value=18, max_value=99, help="You must be 18 or older to apply.")
        
        with col2:
            location = st.text_input("Current Location (City, State, Country) *", help="Where are you currently located?")
            occupation = st.text_input("Occupation/Profession", help="What do you do for work?")
            education = st.selectbox("Education Level", ["High School", "Some College", "Bachelor's", "Master's", "PhD", "Other"])
            relationship_status = st.selectbox("Current Relationship Status", ["Single", "In a relationship", "Married", "Polyamorous", "Other"])
        
        # Physical Information
        st.header("📏 Physical Information")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            height = st.text_input("Height", help="e.g., 5'6\" or 168cm")
            weight = st.text_input("Weight", help="Optional - for compatibility matching")
        
        with col2:
            body_type = st.selectbox("Body Type", ["Not specified", "Petite", "Average", "Curvy", "Athletic", "Plus-size", "Other"])
            hair_color = st.selectbox("Hair Color", ["Not specified", "Blonde", "Brunette", "Black", "Red", "Other"])
        
        with col3:
            eye_color = st.selectbox("Eye Color", ["Not specified", "Blue", "Brown", "Green", "Hazel", "Other"])
            tattoos = st.selectbox("Tattoos", ["None", "Few", "Many", "Extensive"])
        
        # Experience and Interests Section
        st.header("🔞 Experience and Interests")
        
        experience = st.selectbox(
            "Level of Experience *",
            ["Beginner", "Intermediate", "Experienced", "Highly Experienced"],
            help="Your experience level in BDSM/kink dynamics."
        )
        
        # Sir's Kink List Reference
        with st.expander("👑 Sir's Kink Preferences (for reference)", expanded=False):
            st.write("**Sir's interests include (none required):** Bondage, spanking, toy play, face fucking, pics & vids, CBT (milking, edging, cum control), nipple play, humiliation, role play, domestic service, content creation, forced topping, findom, choking, and more.")
            st.write("**Note:** None of these are required - we're looking for compatibility and enthusiasm.")
        
        interests = st.text_area(
            "What are your primary interests and desires? *",
            help="Describe what you are looking for and what excites you in a dynamic. Be specific about your kinks, fetishes, and what you enjoy.",
            height=120
        )
        
        limits = st.text_area(
            "Do you have any hard limits or boundaries? *",
            help="Please list any activities or situations you absolutely will not engage in. Be honest about your limits.",
            height=120
        )
        
        # Kink Compatibility Assessment
        st.subheader("🔍 Kink Compatibility Assessment")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Rate your interest level (1-5):**")
            bondage_interest = st.slider("Bondage & Restraint", 1, 5, 3)
            impact_interest = st.slider("Impact Play (Spanking, etc.)", 1, 5, 3)
            service_interest = st.slider("Service & Submission", 1, 5, 3)
            control_interest = st.slider("Control & Dominance", 1, 5, 3)
        
        with col2:
            st.write("**Additional interests:**")
            roleplay_interest = st.slider("Role Play", 1, 5, 3)
            humiliation_interest = st.slider("Humiliation", 1, 5, 3)
            cbt_interest = st.slider("CBT (Cock & Ball Torture)", 1, 5, 3)
            findom_interest = st.slider("Financial Domination", 1, 5, 3)
        
        # Availability and Commitment
        st.header("📅 Availability and Commitment")
        
        col1, col2 = st.columns(2)
        
        with col1:
            availability = st.text_area(
                "Describe your general availability",
                help="How often are you available and during what times?",
                height=100
            )
            
            time_commitment = st.selectbox(
                "Time Commitment Level",
                ["Not specified", "Few hours per week", "Several hours per week", "Daily availability", "24/7 availability"],
                help="How much time can you realistically commit?"
            )
        
        with col2:
            commitment = st.selectbox(
                "What level of commitment are you seeking?",
                ["Not specified", "Casual", "Regular", "Long-term", "Exclusive"],
                help="What kind of relationship or dynamic are you hoping for?"
            )
            
            travel_availability = st.selectbox(
                "Travel Availability",
                ["Local only", "Regional", "National", "International"],
                help="How far are you willing to travel?"
            )
        
        # Lifestyle and Preferences
        st.header("🏠 Lifestyle and Preferences")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Lifestyle Questions:**")
            smoking = st.selectbox("Do you smoke?", ["No", "Occasionally", "Yes", "Prefer not to say"])
            drinking = st.selectbox("Do you drink alcohol?", ["No", "Occasionally", "Yes", "Prefer not to say"])
            drugs = st.selectbox("Drug use?", ["No", "Occasionally", "Yes", "Prefer not to say"])
        
        with col2:
            st.write("**Preferences:**")
            pets = st.text_input("Do you have pets?", help="Any pets or allergies?")
            hobbies = st.text_area("Hobbies and interests", help="What do you enjoy doing?", height=80)
            living_situation = st.selectbox("Living Situation", ["Alone", "With family", "With roommates", "With partner", "Other"])
        
        # Content Creation Interest
        st.header("📸 Content Creation Interest")
        
        content_interest = st.selectbox(
            "Interest in content creation",
            ["Not interested", "Somewhat interested", "Very interested", "Extremely interested"],
            help="Interest in photos, videos, or other content creation"
        )
        
        if content_interest != "Not interested":
            col1, col2 = st.columns(2)
            
            with col1:
                content_types = st.multiselect(
                    "Types of content you'd be interested in:",
                    ["Photos", "Videos", "Audio", "Written content", "Live streaming", "Other"]
                )
            
            with col2:
                content_comfort = st.selectbox(
                    "Comfort level with content sharing",
                    ["Private only", "Limited sharing", "Public sharing", "Commercial use"]
                )
        
        # Innovation Project Interest (Admin-only feature)
        st.header("🚀 Innovation Project Interest")
        
        innovation_interest = st.selectbox(
            "Interest in advanced technology projects",
            ["Not interested", "Somewhat interested", "Very interested", "Extremely interested"],
            help="Interest in cutting-edge technology and innovation projects"
        )
        
        if innovation_interest != "Not interested":
            st.info("💡 **Innovation Projects:** We're developing advanced technology solutions for enhanced communication and safety.")
        
        # Additional Information
        st.header("📋 Additional Information")
        
        referral = st.text_input("How did you hear about us?", help="e.g., website, friend, specific event.")
        
        expectations = st.text_area(
            "What are your expectations from this dynamic?",
            help="What do you hope to gain or experience?",
            height=100
        )
        
        concerns = st.text_area(
            "Any concerns or questions?",
            help="Anything you'd like to discuss or clarify?",
            height=100
        )
        
        anything_else = st.text_area(
            "Is there anything else you'd like us to know?",
            help="Any additional information you'd like to share about yourself, your interests, or what you're looking for.",
            height=100
        )
        
        # Terms and Conditions
        st.markdown("---")
        st.subheader("📋 Terms and Conditions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            agree_terms = st.checkbox(
                "I agree to the terms and conditions *",
                help="You must agree to the terms to submit your application"
            )
            
            agree_privacy = st.checkbox(
                "I agree to the privacy policy *",
                help="You must agree to the privacy policy to submit your application"
            )
        
        with col2:
            age_verification = st.checkbox(
                "I am 18 years or older *",
                help="You must be 18 or older to apply"
            )
            
            consent_recording = st.checkbox(
                "I consent to potential recording for safety purposes",
                help="Optional - for safety and verification"
            )
        
        # Submit button
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("🚀 Submit Application", use_container_width=True, type="primary")
        with col2:
            if st.form_submit_button("← Back to Portal", use_container_width=True):
                st.session_state.show_application_form = False
                st.rerun()
        
        if submitted:
            # Validation
            required_fields = [full_name, email, age, location, interests, limits]
            required_agreements = [agree_terms, agree_privacy, age_verification]
            
            if not all(required_fields):
                st.error("❌ Please fill in all required fields.")
            elif not all(required_agreements):
                st.error("❌ You must agree to all required terms and conditions.")
            else:
                # Prepare comprehensive application data
                application_data = {
                    "personal_info": {
                        "full_name": full_name,
                        "email": email,
                        "phone": phone,
                        "age": age,
                        "location": location,
                        "occupation": occupation,
                        "education": education,
                        "relationship_status": relationship_status,
                        "height": height,
                        "weight": weight,
                        "body_type": body_type,
                        "hair_color": hair_color,
                        "eye_color": eye_color,
                        "tattoos": tattoos
                    },
                    "experience": {
                        "level": experience,
                        "interests": interests,
                        "limits": limits,
                        "kink_ratings": {
                            "bondage": bondage_interest,
                            "impact": impact_interest,
                            "service": service_interest,
                            "control": control_interest,
                            "roleplay": roleplay_interest,
                            "humiliation": humiliation_interest,
                            "cbt": cbt_interest,
                            "findom": findom_interest
                        }
                    },
                    "availability": {
                        "description": availability,
                        "time_commitment": time_commitment,
                        "commitment_level": commitment,
                        "travel_availability": travel_availability
                    },
                    "lifestyle": {
                        "smoking": smoking,
                        "drinking": drinking,
                        "drugs": drugs,
                        "pets": pets,
                        "hobbies": hobbies,
                        "living_situation": living_situation
                    },
                    "content_creation": {
                        "interest": content_interest,
                        "types": content_types if content_interest != "Not interested" else [],
                        "comfort_level": content_comfort if content_interest != "Not interested" else None
                    },
                    "innovation": {
                        "interest": innovation_interest
                    },
                    "additional": {
                        "referral": referral,
                        "expectations": expectations,
                        "concerns": concerns,
                        "anything_else": anything_else
                    },
                    "consent": {
                        "terms": agree_terms,
                        "privacy": agree_privacy,
                        "age_verification": age_verification,
                        "recording_consent": consent_recording
                    }
                }
                
                st.success("✅ Application submitted successfully! We will review it shortly.")
                st.info("📧 You will receive a confirmation email shortly.")
                
                # Show summary
                with st.expander("📋 Application Summary", expanded=True):
                    st.write("**Personal Information:**")
                    st.write(f"• Name: {full_name}")
                    st.write(f"• Email: {email}")
                    st.write(f"• Age: {age}")
                    st.write(f"• Location: {location}")
                    st.write(f"• Occupation: {occupation}")
                    
                    st.write("**Experience Level:** " + experience)
                    st.write("**Commitment Level:** " + commitment)
                    st.write("**Content Creation Interest:** " + content_interest)
                    st.write("**Innovation Project Interest:** " + innovation_interest)
                    
                    st.write("**Kink Compatibility Scores:**")
                    st.write(f"• Bondage: {bondage_interest}/5")
                    st.write(f"• Impact Play: {impact_interest}/5")
                    st.write(f"• Service: {service_interest}/5")
                    st.write(f"• Control: {control_interest}/5")

if __name__ == "__main__":
    show_comprehensive_application_form()
