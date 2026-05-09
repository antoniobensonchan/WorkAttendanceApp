"""
数据库模块 - 支持局域网共享的 SQLite 数据库操作
包含数据库初始化、增删改查等核心功能
"""

import sqlite3
import sys
import os
from datetime import date
from typing import List, Dict, Optional, Tuple


def get_resource_path(filename):
    """Get the correct path to resource files (works in both dev and frozen mode)"""
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


def get_database_path():
    """Get a writable path for the database file.
    
    Supports multiple deployment modes:
    - Streamlit Cloud: Uses current working directory
    - Frozen EXE (Windows/macOS): Stores in user's Documents/AppData folder
    - Development: Uses project directory
    """
    # Check if running on Streamlit Cloud
    if os.environ.get('STREAMLIT_CLOUD', False) or '/home/appuser' in os.getcwd() or '/mount/src' in os.getcwd():
        # Streamlit Cloud uses /mount/src/your-repo-name
        return os.path.join(os.getcwd(), "attendance.db")
    
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        # Get the bundled database path from _internal
        bundled_db = get_resource_path("attendance.db")
        
        # Platform-specific writable location
        if sys.platform == 'darwin':  # macOS
            app_folder = os.path.expanduser('~/Library/Application Support/WorkAttendanceApp')
        elif sys.platform == 'win32':  # Windows
            user_docs = os.path.expanduser('~\\Documents')
            app_folder = os.path.join(user_docs, 'WorkAttendanceApp')
        else:  # Linux and others
            app_folder = os.path.expanduser('~/.work_attendance_app')
        
        # Create app folder if it doesn't exist
        if not os.path.exists(app_folder):
            try:
                os.makedirs(app_folder, exist_ok=True)
                print(f"Created app folder: {app_folder}")
            except Exception as e:
                print(f"Warning: Could not create app folder {app_folder}: {e}")
                # Fallback to executable directory
                app_folder = os.path.dirname(sys.executable)
        
        target_db = os.path.join(app_folder, "attendance.db")
        
        # Copy bundled database to writable location if it doesn't exist
        if not os.path.exists(target_db):
            if os.path.exists(bundled_db):
                try:
                    import shutil
                    shutil.copy2(bundled_db, target_db)
                    print(f"Copied database from {bundled_db} to: {target_db}")
                except Exception as e:
                    print(f"Warning: Could not copy database: {e}")
                    # If copy fails, try to use bundled location (may be read-only)
                    return bundled_db
            else:
                print(f"Bundled database not found at: {bundled_db}")
        else:
            print(f"Using existing database at: {target_db}")
        
        return target_db
    else:
        # Running as script - use current directory
        return os.path.join(os.getcwd(), "attendance.db")


class DatabaseManager:
    """数据库管理器 - 单例模式，确保多端访问同一数据库"""
    
    _instance = None
    _connection = None
    
    def __new__(cls, db_path: str = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Use writable database path
            if db_path is None:
                db_path = get_database_path()
            cls._instance.db_path = db_path
            print(f"Database path: {db_path}")
            cls._instance._init_database()
        return cls._instance
    
    def _get_connection(self):
        """获取数据库连接（线程安全）"""
        if self._connection is None:
            try:
                # Check if we can write to the database location
                db_dir = os.path.dirname(self.db_path)
                if not os.access(db_dir, os.W_OK):
                    error_msg = (
                        f"資料庫資料夾沒有寫入權限！\n"
                        f"資料庫路徑: {self.db_path}\n"
                        f"資料夾路徑: {db_dir}\n\n"
                        f"解決方案:\n"
                        f"1. 將應用程式移動到可寫入的資料夾（例如：文件）\n"
                        f"   建議位置: C:\\Users\\[您的名稱]\\Documents\\WorkAttendanceApp\n\n"
                        f"2. 或者右鍵點擊資料夾 → 內容 → 安全性 → 編輯 → 給予「修改」權限\n\n"
                        f"3. 或者以系統管理員身分執行應用程式"
                    )
                    raise PermissionError(error_msg)
                
                self._connection = sqlite3.connect(self.db_path, check_same_thread=False)
                self._connection.row_factory = sqlite3.Row
                
                # Test write access with a simple operation
                cursor = self._connection.cursor()
                cursor.execute("CREATE TABLE IF NOT EXISTS _write_test (id INTEGER)")
                cursor.execute("DROP TABLE IF EXISTS _write_test")
                self._connection.commit()
                
                print(f"Successfully connected to database: {self.db_path}")
                
            except PermissionError:
                raise
            except Exception as e:
                error_msg = (
                    f"無法連接資料庫！\n"
                    f"資料庫路徑: {self.db_path}\n"
                    f"錯誤訊息: {str(e)}\n\n"
                    f"可能的解決方案:\n"
                    f"1. 確保資料夾有寫入權限\n"
                    f"2. 檢查是否有其他程式正在使用資料庫\n"
                    f"3. 嘗試以系統管理員身分執行"
                )
                raise ConnectionError(error_msg)
        return self._connection
    
    def _init_database(self):
        """初始化数据库表结构"""
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        cursor = conn.cursor()
        
        # 创建公司表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')
        
        # 创建缺勤原因表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS absent_reasons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reason TEXT NOT NULL UNIQUE
            )
        ''')
        
        # 创建员工表（修改：company改为company_id外键）
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                company_id INTEGER NOT NULL,
                FOREIGN KEY (company_id) REFERENCES companies(id)
            )
        ''')
        
        # 创建工地表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')
        
        # 创建考勤表（每个时段可以关联不同的工地）
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                worker_id INTEGER NOT NULL,
                work_date DATE NOT NULL,
                morning_site_id INTEGER DEFAULT NULL,
                afternoon_site_id INTEGER DEFAULT NULL,
                evening_site_id INTEGER DEFAULT NULL,
                absent_reason_id INTEGER DEFAULT NULL,
                overtime_hours REAL DEFAULT 0,
                FOREIGN KEY (worker_id) REFERENCES workers(id),
                FOREIGN KEY (morning_site_id) REFERENCES sites(id),
                FOREIGN KEY (afternoon_site_id) REFERENCES sites(id),
                FOREIGN KEY (evening_site_id) REFERENCES sites(id),
                FOREIGN KEY (absent_reason_id) REFERENCES absent_reasons(id),
                UNIQUE(worker_id, work_date)
            )
        ''')
        
        # 数据库迁移：为旧数据库添加缺失的列
        self._migrate_database(cursor)
        
        conn.commit()
        conn.close()
    
    def _migrate_database(self, cursor):
        """数据库迁移：为旧数据库添加缺失的列"""
        try:
            # 检查 attendance 表是否有 absent_reason_id 列
            cursor.execute("PRAGMA table_info(attendance)")
            columns = [row[1] for row in cursor.fetchall()]
            
            if 'absent_reason_id' not in columns:
                # 添加缺勤原因ID列
                cursor.execute('ALTER TABLE attendance ADD COLUMN absent_reason_id INTEGER DEFAULT NULL')
                print("数据库迁移：已添加 absent_reason_id 列")
            
            # 检查 workers 表是否有 company_id 列（兼容更旧的版本）
            cursor.execute("PRAGMA table_info(workers)")
            columns = [row[1] for row in cursor.fetchall()]
            
            if 'company_id' not in columns and 'company' in columns:
                # 旧版本有 company 文本字段，需要迁移
                print("检测到旧版 workers 表结构，开始迁移...")
                
                # 创建临时公司表并提取唯一公司名
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS companies_temp (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE
                    )
                ''')
                
                cursor.execute('INSERT OR IGNORE INTO companies (name) SELECT DISTINCT company FROM workers')
                
                # 添加 company_id 列
                cursor.execute('ALTER TABLE workers ADD COLUMN company_id INTEGER')
                
                # 更新 company_id
                cursor.execute('''
                    UPDATE workers 
                    SET company_id = (
                        SELECT id FROM companies WHERE companies.name = workers.company
                    )
                ''')
                
                # 删除旧 company 列（SQLite 不支持直接删除列，需要重建表）
                cursor.execute('''
                    CREATE TABLE workers_new (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        company_id INTEGER NOT NULL,
                        FOREIGN KEY (company_id) REFERENCES companies(id)
                    )
                ''')
                
                cursor.execute('''
                    INSERT INTO workers_new (id, name, company_id)
                    SELECT id, name, company_id FROM workers
                ''')
                
                cursor.execute('DROP TABLE workers')
                cursor.execute('ALTER TABLE workers_new RENAME TO workers')
                
                print("数据库迁移：workers 表结构升级完成")
                
        except Exception as e:
            print(f"数据库迁移警告：{e}")
    
    # ==================== 公司管理 ====================
    
    def add_company(self, name: str) -> bool:
        """添加公司，返回是否成功"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO companies (name) VALUES (?)',
                (name,)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_all_companies(self) -> List[Dict]:
        """获取所有公司列表"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM companies ORDER BY id')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_company_by_id(self, company_id: int) -> Optional[Dict]:
        """根据ID获取公司信息"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM companies WHERE id = ?', (company_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def company_exists(self, name: str) -> bool:
        """检查公司是否已存在"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM companies WHERE name = ?', (name,))
        count = cursor.fetchone()[0]
        return count > 0
    
    def update_company(self, company_id: int, new_name: str) -> bool:
        """更新公司名称，返回是否成功"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE companies SET name = ? WHERE id = ?',
                (new_name, company_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            return False
    
    def delete_company(self, company_id: int) -> Tuple[bool, str]:
        """删除公司，返回(是否成功, 错误信息)
        如果公司有员工关联，则不允许删除
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # 检查是否有员工关联
            cursor.execute('SELECT COUNT(*) FROM workers WHERE company_id = ?', (company_id,))
            worker_count = cursor.fetchone()[0]
            
            if worker_count > 0:
                return False, f"Cannot delete: {worker_count} worker(s) are associated with this company"
            
            # 删除公司
            cursor.execute('DELETE FROM companies WHERE id = ?', (company_id,))
            conn.commit()
            
            if cursor.rowcount > 0:
                return True, ""
            else:
                return False, "Company not found"
                
        except Exception as e:
            return False, str(e)
    
    def get_company_worker_count(self, company_id: int) -> int:
        """获取公司关联的员工数量"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM workers WHERE company_id = ?', (company_id,))
        count = cursor.fetchone()[0]
        return count
    
    # ==================== 员工管理 ====================
    
    def add_worker(self, name: str, company_id: int) -> bool:
        """添加员工，返回是否成功"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO workers (name, company_id) VALUES (?, ?)',
                (name, company_id)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_all_workers(self) -> List[Dict]:
        """获取所有员工列表（含公司名称）"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT w.id, w.name, c.name as company_name
            FROM workers w
            JOIN companies c ON w.company_id = c.id
            ORDER BY w.id
        ''')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_worker_by_id(self, worker_id: int) -> Optional[Dict]:
        """根据ID获取员工信息（含公司名称）"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT w.id, w.name, c.name as company_name
            FROM workers w
            JOIN companies c ON w.company_id = c.id
            WHERE w.id = ?
        ''', (worker_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def worker_exists(self, name: str) -> bool:
        """检查员工是否已存在"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM workers WHERE name = ?', (name,))
        count = cursor.fetchone()[0]
        return count > 0
    
    def get_worker_attendance_count(self, worker_id: int) -> int:
        """获取员工被考勤记录引用的次数"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM attendance WHERE worker_id = ?', (worker_id,))
        count = cursor.fetchone()[0]
        return count
    
    def update_worker(self, worker_id: int, new_name: str, new_company_id: int) -> bool:
        """更新员工信息，返回是否成功"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE workers SET name = ?, company_id = ? WHERE id = ?',
                (new_name, new_company_id, worker_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            return False
    
    def delete_worker(self, worker_id: int) -> Tuple[bool, str]:
        """删除员工，返回(是否成功, 错误信息)
        如果员工已有考勤记录，则不允许删除
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # 检查是否有考勤记录引用
            attendance_count = self.get_worker_attendance_count(worker_id)
            
            if attendance_count > 0:
                return False, f"Cannot delete: {attendance_count} attendance record(s) are associated with this worker"
            
            # 删除员工
            cursor.execute('DELETE FROM workers WHERE id = ?', (worker_id,))
            conn.commit()
            
            if cursor.rowcount > 0:
                return True, ""
            else:
                return False, "Worker not found"
                
        except Exception as e:
            return False, str(e)
    
    # ==================== 工地管理 ====================
    
    def add_site(self, name: str) -> bool:
        """添加工地，返回是否成功"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO sites (name) VALUES (?)',
                (name,)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_all_sites(self) -> List[Dict]:
        """获取所有工地列表"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM sites ORDER BY id')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_site_by_id(self, site_id: int) -> Optional[Dict]:
        """根据ID获取工地信息"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM sites WHERE id = ?', (site_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def site_exists(self, name: str) -> bool:
        """检查工地是否已存在"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM sites WHERE name = ?', (name,))
        count = cursor.fetchone()[0]
        return count > 0
    
    def get_site_attendance_count(self, site_id: int) -> int:
        """获取工地被考勤记录引用的次数（检查所有时段）"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM attendance 
            WHERE morning_site_id = ? 
               OR afternoon_site_id = ? 
               OR evening_site_id = ?
        ''', (site_id, site_id, site_id))
        count = cursor.fetchone()[0]
        return count
    
    def update_site(self, site_id: int, new_name: str) -> bool:
        """更新工地名称，返回是否成功"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE sites SET name = ? WHERE id = ?',
                (new_name, site_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            return False
    
    def delete_site(self, site_id: int) -> Tuple[bool, str]:
        """删除工地，返回(是否成功, 错误信息)
        如果工地已有考勤记录，则不允许删除
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # 检查是否有考勤记录引用
            attendance_count = self.get_site_attendance_count(site_id)
            
            if attendance_count > 0:
                return False, f"Cannot delete: {attendance_count} attendance record(s) are associated with this site"
            
            # 删除工地
            cursor.execute('DELETE FROM sites WHERE id = ?', (site_id,))
            conn.commit()
            
            if cursor.rowcount > 0:
                return True, ""
            else:
                return False, "Site not found"
                
        except Exception as e:
            return False, str(e)
    
    # ==================== 考勤管理 ====================
    
    def add_attendance(self, worker_id: int, work_date: date,
                      morning_site_id: Optional[int], afternoon_site_id: Optional[int], 
                      evening_site_id: Optional[int], absent_reason_id: Optional[int],
                      overtime_hours: float) -> bool:
        """添加考勤记录，返回是否成功"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO attendance 
                (worker_id, work_date, morning_site_id, afternoon_site_id, evening_site_id, absent_reason_id, overtime_hours)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (worker_id, work_date.isoformat(), 
                  morning_site_id, afternoon_site_id, evening_site_id, absent_reason_id, overtime_hours))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def attendance_exists(self, worker_id: int, work_date: date) -> bool:
        """检查某员工在某天是否已有考勤记录"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT COUNT(*) FROM attendance WHERE worker_id = ? AND work_date = ?',
            (worker_id, work_date.isoformat())
        )
        count = cursor.fetchone()[0]
        return count > 0
    
    def get_all_attendance(self) -> List[Dict]:
        """获取所有考勤记录（含关联信息）"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.id, w.name as worker_name, c.name as company_name,
                   s_morning.name as morning_site, 
                   s_afternoon.name as afternoon_site,
                   s_evening.name as evening_site,
                   ar.reason as absent_reason,
                   a.work_date, a.overtime_hours
            FROM attendance a
            JOIN workers w ON a.worker_id = w.id
            JOIN companies c ON w.company_id = c.id
            LEFT JOIN sites s_morning ON a.morning_site_id = s_morning.id
            LEFT JOIN sites s_afternoon ON a.afternoon_site_id = s_afternoon.id
            LEFT JOIN sites s_evening ON a.evening_site_id = s_evening.id
            LEFT JOIN absent_reasons ar ON a.absent_reason_id = ar.id
            ORDER BY a.work_date DESC, a.id DESC
        ''')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_attendance_by_date_range(self, start_date: date, end_date: date) -> List[Dict]:
        """根据日期范围获取考勤记录"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.id, w.name as worker_name, c.name as company_name,
                   s_morning.name as morning_site, 
                   s_afternoon.name as afternoon_site,
                   s_evening.name as evening_site,
                   ar.reason as absent_reason,
                   a.work_date, a.overtime_hours,
                   a.morning_site_id, a.afternoon_site_id, a.evening_site_id,
                   a.worker_id
            FROM attendance a
            JOIN workers w ON a.worker_id = w.id
            JOIN companies c ON w.company_id = c.id
            LEFT JOIN sites s_morning ON a.morning_site_id = s_morning.id
            LEFT JOIN sites s_afternoon ON a.afternoon_site_id = s_afternoon.id
            LEFT JOIN sites s_evening ON a.evening_site_id = s_evening.id
            LEFT JOIN absent_reasons ar ON a.absent_reason_id = ar.id
            WHERE a.work_date >= ? AND a.work_date <= ?
            ORDER BY a.work_date DESC, a.id DESC
        ''', (start_date.isoformat(), end_date.isoformat()))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def update_attendance(self, attendance_id: int, work_date: date,
                         morning_site_id: Optional[int], afternoon_site_id: Optional[int],
                         evening_site_id: Optional[int], absent_reason_id: Optional[int],
                         overtime_hours: float) -> bool:
        """更新考勤记录，返回是否成功"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE attendance SET
                    work_date = ?,
                    morning_site_id = ?,
                    afternoon_site_id = ?,
                    evening_site_id = ?,
                    absent_reason_id = ?,
                    overtime_hours = ?
                WHERE id = ?
            ''', (work_date.isoformat(), morning_site_id, afternoon_site_id,
                  evening_site_id, absent_reason_id, overtime_hours, attendance_id))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            return False
    
    def delete_attendance(self, attendance_id: int) -> Tuple[bool, str]:
        """删除考勤记录，返回(是否成功, 错误信息)"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM attendance WHERE id = ?', (attendance_id,))
            conn.commit()
            
            if cursor.rowcount > 0:
                return True, ""
            else:
                return False, "Attendance record not found"
                
        except Exception as e:
            return False, str(e)
    
    # ==================== 缺勤原因管理 ====================
    
    def add_absent_reason(self, reason: str) -> bool:
        """添加缺勤原因，返回是否成功"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO absent_reasons (reason) VALUES (?)',
                (reason,)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_all_absent_reasons(self) -> List[Dict]:
        """获取所有缺勤原因列表"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, reason FROM absent_reasons ORDER BY id')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_absent_reason_by_id(self, reason_id: int) -> Optional[Dict]:
        """根据ID获取缺勤原因信息"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, reason FROM absent_reasons WHERE id = ?', (reason_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def absent_reason_exists(self, reason: str) -> bool:
        """检查缺勤原因是否已存在"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM absent_reasons WHERE reason = ?', (reason,))
        count = cursor.fetchone()[0]
        return count > 0
    
    def get_absent_reason_attendance_count(self, reason_id: int) -> int:
        """获取缺勤原因被考勤记录引用的次数"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM attendance WHERE absent_reason_id = ?', (reason_id,))
        count = cursor.fetchone()[0]
        return count
    
    def update_absent_reason(self, reason_id: int, new_reason: str) -> bool:
        """更新缺勤原因，返回是否成功"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE absent_reasons SET reason = ? WHERE id = ?',
                (new_reason, reason_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            return False
    
    def delete_absent_reason(self, reason_id: int) -> Tuple[bool, str]:
        """删除缺勤原因，返回(是否成功, 错误信息)
        如果缺勤原因已被考勤记录引用，则不允许删除
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # 检查是否有考勤记录引用
            attendance_count = self.get_absent_reason_attendance_count(reason_id)
            
            if attendance_count > 0:
                return False, f"Cannot delete: {attendance_count} attendance record(s) are using this reason"
            
            # 删除缺勤原因
            cursor.execute('DELETE FROM absent_reasons WHERE id = ?', (reason_id,))
            conn.commit()
            
            if cursor.rowcount > 0:
                return True, ""
            else:
                return False, "Absent reason not found"
                
        except Exception as e:
            return False, str(e)
    
    # ==================== 统计查询 ====================
    
    def get_worker_statistics(self) -> List[Dict]:
        """获取员工统计数据"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                w.id,
                w.name,
                c.name as company_name,
                COUNT(DISTINCT a.work_date) as total_attendance_days,
                (COUNT(a.morning_site_id) + COUNT(a.afternoon_site_id) + COUNT(a.evening_site_id)) as total_attendance_slots,
                COALESCE(SUM(a.overtime_hours), 0) as total_overtime_hours
            FROM workers w
            JOIN companies c ON w.company_id = c.id
            LEFT JOIN attendance a ON w.id = a.worker_id
            GROUP BY w.id, w.name, c.name
            ORDER BY w.id
        ''')
        rows = cursor.fetchall()
        
        result = []
        for row in rows:
            d = dict(row)
            # 计算缺勤天数（假设每个工作日有3个时段）
            total_possible_slots = d['total_attendance_days'] * 3
            d['total_absent_days'] = max(0, total_possible_slots - d['total_attendance_slots']) / 3
            result.append(d)
        
        return result
    
    def get_worker_attendance_calendar(self, start_date: date, end_date: date,
                                       company_ids: Optional[List[int]] = None,
                                       worker_ids: Optional[List[int]] = None) -> List[Dict]:
        """获取员工考勤日历数据（用于可视化展示）
        返回每个员工在指定日期范围内的考勤状态
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT 
                w.id as worker_id,
                w.name as worker_name,
                c.id as company_id,
                c.name as company_name,
                a.work_date,
                a.morning_site_id,
                a.afternoon_site_id,
                a.evening_site_id,
                a.absent_reason_id,
                ar.reason as absent_reason,
                ar.id as absent_reason_db_id
            FROM workers w
            JOIN companies c ON w.company_id = c.id
            LEFT JOIN attendance a ON w.id = a.worker_id 
                AND a.work_date >= ? 
                AND a.work_date <= ?
            LEFT JOIN absent_reasons ar ON a.absent_reason_id = ar.id
        '''
        
        conditions = []
        params = [start_date.isoformat(), end_date.isoformat()]
        
        if company_ids and len(company_ids) > 0:
            placeholders = ','.join(['?' for _ in company_ids])
            conditions.append(f'c.id IN ({placeholders})')
            params.extend(company_ids)
        
        if worker_ids and len(worker_ids) > 0:
            placeholders = ','.join(['?' for _ in worker_ids])
            conditions.append(f'w.id IN ({placeholders})')
            params.extend(worker_ids)
        
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)
        
        query += ' ORDER BY c.name, w.name, a.work_date'
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_site_statistics(self, site_id: Optional[int] = None, 
                           start_date: Optional[date] = None,
                           end_date: Optional[date] = None) -> List[Dict]:
        """获取工地统计数据
        计算总工人数：上午=0.5天，下午=0.5天，晚上=加班小时数
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT 
                s.name as site_name,
                a.work_date,
                COUNT(DISTINCT a.worker_id) as worker_count,
                (
                    COUNT(CASE WHEN a.morning_site_id = s.id THEN 1 END) * 0.5 +
                    COUNT(CASE WHEN a.afternoon_site_id = s.id THEN 1 END) * 0.5 +
                    COALESCE(SUM(CASE WHEN a.evening_site_id = s.id THEN a.overtime_hours ELSE 0 END), 0)
                ) as total_worker_days,
                COALESCE(SUM(CASE WHEN a.evening_site_id = s.id THEN a.overtime_hours ELSE 0 END), 0) as total_overtime_hours
            FROM attendance a
            CROSS JOIN sites s
            WHERE a.morning_site_id = s.id 
               OR a.afternoon_site_id = s.id 
               OR a.evening_site_id = s.id
        '''
        
        conditions = []
        params = []
        
        if site_id:
            conditions.append('s.id = ?')
            params.append(site_id)
        
        if start_date:
            conditions.append('a.work_date >= ?')
            params.append(start_date.isoformat())
        
        if end_date:
            conditions.append('a.work_date <= ?')
            params.append(end_date.isoformat())
        
        if conditions:
            query += ' AND ' + ' AND '.join(conditions)
        
        query += ' GROUP BY s.name, a.work_date ORDER BY a.work_date DESC'
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


# 全局数据库实例
db_manager = DatabaseManager()
