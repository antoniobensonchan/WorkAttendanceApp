"""
Work Attendance Management System
Apple minimalist style interface, LAN multi-user shared version
"""

import streamlit as st
from datetime import date, datetime
from database import db_manager
from i18n import get_text, get_supported_languages


# ==================== Page Configuration ====================
st.set_page_config(
    page_title="工地考勤管理系统",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force light theme and fix text color
st.markdown("""
<style>
/* Force light theme */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f0fdfa 0%, #ccfbf1 50%, #f0fdfa 100%) !important;
}

/* Fix main text color */
[data-testid="stAppViewContainer"] .stText {
    color: #1e293b !important;
}

/* Fix all text elements */
[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3,
[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] span,
[data-testid="stAppViewContainer"] div {
    color: #1e293b !important;
}

/* Fix expander text */
[data-testid="stExpander"] button {
    color: #1e293b !important;
}

/* Fix form labels */
[data-testid="stTextInput"] label,
[data-testid="stSelectbox"] label,
[data-testid="stDateInput"] label,
[data-testid="stNumberInput"] label,
[data-testid="stCheckbox"] label {
    color: #1e293b !important;
}

/* Fix dataframe text */
[data-testid="stDataFrame"] {
    color: #1e293b !important;
}

/* Fix sidebar text */
[data-testid="stSidebar"] {
    color: #1e293b !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div {
    color: #1e293b !important;
}
</style>
""", unsafe_allow_html=True)

# ==================== Initialize Session State ====================
if 'language' not in st.session_state:
    st.session_state.language = 'zh_cn'

def set_language():
    """Language selector callback"""
    pass

# ==================== Load Google Material Design CSS ====================
def get_resource_path(filename):
    """Get the correct path to resource files (works in dev, frozen mode, and Streamlit Cloud)"""
    import sys
    import os
    
    # Check if running on Streamlit Cloud
    if '/home/appuser' in os.getcwd() or '/mount/src' in os.getcwd():
        # On Streamlit Cloud, files are in the current working directory
        return os.path.join(os.getcwd(), filename)
    
    if getattr(sys, 'frozen', False):
        # Running as compiled executable - files are in _internal folder
        application_path = os.path.dirname(sys.executable)
        internal_path = os.path.join(application_path, '_internal')
        if os.path.exists(internal_path):
            application_path = internal_path
    else:
        # Running as script
        application_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(application_path, filename)

def load_css():
    """Load custom Material Design CSS styles"""
    css_path = get_resource_path('style.css')
    with open(css_path, 'r', encoding='utf-8') as f:
        css = f.read()
    
    # Add Material Design color theme
    material_theme = '''
    <style>
    :root {
        --md-primary-color: #14b8a6;
        --md-primary-dark: #0d9488;
        --md-accent-color: #0f766e;
        --md-background: linear-gradient(135deg, #f0fdfa 0%, #ccfbf1 100%);
        --md-surface: #ffffff;
        --md-error: #ef4444;
        --md-success: #10b981;
    }
    </style>
    '''
    st.markdown(material_theme, unsafe_allow_html=True)
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

load_css()

# ==================== Language Selector (Top Right) ====================
def language_selector():
    """Display language selector at top right"""
    languages = get_supported_languages()
    
    # Create columns for layout
    col_space, col_lang = st.columns([4, 1])
    
    with col_lang:
        lang_options = list(languages.keys())
        current_lang_name = [k for k, v in languages.items() if v == st.session_state.language][0]
        
        selected = st.selectbox(
            "",
            options=lang_options,
            index=lang_options.index(current_lang_name),
            key="lang_selector",
            label_visibility="collapsed"
        )
        
        if selected != current_lang_name:
            st.session_state.language = languages[selected]
            st.rerun()

# ==================== Sidebar Navigation ====================
def sidebar_menu():
    """Render sidebar menu"""
    t = lambda key: get_text(key, st.session_state.language)
    
    # Add custom sidebar styling
    st.sidebar.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f5f5f5 100%);
    }
    [data-testid="stSidebarNav"] {
        background-color: transparent;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar title with Modern Teal Gradient
    st.sidebar.markdown(
        '<div style="padding: 24px; margin-bottom: 20px; '
        'background: linear-gradient(135deg, #14b8a6 0%, #0d9488 50%, #0f766e 100%); "'
        'color: white; border-radius: 12px; text-align: center; font-size: 20px; font-weight: 700; "'
        'letter-spacing: 1px; box-shadow: 0 8px 24px rgba(20, 184, 166, 0.4);">'
        f'{t("sidebar_title")}</div>',
        unsafe_allow_html=True
    )
    
    menu_items = [
        (t("nav_home"), "home"),
        (t("nav_companies"), "companies"),
        (t("nav_absent_reasons"), "absent_reasons"),
        (t("nav_workers"), "workers"),
        (t("nav_sites"), "sites"),
        (t("nav_attendance"), "attendance"),
        (t("nav_worker_stats"), "worker_stats"),
        (t("nav_site_stats"), "site_stats"),
        (t("nav_individual_worker_stats"), "individual_worker_stats")
    ]
    
    selected = st.sidebar.radio(
        "",
        options=[item[0] for item in menu_items],
        key="menu_radio",
        label_visibility="collapsed"
    )
    
    return dict(menu_items)[selected]

# ==================== Home Page ====================
def home_page():
    """Home page - System overview"""
    t = lambda key: get_text(key, st.session_state.language)
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown(f'<h1>{t("home_title")}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="text-muted" style="font-size: 17px; margin-top: 20px;">'
                f'{t("home_subtitle")}</p>', 
                unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Statistics cards with Material Design
    col1, col2, col3 = st.columns(3)
    
    workers = db_manager.get_all_workers()
    sites = db_manager.get_all_sites()
    attendance = db_manager.get_all_attendance()
    
    with col1:
        st.markdown(f'''
        <div class="card" style="background: linear-gradient(135deg, #ffffff 0%, #f0fdfa 100%); border-left: 6px solid #14b8a6;">
            <h3 style="color: #0d9488; font-size: 13px; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700;">{t("total_workers")}</h3>
            <p style="font-size: 48px; font-weight: 700; background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">{len(workers)}</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="card" style="background: linear-gradient(135deg, #ffffff 0%, #fef3c7 100%); border-left: 6px solid #f59e0b;">
            <h3 style="color: #d97706; font-size: 13px; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700;">{t("total_sites")}</h3>
            <p style="font-size: 48px; font-weight: 700; background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">{len(sites)}</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="card" style="background: linear-gradient(135deg, #ffffff 0%, #fce7f3 100%); border-left: 6px solid #ec4899;">
            <h3 style="color: #db2777; font-size: 13px; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700;">{t("total_records")}</h3>
            <p style="font-size: 48px; font-weight: 700; background: linear-gradient(135deg, #ec4899 0%, #db2777 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">{len(attendance)}</p>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== Companies Management ====================
def companies_page():
    """Companies management page - Refactored with Apple minimalist style"""
    t = lambda key: get_text(key, st.session_state.language)
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown(f'<h1>{t("companies_title")}</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Get all companies for processing
    companies = db_manager.get_all_companies()
    
    if not companies:
        st.info(t("no_companies"))
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    import pandas as pd
    from io import BytesIO
    
    # Convert to DataFrame for filtering
    df_companies = pd.DataFrame(companies)
    
    # Toolbar layout: [Search (3), Add Company (1), Import (1)]
    toolbar_cols = st.columns([3, 1, 1])
    
    # Column 1: Search input
    with toolbar_cols[0]:
        search_keyword = st.text_input(
            "🔍 搜尋公司",
            placeholder="輸入公司名稱關鍵字...",
            label_visibility="collapsed",
            key="company_search"
        )
    
    # Column 2: Add Company button
    with toolbar_cols[1]:
        if st.button("➕ 新增公司", use_container_width=True, key="add_company_btn"):
            add_company_dialog()
    
    # Column 3: Import popover
    with toolbar_cols[2]:
        with st.popover("📥 導入", use_container_width=True):
            import_dialog_content()
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Filter logic with Pandas fuzzy search
    if search_keyword and search_keyword.strip():
        # Fuzzy search - case insensitive
        filtered_df = df_companies[
            df_companies['name'].str.contains(search_keyword.strip(), case=False, na=False)
        ]
    else:
        # Default: show latest 50 records (sorted by ID descending)
        filtered_df = df_companies.sort_values('id', ascending=False).head(50)
    
    # Limit to 50 records
    total_filtered = len(filtered_df)
    display_df = filtered_df.head(50)
    
    # Display companies list
    st.markdown(f'<h2>{t("companies_list")}</h2>', unsafe_allow_html=True)
    
    if len(display_df) > 0:
        for _, company in display_df.iterrows():
            # Row layout: [ID (1), Name (4), Edit (1), Delete (1)]
            row_cols = st.columns([1, 4, 1, 1])
            
            with row_cols[0]:
                st.markdown(f"<div style='padding: 10px; font-weight: 500; color: #64748b;'>#{company['id']}</div>", unsafe_allow_html=True)
            
            with row_cols[1]:
                st.markdown(f"<div style='padding: 10px; font-size: 16px; font-weight: 500; color: #1e293b;'>{company['name']}</div>", unsafe_allow_html=True)
            
            with row_cols[2]:
                if st.button("✏️ 編輯", key=f"edit_btn_{company['id']}", use_container_width=True):
                    edit_company_dialog(company['id'], company['name'])
            
            with row_cols[3]:
                # Delete button with confirmation
                delete_key = f"delete_btn_{company['id']}"
                confirm_key = f"show_delete_confirm_{company['id']}"
                
                if st.button("🗑️ 刪除", key=delete_key, use_container_width=True):
                    st.session_state[confirm_key] = True
                
                # Show confirmation popover if triggered
                if st.session_state.get(confirm_key, False):
                    with st.popover(t("confirm_delete")):
                        st.markdown(f"**{company['name']}**")
                        
                        # Check if company has workers
                        worker_count = db_manager.get_company_worker_count(company['id'])
                        if worker_count > 0:
                            st.warning(t("has_workers_warning").format(worker_count))
                        
                        confirm_col1, confirm_col2 = st.columns(2)
                        with confirm_col1:
                            if st.button("✅ 確認", key=f"confirm_del_{company['id']}", use_container_width=True):
                                success, error_msg = db_manager.delete_company(company['id'])
                                
                                if success:
                                    st.success(t("delete_success"))
                                    st.session_state[confirm_key] = False
                                    st.rerun()
                                else:
                                    if "worker(s)" in error_msg:
                                        import re
                                        match = re.search(r'(\d+) worker', error_msg)
                                        if match:
                                            worker_count = match.group(1)
                                            st.error(t("has_workers_warning").format(worker_count))
                                        else:
                                            st.error(error_msg)
                                    else:
                                        st.error(t("delete_failed").format(error_msg))
                        
                        with confirm_col2:
                            if st.button("❌ 取消", key=f"cancel_del_{company['id']}", use_container_width=True):
                                st.session_state[confirm_key] = False
                                st.rerun()
        
        # Show limit warning if needed
        if total_filtered > 50:
            st.markdown(f'''
            <div style='padding: 12px; background: #fef3c7; border-left: 4px solid #f59e0b; 
                        border-radius: 8px; margin-top: 16px; color: #92400e;'>
                ⚠️ 僅顯示前 50 筆記錄，請使用搜尋縮小範圍（共 {total_filtered} 筆）
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.info("未找到符合條件的公司")
    
    st.markdown('</div>', unsafe_allow_html=True)


@st.dialog("➕ 新增公司", width="large")
def add_company_dialog():
    """Dialog for adding new company - wide version with two-column layout"""
    t = lambda key: get_text(key, st.session_state.language)
    
    # Two-column layout for future extensibility
    form_cols = st.columns([1, 1])
    
    with form_cols[0]:
        new_company_name = st.text_input(
            t("company_name"),
            placeholder=t("enter_company_name"),
            key="dialog_add_name"
        )
    
    with form_cols[1]:
        # Placeholder for future fields (e.g., company code, address, etc.)
        st.markdown('''
        <div style='padding: 40px 20px; text-align: center; color: #94a3b8; 
                    background: #f8fafc; border-radius: 8px; border: 2px dashed #cbd5e1;'>
            <p style='margin: 0; font-size: 14px;'>更多字段待擴展</p>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    
    # Right-aligned action buttons
    btn_col1, btn_col2 = st.columns([4, 1])
    with btn_col2:
        cancel_col, save_col = st.columns(2)
        
        with cancel_col:
            if st.button("❌ 取消", use_container_width=True, key="dialog_cancel_add"):
                st.rerun()
        
        with save_col:
            if st.button("💾 儲存", use_container_width=True, type="primary", key="dialog_save_add"):
                if new_company_name and new_company_name.strip():
                    if db_manager.company_exists(new_company_name.strip()):
                        st.error(t("site_exists"))
                    else:
                        success = db_manager.add_company(new_company_name.strip())
                        if success:
                            st.success(t("save_success"))
                            st.rerun()
                        else:
                            st.error(t("save_failed"))
                else:
                    st.error(t("fill_all_fields"))


@st.dialog("✏️ 編輯公司", width="large")
def edit_company_dialog(company_id, current_name):
    """Dialog for editing company name - wide version with two-column layout"""
    t = lambda key: get_text(key, st.session_state.language)
    
    # Dynamic title showing current company name
    st.markdown(f'''
    <div style='padding: 10px 0; margin-bottom: 20px; border-bottom: 2px solid #e5e7eb;'>
        <h3 style='margin: 0; color: #1e293b; font-size: 20px;'>
            編輯公司：{current_name}
        </h3>
    </div>
    ''', unsafe_allow_html=True)
    
    # Two-column layout for future extensibility
    form_cols = st.columns([1, 1])
    
    with form_cols[0]:
        new_name = st.text_input(
            t("company_name"),
            value=current_name,
            key=f"edit_name_{company_id}",
            placeholder=t("enter_company_name")
        )
    
    with form_cols[1]:
        # Placeholder for future fields (e.g., company code, address, etc.)
        st.markdown('''
        <div style='padding: 40px 20px; text-align: center; color: #94a3b8; 
                    background: #f8fafc; border-radius: 8px; border: 2px dashed #cbd5e1;'>
            <p style='margin: 0; font-size: 14px;'>更多字段待擴展</p>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    
    # Right-aligned action buttons
    btn_col1, btn_col2 = st.columns([4, 1])
    with btn_col2:
        cancel_col, save_col = st.columns(2)
        
        with cancel_col:
            if st.button("❌ 取消", use_container_width=True, key=f"cancel_edit_{company_id}"):
                st.rerun()
        
        with save_col:
            if st.button("💾 儲存", use_container_width=True, type="primary", key=f"save_edit_{company_id}"):
                if new_name and new_name.strip():
                    if new_name.strip() != current_name:
                        success = db_manager.update_company(company_id, new_name.strip())
                        if success:
                            st.success(t("update_success"))
                            st.rerun()
                        else:
                            st.error(t("update_failed"))
                    else:
                        st.info("沒有變更")
                else:
                    st.error(t("fill_all_fields"))


def import_dialog_content():
    """Content for import popover - two-column layout with instructions and upload"""
    t = lambda key: get_text(key, st.session_state.language)
    import pandas as pd
    from io import BytesIO
    
    st.markdown('''
    <div style='padding: 10px 0; margin-bottom: 15px; border-bottom: 2px solid #e5e7eb;'>
        <h3 style='margin: 0; color: #1e293b; font-size: 18px;'>
            📥 批量導入公司
        </h3>
    </div>
    ''', unsafe_allow_html=True)
    
    # Two-column layout: Left (Instructions & Template) | Right (Upload)
    import_cols = st.columns([2, 3])
    
    with import_cols[0]:
        st.markdown('''
        <div style='padding: 15px; background: linear-gradient(135deg, #f0fdfa 0%, #ccfbf1 100%); 
                    border-radius: 10px; border: 2px solid #14b8a6;'>
            <p style='margin: 0 0 10px 0; color: #0f766e; font-weight: 600; font-size: 14px;'>
                📄 操作指南與模板下載
            </p>
            <p style='margin: 0; color: #115e59; font-size: 12px; line-height: 1.5;'>
                1. 下載Excel模板<br>
                2. 填寫公司名稱<br>
                3. 上傳文件導入
            </p>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
        
        if st.button(t("download_template"), use_container_width=True, key="import_dl_template"):
            template_df = pd.DataFrame({'company_name': ['Company A', 'Company B', 'Company C']})
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                template_df.to_excel(writer, index=False, sheet_name='Companies')
            
            st.download_button(
                label="📥 Download",
                data=output.getvalue(),
                file_name="companies_template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                key="import_dl_file"
            )
    
    with import_cols[1]:
        st.markdown('''
        <div style='padding: 15px; background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                    border-radius: 10px; border: 2px solid #f59e0b;'>
            <p style='margin: 0 0 10px 0; color: #b45309; font-weight: 600; font-size: 14px;'>
                📤 文件上傳器
            </p>
            <p style='margin: 0; color: #92400e; font-size: 12px; line-height: 1.5;'>
                支持 .xlsx / .xls 格式<br>
                拖拽或點擊上傳
            </p>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
        
        # Upload file
        uploaded_file = st.file_uploader(
            "拖拽 Excel 到此",
            type=['xlsx', 'xls'],
            label_visibility="collapsed",
            key="import_upload"
        )
        
        if uploaded_file is not None:
            if st.button("✅ 開始導入", use_container_width=True, type="primary", key="import_start_btn"):
                try:
                    # Read Excel file
                    upload_df = pd.read_excel(uploaded_file)
                    
                    if 'company_name' not in upload_df.columns:
                        st.error(t("invalid_format"))
                    else:
                        imported_count = 0
                        duplicate_count = 0
                        failed_count = 0
                        
                        for _, row in upload_df.iterrows():
                            company_name = str(row['company_name']).strip()
                            
                            if company_name and company_name.lower() != 'nan':
                                if not db_manager.company_exists(company_name):
                                    success = db_manager.add_company(company_name)
                                    if success:
                                        imported_count += 1
                                    else:
                                        failed_count += 1
                                else:
                                    duplicate_count += 1
                        
                        if imported_count > 0:
                            st.toast(f"✅ {t('import_success').format(imported_count)}", icon="🎉")
                            st.rerun()
                        elif duplicate_count > 0:
                            st.warning(t("duplicate_skipped").format(duplicate_count))
                            st.rerun()
                        elif failed_count > 0:
                            st.error("所有公司導入失敗，請檢查文件格式")
                
                except Exception as e:
                    st.error(t("import_failed").format(str(e)))

# ==================== Absent Reasons Management ====================
def absent_reasons_page():
    """Absent reasons management page - Refactored with Apple minimalist style"""
    t = lambda key: get_text(key, st.session_state.language)
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown(f'<h1>{t("absent_reasons_title")}</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Get all absent reasons for processing
    reasons = db_manager.get_all_absent_reasons()
    
    if not reasons:
        st.info(t("no_absent_reasons"))
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    import pandas as pd
    
    # Convert to DataFrame for filtering
    df_reasons = pd.DataFrame(reasons)
    
    # Toolbar layout: [Search (3), Add Reason (1), Import (1)]
    toolbar_cols = st.columns([3, 1, 1])
    
    # Column 1: Search input
    with toolbar_cols[0]:
        search_keyword = st.text_input(
            "🔍 搜尋缺勤原因",
            placeholder="輸入原因關鍵字...",
            label_visibility="collapsed",
            key="absent_reason_search"
        )
    
    # Column 2: Add Reason button
    with toolbar_cols[1]:
        if st.button("➕ 新增原因", use_container_width=True, key="add_reason_btn"):
            add_absent_reason_dialog()
    
    # Column 3: Import popover
    with toolbar_cols[2]:
        with st.popover("📥 導入", use_container_width=True):
            import_absent_reason_dialog_content()
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Filter logic with Pandas fuzzy search
    if search_keyword and search_keyword.strip():
        # Fuzzy search - case insensitive
        filtered_df = df_reasons[
            df_reasons['reason'].str.contains(search_keyword.strip(), case=False, na=False)
        ]
    else:
        # Default: show latest 50 records (sorted by ID descending)
        filtered_df = df_reasons.sort_values('id', ascending=False).head(50)
    
    # Limit to 50 records
    total_filtered = len(filtered_df)
    display_df = filtered_df.head(50)
    
    # Display absent reasons list
    st.markdown(f'<h2>{t("absent_reasons_list")}</h2>', unsafe_allow_html=True)
    
    if len(display_df) > 0:
        for _, reason in display_df.iterrows():
            # Row layout: [ID (1), Reason (4), Edit (1), Delete (1)]
            row_cols = st.columns([1, 4, 1, 1])
            
            with row_cols[0]:
                st.markdown(f"<div style='padding: 10px; font-weight: 500; color: #64748b;'>#{reason['id']}</div>", unsafe_allow_html=True)
            
            with row_cols[1]:
                st.markdown(f"<div style='padding: 10px; font-size: 16px; font-weight: 500; color: #1e293b;'>{reason['reason']}</div>", unsafe_allow_html=True)
            
            with row_cols[2]:
                if st.button("✏️ 編輯", key=f"edit_reason_btn_{reason['id']}", use_container_width=True):
                    edit_absent_reason_dialog(reason['id'], reason['reason'])
            
            with row_cols[3]:
                # Delete button with confirmation
                delete_key = f"delete_reason_btn_{reason['id']}"
                confirm_key = f"show_delete_reason_confirm_{reason['id']}"
                
                if st.button("🗑️ 刪除", key=delete_key, use_container_width=True):
                    st.session_state[confirm_key] = True
                
                # Show confirmation popover if triggered
                if st.session_state.get(confirm_key, False):
                    with st.popover(t("confirm_delete")):
                        st.markdown(f"**{reason['reason']}**")
                        
                        # Check if reason is used in attendance records
                        attendance_count = db_manager.get_absent_reason_attendance_count(reason['id'])
                        if attendance_count > 0:
                            st.warning(f"無法刪除：該原因已被 {attendance_count} 筆考勤記錄引用。")
                        
                        confirm_col1, confirm_col2 = st.columns(2)
                        with confirm_col1:
                            if st.button("✅ 確認", key=f"confirm_del_reason_{reason['id']}", use_container_width=True):
                                success, error_msg = db_manager.delete_absent_reason(reason['id'])
                                
                                if success:
                                    st.success(t("delete_success"))
                                    st.session_state[confirm_key] = False
                                    st.rerun()
                                else:
                                    if "attendance record(s)" in error_msg:
                                        import re
                                        match = re.search(r'(\d+) attendance', error_msg)
                                        if match:
                                            att_count = match.group(1)
                                            st.error(f"無法刪除：該原因已被 {att_count} 筆考勤記錄引用。")
                                        else:
                                            st.error(error_msg)
                                    else:
                                        st.error(t("delete_failed").format(error_msg))
                        
                        with confirm_col2:
                            if st.button("❌ 取消", key=f"cancel_del_reason_{reason['id']}", use_container_width=True):
                                st.session_state[confirm_key] = False
                                st.rerun()
        
        # Show limit warning if needed
        if total_filtered > 50:
            st.markdown(f'''
            <div style='padding: 12px; background: #fef3c7; border-left: 4px solid #f59e0b; 
                        border-radius: 8px; margin-top: 16px; color: #92400e;'>
                ⚠️ 僅顯示前 50 筆記錄，請使用搜尋縮小範圍（共 {total_filtered} 筆）
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.info("未找到符合條件的缺勤原因")
    
    st.markdown('</div>', unsafe_allow_html=True)


@st.dialog("➕ 新增缺勤原因", width="large")
def add_absent_reason_dialog():
    """Dialog for adding new absent reason - wide version with two-column layout"""
    t = lambda key: get_text(key, st.session_state.language)
    
    # Two-column layout for future extensibility
    form_cols = st.columns([1, 1])
    
    with form_cols[0]:
        new_reason = st.text_input(
            t("absent_reason_name"),
            placeholder=t("enter_absent_reason"),
            key="dialog_add_reason"
        )
    
    with form_cols[1]:
        # Placeholder for future fields (e.g., reason category, description, etc.)
        st.markdown('''
        <div style='padding: 40px 20px; text-align: center; color: #94a3b8; 
                    background: #f8fafc; border-radius: 8px; border: 2px dashed #cbd5e1;'>
            <p style='margin: 0; font-size: 14px;'>更多字段待擴展</p>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    
    # Right-aligned action buttons
    btn_col1, btn_col2 = st.columns([4, 1])
    with btn_col2:
        cancel_col, save_col = st.columns(2)
        
        with cancel_col:
            if st.button("❌ 取消", use_container_width=True, key="dialog_cancel_add_reason"):
                st.rerun()
        
        with save_col:
            if st.button("💾 儲存", use_container_width=True, type="primary", key="dialog_save_add_reason"):
                if new_reason and new_reason.strip():
                    if db_manager.absent_reason_exists(new_reason.strip()):
                        st.error(t("reason_exists"))
                    else:
                        success = db_manager.add_absent_reason(new_reason.strip())
                        if success:
                            st.success(t("save_success"))
                            st.rerun()
                        else:
                            st.error(t("save_failed"))
                else:
                    st.error(t("fill_all_fields"))


@st.dialog("✏️ 編輯缺勤原因", width="large")
def edit_absent_reason_dialog(reason_id, current_reason):
    """Dialog for editing absent reason - wide version with two-column layout"""
    t = lambda key: get_text(key, st.session_state.language)
    
    # Dynamic title showing current reason
    st.markdown(f'''
    <div style='padding: 10px 0; margin-bottom: 20px; border-bottom: 2px solid #e5e7eb;'>
        <h3 style='margin: 0; color: #1e293b; font-size: 20px;'>
            編輯缺勤原因：{current_reason}
        </h3>
    </div>
    ''', unsafe_allow_html=True)
    
    # Two-column layout for future extensibility
    form_cols = st.columns([1, 1])
    
    with form_cols[0]:
        new_reason = st.text_input(
            t("absent_reason_name"),
            value=current_reason,
            key=f"edit_reason_{reason_id}",
            placeholder=t("enter_absent_reason")
        )
    
    with form_cols[1]:
        # Placeholder for future fields (e.g., reason category, description, etc.)
        st.markdown('''
        <div style='padding: 40px 20px; text-align: center; color: #94a3b8; 
                    background: #f8fafc; border-radius: 8px; border: 2px dashed #cbd5e1;'>
            <p style='margin: 0; font-size: 14px;'>更多字段待擴展</p>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    
    # Right-aligned action buttons
    btn_col1, btn_col2 = st.columns([4, 1])
    with btn_col2:
        cancel_col, save_col = st.columns(2)
        
        with cancel_col:
            if st.button("❌ 取消", use_container_width=True, key=f"cancel_edit_reason_{reason_id}"):
                st.rerun()
        
        with save_col:
            if st.button("💾 儲存", use_container_width=True, type="primary", key=f"save_edit_reason_{reason_id}"):
                if new_reason and new_reason.strip():
                    if new_reason.strip() != current_reason:
                        success = db_manager.update_absent_reason(reason_id, new_reason.strip())
                        if success:
                            st.success(t("update_success"))
                            st.rerun()
                        else:
                            st.error(t("update_failed"))
                    else:
                        st.info("沒有變更")
                else:
                    st.error(t("fill_all_fields"))


def import_absent_reason_dialog_content():
    """Content for import popover - two-column layout with instructions and upload"""
    t = lambda key: get_text(key, st.session_state.language)
    import pandas as pd
    from io import BytesIO
    
    st.markdown('''
    <div style='padding: 10px 0; margin-bottom: 15px; border-bottom: 2px solid #e5e7eb;'>
        <h3 style='margin: 0; color: #1e293b; font-size: 18px;'>
            📥 批量導入缺勤原因
        </h3>
    </div>
    ''', unsafe_allow_html=True)
    
    # Two-column layout: Left (Instructions & Template) | Right (Upload)
    import_cols = st.columns([2, 3])
    
    with import_cols[0]:
        st.markdown('''
        <div style='padding: 15px; background: linear-gradient(135deg, #f0fdfa 0%, #ccfbf1 100%); 
                    border-radius: 10px; border: 2px solid #14b8a6;'>
            <p style='margin: 0 0 10px 0; color: #0f766e; font-weight: 600; font-size: 14px;'>
                📄 操作指南與模板下載
            </p>
            <p style='margin: 0; color: #115e59; font-size: 12px; line-height: 1.5;'>
                1. 下載Excel模板<br>
                2. 填寫缺勤原因<br>
                3. 上傳文件導入
            </p>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
        
        if st.button(t("download_template"), use_container_width=True, key="import_dl_reason_template"):
            template_df = pd.DataFrame({'reason': ['Sick Leave', 'Personal Leave', 'Vacation']})
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                template_df.to_excel(writer, index=False, sheet_name='AbsentReasons')
            
            st.download_button(
                label="📥 Download",
                data=output.getvalue(),
                file_name="absent_reasons_template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                key="import_dl_reason_file"
            )
    
    with import_cols[1]:
        st.markdown('''
        <div style='padding: 15px; background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                    border-radius: 10px; border: 2px solid #f59e0b;'>
            <p style='margin: 0 0 10px 0; color: #b45309; font-weight: 600; font-size: 14px;'>
                📤 文件上傳器
            </p>
            <p style='margin: 0; color: #92400e; font-size: 12px; line-height: 1.5;'>
                支持 .xlsx / .xls 格式<br>
                拖拽或點擊上傳
            </p>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
        
        # Upload file
        uploaded_file = st.file_uploader(
            "拖拽 Excel 到此",
            type=['xlsx', 'xls'],
            label_visibility="collapsed",
            key="import_reason_upload"
        )
        
        if uploaded_file is not None:
            if st.button("✅ 開始導入", use_container_width=True, type="primary", key="import_reason_start_btn"):
                try:
                    # Read Excel file
                    upload_df = pd.read_excel(uploaded_file)
                    
                    if 'reason' not in upload_df.columns:
                        st.error(t("invalid_format"))
                    else:
                        imported_count = 0
                        duplicate_count = 0
                        failed_count = 0
                        
                        for _, row in upload_df.iterrows():
                            reason = str(row['reason']).strip()
                            
                            if reason and reason.lower() != 'nan':
                                if not db_manager.absent_reason_exists(reason):
                                    success = db_manager.add_absent_reason(reason)
                                    if success:
                                        imported_count += 1
                                    else:
                                        failed_count += 1
                                else:
                                    duplicate_count += 1
                        
                        if imported_count > 0:
                            st.toast(f"✅ {t('import_success').format(imported_count)}", icon="🎉")
                            st.rerun()
                        elif duplicate_count > 0:
                            st.warning(t("duplicate_skipped").format(duplicate_count))
                            st.rerun()
                        elif failed_count > 0:
                            st.error("所有缺勤原因導入失敗，請檢查文件格式")
                
                except Exception as e:
                    st.error(t("import_failed").format(str(e)))

# ==================== Workers Management ====================
def workers_page():
    """Workers management page - Refactored with Apple minimalist style"""
    t = lambda key: get_text(key, st.session_state.language)
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown(f'<h1>{t("workers_title")}</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Get companies for dropdown
    companies = db_manager.get_all_companies()
    
    if not companies:
        st.warning(t("no_companies"))
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Get all workers for processing
    workers = db_manager.get_all_workers()
    
    if not workers:
        st.info(t("no_workers"))
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    import pandas as pd
    
    # Convert to DataFrame for filtering
    df_workers = pd.DataFrame(workers)
    
    # Toolbar layout: [Search (3), Add Worker (1), Import (1)]
    toolbar_cols = st.columns([3, 1, 1])
    
    # Column 1: Search input
    with toolbar_cols[0]:
        search_keyword = st.text_input(
            "🔍 搜尋員工",
            placeholder="輸入姓名或公司關鍵字...",
            label_visibility="collapsed",
            key="worker_search"
        )
    
    # Column 2: Add Worker button
    with toolbar_cols[1]:
        if st.button("➕ 新增員工", use_container_width=True, key="add_worker_btn"):
            add_worker_dialog(companies)
    
    # Column 3: Import popover
    with toolbar_cols[2]:
        with st.popover("📥 導入", use_container_width=True):
            import_worker_dialog_content(companies)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Filter logic with Pandas fuzzy search (match both name and company_name)
    if search_keyword and search_keyword.strip():
        keyword = search_keyword.strip()
        # Fuzzy search - case insensitive on both name and company_name
        filtered_df = df_workers[
            df_workers['name'].str.contains(keyword, case=False, na=False) |
            df_workers['company_name'].str.contains(keyword, case=False, na=False)
        ]
    else:
        # Default: show latest 50 records (sorted by ID descending)
        filtered_df = df_workers.sort_values('id', ascending=False).head(50)
    
    # Limit to 50 records
    total_filtered = len(filtered_df)
    display_df = filtered_df.head(50)
    
    # Display workers list
    st.markdown(f'<h2>{t("workers_list")}</h2>', unsafe_allow_html=True)
    
    if len(display_df) > 0:
        for _, worker in display_df.iterrows():
            # Row layout: [ID (0.5), Name (2.5), Company (2), Edit (1), Delete (1)]
            row_cols = st.columns([0.5, 2.5, 2, 1, 1])
            
            with row_cols[0]:
                st.markdown(f"<div style='padding: 10px; font-weight: 500; color: #64748b;'>#{worker['id']}</div>", unsafe_allow_html=True)
            
            with row_cols[1]:
                st.markdown(f"<div style='padding: 10px; font-size: 16px; font-weight: 500; color: #1e293b;'>{worker['name']}</div>", unsafe_allow_html=True)
            
            with row_cols[2]:
                st.markdown(f"<div style='padding: 10px; font-size: 15px; color: #475569;'>{worker['company_name']}</div>", unsafe_allow_html=True)
            
            with row_cols[3]:
                if st.button("✏️ 編輯", key=f"edit_worker_btn_{worker['id']}", use_container_width=True):
                    edit_worker_dialog(worker['id'], worker['name'], worker['company_name'], companies)
            
            with row_cols[4]:
                # Delete button with confirmation
                delete_key = f"delete_worker_btn_{worker['id']}"
                confirm_key = f"show_delete_worker_confirm_{worker['id']}"
                
                if st.button("🗑️ 刪除", key=delete_key, use_container_width=True):
                    st.session_state[confirm_key] = True
                
                # Show confirmation popover if triggered
                if st.session_state.get(confirm_key, False):
                    with st.popover(t("confirm_delete")):
                        st.markdown(f"**{worker['name']}**")
                        st.markdown(f"所屬公司：{worker['company_name']}")
                        
                        # Check if worker has attendance records
                        attendance_count = db_manager.get_worker_attendance_count(worker['id'])
                        if attendance_count > 0:
                            st.warning(f"無法刪除：該員工已有 {attendance_count} 筆考勤記錄。")
                        
                        confirm_col1, confirm_col2 = st.columns(2)
                        with confirm_col1:
                            if st.button("✅ 確認", key=f"confirm_del_worker_{worker['id']}", use_container_width=True):
                                success, error_msg = db_manager.delete_worker(worker['id'])
                                
                                if success:
                                    st.success(t("delete_success"))
                                    st.session_state[confirm_key] = False
                                    st.rerun()
                                else:
                                    if "attendance record(s)" in error_msg:
                                        import re
                                        match = re.search(r'(\d+) attendance', error_msg)
                                        if match:
                                            att_count = match.group(1)
                                            st.error(f"無法刪除：該員工已有 {att_count} 筆考勤記錄。請先刪除相關考勤記錄。")
                                        else:
                                            st.error(error_msg)
                                    else:
                                        st.error(t("delete_failed").format(error_msg))
                        
                        with confirm_col2:
                            if st.button("❌ 取消", key=f"cancel_del_worker_{worker['id']}", use_container_width=True):
                                st.session_state[confirm_key] = False
                                st.rerun()
        
        # Show limit warning if needed
        if total_filtered > 50:
            st.markdown(f'''
            <div style='padding: 12px; background: #fef3c7; border-left: 4px solid #f59e0b; 
                        border-radius: 8px; margin-top: 16px; color: #92400e;'>
                ⚠️ 僅顯示前 50 筆記錄，請使用搜尋縮小範圍（共 {total_filtered} 筆）
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.info("未找到符合條件的員工")
    
    st.markdown('</div>', unsafe_allow_html=True)


@st.dialog("➕ 新增員工", width="large")
def add_worker_dialog(companies):
    """Dialog for adding new worker - wide version with two-column layout"""
    t = lambda key: get_text(key, st.session_state.language)
    
    # Two-column layout
    form_cols = st.columns([1, 1])
    
    with form_cols[0]:
        worker_name = st.text_input(
            t("worker_name"),
            placeholder=t("enter_worker_name"),
            key="dialog_add_worker_name"
        )
    
    with form_cols[1]:
        # Company selectbox
        company_options = {c['name']: c['id'] for c in companies}
        selected_company = st.selectbox(
            t("col_company_name"),
            options=list(company_options.keys()),
            key="dialog_add_worker_company"
        )
    
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    
    # Right-aligned action buttons
    btn_col1, btn_col2 = st.columns([4, 1])
    with btn_col2:
        cancel_col, save_col = st.columns(2)
        
        with cancel_col:
            if st.button("❌ 取消", use_container_width=True, key="dialog_cancel_add_worker"):
                st.rerun()
        
        with save_col:
            if st.button("💾 儲存", use_container_width=True, type="primary", key="dialog_save_add_worker"):
                if worker_name and worker_name.strip():
                    if db_manager.worker_exists(worker_name.strip()):
                        st.error(t("worker_exists"))
                    else:
                        company_id = company_options[selected_company]
                        success = db_manager.add_worker(worker_name.strip(), company_id)
                        if success:
                            st.success(t("save_success"))
                            st.rerun()
                        else:
                            st.error(t("save_failed"))
                else:
                    st.error(t("fill_all_fields"))


@st.dialog("✏️ 編輯員工", width="large")
def edit_worker_dialog(worker_id, current_name, current_company_name, companies):
    """Dialog for editing worker - wide version with two-column layout"""
    t = lambda key: get_text(key, st.session_state.language)
    
    # Dynamic title showing current worker name
    st.markdown(f'''
    <div style='padding: 10px 0; margin-bottom: 20px; border-bottom: 2px solid #e5e7eb;'>
        <h3 style='margin: 0; color: #1e293b; font-size: 20px;'>
            編輯員工：{current_name}
        </h3>
    </div>
    ''', unsafe_allow_html=True)
    
    # Two-column layout
    form_cols = st.columns([1, 1])
    
    with form_cols[0]:
        new_name = st.text_input(
            t("worker_name"),
            value=current_name,
            key=f"edit_worker_name_{worker_id}",
            placeholder=t("enter_worker_name")
        )
    
    with form_cols[1]:
        # Company selectbox with current selection
        company_options = {c['name']: c['id'] for c in companies}
        selected_company = st.selectbox(
            t("col_company_name"),
            options=list(company_options.keys()),
            index=list(company_options.keys()).index(current_company_name) if current_company_name in company_options else 0,
            key=f"edit_worker_company_{worker_id}"
        )
    
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    
    # Right-aligned action buttons
    btn_col1, btn_col2 = st.columns([4, 1])
    with btn_col2:
        cancel_col, save_col = st.columns(2)
        
        with cancel_col:
            if st.button("❌ 取消", use_container_width=True, key=f"cancel_edit_worker_{worker_id}"):
                st.rerun()
        
        with save_col:
            if st.button("💾 儲存", use_container_width=True, type="primary", key=f"save_edit_worker_{worker_id}"):
                if new_name and new_name.strip():
                    company_id = company_options[selected_company]
                    # Check if name changed and new name already exists
                    if new_name.strip() != current_name and db_manager.worker_exists(new_name.strip()):
                        st.error(t("worker_exists"))
                    else:
                        success = db_manager.update_worker(worker_id, new_name.strip(), company_id)
                        if success:
                            st.success(t("update_success"))
                            st.rerun()
                        else:
                            st.error(t("update_failed"))
                else:
                    st.error(t("fill_all_fields"))


def import_worker_dialog_content(companies):
    """Content for import popover - two-column layout with instructions and upload"""
    t = lambda key: get_text(key, st.session_state.language)
    import pandas as pd
    from io import BytesIO
    
    st.markdown('''
    <div style='padding: 10px 0; margin-bottom: 15px; border-bottom: 2px solid #e5e7eb;'>
        <h3 style='margin: 0; color: #1e293b; font-size: 18px;'>
            📥 批量導入員工
        </h3>
    </div>
    ''', unsafe_allow_html=True)
    
    # Two-column layout: Left (Instructions & Template) | Right (Upload)
    import_cols = st.columns([2, 3])
    
    with import_cols[0]:
        st.markdown('''
        <div style='padding: 15px; background: linear-gradient(135deg, #f0fdfa 0%, #ccfbf1 100%); 
                    border-radius: 10px; border: 2px solid #14b8a6;'>
            <p style='margin: 0 0 10px 0; color: #0f766e; font-weight: 600; font-size: 14px;'>
                📄 操作指南與模板下載
            </p>
            <p style='margin: 0; color: #115e59; font-size: 12px; line-height: 1.5;'>
                1. 下載Excel模板<br>
                2. 填寫姓名和公司<br>
                3. 上傳文件導入
            </p>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
        
        if st.button(t("download_template"), use_container_width=True, key="import_dl_worker_template"):
            template_df = pd.DataFrame({
                'name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
                'company': ['ABC Construction Co.', 'XYZ Engineering Ltd.', 'ABC Construction Co.']
            })
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                template_df.to_excel(writer, index=False, sheet_name='Workers')
            
            st.download_button(
                label="📥 Download",
                data=output.getvalue(),
                file_name="workers_template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                key="import_dl_worker_file"
            )
    
    with import_cols[1]:
        st.markdown('''
        <div style='padding: 15px; background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                    border-radius: 10px; border: 2px solid #f59e0b;'>
            <p style='margin: 0 0 10px 0; color: #b45309; font-weight: 600; font-size: 14px;'>
                📤 文件上傳器
            </p>
            <p style='margin: 0; color: #92400e; font-size: 12px; line-height: 1.5;'>
                支持 .xlsx / .xls 格式<br>
                拖拽或點擊上傳
            </p>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
        
        # Upload file
        uploaded_file = st.file_uploader(
            "拖拽 Excel 到此",
            type=['xlsx', 'xls'],
            label_visibility="collapsed",
            key="import_worker_upload"
        )
        
        if uploaded_file is not None:
            if st.button("✅ 開始導入", use_container_width=True, type="primary", key="import_worker_start_btn"):
                try:
                    # Read Excel file
                    upload_df = pd.read_excel(uploaded_file)
                    
                    # Check required columns
                    if 'name' not in upload_df.columns or 'company' not in upload_df.columns:
                        st.error("Excel格式無效。必須包含 'name' 和 'company' 兩列。")
                    else:
                        # Build company lookup
                        company_lookup = {c['name']: c['id'] for c in companies}
                        
                        imported_count = 0
                        duplicate_count = 0
                        failed_count = 0
                        
                        for _, row in upload_df.iterrows():
                            worker_name = str(row['name']).strip()
                            company_name = str(row['company']).strip()
                            
                            if worker_name and worker_name.lower() != 'nan' and company_name and company_name.lower() != 'nan':
                                # Check if company exists
                                if company_name not in company_lookup:
                                    failed_count += 1
                                    continue
                                
                                # Check if worker already exists
                                if not db_manager.worker_exists(worker_name):
                                    company_id = company_lookup[company_name]
                                    success = db_manager.add_worker(worker_name, company_id)
                                    if success:
                                        imported_count += 1
                                    else:
                                        failed_count += 1
                                else:
                                    duplicate_count += 1
                        
                        if imported_count > 0:
                            st.toast(f"✅ {t('import_success').format(imported_count)}", icon="🎉")
                            st.rerun()
                        elif duplicate_count > 0:
                            st.warning(t("duplicate_skipped").format(duplicate_count))
                            st.rerun()
                        elif failed_count > 0:
                            st.error("所有員工導入失敗，請檢查文件格式和公司名稱是否正確")
                
                except Exception as e:
                    st.error(t("import_failed").format(str(e)))

# ==================== Sites Management ====================
def sites_page():
    """Sites management page - Refactored with Apple minimalist style"""
    t = lambda key: get_text(key, st.session_state.language)
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown(f'<h1>{t("sites_title")}</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Get all sites for processing
    sites = db_manager.get_all_sites()
    
    if not sites:
        st.info(t("no_sites"))
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    import pandas as pd
    
    # Convert to DataFrame for filtering
    df_sites = pd.DataFrame(sites)
    
    # Toolbar layout: [Search (3), Add Site (1), Import (1)]
    toolbar_cols = st.columns([3, 1, 1])
    
    # Column 1: Search input
    with toolbar_cols[0]:
        search_keyword = st.text_input(
            "🔍 搜尋工地",
            placeholder="輸入工地名稱關鍵字...",
            label_visibility="collapsed",
            key="site_search"
        )
    
    # Column 2: Add Site button
    with toolbar_cols[1]:
        if st.button("➕ 新增工地", use_container_width=True, key="add_site_btn"):
            add_site_dialog()
    
    # Column 3: Import popover
    with toolbar_cols[2]:
        with st.popover("📥 導入", use_container_width=True):
            import_site_dialog_content()
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Filter logic with Pandas fuzzy search
    if search_keyword and search_keyword.strip():
        keyword = search_keyword.strip()
        # Fuzzy search - case insensitive on site name
        filtered_df = df_sites[
            df_sites['name'].str.contains(keyword, case=False, na=False)
        ]
    else:
        # Default: show latest 50 records (sorted by ID descending)
        filtered_df = df_sites.sort_values('id', ascending=False).head(50)
    
    # Limit to 50 records
    total_filtered = len(filtered_df)
    display_df = filtered_df.head(50)
    
    # Display sites list
    st.markdown(f'<h2>{t("sites_list")}</h2>', unsafe_allow_html=True)
    
    if len(display_df) > 0:
        for _, site in display_df.iterrows():
            # Row layout: [ID (1), Name (4), Edit (1), Delete (1)]
            row_cols = st.columns([1, 4, 1, 1])
            
            with row_cols[0]:
                st.markdown(f"<div style='padding: 10px; font-weight: 500; color: #64748b;'>#{site['id']}</div>", unsafe_allow_html=True)
            
            with row_cols[1]:
                st.markdown(f"<div style='padding: 10px; font-size: 16px; font-weight: 500; color: #1e293b;'>{site['name']}</div>", unsafe_allow_html=True)
            
            with row_cols[2]:
                if st.button("✏️ 編輯", key=f"edit_site_btn_{site['id']}", use_container_width=True):
                    edit_site_dialog(site['id'], site['name'])
            
            with row_cols[3]:
                # Delete button with confirmation
                delete_key = f"delete_site_btn_{site['id']}"
                confirm_key = f"show_delete_site_confirm_{site['id']}"
                
                if st.button("🗑️ 刪除", key=delete_key, use_container_width=True):
                    st.session_state[confirm_key] = True
                
                # Show confirmation popover if triggered
                if st.session_state.get(confirm_key, False):
                    with st.popover(t("confirm_delete")):
                        st.markdown(f"**{site['name']}**")
                        
                        # Check if site has attendance records
                        attendance_count = db_manager.get_site_attendance_count(site['id'])
                        if attendance_count > 0:
                            st.warning(f"無法刪除：該工地已有 {attendance_count} 筆考勤記錄。")
                        
                        confirm_col1, confirm_col2 = st.columns(2)
                        with confirm_col1:
                            if st.button("✅ 確認", key=f"confirm_del_site_{site['id']}", use_container_width=True):
                                success, error_msg = db_manager.delete_site(site['id'])
                                
                                if success:
                                    st.success(t("delete_success"))
                                    st.session_state[confirm_key] = False
                                    st.rerun()
                                else:
                                    if "attendance record(s)" in error_msg:
                                        import re
                                        match = re.search(r'(\d+) attendance', error_msg)
                                        if match:
                                            att_count = match.group(1)
                                            st.error(f"無法刪除：該工地已被 {att_count} 筆考勤記錄引用。請先刪除相關考勤記錄。")
                                        else:
                                            st.error(error_msg)
                                    else:
                                        st.error(t("delete_failed").format(error_msg))
                        
                        with confirm_col2:
                            if st.button("❌ 取消", key=f"cancel_del_site_{site['id']}", use_container_width=True):
                                st.session_state[confirm_key] = False
                                st.rerun()
        
        # Show limit warning if needed
        if total_filtered > 50:
            st.markdown(f'''
            <div style='padding: 12px; background: #fef3c7; border-left: 4px solid #f59e0b; 
                        border-radius: 8px; margin-top: 16px; color: #92400e;'>
                ⚠️ 僅顯示前 50 筆記錄，請使用搜尋縮小範圍（共 {total_filtered} 筆）
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.info("未找到符合條件的工地")
    
    st.markdown('</div>', unsafe_allow_html=True)


@st.dialog("➕ 新增工地", width="large")
def add_site_dialog():
    """Dialog for adding new site - wide version with two-column layout"""
    t = lambda key: get_text(key, st.session_state.language)
    
    # Two-column layout
    form_cols = st.columns([1, 1])
    
    with form_cols[0]:
        site_name = st.text_input(
            t("site_name"),
            placeholder=t("enter_site_name"),
            key="dialog_add_site_name"
        )
    
    with form_cols[1]:
        # Placeholder for future fields (e.g., address, manager, etc.)
        st.markdown('''
        <div style='padding: 40px 20px; text-align: center; color: #94a3b8; 
                    background: #f8fafc; border-radius: 8px; border: 2px dashed #cbd5e1;'>
            <p style='margin: 0; font-size: 14px;'>更多字段待擴展<br>(地址、負責人等)</p>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    
    # Right-aligned action buttons
    btn_col1, btn_col2 = st.columns([4, 1])
    with btn_col2:
        cancel_col, save_col = st.columns(2)
        
        with cancel_col:
            if st.button("❌ 取消", use_container_width=True, key="dialog_cancel_add_site"):
                st.rerun()
        
        with save_col:
            if st.button("💾 儲存", use_container_width=True, type="primary", key="dialog_save_add_site"):
                if site_name and site_name.strip():
                    if db_manager.site_exists(site_name.strip()):
                        st.error(t("site_exists"))
                    else:
                        success = db_manager.add_site(site_name.strip())
                        if success:
                            st.success(t("save_success"))
                            st.rerun()
                        else:
                            st.error(t("save_failed"))
                else:
                    st.error(t("fill_site_name"))


@st.dialog("✏️ 編輯工地", width="large")
def edit_site_dialog(site_id, current_name):
    """Dialog for editing site - wide version with two-column layout"""
    t = lambda key: get_text(key, st.session_state.language)
    
    # Dynamic title showing current site name
    st.markdown(f'''
    <div style='padding: 10px 0; margin-bottom: 20px; border-bottom: 2px solid #e5e7eb;'>
        <h3 style='margin: 0; color: #1e293b; font-size: 20px;'>
            編輯工地：{current_name}
        </h3>
    </div>
    ''', unsafe_allow_html=True)
    
    # Two-column layout
    form_cols = st.columns([1, 1])
    
    with form_cols[0]:
        new_name = st.text_input(
            t("site_name"),
            value=current_name,
            key=f"edit_site_name_{site_id}",
            placeholder=t("enter_site_name")
        )
    
    with form_cols[1]:
        # Placeholder for future fields (e.g., address, manager, etc.)
        st.markdown('''
        <div style='padding: 40px 20px; text-align: center; color: #94a3b8; 
                    background: #f8fafc; border-radius: 8px; border: 2px dashed #cbd5e1;'>
            <p style='margin: 0; font-size: 14px;'>更多字段待擴展<br>(地址、負責人等)</p>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    
    # Right-aligned action buttons
    btn_col1, btn_col2 = st.columns([4, 1])
    with btn_col2:
        cancel_col, save_col = st.columns(2)
        
        with cancel_col:
            if st.button("❌ 取消", use_container_width=True, key=f"cancel_edit_site_{site_id}"):
                st.rerun()
        
        with save_col:
            if st.button("💾 儲存", use_container_width=True, type="primary", key=f"save_edit_site_{site_id}"):
                if new_name and new_name.strip():
                    if new_name.strip() != current_name:
                        success = db_manager.update_site(site_id, new_name.strip())
                        if success:
                            st.success(t("update_success"))
                            st.rerun()
                        else:
                            st.error(t("update_failed"))
                    else:
                        st.info("沒有變更")
                else:
                    st.error(t("fill_site_name"))


def import_site_dialog_content():
    """Content for import popover - two-column layout with instructions and upload"""
    t = lambda key: get_text(key, st.session_state.language)
    import pandas as pd
    from io import BytesIO
    
    st.markdown('''
    <div style='padding: 10px 0; margin-bottom: 15px; border-bottom: 2px solid #e5e7eb;'>
        <h3 style='margin: 0; color: #1e293b; font-size: 18px;'>
            📥 批量導入工地
        </h3>
    </div>
    ''', unsafe_allow_html=True)
    
    # Two-column layout: Left (Instructions & Template) | Right (Upload)
    import_cols = st.columns([2, 3])
    
    with import_cols[0]:
        st.markdown('''
        <div style='padding: 15px; background: linear-gradient(135deg, #f0fdfa 0%, #ccfbf1 100%); 
                    border-radius: 10px; border: 2px solid #14b8a6;'>
            <p style='margin: 0 0 10px 0; color: #0f766e; font-weight: 600; font-size: 14px;'>
                📄 操作指南與模板下載
            </p>
            <p style='margin: 0; color: #115e59; font-size: 12px; line-height: 1.5;'>
                1. 下載Excel模板<br>
                2. 填寫工地名稱<br>
                3. 上傳文件導入
            </p>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
        
        if st.button(t("download_template"), use_container_width=True, key="import_dl_site_template"):
            template_df = pd.DataFrame({'name': ['Site A - Main Building', 'Site B - Warehouse', 'Site C - Parking Lot']})
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                template_df.to_excel(writer, index=False, sheet_name='Sites')
            
            st.download_button(
                label="📥 Download",
                data=output.getvalue(),
                file_name="sites_template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                key="import_dl_site_file"
            )
    
    with import_cols[1]:
        st.markdown('''
        <div style='padding: 15px; background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                    border-radius: 10px; border: 2px solid #f59e0b;'>
            <p style='margin: 0 0 10px 0; color: #b45309; font-weight: 600; font-size: 14px;'>
                📤 文件上傳器
            </p>
            <p style='margin: 0; color: #92400e; font-size: 12px; line-height: 1.5;'>
                支持 .xlsx / .xls 格式<br>
                拖拽或點擊上傳
            </p>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
        
        # Upload file
        uploaded_file = st.file_uploader(
            "拖拽 Excel 到此",
            type=['xlsx', 'xls'],
            label_visibility="collapsed",
            key="import_site_upload"
        )
        
        if uploaded_file is not None:
            if st.button("✅ 開始導入", use_container_width=True, type="primary", key="import_site_start_btn"):
                try:
                    # Read Excel file
                    upload_df = pd.read_excel(uploaded_file)
                    
                    if 'name' not in upload_df.columns:
                        st.error("Excel格式無效。必須包含 'name' 列。")
                    else:
                        imported_count = 0
                        duplicate_count = 0
                        failed_count = 0
                        
                        for _, row in upload_df.iterrows():
                            site_name = str(row['name']).strip()
                            
                            if site_name and site_name.lower() != 'nan':
                                if not db_manager.site_exists(site_name):
                                    success = db_manager.add_site(site_name)
                                    if success:
                                        imported_count += 1
                                    else:
                                        failed_count += 1
                                else:
                                    duplicate_count += 1
                        
                        if imported_count > 0:
                            st.toast(f"✅ {t('import_success').format(imported_count)}", icon="🎉")
                            st.rerun()
                        elif duplicate_count > 0:
                            st.warning(t("duplicate_skipped").format(duplicate_count))
                            st.rerun()
                        elif failed_count > 0:
                            st.error("所有工地導入失敗，請檢查文件格式")
                
                except Exception as e:
                    st.error(t("import_failed").format(str(e)))

# ==================== Attendance Recording ====================
def attendance_page():
    """Attendance recording page - Refactored with enhanced toolbar and Apple minimalist style"""
    t = lambda key: get_text(key, st.session_state.language)
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown(f'<h1>{t("attendance_title")}</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Get base data
    workers = db_manager.get_all_workers()
    sites = db_manager.get_all_sites()
    absent_reasons = db_manager.get_all_absent_reasons()
    
    if not workers:
        st.warning(t("please_add_workers"))
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    if not sites:
        st.warning(t("please_add_sites"))
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    import pandas as pd
    from datetime import timedelta
    
    # Enhanced toolbar layout: [Date Range (2), Search (1), Add Button (1), Import (1)]
    toolbar_cols = st.columns([2, 1, 1, 1])
    
    # Column 1: Date range filter
    with toolbar_cols[0]:
        today = date.today()
        default_start = today - timedelta(days=30)
        
        date_range_cols = st.columns(2)
        with date_range_cols[0]:
            start_date_filter = st.date_input(
                "📅 開始日期",
                value=default_start,
                key="att_start_date"
            )
        with date_range_cols[1]:
            end_date_filter = st.date_input(
                "📅 結束日期",
                value=today,
                key="att_end_date"
            )
    
    # Column 2: Search input
    with toolbar_cols[1]:
        search_keyword = st.text_input(
            "🔍 搜尋",
            placeholder="員工或工地...",
            label_visibility="collapsed",
            key="att_search"
        )
    
    # Column 3: Add Attendance button
    with toolbar_cols[2]:
        if st.button("➕ 記考勤", use_container_width=True, key="add_attendance_btn"):
            add_attendance_dialog(workers, sites, absent_reasons)
    
    # Column 4: Import popover
    with toolbar_cols[3]:
        with st.popover("📥 導入", use_container_width=True):
            import_attendance_dialog_content(workers, sites, absent_reasons)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Get attendance records filtered by date range
    attendance_records = db_manager.get_attendance_by_date_range(start_date_filter, end_date_filter)
    
    if not attendance_records:
        st.info("在選定日期範圍內無考勤記錄")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Convert to DataFrame for filtering
    df_attendance = pd.DataFrame(attendance_records)
    
    # Filter logic with Pandas fuzzy search (match worker_name or any site name)
    if search_keyword and search_keyword.strip():
        keyword = search_keyword.strip()
        # Fuzzy search on worker name and all site columns
        filtered_df = df_attendance[
            df_attendance['worker_name'].str.contains(keyword, case=False, na=False) |
            df_attendance['morning_site'].fillna('').str.contains(keyword, case=False, na=False) |
            df_attendance['afternoon_site'].fillna('').str.contains(keyword, case=False, na=False) |
            df_attendance['evening_site'].fillna('').str.contains(keyword, case=False, na=False)
        ]
    else:
        filtered_df = df_attendance
    
    # Limit to 50 records
    total_filtered = len(filtered_df)
    display_df = filtered_df.head(50)
    
    # Display attendance records list
    st.markdown(f'<h2>{t("attendance_list")}</h2>', unsafe_allow_html=True)
    
    if len(display_df) > 0:
        for _, record in display_df.iterrows():
            # Create row container with subtle background
            st.markdown('''
            <div style='padding: 12px; margin-bottom: 8px; background: white; 
                        border-radius: 8px; border: 1px solid #e5e7eb;'>
            ''', unsafe_allow_html=True)
            
            # Row layout: [Date (1.5), Worker+Company (3), Sites (3.5), OT (1), Actions (1, 1)]
            row_cols = st.columns([1.5, 3, 3.5, 1, 1, 1])
            
            with row_cols[0]:
                # Format date nicely
                work_date_str = pd.to_datetime(record['work_date']).strftime('%Y-%m-%d')
                st.markdown(f"<div style='font-size: 14px; font-weight: 600; color: #1e293b;'>{work_date_str}</div>", unsafe_allow_html=True)
            
            with row_cols[1]:
                st.markdown(f"<div style='font-size: 15px; font-weight: 500; color: #1e293b;'>{record['worker_name']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size: 12px; color: #64748b;'>{record['company_name']}</div>", unsafe_allow_html=True)
            
            with row_cols[2]:
                # Display time slot badges
                badge_html = "<div style='display: flex; gap: 6px; flex-wrap: wrap;'>"
                
                if record['morning_site']:
                    badge_html += f"""
                    <span style='padding: 4px 10px; background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                                border-radius: 12px; font-size: 11px; color: #1e40af; font-weight: 500;'>
                        🌅 {record['morning_site']}
                    </span>"""
                
                if record['afternoon_site']:
                    badge_html += f"""
                    <span style='padding: 4px 10px; background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                                border-radius: 12px; font-size: 11px; color: #92400e; font-weight: 500;'>
                        ☀️ {record['afternoon_site']}
                    </span>"""
                
                if record['evening_site']:
                    badge_html += f"""
                    <span style='padding: 4px 10px; background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%); 
                                border-radius: 12px; font-size: 11px; color: #3730a3; font-weight: 500;'>
                        🌙 {record['evening_site']}
                    </span>"""
                
                badge_html += "</div>"
                st.markdown(badge_html, unsafe_allow_html=True)
            
            with row_cols[3]:
                # Overtime hours
                ot_hours = float(record['overtime_hours']) if record['overtime_hours'] else 0.0
                if ot_hours > 0:
                    st.markdown(f"<div style='font-size: 14px; color: #dc2626; font-weight: 600;'>+{ot_hours}h</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='font-size: 12px; color: #94a3b8;'>-</div>", unsafe_allow_html=True)
            
            with row_cols[4]:
                if st.button("✏️", key=f"edit_att_btn_{record['id']}", use_container_width=True, help="編輯"):
                    edit_attendance_dialog(record['id'], record, workers, sites, absent_reasons)
            
            with row_cols[5]:
                # Delete button with confirmation
                delete_key = f"delete_att_btn_{record['id']}"
                confirm_key = f"show_delete_att_confirm_{record['id']}"
                
                if st.button("🗑️", key=delete_key, use_container_width=True, help="刪除"):
                    st.session_state[confirm_key] = True
                
                # Show confirmation popover if triggered
                if st.session_state.get(confirm_key, False):
                    with st.popover("確認刪除"):
                        st.markdown(f"**{record['worker_name']}** - {pd.to_datetime(record['work_date']).strftime('%Y-%m-%d')}")
                        
                        confirm_col1, confirm_col2 = st.columns(2)
                        with confirm_col1:
                            if st.button("✅ 確認", key=f"confirm_del_att_{record['id']}", use_container_width=True):
                                success, error_msg = db_manager.delete_attendance(record['id'])
                                
                                if success:
                                    st.success(t("delete_success"))
                                    st.session_state[confirm_key] = False
                                    st.rerun()
                                else:
                                    st.error(t("delete_failed").format(error_msg))
                        
                        with confirm_col2:
                            if st.button("❌ 取消", key=f"cancel_del_att_{record['id']}", use_container_width=True):
                                st.session_state[confirm_key] = False
                                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Show limit warning if needed
        if total_filtered > 50:
            st.markdown(f'''
            <div style='padding: 12px; background: #fef3c7; border-left: 4px solid #f59e0b; 
                        border-radius: 8px; margin-top: 16px; color: #92400e;'>
                ⚠️ 僅顯示前 50 筆記錄，請使用搜尋縮小範圍（共 {total_filtered} 筆）
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.info("未找到符合條件的考勤記錄")
    
    st.markdown('</div>', unsafe_allow_html=True)


@st.dialog("➕ 新增考勤記錄", width="large")
def add_attendance_dialog(workers, sites, absent_reasons):
    """Dialog for adding new attendance record - wide version with two-column layout"""
    t = lambda key: get_text(key, st.session_state.language)
    
    st.markdown('''
    <div style='padding: 10px 0; margin-bottom: 20px; border-bottom: 2px solid #e5e7eb;'>
        <h3 style='margin: 0; color: #1e293b; font-size: 20px;'>
            新增考勤記錄
        </h3>
    </div>
    ''', unsafe_allow_html=True)
    
    # Two-column layout
    form_cols = st.columns([1, 1])
    
    with form_cols[0]:
        # Left column: Date and Worker selection
        work_date = st.date_input(
            t("date"),
            value=date.today(),
            key="dialog_add_att_date"
        )
        
        worker_options = {w['name']: w['id'] for w in workers}
        selected_worker = st.selectbox(
            t("worker"),
            options=list(worker_options.keys()),
            key="dialog_add_att_worker"
        )
    
    with form_cols[1]:
        # Right column: Site selections and overtime
        site_options = {s['name']: s['id'] for s in sites}
        site_names = ["-- 請選擇 --"] + list(site_options.keys())
        
        morning_site = st.selectbox(
            "🌅 " + t("morning"),
            options=site_names,
            key="dialog_add_att_morning"
        )
        
        afternoon_site = st.selectbox(
            "☀️ " + t("afternoon"),
            options=site_names,
            key="dialog_add_att_afternoon"
        )
        
        evening_site = st.selectbox(
            "🌙 " + t("evening"),
            options=site_names,
            key="dialog_add_att_evening"
        )
        
        overtime_hours = st.number_input(
            t("overtime_hours"),
            min_value=0.0,
            max_value=24.0,
            step=0.5,
            value=0.0,
            format="%.1f",
            key="dialog_add_att_overtime"
        )
    
    # Absent reason dropdown (full width)
    if absent_reasons:
        reason_options = {r['reason']: r['id'] for r in absent_reasons}
        reason_names = ["-- 請選擇 --"] + list(reason_options.keys())
        selected_reason = st.selectbox(
            t("absent_reason"),
            options=reason_names,
            key="dialog_add_att_reason"
        )
    else:
        selected_reason = "-- 請選擇 --"
        reason_options = {}
    
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    
    # Right-aligned action buttons
    btn_col1, btn_col2 = st.columns([4, 1])
    with btn_col2:
        cancel_col, save_col = st.columns(2)
        
        with cancel_col:
            if st.button("❌ 取消", use_container_width=True, key="dialog_cancel_add_att"):
                st.rerun()
        
        with save_col:
            if st.button("💾 儲存", use_container_width=True, type="primary", key="dialog_save_add_att"):
                worker_id = worker_options[selected_worker]
                
                # Get site IDs (None if not selected)
                morning_site_id = site_options.get(morning_site) if morning_site != "-- 請選擇 --" else None
                afternoon_site_id = site_options.get(afternoon_site) if afternoon_site != "-- 請選擇 --" else None
                evening_site_id = site_options.get(evening_site) if evening_site != "-- 請選擇 --" else None
                
                # Get absent reason ID (None if not selected)
                absent_reason_id = reason_options.get(selected_reason) if selected_reason != "-- 請選擇 --" and reason_options else None
                
                # Check if at least one site is selected OR absent reason is filled
                if not any([morning_site_id, afternoon_site_id, evening_site_id]) and not absent_reason_id:
                    st.error("請至少選擇一個時段的工地或填寫缺勤原因")
                # Check if already exists
                elif db_manager.attendance_exists(worker_id, work_date):
                    st.error(t("attendance_exists"))
                else:
                    # Enforce OT rule: if evening_site is None, OT must be 0
                    final_overtime = float(overtime_hours) if evening_site_id is not None else 0.0
                    
                    success = db_manager.add_attendance(
                        worker_id=worker_id,
                        work_date=work_date,
                        morning_site_id=morning_site_id,
                        afternoon_site_id=afternoon_site_id,
                        evening_site_id=evening_site_id,
                        absent_reason_id=absent_reason_id,
                        overtime_hours=final_overtime
                    )
                    
                    if success:
                        st.success(t("save_success"))
                        st.rerun()
                    else:
                        st.error(t("save_failed"))


@st.dialog("✏️ 編輯考勤記錄", width="large")
def edit_attendance_dialog(attendance_id, record, workers, sites, absent_reasons):
    """Dialog for editing attendance record - wide version with two-column layout"""
    import pandas as pd
    t = lambda key: get_text(key, st.session_state.language)
    
    # Dynamic title showing worker name and date
    work_date_str = pd.to_datetime(record['work_date']).strftime('%Y-%m-%d')
    st.markdown(f'''
    <div style='padding: 10px 0; margin-bottom: 20px; border-bottom: 2px solid #e5e7eb;'>
        <h3 style='margin: 0; color: #1e293b; font-size: 20px;'>
            編輯考勤：{record['worker_name']} ({work_date_str})
        </h3>
    </div>
    ''', unsafe_allow_html=True)
    
    # Two-column layout
    form_cols = st.columns([1, 1])
    
    with form_cols[0]:
        # Left column: Date and Worker selection
        work_date = st.date_input(
            t("date"),
            value=pd.to_datetime(record['work_date']),
            key=f"dialog_edit_att_date_{attendance_id}"
        )
        
        worker_options = {w['name']: w['id'] for w in workers}
        # Find current worker index
        current_worker_idx = list(worker_options.keys()).index(record['worker_name']) if record['worker_name'] in worker_options else 0
        selected_worker = st.selectbox(
            t("worker"),
            options=list(worker_options.keys()),
            index=current_worker_idx,
            key=f"dialog_edit_att_worker_{attendance_id}"
        )
    
    with form_cols[1]:
        # Right column: Site selections and overtime
        site_options = {s['name']: s['id'] for s in sites}
        site_names = ["-- 請選擇 --"] + list(site_options.keys())
        
        # Find current site indices
        morning_idx = site_names.index(record['morning_site']) if record['morning_site'] and record['morning_site'] in site_names else 0
        afternoon_idx = site_names.index(record['afternoon_site']) if record['afternoon_site'] and record['afternoon_site'] in site_names else 0
        evening_idx = site_names.index(record['evening_site']) if record['evening_site'] and record['evening_site'] in site_names else 0
        
        morning_site = st.selectbox(
            "🌅 " + t("morning"),
            options=site_names,
            index=morning_idx,
            key=f"dialog_edit_att_morning_{attendance_id}"
        )
        
        afternoon_site = st.selectbox(
            "☀️ " + t("afternoon"),
            options=site_names,
            index=afternoon_idx,
            key=f"dialog_edit_att_afternoon_{attendance_id}"
        )
        
        evening_site = st.selectbox(
            "🌙 " + t("evening"),
            options=site_names,
            index=evening_idx,
            key=f"dialog_edit_att_evening_{attendance_id}"
        )
        
        overtime_hours = st.number_input(
            t("overtime_hours"),
            min_value=0.0,
            max_value=24.0,
            step=0.5,
            value=float(record['overtime_hours']) if record['overtime_hours'] else 0.0,
            format="%.1f",
            key=f"dialog_edit_att_overtime_{attendance_id}"
        )
    
    # Absent reason dropdown (full width)
    if absent_reasons:
        reason_options = {r['reason']: r['id'] for r in absent_reasons}
        reason_names = ["-- 請選擇 --"] + list(reason_options.keys())
        # Find current reason index
        current_reason_idx = reason_names.index(record['absent_reason']) if record['absent_reason'] and record['absent_reason'] in reason_names else 0
        selected_reason = st.selectbox(
            t("absent_reason"),
            options=reason_names,
            index=current_reason_idx,
            key=f"dialog_edit_att_reason_{attendance_id}"
        )
    else:
        selected_reason = "-- 請選擇 --"
        reason_options = {}
    
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    
    # Right-aligned action buttons
    btn_col1, btn_col2 = st.columns([4, 1])
    with btn_col2:
        cancel_col, save_col = st.columns(2)
        
        with cancel_col:
            if st.button("❌ 取消", use_container_width=True, key=f"dialog_cancel_edit_att_{attendance_id}"):
                st.rerun()
        
        with save_col:
            if st.button("💾 儲存", use_container_width=True, type="primary", key=f"dialog_save_edit_att_{attendance_id}"):
                worker_id = worker_options[selected_worker]
                
                # Get site IDs (None if not selected)
                morning_site_id = site_options.get(morning_site) if morning_site != "-- 請選擇 --" else None
                afternoon_site_id = site_options.get(afternoon_site) if afternoon_site != "-- 請選擇 --" else None
                evening_site_id = site_options.get(evening_site) if evening_site != "-- 請選擇 --" else None
                
                # Get absent reason ID (None if not selected)
                absent_reason_id = reason_options.get(selected_reason) if selected_reason != "-- 請選擇 --" and reason_options else None
                
                # Check if at least one site is selected OR absent reason is filled
                if not any([morning_site_id, afternoon_site_id, evening_site_id]) and not absent_reason_id:
                    st.error("請至少選擇一個時段的工地或填寫缺勤原因")
                else:
                    # Enforce OT rule: if evening_site is None, OT must be 0
                    final_overtime = float(overtime_hours) if evening_site_id is not None else 0.0
                    
                    success = db_manager.update_attendance(
                        attendance_id=attendance_id,
                        work_date=work_date,
                        morning_site_id=morning_site_id,
                        afternoon_site_id=afternoon_site_id,
                        evening_site_id=evening_site_id,
                        absent_reason_id=absent_reason_id,
                        overtime_hours=final_overtime
                    )
                    
                    if success:
                        st.success(t("update_success"))
                        st.rerun()
                    else:
                        st.error(t("update_failed"))


def import_attendance_dialog_content(workers, sites, absent_reasons):
    """Content for import popover - two-column layout with instructions and upload"""
    t = lambda key: get_text(key, st.session_state.language)
    import pandas as pd
    from io import BytesIO
    
    st.markdown('''
    <div style='padding: 10px 0; margin-bottom: 15px; border-bottom: 2px solid #e5e7eb;'>
        <h3 style='margin: 0; color: #1e293b; font-size: 18px;'>
            📥 批量導入考勤記錄
        </h3>
    </div>
    ''', unsafe_allow_html=True)
    
    # Two-column layout: Left (Instructions & Template) | Right (Upload)
    import_cols = st.columns([2, 3])
    
    with import_cols[0]:
        st.markdown('''
        <div style='padding: 15px; background: linear-gradient(135deg, #f0fdfa 0%, #ccfbf1 100%); 
                    border-radius: 10px; border: 2px solid #14b8a6;'>
            <p style='margin: 0 0 10px 0; color: #0f766e; font-weight: 600; font-size: 14px;'>
                📄 操作指南與模板下載
            </p>
            <p style='margin: 0; color: #115e59; font-size: 12px; line-height: 1.5;'>
                1. 下載Excel模板<br>
                2. 填寫考勤數據<br>
                3. 上傳文件導入
            </p>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
        
        if st.button(t("download_template"), use_container_width=True, key="import_dl_att_template"):
            template_df = pd.DataFrame({
                'date': ['2024-01-15', '2024-01-15', '2024-01-16'],
                'worker_name': ['John Doe', 'Jane Smith', 'John Doe'],
                'morning_site': ['Site A', 'Site B', 'Site A'],
                'afternoon_site': ['Site A', 'Site B', 'Site C'],
                'evening_site': ['', 'Site B', ''],
                'overtime_hours': [0.0, 2.0, 0.0],
                'absent_reason': ['', '', 'Sick Leave']
            })
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                template_df.to_excel(writer, index=False, sheet_name='Attendance')
            
            st.download_button(
                label="📥 Download",
                data=output.getvalue(),
                file_name="attendance_template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                key="import_dl_att_file"
            )
    
    with import_cols[1]:
        st.markdown('''
        <div style='padding: 15px; background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                    border-radius: 10px; border: 2px solid #f59e0b;'>
            <p style='margin: 0 0 10px 0; color: #b45309; font-weight: 600; font-size: 14px;'>
                📤 文件上傳器
            </p>
            <p style='margin: 0; color: #92400e; font-size: 12px; line-height: 1.5;'>
                支持 .xlsx / .xls 格式<br>
                拖拽或點擊上傳
            </p>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
        
        # Upload file
        uploaded_file = st.file_uploader(
            "拖拽 Excel 到此",
            type=['xlsx', 'xls'],
            label_visibility="collapsed",
            key="import_att_upload"
        )
        
        if uploaded_file is not None:
            if st.button("✅ 開始導入", use_container_width=True, type="primary", key="import_att_start_btn"):
                try:
                    # Read Excel file
                    upload_df = pd.read_excel(uploaded_file)
                    
                    # Check required columns
                    required_cols = ['date', 'worker_name']
                    if not all(col in upload_df.columns for col in required_cols):
                        st.error(f"Excel格式無效。必須包含以下列: {', '.join(required_cols)}")
                    else:
                        # Build lookups
                        worker_lookup = {w['name']: w['id'] for w in workers}
                        site_lookup = {s['name']: s['id'] for s in sites}
                        reason_lookup = {r['reason']: r['id'] for r in absent_reasons} if absent_reasons else {}
                        
                        imported_count = 0
                        duplicate_count = 0
                        failed_count = 0
                        
                        for _, row in upload_df.iterrows():
                            try:
                                # Parse date
                                work_date = pd.to_datetime(row['date']).date()
                                
                                # Get worker ID
                                worker_name = str(row['worker_name']).strip()
                                if worker_name not in worker_lookup:
                                    failed_count += 1
                                    continue
                                
                                worker_id = worker_lookup[worker_name]
                                
                                # Check if already exists
                                if db_manager.attendance_exists(worker_id, work_date):
                                    duplicate_count += 1
                                    continue
                                
                                # Get site IDs
                                morning_site = str(row.get('morning_site', '')).strip() if pd.notna(row.get('morning_site')) else ''
                                afternoon_site = str(row.get('afternoon_site', '')).strip() if pd.notna(row.get('afternoon_site')) else ''
                                evening_site = str(row.get('evening_site', '')).strip() if pd.notna(row.get('evening_site')) else ''
                                
                                morning_site_id = site_lookup.get(morning_site) if morning_site else None
                                afternoon_site_id = site_lookup.get(afternoon_site) if afternoon_site else None
                                evening_site_id = site_lookup.get(evening_site) if evening_site else None
                                
                                # Get absent reason ID
                                absent_reason = str(row.get('absent_reason', '')).strip() if pd.notna(row.get('absent_reason')) else ''
                                absent_reason_id = reason_lookup.get(absent_reason) if absent_reason and absent_reason in reason_lookup else None
                                
                                # Check if at least one site is selected OR absent reason is filled
                                if not any([morning_site_id, afternoon_site_id, evening_site_id]) and not absent_reason_id:
                                    failed_count += 1
                                    continue
                                
                                # Get overtime hours
                                overtime_hours = float(row.get('overtime_hours', 0.0)) if pd.notna(row.get('overtime_hours')) else 0.0
                                # Enforce OT rule
                                if evening_site_id is None:
                                    overtime_hours = 0.0
                                
                                # Add attendance record
                                success = db_manager.add_attendance(
                                    worker_id=worker_id,
                                    work_date=work_date,
                                    morning_site_id=morning_site_id,
                                    afternoon_site_id=afternoon_site_id,
                                    evening_site_id=evening_site_id,
                                    absent_reason_id=absent_reason_id,
                                    overtime_hours=overtime_hours
                                )
                                
                                if success:
                                    imported_count += 1
                                else:
                                    failed_count += 1
                            except Exception:
                                failed_count += 1
                        
                        if imported_count > 0:
                            st.toast(f"✅ {t('import_success').format(imported_count)}", icon="🎉")
                            st.rerun()
                        elif duplicate_count > 0:
                            st.warning(t("duplicate_skipped").format(duplicate_count))
                            st.rerun()
                        elif failed_count > 0:
                            st.error("所有考勤記錄導入失敗，請檢查文件格式和數據有效性")
                
                except Exception as e:
                    st.error(t("import_failed").format(str(e)))

# ==================== Worker Statistics Dashboard ====================
def worker_stats_page():
    """Worker statistics dashboard with visual calendar view"""
    t = lambda key: get_text(key, st.session_state.language)
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown(f'<h1>{t("worker_stats_title")}</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Legend
    st.markdown(f"""
    <div style="margin-bottom: 20px; padding: 15px; background: white; border-radius: 8px;">
        <h4 style="margin-top: 0;">{t("attendance_status_legend")}</h4>
        <div style="display: flex; gap: 30px; align-items: center;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="display: inline-block; width: 16px; height: 16px; background: #10b981; border-radius: 50%;"></span>
                <span>{t("worked_on_site")}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="display: inline-block; width: 16px; height: 16px; background: #ef4444; border-radius: 50%;"></span>
                <span>{t("absent_no_reason")}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="display: inline-block; width: 16px; height: 16px; background: #f59e0b; border-radius: 50%;"></span>
                <span>{t("absent_with_reason")}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="display: inline-block; width: 16px; height: 16px; background: #e5e7eb; border-radius: 50%;"></span>
                <span>{t("no_record")}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Filter section
    st.markdown(f"### {t('filters')}")
    col1, col2, col3, col4 = st.columns(4)
    
    # Date range filters (default to last 10 days)
    from datetime import date, timedelta
    today = date.today()
    default_start = today - timedelta(days=9)
    
    with col1:
        start_date = st.date_input(t("start_date"), value=default_start)
    
    with col2:
        end_date = st.date_input(t("end_date"), value=today)
    
    # Company filter (multi-select)
    companies = db_manager.get_all_companies()
    company_names = [c['name'] for c in companies]
    
    with col3:
        selected_companies = st.multiselect(
            t("filter_by_company"),
            options=company_names,
            default=[],
            help=t("select_companies_help")
        )
    
    # Worker filter (multi-select)
    workers = db_manager.get_all_workers()
    worker_names = [w['name'] for w in workers]
    
    with col4:
        selected_workers = st.multiselect(
            t("filter_by_worker"),
            options=worker_names,
            default=[],
            help=t("select_workers_help")
        )
    
    # Get filter values - convert names to IDs
    company_ids = []
    if selected_companies:
        company_dict = {c['name']: c['id'] for c in companies}
        company_ids = [company_dict[name] for name in selected_companies]
    
    worker_ids = []
    if selected_workers:
        worker_dict = {w['name']: w['id'] for w in workers}
        worker_ids = [worker_dict[name] for name in selected_workers]
    
    # Get attendance calendar data
    calendar_data = db_manager.get_worker_attendance_calendar(
        start_date=start_date,
        end_date=end_date,
        company_ids=company_ids if company_ids else None,
        worker_ids=worker_ids if worker_ids else None
    )
    
    if not calendar_data:
        st.info(t("no_attendance_records"))
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Organize data by worker and date
    from collections import defaultdict
    worker_dates = defaultdict(dict)
    worker_info = {}
    
    for record in calendar_data:
        wid = record['worker_id']
        wname = record['worker_name']
        cname = record['company_name']
        work_date = record['work_date']
        
        worker_info[wid] = {'name': wname, 'company': cname}
        
        if work_date:  # If there's an attendance record
            # Determine status
            has_site = any([
                record['morning_site_id'],
                record['afternoon_site_id'],
                record['evening_site_id']
            ])
            
            if has_site:
                status = 'worked'  # Green
            elif record['absent_reason_db_id'] == 7:  # "No Reason"
                status = 'no_reason'  # Red
            elif record['absent_reason_id']:
                status = 'with_reason'  # Yellow
            else:
                status = 'no_record'  # Gray
            
            worker_dates[wid][work_date] = status
    
    # Generate all dates in range
    all_dates = []
    current_date = start_date
    while current_date <= end_date:
        all_dates.append(current_date.isoformat())
        current_date += timedelta(days=1)
    
    # Build table data
    table_data = []
    for wid in sorted(worker_info.keys()):
        info = worker_info[wid]
        row = {
            'Company': info['company'],
            'Worker Name': info['name']
        }
        
        # Add status for each date
        for d in all_dates:
            status = worker_dates[wid].get(d, 'no_record')
            row[d] = status
        
        table_data.append(row)
    
    # Create DataFrame
    import pandas as pd
    df = pd.DataFrame(table_data)
    
    # Function to render colored circles
    def status_circle(status):
        colors = {
            'worked': '#10b981',      # Green
            'no_reason': '#ef4444',   # Red
            'with_reason': '#f59e0b', # Yellow
            'no_record': '#e5e7eb'    # Gray
        }
        color = colors.get(status, '#e5e7eb')
        return f'<div style="width: 16px; height: 16px; background: {color}; border-radius: 50%; margin: 0 auto;"></div>'
    
    # Display with styled HTML
    st.markdown(f"### {t('attendance_calendar')}")
    
    # Create HTML table with responsive container
    html_table = '''
    <div style="overflow-x: auto; width: 100%; margin-top: 10px; position: relative;">
        <table style="border-collapse: collapse; width: 100%; font-size: 12px; min-width: 800px; position: relative;">
    '''
    
    # Header row with darker background
    html_table += '<thead><tr style="background: #374151; color: white;">'
    html_table += '<th style="padding: 10px 8px; border: 1px solid #4b5563; text-align: left; position: sticky; left: 0; background: #374151; z-index: 20; font-weight: 600; min-width: 150px;">Company</th>'
    html_table += '<th style="padding: 10px 8px; border: 1px solid #4b5563; text-align: left; position: sticky; left: 150px; background: #374151; z-index: 20; font-weight: 600; min-width: 150px;">Worker</th>'
    
    for d in all_dates:
        date_obj = date.fromisoformat(d)
        display_date = date_obj.strftime('%m/%d')
        day_name = date_obj.strftime('%a')
        html_table += f'<th style="padding: 10px 6px; border: 1px solid #4b5563; text-align: center; min-width: 45px; font-weight: 600; position: relative;">{display_date}<br><small style="font-weight: normal;">{day_name}</small></th>'
    
    html_table += '</tr></thead>'
    
    # Data rows
    html_table += '<tbody>'
    for idx, row in df.iterrows():
        bg_color = '#ffffff' if idx % 2 == 0 else '#f9fafb'
        html_table += f'<tr style="background: {bg_color};">'
        
        # Company column
        html_table += f'<td style="padding: 8px; border: 1px solid #d1d5db; position: sticky; left: 0; background: {bg_color}; z-index: 15; min-width: 150px;">{row["Company"]}</td>'
        
        # Worker name column
        html_table += f'<td style="padding: 8px; border: 1px solid #d1d5db; position: sticky; left: 150px; background: {bg_color}; z-index: 15; font-weight: 500; min-width: 150px;">{row["Worker Name"]}</td>'
        
        # Date columns
        for d in all_dates:
            status = row[d]
            circle_html = status_circle(status)
            html_table += f'<td style="padding: 8px 6px; border: 1px solid #d1d5db; text-align: center; position: relative; z-index: 1;">{circle_html}</td>'
        
        html_table += '</tr>'
    
    html_table += '</tbody></table></div>'
    
    st.markdown(html_table, unsafe_allow_html=True)
    
    # Summary statistics
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown(f"### {t('summary_statistics')}")
    
    total_worked = sum(1 for row in table_data for d in all_dates if row[d] == 'worked')
    total_no_reason = sum(1 for row in table_data for d in all_dates if row[d] == 'no_reason')
    total_with_reason = sum(1 for row in table_data for d in all_dates if row[d] == 'with_reason')
    total_no_record = sum(1 for row in table_data for d in all_dates if row[d] == 'no_record')
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(t("days_worked"), total_worked)
    with col2:
        st.metric(t("absent_no_reason_count"), total_no_reason)
    with col3:
        st.metric(t("absent_with_reason_count"), total_with_reason)
    with col4:
        st.metric(t("no_record_count"), total_no_record)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== Site Statistics Dashboard ====================
def site_stats_page():
    """Site statistics dashboard with pivot table view"""
    t = lambda key: get_text(key, st.session_state.language)
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown(f'<h1>{t("site_stats_title")}</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Filter section
    st.markdown(f"### {t('filters')}")
    col1, col2, col3 = st.columns(3)
    
    # Date range filters (default to last 10 days)
    from datetime import date, timedelta
    today = date.today()
    default_start = today - timedelta(days=9)
    
    with col1:
        start_date = st.date_input(t("start_date"), value=default_start)
    
    with col2:
        end_date = st.date_input(t("end_date"), value=today)
    
    # Site multi-select filter
    all_sites_list = db_manager.get_all_sites()
    site_options = {site['name']: site['id'] for site in all_sites_list}
    
    with col3:
        selected_sites = st.multiselect(
            t("filter_by_site"),
            options=list(site_options.keys()),
            default=[],
            help=t("select_sites_help")
        )
    
    # Get all sites
    sites = db_manager.get_all_sites()
    if not sites:
        st.info("No sites available. Please add sites first.")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Get attendance data for the date range
    conn = db_manager._get_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT 
            s.id as site_id,
            s.name as site_name,
            a.work_date,
            (
                COUNT(CASE WHEN a.morning_site_id = s.id THEN 1 END) * 0.5 +
                COUNT(CASE WHEN a.afternoon_site_id = s.id THEN 1 END) * 0.5 +
                COALESCE(SUM(CASE WHEN a.evening_site_id = s.id THEN a.overtime_hours ELSE 0 END), 0)
            ) as total_worker_days
        FROM attendance a
        CROSS JOIN sites s
        WHERE a.work_date >= ? AND a.work_date <= ?
          AND (a.morning_site_id = s.id OR a.afternoon_site_id = s.id OR a.evening_site_id = s.id)
    '''
    
    params = [start_date.isoformat(), end_date.isoformat()]
    
    # Add site filter if sites are selected
    if selected_sites and len(selected_sites) > 0:
        selected_site_ids = [site_options[site_name] for site_name in selected_sites]
        placeholders = ','.join(['?' for _ in selected_site_ids])
        query += f' AND s.id IN ({placeholders})'
        params.extend(selected_site_ids)
    
    query += ' GROUP BY s.id, s.name, a.work_date ORDER BY a.work_date DESC, s.name'
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    if not rows:
        st.info("No attendance records found for the selected date range.")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Organize data by date and site
    from collections import defaultdict
    date_site_data = defaultdict(lambda: defaultdict(float))
    all_dates = set()
    all_sites = {}
    
    for row in rows:
        site_id = row['site_id']
        site_name = row['site_name']
        work_date = row['work_date']
        worker_days = row['total_worker_days']
        
        all_dates.add(work_date)
        all_sites[site_id] = site_name
        date_site_data[work_date][site_name] = worker_days
    
    # Sort dates
    sorted_dates = sorted(all_dates, reverse=True)
    sorted_site_names = sorted(all_sites.values())
    
    # Create pivot table data (sites as rows, dates as columns)
    table_data = []
    for site_name in sorted_site_names:
        row = {'Site': site_name}
        for d in sorted_dates:
            row[d] = date_site_data[d].get(site_name, 0.0)
        table_data.append(row)
    
    # Add total row (sum across all sites for each date)
    total_row = {'Site': 'Total'}
    for d in sorted_dates:
        total_row[d] = round(sum(date_site_data[d].get(site_name, 0.0) for site_name in sorted_site_names), 2)
    table_data.append(total_row)
    
    # Create DataFrame
    import pandas as pd
    df = pd.DataFrame(table_data)
    
    # Display table with custom styling for Total row
    st.markdown("### 📊 Site Worker Days by Date")
    
    # Create styled HTML table
    html_table = '<div style="overflow-x: auto; width: 100%; margin-top: 10px;">'
    html_table += '<table style="border-collapse: collapse; width: 100%; font-size: 13px;">'
    
    # Header row
    html_table += '<thead><tr style="background: #374151; color: white;">'
    for col in df.columns:
        html_table += f'<th style="padding: 10px 8px; border: 1px solid #4b5563; text-align: center; position: sticky; left: 0; background: #374151; z-index: 10; font-weight: 600;">{col}</th>'
    html_table += '</tr></thead>'
    
    # Data rows
    html_table += '<tbody>'
    for idx, row in df.iterrows():
        is_total_row = row['Site'] == 'Total'
        bg_color = '#e5e7eb' if is_total_row else ('#ffffff' if idx % 2 == 0 else '#f9fafb')
        font_weight = 'bold' if is_total_row else 'normal'
        text_color = '#111827' if is_total_row else '#374151'
        
        html_table += f'<tr style="background: {bg_color};">'
        
        # Site column (sticky)
        html_table += f'<td style="padding: 8px; border: 1px solid #d1d5db; position: sticky; left: 0; background: {bg_color}; z-index: 5; font-weight: {font_weight}; color: {text_color}; min-width: 150px;">{row["Site"]}</td>'
        
        # Date columns
        for d in sorted_dates:
            value = row[d]
            cell_style = f'padding: 8px 6px; border: 1px solid #d1d5db; text-align: center; font-weight: {font_weight}; color: {text_color};'
            html_table += f'<td style="{cell_style}">{value:.2f}</td>'
        
        html_table += '</tr>'
    
    html_table += '</tbody></table></div>'
    
    st.markdown(html_table, unsafe_allow_html=True)
    
    # Summary statistics
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### 📈 Summary by Site")
    
    # Calculate totals for each site
    summary_data = []
    for site_name in sorted_site_names:
        total_days = sum(date_site_data[d].get(site_name, 0.0) for d in sorted_dates)
        summary_data.append({'Site': site_name, 'Total Worker Days': round(total_days, 2)})
    
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True,
        height=300
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== Individual Worker Stats Page ====================
def individual_worker_stats_page():
    """Individual worker attendance records page"""
    import sqlite3
    t = lambda key: get_text(key, st.session_state.language)
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown(f'<h1>{t("individual_worker_stats_title")}</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Filter section
    st.markdown(f"### {t('filters')}")
    col1, col2, col3 = st.columns(3)
    
    # Date range filters (default to last 10 days)
    from datetime import date, timedelta
    today = date.today()
    default_start = today - timedelta(days=9)
    
    with col1:
        start_date = st.date_input(t("start_date"), value=default_start)
    
    with col2:
        end_date = st.date_input(t("end_date"), value=today)
    
    # Worker filter (single select)
    workers = db_manager.get_all_workers()
    if not workers:
        st.info(t("no_workers"))
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    worker_options = {w['name']: w['id'] for w in workers}
    
    with col3:
        selected_worker_name = st.selectbox(
            t("filter_by_worker"),
            options=list(worker_options.keys()),
            index=None,
            placeholder=t("select_worker_placeholder")
        )
    
    # Only show data if a worker is selected
    if not selected_worker_name:
        st.info(t("please_select_worker"))
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Get selected worker ID
    worker_id = worker_options[selected_worker_name]
    
    # Get attendance records for the selected worker and date range
    conn = db_manager._get_connection()
    conn.row_factory = sqlite3.Row  # Enable dictionary-like access
    cursor = conn.cursor()
    
    query = '''
        SELECT 
            a.id,
            w.name as worker_name,
            c.name as company_name,
            ms.name as morning_site,
            afs.name as afternoon_site,
            es.name as evening_site,
            ar.reason as absent_reason,
            a.work_date,
            a.overtime_hours
        FROM attendance a
        JOIN workers w ON a.worker_id = w.id
        LEFT JOIN companies c ON w.company_id = c.id
        LEFT JOIN sites ms ON a.morning_site_id = ms.id
        LEFT JOIN sites afs ON a.afternoon_site_id = afs.id
        LEFT JOIN sites es ON a.evening_site_id = es.id
        LEFT JOIN absent_reasons ar ON a.absent_reason_id = ar.id
        WHERE a.worker_id = ? AND a.work_date >= ? AND a.work_date <= ?
        ORDER BY a.work_date DESC
    '''
    
    cursor.execute(query, [worker_id, start_date.isoformat(), end_date.isoformat()])
    rows = cursor.fetchall()
    
    if not rows:
        st.info(t("no_attendance_records"))
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Display attendance records table
    st.markdown(f"### {t('attendance_records_table')}")
    
    import pandas as pd
    
    # Convert Row objects to dictionaries for DataFrame
    df = pd.DataFrame([dict(row) for row in rows])
    
    # Format date before renaming columns
    df['work_date'] = pd.to_datetime(df['work_date']).dt.strftime('%Y-%m-%d')
    
    # Rename columns after formatting
    df.columns = [t("col_id"), t("col_worker_name"), t("col_company_name"), 
                  "上午工地", "下午工地", "晚上工地", t("col_absent_reason"), t("col_work_date"), t("col_overtime")]
    
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        height=500
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== Main Entry Point ====================
def main():
    """Main entry point"""
    # Display language selector at top
    language_selector()
    
    page = sidebar_menu()
    
    # Page routing
    if page == "home":
        home_page()
    elif page == "companies":
        companies_page()
    elif page == "absent_reasons":
        absent_reasons_page()
    elif page == "workers":
        workers_page()
    elif page == "sites":
        sites_page()
    elif page == "attendance":
        attendance_page()
    elif page == "worker_stats":
        worker_stats_page()
    elif page == "site_stats":
        site_stats_page()
    elif page == "individual_worker_stats":
        individual_worker_stats_page()

if __name__ == "__main__":
    main()
