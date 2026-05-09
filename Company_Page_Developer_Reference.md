# Company Management Page - Developer Quick Reference

## 📁 Files Modified

### main.py
- **Function**: `companies_page()` (Lines ~246-385)
- **Dialog**: `add_company_dialog()` (Lines ~387-430)
- **Dialog**: `edit_company_dialog()` (Lines ~432-485)
- **Helper**: `import_dialog_content()` (Lines ~487-560)

### database.py
- **Method**: `get_company_worker_count(company_id)` (Lines ~260-266)

---

## 🔑 Key Code Patterns

### 1. Wide Dialog Pattern
```python
@st.dialog("Dialog Title", width="large")
def my_dialog():
    # Two-column layout
    cols = st.columns([1, 1])
    
    with cols[0]:
        # Left column content
        value = st.text_input("Label")
    
    with cols[1]:
        # Right column content
        st.markdown("Placeholder or future field")
    
    # Action buttons
    if st.button("Save"):
        # Save logic
        st.rerun()
```

### 2. Toolbar Layout Pattern
```python
# Three-column toolbar [3, 1, 1]
toolbar_cols = st.columns([3, 1, 1])

with toolbar_cols[0]:
    search = st.text_input("Search", label_visibility="collapsed")

with toolbar_cols[1]:
    if st.button("Add", use_container_width=True):
        add_dialog()

with toolbar_cols[2]:
    with st.popover("Import"):
        import_content()
```

### 3. Row Display Pattern
```python
# Four-column row [1, 4, 1, 1]
for _, item in display_df.iterrows():
    row_cols = st.columns([1, 4, 1, 1])
    
    with row_cols[0]:
        st.markdown(f"#{item['id']}")
    
    with row_cols[1]:
        st.markdown(f"**{item['name']}**")
    
    with row_cols[2]:
        if st.button("Edit", key=f"edit_{item['id']}"):
            edit_dialog(item['id'])
    
    with row_cols[3]:
        if st.button("Delete", key=f"del_{item['id']}"):
            st.session_state[f"confirm_{item['id']}"] = True
```

### 4. Search Filter Pattern
```python
import pandas as pd

df = pd.DataFrame(data)

# Fuzzy search
if search_keyword and search_keyword.strip():
    filtered_df = df[
        df['name'].str.contains(search_keyword.strip(), case=False, na=False)
    ]
else:
    # Default: latest 50 records
    filtered_df = df.sort_values('id', ascending=False).head(50)

# Limit display
display_df = filtered_df.head(50)
total_count = len(filtered_df)
```

### 5. Delete Confirmation Pattern
```python
# In row display
if st.button("Delete", key=f"del_{item_id}"):
    st.session_state[f"confirm_{item_id}"] = True

# Show confirmation
if st.session_state.get(f"confirm_{item_id}", False):
    with st.popover("Confirm Delete"):
        st.warning("Warning message")
        
        if st.button("Confirm", key=f"confirm_{item_id}"):
            success, error = db.delete(item_id)
            if success:
                st.success("Deleted!")
                st.rerun()
        
        if st.button("Cancel", key=f"cancel_{item_id}"):
            st.session_state[f"confirm_{item_id}"] = False
            st.rerun()
```

---

## 🗄️ Database Methods

### Company Operations
```python
# Add company
db_manager.add_company(name: str) -> bool

# Get all companies
db_manager.get_all_companies() -> List[Dict]

# Check if exists
db_manager.company_exists(name: str) -> bool

# Update company
db_manager.update_company(company_id: int, new_name: str) -> bool

# Delete company (returns tuple)
db_manager.delete_company(company_id: int) -> Tuple[bool, str]

# Get worker count
db_manager.get_company_worker_count(company_id: int) -> int
```

---

## 🎨 Styling Guidelines

### Apple Minimalist CSS Classes
```css
/* Already defined in main.py */
.main-container {
    background: white;
    border-radius: 12px;
    padding: 20px;
}

.divider {
    height: 1px;
    background: #f5f5f7;
    margin: 20px 0;
}
```

### Inline HTML Styling
```python
# Clean text display
st.markdown(f"""
<div style='padding: 10px; font-size: 16px; font-weight: 500; color: #1e293b;'>
    {text}
</div>
""", unsafe_allow_html=True)

# Gradient info box
st.markdown("""
<div style='padding: 15px; background: linear-gradient(135deg, #f0fdfa 0%, #ccfbf1 100%); 
            border-radius: 10px; border: 2px solid #14b8a6;'>
    Content here
</div>
""", unsafe_allow_html=True)
```

---

## ⚠️ Common Pitfalls

### 1. Unique Keys
❌ **Wrong**: Using same key for multiple buttons
```python
for item in items:
    st.button("Edit", key="edit_btn")  # ERROR!
```

✅ **Correct**: Include unique identifier
```python
for item in items:
    st.button("Edit", key=f"edit_btn_{item['id']}")  # OK!
```

### 2. Session State Management
❌ **Wrong**: Not initializing session state
```python
if st.session_state["show_confirm"]:  # KeyError!
    ...
```

✅ **Correct**: Use .get() with default
```python
if st.session_state.get("show_confirm", False):
    ...
```

### 3. Dialog Placement
❌ **Wrong**: Defining dialog inside loop
```python
for item in items:
    @st.dialog("Edit")  # ERROR!
    def edit_dialog():
        ...
```

✅ **Correct**: Define dialog at module level
```python
@st.dialog("Edit")
def edit_dialog(item_id):
    ...

for item in items:
    if st.button("Edit"):
        edit_dialog(item['id'])
```

### 4. Rerun Logic
❌ **Wrong**: Forgetting to rerun after changes
```python
if st.button("Save"):
    db.save(data)
    st.success("Saved!")
    # Missing st.rerun() - UI won't update!
```

✅ **Correct**: Always rerun after database changes
```python
if st.button("Save"):
    db.save(data)
    st.success("Saved!")
    st.rerun()  # Refresh UI
```

---

## 🔍 Debugging Tips

### 1. Check Session State
```python
# Add this temporarily to see session state
st.json(dict(st.session_state))
```

### 2. Verify Data Filtering
```python
# Debug: Show filter results
st.write(f"Total: {len(df)}, Filtered: {len(filtered_df)}, Display: {len(display_df)}")
```

### 3. Test Database Methods
```python
# Quick test in Python console
from database import db_manager
print(db_manager.get_all_companies())
print(db_manager.get_company_worker_count(1))
```

### 4. Check Dialog Rendering
```python
# Ensure dialog is defined BEFORE it's called
# Move @st.dialog decorators to top of file if needed
```

---

## 📝 Code Snippets

### Import Excel Template Generator
```python
import pandas as pd
from io import BytesIO

template_df = pd.DataFrame({'company_name': ['Company A', 'Company B']})
output = BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    template_df.to_excel(writer, index=False, sheet_name='Companies')

st.download_button(
    label="Download Template",
    data=output.getvalue(),
    file_name="companies_template.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
```

### Process Uploaded Excel
```python
uploaded_file = st.file_uploader("Upload", type=['xlsx', 'xls'])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    if 'company_name' not in df.columns:
        st.error("Invalid format")
    else:
        for _, row in df.iterrows():
            name = str(row['company_name']).strip()
            if name and name.lower() != 'nan':
                if not db_manager.company_exists(name):
                    db_manager.add_company(name)
```

### Toast Notification
```python
# Success notification
st.toast(f"✅ Successfully imported {count} companies", icon="🎉")

# Error notification (use st.error instead)
st.error("Import failed: Invalid format")
```

---

## 🚀 Performance Checklist

- [ ] Limit displayed records to 50
- [ ] Use Pandas for filtering (not Python loops)
- [ ] Lazy load dialogs (define but don't call until needed)
- [ ] Minimize st.rerun() calls
- [ ] Use session state for UI state management
- [ ] Avoid nested function definitions
- [ ] Cache expensive operations if needed

---

## 🧪 Testing Checklist

- [ ] Add company with unique name → Success
- [ ] Add company with duplicate name → Error shown
- [ ] Add company with empty name → Error shown
- [ ] Edit company name → Updates correctly
- [ ] Edit to duplicate name → Error shown
- [ ] Delete company with no workers → Success
- [ ] Delete company with workers → Warning shown
- [ ] Search with keyword → Filters correctly
- [ ] Search with no results → "No matches" shown
- [ ] Import valid Excel → Companies added
- [ ] Import invalid Excel → Error shown
- [ ] Import with duplicates → Skipped correctly
- [ ] More than 50 results → Warning shown

---

## 📚 Related Documentation

- [Streamlit Dialogs](https://docs.streamlit.io/library/api-reference/layout/st.dialog)
- [Streamlit Popovers](https://docs.streamlit.io/library/api-reference/layout/st.popover)
- [Streamlit Columns](https://docs.streamlit.io/library/api-reference/layout/st.columns)
- [Pandas String Methods](https://pandas.pydata.org/docs/reference/series.html#string-handling)

---

**Quick Start Command**:
```bash
python -m streamlit run main.py --server.port 8502
```

**Test Script**:
```bash
python test_company_refactor.py
```

---

Last Updated: 2026-04-25
