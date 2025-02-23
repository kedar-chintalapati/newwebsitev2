import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import folium_static
import xmltodict

# 1. PAGE CONFIG
st.set_page_config(
    page_title="Cancer Support App",
    layout="wide",
    page_icon=":hospital:",
    initial_sidebar_state="expanded"
)

# 2. CUSTOM CSS & LOTTIE BACKGROUND
st.markdown(
    """
    <style>
    /* ------------------------------------------------------------------
       1. GLOBAL RESETS & FONTS
    ------------------------------------------------------------------ */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
      margin: 0;
      padding: 0;
      font-family: 'Poppins', sans-serif;
      background-color: #000000 !important; /* fallback if Lottie fails */
      color: #FFFFFF !important;
      overflow-x: hidden; /* no horizontal scroll */
    }

    /* Hide default Streamlit menu & footer */
    [data-testid="stHeader"] {display: none !important;}
    footer {visibility: hidden;}

    /* 
      2. LOTTIE BACKGROUND
      We'll place a <lottie-player> behind everything with z-index:-999 
    */
    .lottie-bg-container {
      position: fixed;
      top: 0; left: 0;
      width: 100%;
      height: 100%;
      z-index: -999;
      overflow: hidden;
    }
    .lottie-bg-container lottie-player {
      width: 100% !important;
      height: 100% !important;
      background: #00000000 !important;
    }

    /* 
      3. MAKE MAIN CONTENT TRANSPARENT 
      so the background is visible
    */
    .block-container, .main, .css-18e3th9, .css-1cpxqw2, .css-1d391kg {
      background: transparent !important;
    }

    /* 
      4. SIDEBAR STYLING 
    */
    [data-testid="stSidebar"] {
      background: rgba(10, 10, 10, 0.8) !important;
      backdrop-filter: blur(8px);
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] li, 
    [data-testid="stSidebar"] div, [data-testid="stSidebar"] span {
      color: #EEE !important;
      text-shadow: 1px 1px 2px #000000;
    }

    /* 
      5. SCROLL-SNAP FOR FULL-SCREEN SECTIONS 
    */
    html {
      scroll-behavior: smooth;
    }
    [data-testid="stAppViewContainer"] {
      scroll-snap-type: y mandatory;
    }
    .section {
      scroll-snap-align: start;
      min-height: 100vh;
      padding: 60px 20px;
    }

    /* 
      6. HEADINGS & NEON GLOW
    */
    h1, h2, h3, h4 {
      text-shadow: 0 0 8px rgba(255,255,255,0.1),
                   1px 1px 6px rgba(0,0,0,0.8);
      font-weight: 600;
      color: #ffffff;
    }
    h1 {
      font-size: 3rem !important;
    }

    /* 
      7. BUTTONS 
    */
    div.stButton > button {
      background: linear-gradient(to right, #ff0080, #7928ca);
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
      8. INPUTS, SELECTS, TEXTAREAS
    */
    input, select, textarea {
      background-color: rgba(50, 50, 60, 0.8) !important;
      color: #fff !important;
      border: 1px solid #555 !important;
      border-radius: 6px !important;
    }
    input:focus, select:focus, textarea:focus {
      outline: none !important;
      border: 1px solid #7928ca !important;
    }

    /* 8a. Fix placeholder color in dropdowns / multiselect */
    .stMultiSelect .css-1wa3eu0-placeholder {
      color: #aaa !important;
    }
    .stMultiSelect div[role="option"] {
      color: #fff !important;
      background-color: #333 !important;
    }

    /* 
      9. TABLES & DATAFRAMES 
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
      10. SCROLLBAR 
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
    </style>

    <!--  Lottie Background Container  -->
    <div class="lottie-bg-container">
      <lottie-player 
          src="https://assets1.lottiefiles.com/packages/lf20_3rwasyjy.json" 
          background="transparent"  
          speed="1"  
          loop  
          autoplay
      >
      </lottie-player>
    </div>
    """,
    unsafe_allow_html=True
)

# 3. SIDEBAR NAVIGATION (ANCHOR LINKS)
st.sidebar.title("Navigation")
st.sidebar.markdown("""
<ul style="list-style:none; padding-left: 0;">
  <li><a href="#home">Home</a></li>
  <li><a href="#locate-hospitals">Locate Hospitals</a></li>
  <li><a href="#accommodation-resources">Accommodation Resources</a></li>
  <li><a href="#latest-research">Latest Research</a></li>
  <li><a href="#financial-support">Financial Support</a></li>
  <li><a href="#clinical-trials">Clinical Trials</a></li>
  <li><a href="#emotional-support">Emotional & Social Support</a></li>
  <li><a href="#interactive-tools">Interactive Tools & Extras</a></li>
</ul>
""", unsafe_allow_html=True)


# 4. HOME SECTION
st.markdown('<div class="section" id="home"></div>', unsafe_allow_html=True)
st.markdown("""
# Home
## Cancer Support Web Application

A comprehensive platform to assist cancer patients and their families with hospital searches, 
accommodation resources, latest research, clinical trials, financial support, and more.

---
""")

st.image(
    "https://www.cancer.org/content/dam/cancer-org/images/logos/cancerorg-logo.png",
    use_column_width=True
)


# 5. LOCATE HOSPITALS
st.markdown('<div class="section" id="locate-hospitals"></div>', unsafe_allow_html=True)
st.title("Locate the Best Cancer Hospitals Nearby")

st.markdown("""
Find top-rated cancer hospitals in your area. Use the interactive map below to explore nearby facilities.
""")

location = st.text_input("Enter your city or ZIP code:", "New York")
if st.button("Find Hospitals"):
    with st.spinner("Searching for hospitals..."):
        headers = {"User-Agent": "CancerSupportApp/1.0 (your_email@example.com)"}
        geocode_url = "https://nominatim.openstreetmap.org/search"
        geocode_params = {"q": location, "format": "json", "limit": 1}
        
        try:
            geocode_response = requests.get(geocode_url, headers=headers, params=geocode_params, timeout=10)
            geocode_response.raise_for_status()
            geocode_data = geocode_response.json()
        except Exception as e:
            st.error(f"Geocoding error: {e}")
            st.stop()
        
        if geocode_data:
            lat = geocode_data[0].get('lat')
            lon = geocode_data[0].get('lon')
            if lat and lon:
                lat, lon = float(lat), float(lon)
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
                except Exception as e:
                    st.error(f"Overpass API error: {e}")
                    st.stop()

                hospitals = []
                for element in overpass_data.get('elements', []):
                    tags = element.get('tags', {})
                    name = tags.get('name', 'Unnamed Hospital')
                    lat_h = element.get('lat') or (element.get('center', {}).get('lat') if element.get('center') else None)
                    lon_h = element.get('lon') or (element.get('center', {}).get('lon') if element.get('center') else None)
                    if lat_h and lon_h:
                        hospitals.append({"Name": name, "Latitude": lat_h, "Longitude": lon_h})
                
                if hospitals:
                    df_hospitals = pd.DataFrame(hospitals)
                    # Display map
                    m = folium.Map(location=[lat, lon], zoom_start=12)
                    folium.Marker(
                        [lat, lon],
                        popup="Your Location",
                        icon=folium.Icon(color='red', icon='home')
                    ).add_to(m)
                    
                    for _, row in df_hospitals.iterrows():
                        folium.Marker(
                            [row['Latitude'], row['Longitude']],
                            popup=row['Name'],
                            icon=folium.Icon(color='blue', icon='plus-sign')
                        ).add_to(m)
                    
                    folium_static(m, width=700, height=500)
                    
                    st.subheader("List of Hospitals")
                    st.dataframe(df_hospitals)
                else:
                    st.warning("No hospitals found within a 50km radius.")
            else:
                st.warning("Could not retrieve latitude/longitude.")
        else:
            st.warning("Location not found. Please try again.")


# 6. ACCOMMODATION RESOURCES
st.markdown('<div class="section" id="accommodation-resources"></div>', unsafe_allow_html=True)
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


# 7. LATEST RESEARCH
st.markdown('<div class="section" id="latest-research"></div>', unsafe_allow_html=True)
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
        try:
            response = requests.get(base_url, params=params).json()
            id_list = response['esearchresult']['idlist']
        except Exception as e:
            st.error(f"Error searching PubMed: {e}")
            st.stop()

        if id_list:
            fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
            fetch_params = {
                "db": "pubmed",
                "id": ",".join(id_list),
                "retmode": "xml",
                "rettype": "abstract"
            }
            try:
                fetch_response = requests.get(fetch_url, params=fetch_params).text
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
                st.error(f"Error fetching PubMed abstracts: {e}")
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


# 8. FINANCIAL SUPPORT
st.markdown('<div class="section" id="financial-support"></div>', unsafe_allow_html=True)
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
        # Placeholder calculation: e.g., 0% for Stage IV
        tax = 0
        st.write(f"**Estimated Tax on Withdrawal:** ${tax}")
        st.success("Calculation completed. Please consult a financial advisor for accurate information.")


# 9. CLINICAL TRIALS
st.markdown('<div class="section" id="clinical-trials"></div>', unsafe_allow_html=True)
st.title("Clinical Trials Finder")
st.markdown("""
**Find relevant clinical trials based on your condition, location, and treatment phase. Participate in studies to access cutting-edge treatments.**
""")

cancer_type_ct = st.text_input("Enter your cancer type (e.g., Lung Cancer):", "Lung Cancer", key="ct_input")
location_ct = st.text_input("Enter your location or ZIP code:", "New York", key="ct_loc")
phase_ct = st.selectbox("Select Trial Phase:", ["All", "Phase 1", "Phase 2", "Phase 3", "Phase 4"], key="ct_phase")

if st.button("Find Clinical Trials", key="ct_button"):
    with st.spinner("Searching for clinical trials..."):
        query = f"{cancer_type_ct}[Condition] AND {location_ct}[Location]"
        if phase_ct != "All":
            query += f" AND {phase_ct}[Phase]"
        
        base_url = "https://clinicaltrials.gov/api/query/study/search/brief"
        params = {
            "expr": query,
            "min_rnk": 1,
            "max_rnk": 20,
            "fmt": "xml"
        }
        headers = {"User-Agent": "CancerSupportApp/1.0 (your_email@example.com)"}
        
        try:
            response = requests.get(base_url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
        except Exception as e:
            st.error(f"ClinicalTrials.gov error: {e}")
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
            st.error(f"Error parsing clinical trials data: {e}")

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


# 10. EMOTIONAL & SOCIAL SUPPORT
st.markdown('<div class="section" id="emotional-support"></div>', unsafe_allow_html=True)
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


# 11. INTERACTIVE TOOLS & EXTRAS
st.markdown('<div class="section" id="interactive-tools"></div>', unsafe_allow_html=True)
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
