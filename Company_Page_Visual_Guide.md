# Company Management Page - Visual Guide

## 🎨 UI Layout Overview

### Main Page Structure
```
┌─────────────────────────────────────────────────────────────────┐
│                    Companies Management                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────┐  ┌──────────┐  ┌──────────┐         │
│  │  🔍 Search Box       │  │ ➕ Add   │  │ 📥 Import│         │
│  │  (Width: 3)          │  │ (Width:1)│  │ (Width:1)│         │
│  └──────────────────────┘  └──────────┘  └──────────┘         │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                         Companies List                          │
├─────────────────────────────────────────────────────────────────┤
│  #1    ABC Construction Co.           [✏️ Edit] [🗑️ Delete]   │
│  #2    XYZ Engineering Ltd.           [✏️ Edit] [🗑️ Delete]   │
│  #3    DEF Builders Inc.              [✏️ Edit] [🗑️ Delete]   │
│  ...                                                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📱 Wide Dialog Examples

### Add Company Dialog (width="large")
```
┌──────────────────────────────────────────────────────────┐
│                  ➕ 新增公司                               │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────────────────┐  ┌────────────────────────┐ │
│  │ Company Name:          │  │                        │ │
│  │ [__________________]   │  │  更多字段待擴展         │ │
│  │                        │  │  (Placeholder)         │ │
│  └────────────────────────┘  └────────────────────────┘ │
│                                                          │
│                                        [❌ Cancel][💾 Save]│
└──────────────────────────────────────────────────────────┘
```

### Edit Company Dialog (width="large")
```
┌──────────────────────────────────────────────────────────┐
│                  ✏️ 編輯公司：ABC Construction            │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────────────────┐  ┌────────────────────────┐ │
│  │ Company Name:          │  │                        │ │
│  │ [ABC Construction___]  │  │  更多字段待擴展         │ │
│  │                        │  │  (Placeholder)         │ │
│  └────────────────────────┘  └────────────────────────┘ │
│                                                          │
│                                        [❌ Cancel][💾 Save]│
└──────────────────────────────────────────────────────────┘
```

### Import Popover
```
┌──────────────────────────────────────────────────────────┐
│  📥 導入                                                  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────┐  ┌────────────────────────────┐   │
│  │ 📄 操作指南      │  │ 📤 文件上傳器               │   │
│  │                  │  │                            │   │
│  │ 1. 下載模板      │  │ [Drag & Drop Area]         │   │
│  │ 2. 填寫公司名稱  │  │                            │   │
│  │ 3. 上傳文件導入  │  │ [Browse Files]             │   │
│  │                  │  │                            │   │
│  │ [Download Button]│  │ [✅ 開始導入]              │   │
│  └──────────────────┘  └────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

### Delete Confirmation Popover
```
┌──────────────────────────────────────┐
│  確定要刪除這家公司嗎？               │
├──────────────────────────────────────┤
│  **ABC Construction Co.**            │
│                                      │
│  ⚠️ 無法刪除：該公司有 9 名員工關聯。 │
│     請先重新分配或刪除員工。          │
│                                      │
│  [✅ 確認]        [❌ 取消]          │
└──────────────────────────────────────┘
```

---

## 🔍 Search Functionality

### Example 1: Search for "ABC"
```
Search Box: [ABC_____________]

Results:
  #1    ABC Construction Co.           [✏️ Edit] [🗑️ Delete]
  #5    ABC Engineering Services       [✏️ Edit] [🗑️ Delete]
```

### Example 2: Search for "Construction"
```
Search Box: [Construction______]

Results:
  #1    ABC Construction Co.           [✏️ Edit] [🗑️ Delete]
  #8    Modern Construction Ltd.       [✏️ Edit] [🗑️ Delete]
```

### Example 3: More than 50 results
```
Search Box: [A_________________]

Results:
  #3    Alpha Builders                 [✏️ Edit] [🗑️ Delete]
  #7    Apex Construction              [✏️ Edit] [🗑️ Delete]
  ... (48 more rows) ...
  
⚠️ 僅顯示前 50 筆記錄，請使用搜尋縮小範圍（共 127 筆）
```

---

## 🎨 Color Scheme (Apple Minimalist)

### Primary Colors
- **Background**: `#ffffff` (Pure White)
- **Text Primary**: `#1e293b` (Dark Slate)
- **Text Secondary**: `#64748b` (Slate Gray)
- **Accent Blue**: `#0071e3` (Apple Blue)

### Status Colors
- **Success**: `#10b981` (Emerald Green)
- **Warning**: `#f59e0b` (Amber)
- **Error**: `#ef4444` (Red)
- **Info**: `#3b82f6` (Blue)

### Gradient Accents (Import Section)
- **Template Download**: `linear-gradient(135deg, #f0fdfa 0%, #ccfbf1 100%)`
- **File Upload**: `linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)`

---

## 💡 Interaction Flow

### Adding a New Company
```
1. User clicks "➕ 新增公司" button
         ↓
2. Wide dialog opens with two-column layout
         ↓
3. User types company name in left column
         ↓
4. User clicks "💾 儲存" button
         ↓
5. System validates:
   - Not empty?
   - Not duplicate?
         ↓
6. Success: Toast notification + Auto rerun
   Error: Show error message
```

### Editing a Company
```
1. User clicks "✏️ 編輯" on a row
         ↓
2. Wide dialog opens with current name pre-filled
         ↓
3. User modifies the name
         ↓
4. User clicks "💾 儲存"
         ↓
5. System updates database
         ↓
6. Page refreshes with updated name
```

### Deleting a Company
```
1. User clicks "🗑️ 刪除" on a row
         ↓
2. Session state flag is set
         ↓
3. Confirmation popover appears
         ↓
4. System checks worker count:
   - If > 0: Show warning with count
   - If = 0: Allow deletion
         ↓
5. User clicks "✅ 確認" or "❌ 取消"
         ↓
6. If confirmed and no workers:
   - Delete from database
   - Refresh page
```

### Importing Companies
```
1. User clicks "📥 導入" popover
         ↓
2. Two-column import interface appears
         ↓
3. Left side: User downloads template
         ↓
4. User fills Excel file with company names
         ↓
5. Right side: User uploads filled file
         ↓
6. User clicks "✅ 開始導入"
         ↓
7. System processes each row:
   - Skip duplicates
   - Add new companies
         ↓
8. Toast notification shows results
         ↓
9. Page refreshes with new companies
```

---

## 📊 Performance Optimizations

### 1. Record Limiting
- Only render first 50 records by default
- Reduces DOM size and improves rendering speed
- Encourages use of search for large datasets

### 2. Lazy Loading
- Dialogs only render when triggered
- Popovers load content on demand
- Minimal initial page load

### 3. Efficient Filtering
- Pandas vectorized operations for search
- Case-insensitive matching with `.str.contains()`
- No full table scans on every keystroke

### 4. Smart Reruns
- Only rerun after successful operations
- Avoid unnecessary re-renders
- Session state management for UI state

---

## 🎯 Key Features Summary

| Feature | Implementation | Benefit |
|---------|---------------|---------|
| Wide Dialogs | `width="large"` | Better screen utilization |
| Two-Column Forms | `st.columns([1, 1])` | Future extensibility |
| Real-time Search | Pandas filtering | Instant feedback |
| 50-Record Limit | `.head(50)` | Performance optimization |
| Delete Safety | Worker count check | Data integrity |
| Import Wizard | Split-pane popover | Clear workflow |
| Apple Style | Minimal backgrounds | Clean aesthetics |
| Toast Notifications | `st.toast()` | Non-intrusive feedback |

---

## 🔧 Responsive Behavior

### Desktop (> 1200px)
- Full wide dialog width (~80% screen)
- Three-column toolbar visible
- All buttons in single row

### Tablet (768px - 1200px)
- Dialog adapts to ~90% screen width
- Toolbar columns may wrap
- Buttons remain accessible

### Mobile (< 768px)
- Dialog becomes full-screen overlay
- Toolbar stacks vertically
- Touch-friendly button sizes

---

## ♿ Accessibility Considerations

- ✅ Proper label associations (hidden with `label_visibility`)
- ✅ Sufficient color contrast ratios
- ✅ Keyboard navigable elements
- ✅ Clear focus indicators
- ✅ Descriptive button text
- ✅ Error messages near inputs
- ✅ Confirmation before destructive actions

---

**Last Updated**: 2026-04-25
**Version**: 2.0 (Refactored)
