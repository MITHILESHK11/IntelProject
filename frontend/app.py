import streamlit as st
import requests
import pandas as pd
import json
import time
import base64
from datetime import datetime

# --- CONFIGURATION ---
API_URL = "http://127.0.0.1:8000"
st.set_page_config(
    page_title="Intel Knowledge Nexus",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- INITIALIZE SESSION STATE ---
if "app_state" not in st.session_state:
    st.session_state.app_state = "landing"
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = [{"id": "default", "name": "General Inquiries", "messages": []}]
if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = "default"
if "current_doc" not in st.session_state:
    st.session_state.current_doc = None
if "selected_inspector_item" not in st.session_state:
    st.session_state.selected_inspector_item = None

# --- ASSETS & STYLING ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg_img_path = r"d:\DELL\Documents\Intel\Intel Project - Enterprise Document Analyzer\Intel Project - Enterprise Document Analyzer\Images\BG.png"
try:
    bin_str = get_base64_of_bin_file(bg_img_path)
    bg_css = f"""
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    """
except:
    bg_css = "background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);"

# --- CUSTOM CSS (PREMIUM AESTHETICS) ---
st.markdown(f"""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        {bg_css}
        color: #f8fafc;
    }}
</style>
""" + """
<style>

    /* Landing Page Styling */
    .landing-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }

    /* Gradient Text */
    .gradient-text {
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 3rem;
        margin-bottom: 20px;
    }

    /* Primary Button */
    .stButton > button {
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: none;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #0ea5e9, #6366f1);
        color: white;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    }

    /* Sidebar / Nav */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    /* Dashboard Widgets */
    .css-card {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 12px;
        padding: 15px;
        border: 1px solid rgba(255,255,255,0.05);
    }

    /* Source Pills */
    .source-pill {
        background: #334155;
        color: #94a3b8;
        padding: 4px 12px;
        border-radius: 100px;
        font-size: 0.75rem;
        border: 1px solid #475569;
        margin: 4px;
        display: inline-block;
        transition: 0.2s;
    }
    .source-pill:hover {
        background: #475569;
        color: white;
    }

</style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def get_pdf_display(file):
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    return pdf_display

def switch_view(view_name):
    st.session_state.app_state = view_name
    st.rerun()

# --- LANDING PAGE ---
if st.session_state.app_state == "landing":
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # st.markdown('<div class="landing-card">', unsafe_allow_html=True)
        st.markdown('<h1 class="gradient-text">Intel Nexus</h1>', unsafe_allow_html=True)
        st.write("Enterprise Document Analyzer & RAG Knowledge Base")
        
        # Navigation to Dashboard (Bypass Upload)
        if st.button("👉 Go to Dashboard", type="secondary", use_container_width=True):
             switch_view("dashboard")

        st.divider()
        
        # Upload
        uploaded_file = st.file_uploader("Drop your PDF document here", type="pdf")
        
        if uploaded_file:
            # Preview and Mode Selection
            m_col1, m_col2 = st.columns([1, 1])
            with m_col1:
                st.markdown("### Preview")
                pdf_html = get_pdf_display(uploaded_file)
                st.markdown(pdf_html, unsafe_allow_html=True)
            
            with m_col2:
                st.markdown("### Configuration")
                mode = st.radio("Extraction Mode", ["OCR", "GEMINI"], 
                               help="OCR: High-speed text extraction\nGEMINI: High-accuracy vision-based reasoning",
                               horizontal=True)
                
                st.info("Ingesting this document will index it into the vector knowledge base for real-time querying.")
                
                if st.button("🚀 Ingest Document", type="primary", use_container_width=True):
                    with st.status("Initializing AI Pipeline...", expanded=True) as status:
                        # Prepare file for upload
                        uploaded_file.seek(0)
                        files = {"file": (uploaded_file.name, uploaded_file.read(), "application/pdf")}
                        params = {"mode": mode}
                        
                        try:
                            resp = requests.post(f"{API_URL}/upload", files=files, params=params, timeout=3600)
                            if resp.status_code == 200:
                                data = resp.json()
                                st.session_state.current_doc = data["doc_id"]
                                status.update(label="Ingestion Complete!", state="complete", expanded=False)
                                st.success(f"Success! Document '{data['doc_id']}' is ready.")
                                time.sleep(1)
                                switch_view("dashboard")
                            else:
                                st.error(f"Error: {resp.text}")
                        except Exception as e:
                            st.error(f"Connection Failed: {e}")
        
        # st.markdown('</div>', unsafe_allow_html=True)

# --- DASHBOARD PAGE ---
elif st.session_state.app_state == "dashboard":
    
    # 1. SIDEBAR NAVIGATION
    with st.sidebar:
        st.markdown('<h2 style="font-weight:700; color:#38bdf8;">Nexus Dash</h2>', unsafe_allow_html=True)
        st.divider()
        
        # Navigation
        nav_mode = st.radio("Navigation", ["💬 Chat", "👁 Inspector", "💾 Database"], label_visibility="collapsed")
        
        st.divider()
        if st.button("⬅ New Upload", use_container_width=True):
            switch_view("landing")
            
        st.sidebar.markdown(f"""
        <div style='position: fixed; bottom: 20px; left: 20px; opacity: 0.5; font-size: 0.8rem;'>
            Active: {st.session_state.current_doc or 'None'}
        </div>
        """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # VIEW: CHAT
    # ---------------------------------------------------------
    if nav_mode == "💬 Chat":
        c_hist, c_main, c_ref = st.columns([1, 2, 1])
        
        with c_hist:
            st.markdown("### History")
            # Multiple Conversations
            for chat in st.session_state.chat_sessions:
                active_style = "cursor:pointer; background:rgba(56, 189, 248, 0.2); border-left: 3px solid #38bdf8;" if chat["id"] == st.session_state.active_chat_id else "cursor:pointer;"
                if st.button(f"📄 {chat['name']}", key=f"nav_{chat['id']}", use_container_width=True):
                    st.session_state.active_chat_id = chat["id"]
                    st.rerun()
            
            if st.button("+ New Thread", use_container_width=True):
                new_id = str(int(time.time()))
                st.session_state.chat_sessions.append({"id": new_id, "name": f"Session {len(st.session_state.chat_sessions)}", "messages": []})
                st.session_state.active_chat_id = new_id
                st.rerun()

        with c_main:
            st.markdown(f"### Chat: {[c['name'] for c in st.session_state.chat_sessions if c['id']==st.session_state.active_chat_id][0]}")
            
            # Message History
            current_chat = next(c for c in st.session_state.chat_sessions if c['id'] == st.session_state.active_chat_id)
            
            chat_container = st.container(height=500)
            with chat_container:
                for msg in current_chat["messages"]:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])

            # Input
            if prompt := st.chat_input("Ask about your documents..."):
                current_chat["messages"].append({"role": "user", "content": prompt})
                with st.chat_message("user"): st.markdown(prompt)
                
                with st.chat_message("assistant"):
                    with st.spinner("Analyzing knowledge..."):
                        try:
                            resp = requests.get(f"{API_URL}/search", params={"q": prompt, "limit": 4})
                            if resp.status_code == 200:
                                data = resp.json()
                                # Get AI Synthesis and Chunks
                                answer = data.get("answer", "I couldn't synthesize an answer, but here are the relevant extracts.")
                                chunks = data.get('documents', [[]])[0]
                                metas = data.get('metadatas', [[]])[0]
                                
                                # Store for reference panel
                                st.session_state.last_search_results = data
                                
                                current_chat["messages"].append({"role": "assistant", "content": answer})
                                st.markdown(answer)
                                
                                # Show Quick Sources
                                if metas:
                                    st.markdown("---")
                                    st.caption("Quick Sources:")
                                    for m in metas[:3]:
                                        st.markdown(f"<span class='source-pill'>Pg {m.get('page','?')}</span>", unsafe_allow_html=True)
                        except Exception as e:
                            st.error(f"Search failed: {e}")
                st.rerun()

        with c_ref:
            st.markdown("### References")
            if "last_search_results" in st.session_state:
                res = st.session_state.last_search_results
                metas = res.get('metadatas', [[]])[0]
                for i, m in enumerate(metas):
                    with st.expander(f"Ref {i+1}: Pg {m.get('page','?')}"):
                        st.write(res.get('documents',[[]])[0][i])
                        doc_id = m.get('doc_id')
                        page = m.get('page')
                        bbox = m.get('bbox')
                        if doc_id and page and bbox:
                            bbox_str = ",".join(map(str, bbox)) if isinstance(bbox, list) else str(bbox)
                            st.image(f"{API_URL}/citation/{doc_id}/{page}/{bbox_str}", caption="Visual Source")
            else:
                st.info("References will appear here after you ask a question.")

    # ---------------------------------------------------------
    # VIEW: INSPECTOR
    # ---------------------------------------------------------
    elif nav_mode == "👁 Inspector":
        if not st.session_state.current_doc:
            st.warning("No active document selected. Please go to Database or Upload one.")
        else:
            doc_id = st.session_state.current_doc
            st.markdown(f"### Object Inspector: {doc_id}")
            
            # Fetch Structure
            try:
                resp = requests.get(f"{API_URL}/documents/{doc_id}")
                if resp.status_code == 200:
                    arts = resp.json()
                    
                    tabs = st.tabs(["🖼 Images", "📊 Tables", "📄 Chunks", "📜 Full Doc"])
                    
                    with tabs[0]:
                        imgs = arts.get("images", [])
                        if not imgs: st.write("No images found.")
                        cols = st.columns(2)
                        for idx, img in enumerate(imgs):
                            with cols[idx % 2]:
                                if st.button(f"View Pg {img['page']} Image", key=f"btn_img_{idx}"):
                                    st.session_state.selected_inspector_item = {"type": "img", "data": img}
                                
                    with tabs[1]:
                        tbls = arts.get("tables", [])
                        if not tbls: st.write("No tables found.")
                        for idx, tbl in enumerate(tbls):
                            if st.button(f"Inspect Table (Pg {tbl['page']})", key=f"btn_tbl_{idx}"):
                                st.session_state.selected_inspector_item = {"type": "tbl", "data": tbl}
                                
                    with tabs[2]:
                        st.caption("Browse extracted knowledge chunks")
                        # We'd ideally fetch chunks here
                        st.write("Browse chunks via the Database tab for full index list.")
                        
                    with tabs[3]:
                         st.markdown(f'<iframe src="{arts["pdf_url"]}" width="100%" height="800"></iframe>', unsafe_allow_html=True)
                    
                    # Detail Overlay (Below tabs)
                    if st.session_state.selected_inspector_item:
                        st.divider()
                        sel = st.session_state.selected_inspector_item
                        st.markdown(f"#### Detail View: {sel['type'].upper()}")
                        
                        if sel["type"] == "img":
                            st.info(f"**Context Summary:** {sel['data'].get('caption', 'No summary available.')}")
                            st.image(f"{API_URL}/static/images/{sel['data']['image_id']}", use_container_width=True)
                        elif sel["type"] == "tbl":
                            df = pd.DataFrame(sel["data"]["data"], columns=sel["data"]["headers"])
                            st.dataframe(df, use_container_width=True)
                        
                        if st.button("Close Detail"):
                            st.session_state.selected_inspector_item = None
                            st.rerun()
            except:
                st.error("Could not reach backend to fetch objects.")

    # ---------------------------------------------------------
    # VIEW: DATABASE
    # ---------------------------------------------------------
    elif nav_mode == "💾 Database":
        st.markdown("### Knowledge Repository")
        
        # Confirmation Logic for Reset
        with st.expander("🚨 Danger Zone", expanded=False):
            st.warning("Resetting the database will delete ALL documents, chunks, and images.")
            confirm_input = st.text_input("Type 'CONFIRM' to wipe everything:")
            if st.button("Destroy Database", type="primary", disabled=confirm_input != "CONFIRM"):
                requests.delete(f"{API_URL}/database/reset")
                st.session_state.current_doc = None
                st.success("Wiped everything. Ready for fresh intake.")
                st.rerun()

        # List Documents
        try:
            r = requests.get(f"{API_URL}/database/inspect")
            if r.status_code == 200:
                db_data = r.json()
                if not db_data: 
                    st.info("No documents in database.")
                else:
                    for doc_id, chunks in db_data.items():
                        with st.expander(f"📄 {doc_id} ({len(chunks)} chunks)"):
                            col_a, col_b = st.columns([4, 1])
                            with col_a:
                                if st.button(f"Activate {doc_id}", key=f"act_{doc_id}"):
                                    st.session_state.current_doc = doc_id
                                    st.rerun()
                            with col_b:
                                if st.button(f"Delete", key=f"del_{doc_id}", type="primary"):
                                    requests.delete(f"{API_URL}/documents/{doc_id}")
                                    if st.session_state.current_doc == doc_id: st.session_state.current_doc = None
                                    st.rerun()
                            
                            # Show table of first 5 chunks
                            df_chunks = pd.DataFrame([{"Content": c["text"][:100]+"...", "Page": c["metadata"].get("page")} for c in chunks[:5]])
                            st.table(df_chunks)
        except:
             st.error("Connection Error with Knowledge Base API.")
