import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import folium_static
from datetime import datetime
import xmltodict

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Cancer Support App",
    layout="wide",
    page_icon=":hospital:"
)

# --- CUSTOM CSS STYLES ---
st.markdown(
    """
    <style>
    /* Hide default Streamlit menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Global fonts and background */
    html, body {
        background: linear-gradient(135deg, #0e0e0e 0%, #1c1c1c 100%);
        color: #FFFFFF;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Sidebar styling */
    .css-1cpxqw2, .css-1d391kg, .css-18e3th9 {
        background-color: #1c1c1c !important;
        border-right: 1px solid #444 !important;
    }
    .css-1cpxqw2 a, .css-1d391kg a {
        color: #EEE !important;
        font-weight: 500 !important;
    }
    .css-1cpxqw2 .css-qrbaxs, .css-1d391kg .css-qrbaxs {
        color: #FFF !important;
    }

    /* Scrollbar */
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

    /* Titles and headings */
    h1, h2, h3, h4 {
        text-shadow: 1px 1px 2px #000000;
    }

    /* Buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #F83600 0%, #F9D423 100%);
        color: #000;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        cursor: pointer;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        filter: brightness(1.1);
        transform: scale(1.02);
    }

    /* Inputs */
    input, select, textarea {
        border-radius: 6px !important;
        background-color: #2f2f2f !important;
        color: #fff !important;
        border: 1px solid #555 !important;
    }
    input:focus, select:focus, textarea:focus {
        outline: none !important;
        border: 1px solid #f9d423 !important;
    }

    /* Dataframe styling */
    .stDataFrame, .stDataFrame table {
        color: #fff !important;
        background-color: #2f2f2f !important;
    }
    .stDataFrame tr:nth-child(even) {
        background-color: #3f3f3f !important;
    }
    .stDataFrame thead tr {
        background-color: #444 !important;
    }

    /* Headers in dataframes */
    .stDataFrame thead tr th {
        color: #f0f0f0 !important;
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
        <div style="
            text-align: center; 
            padding: 60px 20px; 
            background: linear-gradient(135deg, rgba(248,54,0,0.2), rgba(249,212,35,0.2));
            border-radius: 10px;
            margin-bottom: 2rem;">
            <h1 style="font-size: 3rem; color: #ffffff; 
                       text-shadow: 2px 2px 8px rgba(0,0,0,0.7);
                       margin-bottom: 0.5rem;">
                Cancer Support Web Application
            </h1>
            <p style="font-size: 1.2rem; max-width: 700px; margin: 0 auto; line-height: 1.6; color: #f0f0f0;">
                A comprehensive platform to assist cancer patients and their families with hospital searches, 
                accommodation resources, latest research, clinical trials, financial support, and more.
            </p>
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
            # Define headers with User-Agent for Nominatim API
            headers = {
                "User-Agent": "CancerSupportApp/1.0 (your_email@example.com)"
            }
            
            # Geocoding using Nominatim with headers
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
                
                # Overpass API to find hospitals
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
            # Fetch latest 10 articles from PubMed
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
                # Fetch article details
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

    # Placeholder for Notifications and AI Chatbot
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
            # Refine the search query with field-specific tags
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
            
            # Define headers with User-Agent
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
            
            # Parse the XML response
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
                        
                        # Handle multiple locations
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
    
    # Checklist Generator
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
    
    # Donation Hub
    st.header("Donation Hub")
    st.markdown("""
    **Support patients in need by donating to reputable charities and crowdfunding platforms:**
    
    - **CancerCare**: [Donate](https://www.cancercare.org/donate)
    - **Ronald McDonald House Charities**: [Donate](https://www.rmhc.org/donate)
    - **GoFundMe**: [Create a Fundraiser](https://www.gofundme.com/)
    - **Crowdfunder**: [Start a Campaign](https://www.crowdfunder.com/)
    """)

