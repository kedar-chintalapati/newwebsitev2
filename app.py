import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import folium_static
import xmltodict

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Cancer Support App",
    layout="wide",
    page_icon=":hospital:",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS WITH ANIMATIONS ---
st.markdown(
    """
    <style>
    /* 
     =============================================================================
       0. IMPORT FONTS 
     =============================================================================
    */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    /* 
     =============================================================================
       1. OVERRIDE STREAMLIT'S DEFAULT (LIGHT) THEME
         Target modern Streamlit containers by data-testid or class:
         - stAppViewContainer: main page area
         - stSidebar: the sidebar area
     =============================================================================
    */
    html, body, [data-testid="stAppViewContainer"] {
        margin: 0; 
        padding: 0;
        font-family: 'Poppins', sans-serif;
        color: #FFFFFF !important;
        background: linear-gradient(135deg, #232526, #414345, #232526);
        background-size: 600% 600%;
        animation: gradientBG 20s ease infinite;
    }
    [data-testid="stSidebar"] {
        background: rgba(0, 0, 0, 0.85) !important;
    }
    /* Force the main block container to be transparent */
    .css-18e3th9, .css-1cpxqw2, .css-1d391kg, .block-container {
        background: transparent !important;
    }

    @keyframes gradientBG {
      0% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }

    /* Hide default Streamlit menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* 
     =============================================================================
       2. SCROLLBAR
     =============================================================================
    */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #1c1c1c;
    }
    ::-webkit-scrollbar-thumb {
        background-color: #666;
        border-radius: 4px;
    }

    /* 
     =============================================================================
       3. HEADINGS & TEXT
     =============================================================================
    */
    h1, h2, h3, h4 {
        font-family: 'Poppins', sans-serif;
        text-shadow: 1px 1px 6px rgba(0, 0, 0, 0.8),
                     0 0 8px rgba(255, 255, 255, 0.1);
        color: #FFFFFF;
    }
    h1 {
        font-size: 3rem !important;
        font-weight: 600;
    }
    h2 {
        font-size: 2.2rem !important;
    }
    h3 {
        font-size: 1.6rem !important;
    }
    h4 {
        font-size: 1.3rem !important;
    }
    p, div, label, span, li, a, button {
        color: #EEE !important;
        font-family: 'Poppins', sans-serif !important;
    }

    /* 
     =============================================================================
       4. BUTTONS
     =============================================================================
    */
    div.stButton > button {
        background: linear-gradient(to right, #6a11cb, #2575fc);
        color: #fff;
        border: none;
        border-radius: 30px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        cursor: pointer;
        transition: 0.3s;
        box-shadow: 0 3px 8px rgba(0,0,0,0.3);
    }
    div.stButton > button:hover {
        filter: brightness(1.1);
        transform: scale(1.03);
        box-shadow: 0 6px 14px rgba(0,0,0,0.4);
    }

    /* 
     =============================================================================
       5. FORM INPUTS
     =============================================================================
    */
    input, select, textarea {
        border-radius: 6px !important;
        background-color: rgba(50, 50, 60, 0.8) !important;
        color: #fff !important;
        border: 1px solid #555 !important;
        font-family: 'Poppins', sans-serif;
    }
    input:focus, select:focus, textarea:focus {
        outline: none !important;
        border: 1px solid #2575fc !important;
    }

    /* 
     =============================================================================
       6. TABLES & DATAFRAMES
     =============================================================================
    */
    .stDataFrame, .stDataFrame table {
        color: #fff !important;
        background-color: #2f2f3f !important;
    }
    .stDataFrame tr:nth-child(even) {
        background-color: #3f3f5f !important;
    }
    .stDataFrame thead tr {
        background-color: #444 !important;
    }
    .stDataFrame thead tr th {
        color: #f0f0f0 !important;
    }

    /* 
     =============================================================================
       7. HERO / SECTION STYLING
     =============================================================================
    */
    .hero-section {
        position: relative;
        text-align: center; 
        padding: 80px 20px; 
        margin-bottom: 2rem;
        background: rgba(0, 0, 0, 0.4);
        border-radius: 10px;
        overflow: hidden;
    }
    .hero-section::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(#ffffff33, #00000000);
        animation: pulse 6s infinite;
        z-index: 1;
    }
    @keyframes pulse {
        0% { transform: scale(1); opacity: 0.7; }
        50% { transform: scale(1.2); opacity: 0.3; }
        100% { transform: scale(1); opacity: 0.7; }
    }
    .hero-content {
        position: relative;
        z-index: 2;
        max-width: 800px;
        margin: 0 auto;
    }
    .hero-content h1 {
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
        color: #fff;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.7),
                     0 0 10px rgba(255,255,255,0.2);
    }
    .hero-content p {
        font-size: 1.2rem;
        line-height: 1.6;
        color: #ddd;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
options = st.sidebar.radio("Go to", [
    "Home",
    "Locate Hospitals",
    "Accommodation Resources",
    "Latest Research",
    "Financial Support",
    "Clinical Trials",
    "Emotional & Social Support",
    "Interactive Tools & Extras"
])

# =========================
#        HOME PAGE
# =========================
if options == "Home":
    # Hero Section
    st.markdown(
        """
        <div class="hero-section">
            <div class="hero-content">
                <h1>Cancer Support Web Application</h1>
                <p>A comprehensive platform to assist cancer patients and their families 
                   with hospital searches, accommodation resources, latest research, 
                   clinical trials, financial support, and more.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("""
    Welcome to the **Cancer Support Web Application**. Navigate through the sidebar to access various sections:

    - **Locate Hospitals**: Find top-rated cancer hospitals near you.
    - **Accommodation Resources**: Discover lodging options during treatment.
    - **Latest Research**: Stay updated with the newest cancer research.
    - **Financial Support**: Learn about financial relief and legal rights.
    - **Clinical Trials**: Find relevant clinical trials for your condition.
    - **Emotional & Social Support**: Access mental health resources and support groups.
    - **Interactive Tools & Extras**: Utilize tools like checklists and donation hubs.
    """)

    st.image(
        "https://www.cancer.org/content/dam/cancer-org/images/logos/cancerorg-logo.png",
        use_column_width=True
    )

# =========================
#  LOCATE HOSPITALS PAGE
# =========================
elif options == "Locate Hospitals":
    st.title("Locate the Best Cancer Hospitals Nearby")
    
    st.markdown("""
    **Find top-rated cancer hospitals specializing in your area. Use the interactive map below to explore nearby facilities.**
    """)
    
    # User input for location
    location = st.text_input("Enter your city or ZIP code:", "New York")
    
    if st.button("Find Hospitals"):
        with st.spinner("Searching for hospitals..."):
            headers = {
                "User-Agent": "CancerSupportApp/1.0 (your_email@example.com)"
            }
            geocode_url = "https://nominatim.openstreetmap.org/search"
            geocode_params = {
                "q": location,
                "format": "json",
                "limit": 1
            }
            
            try:
                geocode_response = requests.get(geocode_url, headers=headers, params=geocode_params, timeout=10)
                geocode_response.raise_for_status()
                geocode_data = geocode_response.json()
            except requests.exceptions.HTTPError as http_err:
                st.error(f"HTTP error occurred during geocoding: {http_err}")
                st.stop()
            except requests.exceptions.Timeout:
                st.error("The request timed out. Please try again later.")
                st.stop()
            except requests.exceptions.RequestException as req_err:
                st.error(f"An error occurred during geocoding: {req_err}")
                st.stop()
            except ValueError:
                st.error("Received an invalid response from the geocoding service.")
                st.stop()
            
            if geocode_data:
                lat = geocode_data[0].get('lat')
                lon = geocode_data[0].get('lon')
                
                if not lat or not lon:
                    st.error("Could not retrieve latitude and longitude for the specified location.")
                    st.stop()
                
                try:
                    lat = float(lat)
                    lon = float(lon)
                except ValueError:
                    st.error("Invalid latitude or longitude values received.")
                    st.stop()
                
                overpass_url = "http://overpass-api.de/api/interpreter"
                overpass_query = f"""
                [out:json];
                (
                  node["amenity"="hospital"](around:50000,{lat},{lon});
                  way["amenity"="hospital"](around:50000,{lat},{lon});
                  relation["amenity"="hospital"](around:50000,{lat},{lon});
                );
                out center;
                """
                
                try:
                    overpass_response = requests.get(overpass_url, params={'data': overpass_query}, headers=headers, timeout=10)
                    overpass_response.raise_for_status()
                    overpass_data = overpass_response.json()
                except requests.exceptions.HTTPError as http_err:
                    st.error(f"HTTP error occurred while fetching hospitals: {http_err}")
                    st.stop()
                except requests.exceptions.Timeout:
                    st.error("The request to Overpass API timed out. Please try again later.")
                    st.stop()
                except requests.exceptions.RequestException as req_err:
                    st.error(f"An error occurred while fetching hospitals: {req_err}")
                    st.stop()
                except ValueError:
                    st.error("Received an invalid response from the Overpass API.")
                    st.stop()
                
                hospitals = []
                for element in overpass_data.get('elements', []):
                    tags = element.get('tags', {})
                    name = tags.get('name', 'Unnamed Hospital')
                    lat_h = element.get('lat') or (element.get('center', {}).get('lat') if element.get('center') else None)
                    lon_h = element.get('lon') or (element.get('center', {}).get('lon') if element.get('center') else None)
                    if lat_h and lon_h:
                        hospitals.append({
                            "Name": name,
                            "Latitude": lat_h,
                            "Longitude": lon_h
                        })
                
                if hospitals:
                    df_hospitals = pd.DataFrame(hospitals)
                    
                    # Display on map
                    m = folium.Map(location=[lat, lon], zoom_start=12)
                    folium.Marker(
                        [lat, lon],
                        popup="Your Location",
                        icon=folium.Icon(color='red', icon='home')
                    ).add_to(m)
                    
                    for idx, row in df_hospitals.iterrows():
                        folium.Marker(
                            [row['Latitude'], row['Longitude']],
                            popup=row['Name'],
                            icon=folium.Icon(color='blue', icon='plus-sign')
                        ).add_to(m)
                    
                    folium_static(m, width=700, height=500)
                    
                    st.subheader("List of Hospitals")
                    st.dataframe(df_hospitals)
                else:
                    st.error("No hospitals found within a 50km radius.")
            else:
                st.error("Location not found. Please try a different location.")

# =========================
#  ACCOMMODATION RESOURCES
# =========================
elif options == "Accommodation Resources":
    st.title("Accommodation Resources")
    st.markdown("""
    **Find lodging solutions for patients and their families during treatment. Below are some recommended resources:**
    """)
    
    st.header("Ronald McDonald House Charities")
    st.markdown("""
    [Ronald McDonald House](https://www.rmhc.org/) provides a place for families to stay while their loved ones receive treatment.
    """)
    
    st.header("Local Support Housing Programs")
    st.markdown("""
    - **CancerCare Housing Assistance**: [CancerCare](https://www.cancercare.org/)
    - **Hospice Housing Programs**: [Hospice Foundation](https://hospicefoundation.org/)
    """)
    
    st.header("Low-Cost Hotels Near Treatment Centers")
    st.markdown("""
    - [Booking.com](https://www.booking.com/) - Filter by proximity to your treatment center.
    - [Airbnb](https://www.airbnb.com/) - Affordable lodging options.
    """)
    
    st.header("Booking Links")
    st.markdown("""
    - [Reserve a Ronald McDonald House](https://www.rmhc.org/find-a-house)
    - [CancerCare Housing Assistance](https://www.cancercare.org/support_resources/housing_assistance)
    """)

# =========================
#   LATEST RESEARCH
# =========================
elif options == "Latest Research":
    st.title("Latest Research and AI-Driven Insights")
    st.markdown("""
    **Stay updated with the latest research, treatment advancements, and breakthroughs related to your specific cancer type.**
    """)
    
    cancer_type = st.text_input("Enter your cancer type (e.g., Breast Cancer):", "Breast Cancer")
    
    if st.button("Get Latest Research"):
        with st.spinner("Fetching latest research articles..."):
            base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
            params = {
                "db": "pubmed",
                "term": cancer_type,
                "retmax": 10,
                "sort": "pub date",
                "retmode": "json"
            }
            response = requests.get(base_url, params=params).json()
            id_list = response['esearchresult']['idlist']
            
            if id_list:
                fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
                fetch_params = {
                    "db": "pubmed",
                    "id": ",".join(id_list),
                    "retmode": "xml",
                    "rettype": "abstract"
                }
                fetch_response = requests.get(fetch_url, params=fetch_params).text
                
                # Parse XML response using xmltodict
                try:
                    data_dict = xmltodict.parse(fetch_response)
                    articles = data_dict.get('PubmedArticleSet', {}).get('PubmedArticle', [])
                    
                    if isinstance(articles, dict):
                        articles = [articles]
                    
                    st.markdown("### Latest Research Articles")
                    for article in articles:
                        title = article.get('MedlineCitation', {}).get('Article', {}).get('ArticleTitle', 'No Title')
                        pmid = article.get('MedlineCitation', {}).get('PMID', {}).get('#text', '')
                        link = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                        st.markdown(f"#### [{title}]({link})")
                except Exception as e:
                    st.error("Error parsing research articles.")
            else:
                st.warning("No articles found for the specified cancer type.")

    st.markdown("---")
    st.header("Stay Informed")
    st.markdown("""
    **Subscribe to email notifications** to receive updates on newly published studies and breakthroughs.

    *Feature coming soon!*
    """)

    st.header("AI Chatbot Assistance")
    st.markdown("""
    **Have questions about the latest research or treatments?**

    *AI chatbot integration is under development!*
    """)

# =========================
#  FINANCIAL SUPPORT
# =========================
elif options == "Financial Support":
    st.title("Financial Support and Legal Options")
    st.markdown("""
    **Access information on financial relief, legal rights, and assistance programs to help manage the financial burden of cancer treatment.**
    """)
    
    st.header("Corporate Angel Network")
    st.markdown("""
    **Details on Corporate Angel Network**:
    - **Free Flights for Patients**: Assistance with travel arrangements for treatment.
    - **How to Apply**: [Corporate Angel Network Application](https://apexlg.com/an-example-of-social-entrepreneurship-from-nbcs-shark-tank/)
    """)
    
    st.header("Tax-Free Retirement Withdrawals")
    st.markdown("""
    Stage IV patients can withdraw money from retirement accounts tax-free under specific conditions.
    
    **More Information**:
    - [Diana Award](https://diana-award.org.uk/)
    - [IRS Guidelines on Retirement Withdrawals](https://www.irs.gov/retirement-plans/retirement-plans-faqs-regarding-required-minimum-distributions)
    """)
    
    st.header("Insurance Navigation")
    st.markdown("""
    - **Understanding Coverage**: [Health Insurance Basics](https://www.healthcare.gov/glossary/)
    - **Assistance Programs for Uninsured Patients**: [CancerCare Assistance](https://www.cancercare.org/)
    """)
    
    st.header("Interactive Financial Calculator")
    st.markdown("Estimate potential savings, grants, or tax benefits based on your data.")
    
    with st.form("financial_calculator"):
        income = st.number_input("Enter your annual income ($):", min_value=0, value=50000, step=1000)
        retirement_withdraw = st.number_input("Enter amount to withdraw from retirement account ($):", min_value=0, value=10000, step=1000)
        submitted = st.form_submit_button("Calculate")
        
        if submitted:
            # Placeholder calculation: Assuming 0% tax for Stage IV withdrawals
            tax = 0  # Placeholder logic
            st.write(f"**Estimated Tax on Withdrawal:** ${tax}")
            st.success("Calculation completed. Please consult a financial advisor for accurate information.")

# =========================
#   CLINICAL TRIALS
# =========================
elif options == "Clinical Trials":
    st.title("Clinical Trials Finder")
    st.markdown("""
    **Find relevant clinical trials based on your condition, location, and treatment phase. Participate in studies to access cutting-edge treatments.**
    """)
    
    # User Inputs
    cancer_type = st.text_input("Enter your cancer type (e.g., Lung Cancer):", "Lung Cancer")
    location = st.text_input("Enter your location or ZIP code:", "New York")
    phase = st.selectbox("Select Trial Phase:", ["All", "Phase 1", "Phase 2", "Phase 3", "Phase 4"])
    
    if st.button("Find Clinical Trials"):
        with st.spinner("Searching for clinical trials..."):
            query = f"{cancer_type}[Condition] AND {location}[Location]"
            if phase != "All":
                query += f" AND {phase}[Phase]"
            
            base_url = "https://clinicaltrials.gov/api/query/study/search/brief"
            params = {
                "expr": query,
                "min_rnk": 1,
                "max_rnk": 20,
                "fmt": "xml"
            }
            headers = {
                "User-Agent": "CancerSupportApp/1.0 (your_email@example.com)"
            }
            
            try:
                response = requests.get(base_url, params=params, headers=headers, timeout=10)
                response.raise_for_status()
            except requests.exceptions.HTTPError as http_err:
                st.error(f"HTTP error occurred while fetching clinical trials: {http_err}")
                st.stop()
            except requests.exceptions.Timeout:
                st.error("The request timed out. Please try again later.")
                st.stop()
            except requests.exceptions.RequestException as req_err:
                st.error(f"An error occurred while fetching clinical trials: {req_err}")
                st.stop()
            
            try:
                data_dict = xmltodict.parse(response.content)
                studies = data_dict.get('clinical_studies', {}).get('clinical_study', [])
                
                if isinstance(studies, dict):
                    studies = [studies]
                
                if studies:
                    st.markdown("### Found Clinical Trials")
                    for study in studies:
                        title = study.get('official_title', 'No Title')
                        status = study.get('overall_status', 'Status Unknown')
                        
                        location_info = study.get('location_countries', {}).get('location_country', [])
                        if isinstance(location_info, dict):
                            location_info = [location_info]
                        locations = ", ".join([loc.get('location', 'Unknown') for loc in location_info])
                        
                        phase_text = study.get('phase', 'N/A')
                        nct_id = study.get('id_info', {}).get('nct_id', '')
                        link = f"https://clinicaltrials.gov/ct2/show/{nct_id}" if nct_id else "#"
                        
                        st.markdown(f"#### [{title}]({link})")
                        st.write(f"**Status:** {status}")
                        st.write(f"**Phase:** {phase_text}")
                        st.write(f"**Locations:** {locations}")
                        st.markdown("---")
                else:
                    st.warning("No clinical trials found for the given criteria.")
            except Exception as e:
                st.error("Error parsing clinical trials data.")
    
    st.markdown("---")
    st.header("Enrollment Guide")
    st.markdown("""
    **How to Enroll in a Trial**:
    1. **Consult Your Doctor**: Discuss eligibility and suitability.
    2. **Contact the Study Team**: Reach out via the provided links.
    3. **Understand the Commitment**: Review the study requirements and benefits.
    
    **Pros and Cons of Participation**:
    - **Pros**: Access to new treatments, close monitoring, contributing to research.
    - **Cons**: Possible side effects, time commitment, uncertain outcomes.
    """)

# =========================
# EMOTIONAL & SOCIAL SUPPORT
# =========================
elif options == "Emotional & Social Support":
    st.title("Emotional and Social Support")
    st.markdown("""
    **Address mental health and community-building needs with the resources below.**
    """)
    
    st.header("Counseling Options")
    st.markdown("""
    - **American Cancer Society Counseling Services**: [Find a Counselor](https://www.cancer.org/treatment/support-programs-and-services/find-support.html)
    - **CancerCare Therapy Services**: [Access Therapy](https://www.cancercare.org/services/therapy)
    - **Psychology Today**: [Find a Therapist](https://www.psychologytoday.com/us/therapists/cancer)
    """)
    
    st.header("Support Groups")
    st.markdown("""
    - **Meetup**: [Cancer Support Groups](https://www.meetup.com/topics/cancer-support/)
    - **Cancer Support Community**: [Join a Group](https://www.cancersupportcommunity.org/join-a-group)
    - **Local Hospitals and Clinics**: Many offer in-person and virtual support groups.
    """)

# =========================
# INTERACTIVE TOOLS & EXTRAS
# =========================
elif options == "Interactive Tools & Extras":
    st.title("Interactive Tools and Extras")
    st.markdown("""
    **Utilize the tools below to manage tasks and support your journey.**
    """)
    
    st.header("Checklist Generator")
    st.markdown("Create your personalized to-do list based on your needs.")
    
    with st.form("checklist_form"):
        financial_tasks = st.multiselect("Financial Tasks", [
            "Apply for insurance",
            "Meet with financial advisor",
            "Fill out tax forms",
            "Explore Corporate Angel Network",
            "Plan budget for treatments"
        ])
        medical_appointments = st.multiselect("Medical Appointments", [
            "Schedule doctor's visit",
            "Radiation therapy session",
            "Chemotherapy session",
            "Follow-up consultations",
            "Get second opinion"
        ])
        other_tasks = st.multiselect("Other Tasks", [
            "Call support group",
            "Arrange transportation",
            "Update personal documents",
            "Organize living space",
            "Plan meals"
        ])
        
        submitted = st.form_submit_button("Generate Checklist")
        
        if submitted:
            st.markdown("### Your Personalized Checklist")
            if financial_tasks:
                st.markdown("**Financial Tasks:**")
                for task in financial_tasks:
                    st.write(f"- [ ] {task}")
            if medical_appointments:
                st.markdown("**Medical Appointments:**")
                for task in medical_appointments:
                    st.write(f"- [ ] {task}")
            if other_tasks:
                st.markdown("**Other Tasks:**")
                for task in other_tasks:
                    st.write(f"- [ ] {task}")
    
    st.markdown("---")
    
    st.header("Donation Hub")
    st.markdown("""
    **Support patients in need by donating to reputable charities and crowdfunding platforms:**
    
    - **CancerCare**: [Donate](https://www.cancercare.org/donate)
    - **Ronald McDonald House Charities**: [Donate](https://www.rmhc.org/donate)
    - **GoFundMe**: [Create a Fundraiser](https://www.gofundme.com/)
    - **Crowdfunder**: [Start a Campaign](https://www.crowdfunder.com/)
    """)
