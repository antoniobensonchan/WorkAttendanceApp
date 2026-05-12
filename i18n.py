"""
Multi-language support module
Supports: English, Simplified Chinese, Traditional Chinese
"""

# Language dictionary
LANGUAGES = {
    "en": {
        # System
        "system_title": "Work Attendance Management System",
        "sidebar_title": "📋 Attendance System",
        
        # Navigation
        "nav_home": "🏠 Home",
        "nav_companies": "🏢 Companies",
        "nav_absent_reasons": "⚠️ Absent Reasons",
        "nav_workers": "👥 Workers",
        "nav_sites": "🏗️ Sites",
        "nav_attendance": "📝 Attendance",
        "nav_worker_stats": "📊 Worker Stats",
        "nav_site_stats": "📈 Site Stats",
        "nav_individual_worker_stats": "👤 Individual Worker Stats",
        
        # Companies Page
        "companies_title": "Companies Management",
        "add_company": "➕ Add Company",
        "import_companies": "📥 Import Companies from Excel",
        "company_name": "Company Name",
        "enter_company_name": "Enter company name",
        "companies_list": "Companies List",
        "no_companies": "No companies yet, please add companies first",
        "download_template": "📄 Download Excel Template",
        "upload_excel": "Upload Excel File",
        "import_success": "✅ Successfully imported {} companies",
        "import_failed": "❌ Import failed: {}",
        "invalid_format": "Invalid Excel format. Please use the template.",
        "duplicate_skipped": "⚠️ Skipped {} duplicate companies",
        "edit_company": "✏️ Edit",
        "delete_company": "🗑️ Delete",
        "update_company": "Update Company",
        "confirm_delete": "Are you sure you want to delete this company?",
        "delete_success": "✅ Company deleted successfully",
        "delete_failed": "❌ Delete failed: {}",
        "update_success": "✅ Company updated successfully",
        "update_failed": "❌ Update failed",
        "has_workers_warning": "Cannot delete: This company has {} worker(s) associated with it. Please reassign or delete workers first.",
        
        # Absent Reasons Page
        "absent_reasons_title": "Absent Reasons Management",
        "add_absent_reason": "➕ Add Absent Reason",
        "absent_reason_name": "Reason Name",
        "enter_absent_reason": "Enter absent reason",
        "absent_reasons_list": "Absent Reasons List",
        "no_absent_reasons": "No absent reasons yet, please add reasons first",
        "reason_exists": "This reason already exists, please do not add duplicates",
        
        # Home Page
        "home_title": "Welcome to Work Attendance System",
        "home_subtitle": "Modern Design · LAN Multi-user · Offline Operation",
        "total_workers": "👥 Total Workers",
        "total_sites": "🏗️ Total Sites",
        "total_records": "📊 Attendance Records",
        "data_backup": "💾 Data Backup",
        "attendance_trend": "📈 30-Day Attendance Trend",
        "site_distribution": "🏗️ Site Distribution",
        "weekly_pattern": "🗓️ Weekly Pattern",
        
        # Workers Page
        "workers_title": "Workers Management",
        "add_worker": "➕ Add Worker",
        "worker_name": "Worker Name",
        "company": "Company",
        "enter_worker_name": "Enter worker name",
        "enter_company": "Enter company name",
        "save": "Save",
        "workers_list": "Workers List",
        "no_workers": "No workers yet, please add workers first",
        
        # Sites Page
        "sites_title": "Sites Management",
        "add_site": "➕ Add Site",
        "site_name": "Site Name",
        "enter_site_name": "Enter site name",
        "sites_list": "Sites List",
        "no_sites": "No sites yet, please add sites first",
        
        # Attendance Page
        "attendance_title": "Attendance Recording",
        "add_attendance": "📝 New Attendance Record",
        "date": "Date",
        "worker": "Worker",
        "site": "Site",
        "absent_reason": "Absent Reason",
        "attendance_status": "Attendance Status",
        "morning": "Morning",
        "afternoon": "Afternoon",
        "evening": "Evening",
        "overtime_hours": "Overtime Hours",
        "submit": "Submit",
        "attendance_list": "Attendance Records",
        "no_attendance": "No attendance records yet",
        "please_add_workers": "Please add workers first",
        "please_add_sites": "Please add sites first",
        
        # Validation Messages
        "fill_all_fields": "Please fill in all fields",
        "worker_exists": "Worker already exists, please do not add duplicates",
        "site_exists": "Site already exists, please do not add duplicates",
        "attendance_exists": "⚠️ This worker already has attendance record for this date",
        "save_success": "✅ Saved successfully",
        "save_failed": "Save failed",
        "fill_site_name": "Please enter site name",
        
        # Statistics
        "worker_stats_title": "Worker Statistics Dashboard",
        "site_stats_title": "Site Statistics Dashboard",
        "individual_worker_stats_title": "Individual Worker Stats",
        "no_stats": "No statistics data yet",
        
        # Table Headers - Workers
        "col_id": "ID",
        "col_name": "Name",
        "col_company": "Company",
        
        # Table Headers - Attendance
        "col_worker_name": "Worker Name",
        "col_site_name": "Site Name",
        "col_absent_reason": "Absent Reason",
        "col_work_date": "Date",
        "col_morning": "Morning",
        "col_afternoon": "Afternoon",
        "col_evening": "Evening",
        "col_overtime": "Overtime (hrs)",
        
        # Table Headers - Statistics
        "col_total_att_days": "Total Attendance Days",
        "col_total_abs_days": "Total Absent Days",
        "col_total_slots": "Total Attendance Slots",
        "col_total_overtime": "Total Overtime Hours",
        
        # Site Stats Filters
        "filter_site": "Filter by Site",
        "all_sites": "All Sites",
        "start_date": "Start Date",
        "end_date": "End Date",
        
        # Table Headers - Site Stats
        "col_worker_count": "Worker Count",
        "col_total_att_hours": "Total Attendance Hours",
        "col_total_ot_hours": "Total Overtime Hours",
        "total_worker_days": "Total Worker Days",
        
        # Company column
        "col_company_name": "Company",
        
        # Worker Stats Dashboard
        "attendance_status_legend": "📊 Attendance Status Legend",
        "worked_on_site": "Worked on site (Green)",
        "absent_no_reason": "Absent - No Reason (Red)",
        "absent_with_reason": "Absent - With Reason (Yellow)",
        "no_record": "No Record (Gray)",
        "filters": "🔍 Filters",
        "filter_by_company": "Filter by Company",
        "filter_by_worker": "Filter by Worker",
        "filter_by_site": "Filter by Site",
        "select_companies_help": "Select one or more companies (leave empty for all)",
        "select_workers_help": "Select one or more workers (leave empty for all)",
        "select_sites_help": "Select one or more sites (leave empty for all)",
        "select_worker_placeholder": "-- Select a worker --",
        "please_select_worker": "Please select a worker to view attendance records.",
        "attendance_records_table": "📋 Attendance Records",
        "attendance_calendar": "📅 Attendance Calendar",
        "summary_statistics": "📈 Summary Statistics",
        "days_worked": "Days Worked",
        "absent_no_reason_count": "Absent (No Reason)",
        "absent_with_reason_count": "Absent (With Reason)",
        "no_record_count": "No Record",
        "no_attendance_records": "No attendance records found for the selected filters.",
    },
    
    "zh_cn": {
        # System
        "system_title": "工地考勤管理系统",
        "sidebar_title": "📋 考勤系统",
        
        # Navigation
        "nav_home": "🏠 首页",
        "nav_companies": "🏢 公司管理",
        "nav_absent_reasons": "⚠️ 缺勤原因",
        "nav_workers": "👥 员工管理",
        "nav_sites": "🏗️ 工地管理",
        "nav_attendance": "📝 考勤记录",
        "nav_worker_stats": "📊 员工统计看板",
        "nav_site_stats": "📈 工地统计看板",
        "nav_individual_worker_stats": "👤 个人员工统计",
        
        # Companies Page
        "companies_title": "公司管理",
        "add_company": "➕ 新增公司",
        "import_companies": "📥 从 Excel导入公司",
        "company_name": "公司名称",
        "enter_company_name": "请输入公司名称",
        "companies_list": "公司列表",
        "no_companies": "暂无公司数据，请先添加公司",
        "download_template": "📄 下载Excel模板",
        "upload_excel": "上传Excel文件",
        "import_success": "✅ 成功导入 {} 家公司",
        "import_failed": "❌ 导入失败：{}",
        "invalid_format": "Excel格式无效。请使用模板。",
        "duplicate_skipped": "⚠️ 跳过 {} 家重复公司",
        "edit_company": "✏️ 编辑",
        "delete_company": "🗑️ 删除",
        "update_company": "更新公司",
        "confirm_delete": "确定要删除这家公司吗？",
        "delete_success": "✅ 公司删除成功",
        "delete_failed": "❌ 删除失败：{}",
        "update_success": "✅ 公司更新成功",
        "update_failed": "❌ 更新失败",
        "has_workers_warning": "无法删除：该公司有 {} 名员工关联。请先重新分配或删除员工。",
        
        # Absent Reasons Page
        "absent_reasons_title": "缺勤原因管理",
        "add_absent_reason": "➕ 新增缺勤原因",
        "absent_reason_name": "原因名称",
        "enter_absent_reason": "请输入缺勤原因",
        "absent_reasons_list": "缺勤原因列表",
        "no_absent_reasons": "暂无缺勤原因，请先添加原因",
        "reason_exists": "该原因已存在，请勿重复添加",
        
        # Home Page
        "home_title": "欢迎使用工地考勤管理系统",
        "home_subtitle": "现代设计 · 局域网多人共享 · 纯本地离线运行",
        "total_workers": "👥 员工总数",
        "total_sites": "🏗️ 工地总数",
        "total_records": "📊 考勤记录",
        "data_backup": "💾 数据备份",
        "attendance_trend": "📈 最近30日出勤趋势",
        "site_distribution": "🏗️ 各工地人数分布",
        "weekly_pattern": "🗓️ 每周出勤模式",
        
        # Workers Page
        "workers_title": "员工管理",
        "add_worker": "➕ 新增员工",
        "worker_name": "员工姓名",
        "company": "所属公司",
        "enter_worker_name": "请输入员工姓名",
        "enter_company": "请输入所属公司",
        "save": "保存",
        "workers_list": "员工列表",
        "no_workers": "暂无员工数据，请先添加员工",
        
        # Sites Page
        "sites_title": "工地管理",
        "add_site": "➕ 添加工地",
        "site_name": "工地名称",
        "enter_site_name": "请输入工地名称",
        "sites_list": "工地列表",
        "no_sites": "暂无工地数据，请先添加工地",
        
        # Attendance Page
        "attendance_title": "考勤记录",
        "add_attendance": "📝 新增考勤记录",
        "date": "日期",
        "worker": "员工",
        "site": "工地",
        "absent_reason": "缺勤原因",
        "attendance_status": "出勤情况",
        "morning": "上午出勤",
        "afternoon": "下午出勤",
        "evening": "晚上出勤",
        "overtime_hours": "加班小时数",
        "submit": "提交",
        "attendance_list": "考勤记录列表",
        "no_attendance": "暂无考勤记录",
        "please_add_workers": "请先添加员工",
        "please_add_sites": "请先添加工地",
        
        # Validation Messages
        "fill_all_fields": "请填写所有字段",
        "worker_exists": "该员工已存在，请勿重复添加",
        "site_exists": "该工地已存在，请勿重复添加",
        "attendance_exists": "⚠️ 该员工在此日期已有考勤记录，请勿重复提交",
        "save_success": "✅ 保存成功",
        "save_failed": "保存失败",
        "fill_site_name": "请填写工地名称",
        
        # Statistics
        "worker_stats_title": "员工统计看板",
        "site_stats_title": "工地统计看板",
        "individual_worker_stats_title": "个人员工统计",
        "no_stats": "暂无统计数据",
        
        # Table Headers - Workers
        "col_id": "ID",
        "col_name": "姓名",
        "col_company": "所属公司",
        
        # Table Headers - Attendance
        "col_worker_name": "员工姓名",
        "col_site_name": "工地名称",
        "col_absent_reason": "缺勤原因",
        "col_work_date": "日期",
        "col_morning": "上午",
        "col_afternoon": "下午",
        "col_evening": "晚上",
        "col_overtime": "加班小时",
        
        # Table Headers - Statistics
        "col_total_att_days": "总出勤天数",
        "col_total_abs_days": "总缺勤天数",
        "col_total_slots": "总出勤时段数",
        "col_total_overtime": "总加班小时数",
        
        # Site Stats Filters
        "filter_site": "按工地筛选",
        "all_sites": "全部工地",
        "start_date": "开始日期",
        "end_date": "结束日期",
        
        # Table Headers - Site Stats
        "col_worker_count": "出勤员工人数",
        "col_total_att_hours": "当日总出勤工时",
        "col_total_ot_hours": "当日总加班工时",
        "total_worker_days": "总工人数（天）",
        
        # Company column
        "col_company_name": "公司名称",
        
        # Worker Stats Dashboard
        "attendance_status_legend": "📊 考勤状态图例",
        "worked_on_site": "出勤工地 (绿色)",
        "absent_no_reason": "缺勤 - 无理由 (红色)",
        "absent_with_reason": "缺勤 - 有理由 (黄色)",
        "no_record": "无记录 (灰色)",
        "filters": "🔍 筛选条件",
        "filter_by_company": "按公司筛选",
        "filter_by_worker": "按员工筛选",
        "filter_by_site": "按工地筛选",
        "select_companies_help": "选择一个或多个公司（留空显示全部）",
        "select_workers_help": "选择一个或多个员工（留空显示全部）",
        "select_sites_help": "选择一个或多个工地（留空显示全部）",
        "select_worker_placeholder": "-- 选择员工 --",
        "please_select_worker": "请选择一个员工以查看考勤记录。",
        "attendance_records_table": "📋 考勤记录",
        "attendance_calendar": "📅 考勤日历",
        "summary_statistics": "📈 统计摘要",
        "days_worked": "出勤天数",
        "absent_no_reason_count": "缺勤 (无理由)",
        "absent_with_reason_count": "缺勤 (有理由)",
        "no_record_count": "无记录",
        "no_attendance_records": "未找到符合筛选条件的考勤记录。",
    },
    
    "zh_tw": {
        # System
        "system_title": "工地考勤管理系統",
        "sidebar_title": "📋 考勤系統",
        
        # Navigation
        "nav_home": "🏠 首頁",
        "nav_companies": "🏢 公司管理",
        "nav_absent_reasons": "⚠️ 缺勤原因",
        "nav_workers": "👥 員工管理",
        "nav_sites": "🏗️ 工地管理",
        "nav_attendance": "📝 考勤記錄",
        "nav_worker_stats": "📊 員工統計看板",
        "nav_site_stats": "📈 工地統計看板",
        "nav_individual_worker_stats": "👤 個別員工統計",
        
        # Companies Page
        "companies_title": "公司管理",
        "add_company": "➕ 新增公司",
        "import_companies": "📥 從 Excel導入公司",
        "company_name": "公司名稱",
        "enter_company_name": "請輸入公司名稱",
        "companies_list": "公司列表",
        "no_companies": "暫無公司資料，請先新增公司",
        "download_template": "📄 下載Excel模板",
        "upload_excel": "上傳Excel文件",
        "import_success": "✅ 成功導入 {} 家公司",
        "import_failed": "❌ 導入失敗：{}",
        "invalid_format": "Excel格式無效。請使用模板。",
        "duplicate_skipped": "⚠️ 跳過 {} 家重複公司",
        "edit_company": "✏️ 編輯",
        "delete_company": "🗑️ 刪除",
        "update_company": "更新公司",
        "confirm_delete": "確定要刪除這家公司嗎？",
        "delete_success": "✅ 公司刪除成功",
        "delete_failed": "❌ 刪除失敗：{}",
        "update_success": "✅ 公司更新成功",
        "update_failed": "❌ 更新失敗",
        "has_workers_warning": "無法刪除：該公司有 {} 名員工關聯。請先重新分配或刪除員工。",
        
        # Absent Reasons Page
        "absent_reasons_title": "缺勤原因管理",
        "add_absent_reason": "➕ 新增缺勤原因",
        "absent_reason_name": "原因名稱",
        "enter_absent_reason": "請輸入缺勤原因",
        "absent_reasons_list": "缺勤原因列表",
        "no_absent_reasons": "暫無缺勤原因，請先新增原因",
        "reason_exists": "該原因已存在，請勿重複新增",
        
        # Home Page
        "home_title": "歡迎使用工地考勤管理系統",
        "home_subtitle": "現代設計 · 區域網路多人共用 · 純本機離線運行",
        "total_workers": "👥 員工總數",
        "total_sites": "🏗️ 工地總數",
        "total_records": "📊 考勤記錄",
        "data_backup": "💾 資料備份",
        "attendance_trend": "📈 最近30日出勤趨勢",
        "site_distribution": "🏗️ 各工地人數分佈",
        "weekly_pattern": "🗓️ 每週出勤模式",
        
        # Workers Page
        "workers_title": "員工管理",
        "add_worker": "➕ 新增員工",
        "worker_name": "員工姓名",
        "company": "所屬公司",
        "enter_worker_name": "請輸入員工姓名",
        "enter_company": "請輸入所屬公司",
        "save": "儲存",
        "workers_list": "員工列表",
        "no_workers": "暫無員工資料，請先新增員工",
        
        # Sites Page
        "sites_title": "工地管理",
        "add_site": "➕ 新增工地",
        "site_name": "工地名稱",
        "enter_site_name": "請輸入工地名稱",
        "sites_list": "工地列表",
        "no_sites": "暫無工地資料，請先新增工地",
        
        # Attendance Page
        "attendance_title": "考勤記錄",
        "add_attendance": "📝 新增考勤記錄",
        "date": "日期",
        "worker": "員工",
        "site": "工地",
        "absent_reason": "缺勤原因",
        "attendance_status": "出勤情況",
        "morning": "上午出勤",
        "afternoon": "下午出勤",
        "evening": "晚上出勤",
        "overtime_hours": "加班小時數",
        "submit": "提交",
        "attendance_list": "考勤記錄列表",
        "no_attendance": "暫無考勤記錄",
        "please_add_workers": "請先新增員工",
        "please_add_sites": "請先新增工地",
        
        # Validation Messages
        "fill_all_fields": "請填寫所有欄位",
        "worker_exists": "該員工已存在，請勿重複新增",
        "site_exists": "該工地已存在，請勿重複新增",
        "attendance_exists": "⚠️ 該員工在此日期已有考勤記錄，請勿重複提交",
        "save_success": "✅ 儲存成功",
        "save_failed": "儲存失敗",
        "fill_site_name": "請填寫工地名稱",
        
        # Statistics
        "worker_stats_title": "員工統計看板",
        "site_stats_title": "工地統計看板",
        "individual_worker_stats_title": "個別員工統計",
        "no_stats": "暫無統計資料",
        
        # Table Headers - Workers
        "col_id": "ID",
        "col_name": "姓名",
        "col_company": "所屬公司",
        
        # Table Headers - Attendance
        "col_worker_name": "員工姓名",
        "col_site_name": "工地名稱",
        "col_absent_reason": "缺勤原因",
        "col_work_date": "日期",
        "col_morning": "上午",
        "col_afternoon": "下午",
        "col_evening": "晚上",
        "col_overtime": "加班小時",
        
        # Table Headers - Statistics
        "col_total_att_days": "總出勤天數",
        "col_total_abs_days": "總缺勤天數",
        "col_total_slots": "總出勤時段數",
        "col_total_overtime": "總加班小時數",
        
        # Site Stats Filters
        "filter_site": "按工地篩選",
        "all_sites": "全部工地",
        "start_date": "開始日期",
        "end_date": "結束日期",
        
        # Table Headers - Site Stats
        "col_worker_count": "出勤員工人數",
        "col_total_att_hours": "當日總出勤工時",
        "col_total_ot_hours": "當日總加班工時",
        "total_worker_days": "總工人數（天）",
        
        # Company column
        "col_company_name": "公司名稱",
        
        # Worker Stats Dashboard
        "attendance_status_legend": "📊 考勤狀態圖例",
        "worked_on_site": "出勤工地 (綠色)",
        "absent_no_reason": "缺勤 - 無理由 (紅色)",
        "absent_with_reason": "缺勤 - 有理由 (黃色)",
        "no_record": "無記錄 (灰色)",
        "filters": "🔍 篩選條件",
        "filter_by_company": "按公司篩選",
        "filter_by_worker": "按員工篩選",
        "filter_by_site": "按工地篩選",
        "select_companies_help": "選擇一個或多個公司（留空顯示全部）",
        "select_workers_help": "選擇一個或多個員工（留空顯示全部）",
        "select_sites_help": "選擇一個或多個工地（留空顯示全部）",
        "select_worker_placeholder": "-- 選擇員工 --",
        "please_select_worker": "請選擇一個員工以查看考勤記錄。",
        "attendance_records_table": "📋 考勤記錄",
        "attendance_calendar": "📅 考勤日曆",
        "summary_statistics": "📈 統計摘要",
        "days_worked": "出勤天數",
        "absent_no_reason_count": "缺勤 (無理由)",
        "absent_with_reason_count": "缺勤 (有理由)",
        "no_record_count": "無記錄",
        "no_attendance_records": "未找到符合篩選條件的考勤記錄。",
    }
}

def get_text(key, lang="zh_cn"):
    """Get text by key and language"""
    if lang not in LANGUAGES:
        lang = "zh_cn"
    return LANGUAGES[lang].get(key, key)

def get_supported_languages():
    """Get list of supported languages"""
    return {
        "English": "en",
        "简体中文": "zh_cn",
        "繁體中文": "zh_tw"
    }
