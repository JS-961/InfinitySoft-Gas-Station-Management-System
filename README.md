# InfinitySoft-Gas-Station-Management-System

A desktop application built with Python (Tkinter) and SQLite for managing daily operations of a gas station.  
The system was developed as part of an internship project and evolved into a fully functional, client-ready product.

Features:

- Modular dashboards for different aspects of station management:
  - State Vouchers
  - Washing Services
  - Expenses
  - Debts
  - Customer Vouchers
  - Gas/Oil Filters
  - Liters Plus
  - Debt Collection
  - User Management (admin only)
- Add/Edit forms in separate top-level windows with enforced dimensions
- Unified styling and synchronized titles across dashboards
- Currency toggle between USD and L.L, displayed consistently in UI and reports
- Date pickers with automatic time filling for relevant entries
- PDF report export with date range filters and totals
- Report previews matching the final PDF table formatting
- Role-based login system with restricted access for non-admin users
- Optimized SQLite database:
  - All text fields use `VARCHAR(n)` instead of `TEXT`
  - Date fields use `DATETIME` instead of `DATE`
- Bilingual PDF support (English + Arabic) for report titles and labels

---

Project Structure

gas_station_modular/
├─ assets/ # Images, icons, and branding
│ ├─ logo.png
│ └─ other assets
├─ base/ # Base classes for forms and dashboards
│ ├─ base_form.py
│ └─ base_view.py
├─ reports/ # PDF or report templates/output
├─ screens/ # All dashboard and form screens
│ ├─ menu.py
│ ├─ login.py
│ ├─ expenses_dashboard.py
│ ├─ liters_plus_dashboard.py
│ ├─ gas_oil_filter_dashboard.py
│ ├─ statevouchers_dashboard.py
│ ├─ customer_vouchers_dashboard.py
│ ├─ debts_dashboard.py
│ ├─ washing_dashboard.py
│ ├─ debt_collection_dashboard.py
│ ├─ manage_users_dashboard.py
│ ├─ expenses_form.py
│ ├─ statevouchers_form.py
│ └─ washing_form.py
├─ utils/ # Utility functions
│ └─ pdf_exporter.py # PDF generation logic
├─ gas_station.db # SQLite database
├─ main.py # Main entry point
└─ requirements.txt

---

Requirements

Install dependencies:

pip install -r requirements.txt

Note: Tkinter ships with most Python distributions, but ensure it’s included in your installation.

---

Running the Application

From the project root: python main.py

---

Usage Overview

1. Login
   - Admin credentials grant full access.
   - User credentials restrict access to sensitive dashboards.

2. Navigation
   - The main menu provides quick access to all dashboards.
   - Each dashboard includes an "Add" button to open the corresponding form in a new window.

3. Currency Toggle 
   - Available on applicable dashboards to switch between USD and L.L.

4. Report Generation 
   - Navigate to the report screen for the desired dashboard.
   - Select a "From" and "To" date range.
   - Preview the report inside the app.
   - Export to PDF with totals included.

---

Database Notes

- All database interactions use SQLite.
- Structure optimized for storage efficiency:
  - Text fields: `VARCHAR(n)` with sensible length limits.
  - Dates: `DATETIME` for precise timestamp storage.
- The database file is editable using any SQLite editor for administrative adjustments.

---

Future Improvements

- Additional filters for reports (by type, user, etc.).
- Automatic backup system for the database.
- More advanced currency exchange integration.
- Packaging as a standalone executable for Windows deployment.

---

Author

Developed by Jawad Saad during an internship at InfinitySoft.  
Special thanks to the InfinitySoft team for guidance and feedback throughout the project.


