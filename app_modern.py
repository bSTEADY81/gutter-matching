import streamlit as st
import pandas as pd
import os
import time

# ====================================
# 1. PAGE CONFIGURATION & SETUP
# ====================================
st.set_page_config(
    page_title="Gutter Gauge - Professional Gutter Matching",
    page_icon="📏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ====================================
# 1.5 LOGIN AUTHENTICATION
# ====================================
def check_password():
    """Returns True if the user has entered the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["passwords"]["kcs_team"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    # First run or password not yet correct
    if "password_correct" not in st.session_state:
        st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; min-height: 80vh;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 40px; border-radius: 16px; text-align: center;
                        box-shadow: 0 10px 40px rgba(0,0,0,0.2); max-width: 400px; width: 100%;">
                <h1 style="color: white; margin-bottom: 8px;">Gutter Gauge</h1>
                <p style="color: rgba(255,255,255,0.8); margin-bottom: 24px;">KCs Building Products</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.text_input(
            "Enter password to access",
            type="password",
            on_change=password_entered,
            key="password",
            placeholder="Password"
        )
        return False

    # Password incorrect
    elif not st.session_state["password_correct"]:
        st.text_input(
            "Enter password to access",
            type="password",
            on_change=password_entered,
            key="password",
            placeholder="Password"
        )
        st.error("Incorrect password. Please try again.")
        return False

    # Password correct
    else:
        return True

def check_admin_mode():
    """Check if admin mode is enabled (for viewing buy prices)."""
    return st.session_state.get("admin_mode", False)

def toggle_admin_mode():
    """Toggle admin mode on/off with password verification."""
    if "admin_password_input" in st.session_state:
        admin_pw = st.secrets.get("passwords", {}).get("admin", None)
        if admin_pw and st.session_state["admin_password_input"] == admin_pw:
            st.session_state["admin_mode"] = True
            if "admin_password_input" in st.session_state:
                del st.session_state["admin_password_input"]
        else:
            st.session_state["admin_mode"] = False

# Check authentication before showing any content
if not check_password():
    st.stop()

# ====================================
# 2. CUSTOM CSS INJECTION
# ====================================
def load_custom_css():
    """Load and inject custom CSS styling"""
    if os.path.exists("style.css"):
        with open("style.css", "r") as f:
            css = f.read()
            st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    # Additional inline CSS for specific components
    st.markdown("""
    <style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Custom container styling */
    .input-container {
        background: #F8F9FA;
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 24px;
        border: 1px solid #E2E8F0;
    }

    /* Match score visualization */
    .score-container {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 12px 0;
    }

    .score-bar {
        flex: 1;
        height: 12px;
        background: #E2E8F0;
        border-radius: 6px;
        overflow: hidden;
    }

    .score-fill {
        height: 100%;
        background: linear-gradient(90deg, #27AE60 0%, #F39C12 50%, #E74C3C 100%);
        transition: width 0.5s ease;
    }

    /* Dimension comparison table */
    .dimension-table {
        width: 100%;
        border-collapse: collapse;
        margin: 16px 0;
    }

    .dimension-table th {
        background: #F8F9FA;
        padding: 12px;
        text-align: left;
        font-weight: 600;
        font-size: 14px;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border-bottom: 2px solid #E2E8F0;
    }

    .dimension-table td {
        padding: 12px;
        font-size: 16px;
        border-bottom: 1px solid #E2E8F0;
    }

    .exact-match { color: #27AE60; font-weight: 600; }
    .close-match { color: #F39C12; font-weight: 500; }
    .far-match { color: #E74C3C; font-weight: 500; }

    /* Image placeholder */
    .image-placeholder {
        background: #F8F9FA;
        padding: 60px;
        text-align: center;
        border-radius: 12px;
        border: 2px dashed #E2E8F0;
        color: #718096;
        font-size: 18px;
        margin: 20px 0;
    }

    .image-placeholder-icon {
        font-size: 48px;
        margin-bottom: 12px;
        opacity: 0.5;
    }
    </style>
    """, unsafe_allow_html=True)

load_custom_css()

# ====================================
# 3. DATA LOADING & CLEANING
# ====================================
@st.cache_data(ttl=10)
def load_data():
    """Load and clean the gutter data"""
    df = pd.read_csv("gutters.csv")

    # Ensure columns are numeric
    cols = ['Face', 'Base', 'Back']
    for col in cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop rows with missing dimensions
    clean_df = df.dropna(subset=['Face', 'Base', 'Back'])
    return clean_df

# Load data
try:
    df = load_data()
except Exception as e:
    st.error(f"❌ Error loading database: {e}")
    st.stop()

# ====================================
# 4. HERO SECTION
# ====================================
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 48px 32px;
            border-radius: 16px;
            margin-bottom: 32px;
            text-align: center;
            box-shadow: 0 8px 24px rgba(0,0,0,0.12);">
    <h1 style="color: white; font-size: 56px; font-weight: 800; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
        📏 Gutter Gauge Professional
    </h1>
    <p style="color: white; font-size: 20px; margin: 12px 0 0 0; opacity: 0.95;">
        Find the perfect gutter profile match from our extensive database
    </p>
    <p style="color: white; font-size: 16px; margin: 8px 0 0 0; opacity: 0.9;">
        ✓ """ + str(len(df)) + """ profiles available • ✓ 25+ suppliers • ✓ Instant matching
    </p>
</div>
""", unsafe_allow_html=True)

# ====================================
# 5. SIDEBAR CONFIGURATION
# ====================================
with st.sidebar:
    st.markdown("### 🎯 Search Filters")
    st.markdown("---")

    # State selection
    st.markdown("#### 📍 Location")
    state_input = st.selectbox(
        "Select State",
        ["QLD", "NSW", "VIC", "TAS", "SA", "WA", "NT", "ACT"],
        help="Filter gutters available in your state"
    )

    st.markdown("")

    # Shape selection
    st.markdown("#### 📐 Profile Type")
    shape_input = st.radio(
        "Select Shape",
        ["All", "Quad", "Square", "Half Round"],
        help="Filter by gutter profile shape"
    )

    # Statistics
    st.markdown("---")
    st.metric("Database Size", f"{len(df)} profiles")
    st.metric("Suppliers", "25+")
    st.metric("With Pricing", f"{df['Sell Price (inc gst)'].notna().sum()} items")

    # Admin Mode Section (for viewing wholesale/buy prices)
    st.markdown("---")
    st.markdown("#### 🔐 Admin Access")

    if check_admin_mode():
        st.success("Admin mode active")
        if st.button("🔓 Exit Admin Mode", use_container_width=True):
            st.session_state["admin_mode"] = False
            st.rerun()
    else:
        with st.expander("Unlock Buy Prices"):
            st.text_input(
                "Admin Password",
                type="password",
                key="admin_password_input",
                placeholder="Enter admin password",
                on_change=toggle_admin_mode
            )
            st.caption("Contact management for access")

# ====================================
# 6. MAIN INPUT SECTION
# ====================================
# Input container with styled background
st.markdown('<div class="input-container">', unsafe_allow_html=True)
st.markdown("### 📏 Enter Site Measurements")
st.markdown("*Measure each dimension in millimeters for accurate matching*")

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("**Base (Width)**")
    u_base = st.number_input(
        "Base measurement",
        min_value=0,
        value=0,
        step=1,
        help="Width of the gutter base in mm",
        label_visibility="collapsed"
    )

with col2:
    st.markdown("**Face (Front)**")
    u_face = st.number_input(
        "Face measurement",
        min_value=0,
        value=0,
        step=1,
        help="Front height of the gutter in mm",
        label_visibility="collapsed"
    )

with col3:
    st.markdown("**Back (Rear)**")
    u_back = st.number_input(
        "Back measurement",
        min_value=0,
        value=0,
        step=1,
        help="Rear height of the gutter in mm",
        label_visibility="collapsed"
    )

st.markdown('</div>', unsafe_allow_html=True)

# ====================================
# 7. MATCHING ALGORITHM HELPERS
# ====================================
def calculate_match_score(error_score):
    """Convert error score to match percentage (0-100)"""
    max_error = 20  # Maximum tolerable error
    if error_score >= max_error:
        return 0
    return max(0, 100 - (error_score / max_error * 100))

def get_match_quality(score):
    """Get match quality label and color"""
    if score >= 90:
        return "Excellent Match", "#27AE60"
    elif score >= 70:
        return "Good Match", "#F39C12"
    elif score >= 50:
        return "Fair Match", "#E67E22"
    else:
        return "Poor Match", "#E74C3C"

def get_rank_badge(rank):
    """Get HTML for rank badge"""
    if rank == 1:
        return '<span class="rank-badge rank-1">🥇 BEST MATCH</span>'
    elif rank == 2:
        return '<span class="rank-badge rank-2">🥈 2ND BEST</span>'
    elif rank == 3:
        return '<span class="rank-badge rank-3">🥉 3RD BEST</span>'
    else:
        return f'<span class="rank-badge" style="background: #E2E8F0; color: #718096;">#{rank}</span>'

def format_dimension_diff(diff):
    """Format dimension difference with color coding"""
    if diff == 0:
        return f'<span class="exact-match">Exact ✓</span>'
    elif abs(diff) <= 2:
        return f'<span class="close-match">{diff:+.0f}mm</span>'
    else:
        return f'<span class="far-match">{diff:+.0f}mm</span>'

# ====================================
# 8. FIND MATCH BUTTON & LOGIC
# ====================================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    find_match = st.button(
        "🔍 Find Best Match",
        use_container_width=True,
        type="primary"
    )

# ====================================
# 9. MATCHING RESULTS
# ====================================
if find_match:
    if u_base == 0:
        st.warning("⚠️ Please enter at least a Base measurement to find matches.")
    else:
        # Show loading state
        with st.spinner("🔍 Searching database for best matches..."):
            time.sleep(0.5)  # Brief delay for UX

            # Filter by state
            filtered_df = df[df['State'].fillna('').str.contains(state_input, case=False, na=False)].copy()

            # Filter by shape
            if shape_input != "All":
                filtered_df = filtered_df[filtered_df['Gutter Description'].str.contains(shape_input, case=False, na=False)]

            if filtered_df.empty:
                st.error(f"❌ No products found in {state_input} with shape '{shape_input}'")
            else:
                # Calculate differences and error score
                filtered_df['Diff_Base'] = abs(filtered_df['Base'] - u_base)
                filtered_df['Diff_Face'] = abs(filtered_df['Face'] - u_face)
                filtered_df['Diff_Back'] = abs(filtered_df['Back'] - u_back)

                # Weighted error calculation
                filtered_df['Error_Score'] = (
                    filtered_df['Diff_Base'] * 2.5 +
                    filtered_df['Diff_Face'] * 2 +
                    filtered_df['Diff_Back']
                )

                # Convert to match score percentage
                filtered_df['Match_Score'] = filtered_df['Error_Score'].apply(calculate_match_score)

                # Sort by lowest error (best match first)
                results = filtered_df.sort_values(by='Error_Score').head(5)

                # Display status
                best_match = results.iloc[0]
                match_score = best_match['Match_Score']
                quality, color = get_match_quality(match_score)

                # Success/Warning message
                if match_score >= 90:
                    st.balloons()
                    st.success(f"✅ **{quality}!** Found {len(results)} matching profiles.")
                elif match_score >= 70:
                    st.success(f"✓ **{quality}** - {len(results)} profiles found.")
                else:
                    st.warning(f"⚠️ No exact matches found. Showing {len(results)} closest options.")

                st.markdown("---")

                # Display results
                st.markdown("### 🎯 Matching Results")

                for idx, (index, row) in enumerate(results.iterrows(), 1):
                    # Create result card with container
                    with st.container(border=True):
                        # Header with rank badge
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(
                                f"{get_rank_badge(idx)} **{row['Gutter Description']}** - {row['Supplier']}",
                                unsafe_allow_html=True
                            )
                        with col2:
                            match_pct = row['Match_Score']
                            st.markdown(
                                f"<div style='text-align: right; font-size: 20px; font-weight: 700; color: {get_match_quality(match_pct)[1]}'>"
                                f"{match_pct:.0f}% Match</div>",
                                unsafe_allow_html=True
                            )

                        # Match score bar
                        st.markdown(
                            f"""<div class="score-container">
                                <div class="score-bar">
                                    <div class="score-fill" style="width: {match_pct}%;"></div>
                                </div>
                            </div>""",
                            unsafe_allow_html=True
                        )

                        # Image display
                        if pd.notna(row.get('Image Path')) and os.path.exists(row['Image Path']):
                            st.image(row['Image Path'], use_container_width=True)
                        else:
                            st.markdown("""
                            <div class="image-placeholder">
                                <div class="image-placeholder-icon">📷</div>
                                Image not available
                            </div>
                            """, unsafe_allow_html=True)

                        # Dimensions comparison table
                        st.markdown("#### 📐 Dimension Comparison")

                        dimensions_html = f"""
                        <table class="dimension-table">
                            <thead>
                                <tr>
                                    <th>Dimension</th>
                                    <th>Your Measurement</th>
                                    <th>Product Dimension</th>
                                    <th>Difference</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><strong>Base</strong></td>
                                    <td>{u_base}mm</td>
                                    <td>{row['Base']:.0f}mm</td>
                                    <td>{format_dimension_diff(row['Base'] - u_base)}</td>
                                </tr>
                                <tr>
                                    <td><strong>Face</strong></td>
                                    <td>{u_face}mm</td>
                                    <td>{row['Face']:.0f}mm</td>
                                    <td>{format_dimension_diff(row['Face'] - u_face)}</td>
                                </tr>
                                <tr>
                                    <td><strong>Back</strong></td>
                                    <td>{u_back}mm</td>
                                    <td>{row['Back']:.0f}mm</td>
                                    <td>{format_dimension_diff(row['Back'] - u_back)}</td>
                                </tr>
                            </tbody>
                        </table>
                        """
                        st.markdown(dimensions_html, unsafe_allow_html=True)

                        # Product details
                        st.markdown("#### 📦 Product Details")
                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.markdown(f"**Supplier Code**")
                            if pd.notna(row['Supplier Code']):
                                st.code(row['Supplier Code'])
                            else:
                                st.markdown("*Not available*")

                        with col2:
                            if pd.notna(row['Product URL 1']):
                                st.link_button(
                                    "📄 View Spec Sheet",
                                    row['Product URL 1'],
                                    use_container_width=True
                                )
                            else:
                                st.markdown("*No spec sheet*")

                        with col3:
                            st.markdown(f"**Pricing**")
                            if pd.notna(row.get('Sell Price (inc gst)')):
                                st.markdown(f"Sell: **${row['Sell Price (inc gst)']:.2f}** inc GST")
                            # Only show buy price if admin mode is enabled
                            if check_admin_mode() and pd.notna(row.get('Buy Price (inc gst)')):
                                st.markdown(f"🔐 Buy: ${row['Buy Price (inc gst)']:.2f} inc GST")
                            if pd.isna(row.get('Sell Price (inc gst)')):
                                st.markdown("*Price on application*")

# ====================================
# 10. FOOTER
# ====================================
st.markdown("---")
st.markdown(
    """<div style='text-align: center; color: #718096; font-size: 14px; padding: 20px 0;'>
    Gutter Gauge Professional v2.0 • Powered by Streamlit • © 2024
    </div>""",
    unsafe_allow_html=True
)