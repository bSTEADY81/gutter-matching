# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Gutter Matching MVP - a Streamlit application that helps KCs Building Products team find the best matching gutter profile from a database of 55+ products. Uses weighted Euclidean distance to match user measurements (Base, Face, Back) against product database.

## Running the Application

```bash
streamlit run app_modern.py
```

Requires `.streamlit/secrets.toml` with password (not in repo):
```toml
[passwords]
kcs_team = "your_password"
```

## Architecture

### Core Files
- `app_modern.py` - Main Streamlit application with login authentication
- `gutters.csv` - Product database (dimensions, pricing, supplier info)
- `style.css` - Custom CSS styling
- `.streamlit/config.toml` - Streamlit theme and server config
- `images/` - Product images organized by supplier (metroll/, lysaght/, rollsec/)

### Matching Algorithm (app_modern.py)
- Weighted Euclidean distance calculation
- Weights: Base (2.5x), Face (2x), Back (1x)
- Results sorted by Error_Score, converted to Match_Score percentage (0-100%)

### Authentication
Password-protected via `check_password()` function at app entry. Password stored in Streamlit secrets, not in code.

### Data Model (gutters.csv)
| Column | Description |
|--------|-------------|
| Face, Base, Back | Dimensions in mm |
| Gutter Description | Product name |
| Supplier | Manufacturer (Metroll, Lysaght, Rollsec, etc.) |
| State | Australian state availability |
| Supplier Code | Internal ordering code |
| Sell Price (inc gst) | Customer price |
| Buy Price (inc gst) | Wholesale cost (sensitive) |
| Image Path | Relative path to product image |

### Supplier Code Prefixes
- `ME.` = Metroll
- `LY.` = Lysaght
- `RS.` = Rollsec
- `S.` = Stramit
- `ST` = Stratco

## Deployment

Deployed on Streamlit Cloud from GitHub repo `bSTEADY81/gutter-matching`.

**Important:** Add secrets in Streamlit Cloud dashboard (Settings > Secrets) - they are not in the repo.

## Cache Management

Data cached with `@st.cache_data(ttl=10)`. Clear with 'C' key in Streamlit or redeploy.
