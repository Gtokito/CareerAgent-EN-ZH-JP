# CareerAgent-EN-ZH-JP

> **Automated Career Alignment & Strategic Resume Pipeline Engine**  
> 具備職缺需求自動解析 (JD Parser)、候選人特質對齊 (Candidate Matcher) 與多語系客製化履歷生成之全自動職涯管線引擎。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9+-brightgreen.svg)](https://www.python.org/)

---

## 🌟 核心特色 (Key Features)

1. **職缺結構化解析 (JD Parsing)**
   - 自動萃取職缺關鍵條件、技能標籤、企業核心訴求與職責矩陣。
2. **多維度能力對齊 (Candidate Alignment)**
   - 結合個人經歷庫（Experience Pool）與技能樹，進行語義相似度與權重匹配。
3. **多語系履歷生成 (Multi-Language Pipeline)**
   - 支援自動產出符合國際標準之繁體中文 (ZH)、英文 (EN) 與日文 (JP) 履歷草稿。
4. **邊界防護與品質審查 (Boundary Guard & QA)**
   - 內建 `boundary_guard.py` 與 `resume_qa.py`，嚴防模型幻覺並確保內容真實客觀。
5. **Google Drive / Docs 雲端同步 (Cloud Integration)**
   - 支援將生成履歷無縫同步發布至 Google Drive 與雲端簡報/文件。

---

## 📂 專案架構 (Project Structure)

```text
CareerAgent-EN-ZH-JP/
├── candidate_matcher.py        # 候選人條件與職缺需求對齊引擎 (支援開箱即用 Demo)
├── jd_parser.py                # 職缺描述 (JD) 結構化萃取器
├── career_bridge.py            # 調度溝通橋接器
├── career_runner.py            # 管線執行入口
├── resume_version_manager.py   # 履歷多版本管理
├── resume_qa.py                # 履歷生成品質稽核 (QA)
├── boundary_guard.py           # 安全防護與格式校驗閘門
├── workspace.py                # 工作區管理
├── tool.py                     # 輔助工具集合
├── prompts/                    # 結構化 Prompt 契約
├── google/                     # Google Drive / OAuth 整合模組
├── examples/                   # 合成範例資料 (Profile & Sample JD)
└── requirements.txt            # 專案相依套件
```

---

## 🚀 快速開始 (Quick Start)

### 1. 下載倉庫

```bash
git clone https://github.com/Gtokito/CareerAgent-EN-ZH-JP.git
cd CareerAgent-EN-ZH-JP
```

### 2. 安裝環境依賴

```bash
pip install -r requirements.txt
```

### 3. 一鍵執行範例匹配對齊 (開箱即用)

專案已內建合成範例資料，直接執行即可體驗職缺比對效果：

```bash
python3 candidate_matcher.py
```

### 4. 配置自訂經歷庫 (選用)

若要使用您自己的經歷進行分析：
1. 建立 `knowledge/` 資料夾：`mkdir knowledge`
2. 將您的 Markdown 經歷放入 `knowledge/`（亦可參考 `examples/sample_profile/` 之格式）。

---

## 🔒 隱私與安全聲明 (Privacy & Security)

- 本開源版本已完全剔除任何個人敏感資料 (PII)、真實求職檔案與 API 私鑰。
- 所有測試與範例資料均使用合成數據 (Synthetic Fixtures)。
- 如需啟用 Google Drive 自動同步，請於本機安全配置自己的 Google Cloud OAuth 憑證 (`.env.example`)。

---

## 📄 開源授權 (License)

本專案採用 [MIT License](LICENSE) 授權。
