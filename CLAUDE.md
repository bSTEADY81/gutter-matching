# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Gutter Matching MVP application built with Streamlit that helps users find the best matching gutter profile from a database of 55+ products across multiple suppliers. The app uses a weighted Euclidean distance algorithm to match user measurements (Base/Width, Face/Front, Back/Rear) against a product database.

## Key Commands

### Running the Application
```bash
# Run original version
streamlit run app.py

# Run modern UI version (professional redesign)
streamlit run app_modern.py --server.port 8502

# Both apps run simultaneously on different ports (8501 and 8502)
```

### Data Management Scripts
```bash
# Sync prices from Master Price List CSV
python3 add_buy_prices.py

# Find missing supplier codes using pattern matching
python3 find_missing_codes.py

# Apply found supplier codes to gutters.csv
python3 apply_supplier_codes.py

# Copy/sync images from Google Drive
python3 copy_images_from_gdrive.py
# OR use comprehensive scanner
python3 copy_all_gutter_images.py

# Generate pricing coverage report
python3 generate_price_report.py

# Fix image mappings manually
python3 fix_missing_images.py
```

## Architecture & Data Flow

### Core Data Model
The system revolves around `gutters.csv` which contains:
- **Dimensions**: Face, Base, Back (in mm)
- **Product Info**: Gutter Description, Supplier, State availability
- **Commercial**: Supplier Code, Buy Price (inc gst), Sell Price (inc gst)
- **Media**: Product URL 1 (spec sheets), Image Path (local images)

### Matching Algorithm
Located in both `app.py` and `app_modern.py`:
- Weighted Euclidean distance calculation
- Weights: Base (2.5x), Face (2x), Back (1x)
- Results sorted by Error_Score (lower is better)
- Modern version converts to Match_Score percentage (0-100%)

### Price Synchronization Pipeline
1. **Master Price List** (`/Users/bjc/Documents/Brads Projects/SORs Project/KCs Product Masterlist Feb 2025 - Master Price List.csv`) contains authoritative pricing
2. **Supplier Code Patterns**:
   - `S.` = Stramit
   - `ST` = Stratco
   - `ME` = Metroll
   - `LY` = Lysaght
   - `RS` = Rollsec
3. **Price Formulas** (for Pantex from PDF):
   - Buy Inc GST = Buy Ex GST × 1.1
   - Sell Inc GST = Buy Inc GST × 1.46

### Image Management System
Images are sourced from Google Drive and copied locally:
- **Google Drive Path**: `/Users/bjc/Library/CloudStorage/GoogleDrive-kcsbpstaff@gmail.com/My Drive/KCs BP/Suppliers/*/2 - Product Info Brochures/*Gutter*`
- **Local Storage**: `images/{supplier}/` folders
- **Fuzzy Matching**: Scripts use SequenceMatcher to match image filenames to gutter descriptions
- **Coverage**: Currently 25/55 products have images (Metroll, Lysaght, Rollsec complete)

## UI Versions

### Original (`app.py`)
- Basic Streamlit interface
- Centered layout
- Expander-based results display
- Simple metric display

### Modern (`app_modern.py`)
- Professional redesign with custom CSS (`style.css`)
- Wide layout with hero section
- Rank badges (🥇🥈🥉) and match percentage
- Dimension comparison tables
- Loading animations and visual feedback
- Theme configuration in `.streamlit/config.toml`

## External Dependencies

### Data Sources
- **Master Price List**: Located at `/Users/bjc/Documents/Brads Projects/SORs Project/`
- **Pantex PDF**: `/Users/bjc/Downloads/Pantex Roofing Systems - KCs Building Products - 01-02-2022 - Pricing Catalogue.pdf`
- **Google Drive Images**: Synced via CloudStorage to local filesystem

### Key Python Dependencies
- `streamlit`: Web framework
- `pandas`: Data manipulation
- `difflib.SequenceMatcher`: Fuzzy string matching for image/code mapping

## Critical Business Logic

### Supplier Code Resolution
The `find_missing_codes.py` script implements intelligent pattern matching:
1. Filters Master Price List by supplier prefix
2. Extracts keywords from gutter descriptions (Quad, Half Round, dimensions)
3. Searches for matches in Description and Product columns
4. Suggests best matches for manual review

### Image Mapping
The `copy_all_gutter_images.py` script:
1. Scans for files with "gutter" in filename
2. Copies from Google Drive folders to local `images/` directory
3. Uses fuzzy matching (threshold 0.5) to map to gutters
4. Manual corrections needed for ~5 products due to naming variations

### Price Coverage
Current state: 45/55 products have pricing (81.8%)
- Missing: Steeline (POA), most Stramit/Stratco products
- Complete: All Metroll, Lysaght, Rollsec products

## Development Notes

### Cache Management
Streamlit caches data with `@st.cache_data(ttl=10)` - 10 second TTL to handle CSV updates. Clear cache manually with 'C' key in Streamlit interface if needed.

### Background Processes
Multiple Streamlit instances can run simultaneously on different ports for A/B testing or development.

### File Modifications
When gutters.csv is modified externally (e.g., Excel), re-read the file in scripts before making edits to avoid conflicts.