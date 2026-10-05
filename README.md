# Career Agent (GitHub-Career)

> **Automated Career Alignment & Strategic Resume Pipeline Engine**  
> 具備職缺需求自動解析 (JD Parser)、候選人特質對齊 (Candidate Matcher) 與多語系客製化履歷生成之全自動職涯管線引擎。

---

## 🌟 核心特色 (Key Features)

1. **職缺結構化解析 (JD Parsing)**
   - 自動萃取職缺關鍵條件、技能標籤、企業核心訴求與職責矩陣。
2. **多維度能力對齊 (Candidate Alignment)**
   - 結合個人經歷庫（Experience Pool）與技能樹，進行語義相似度與權重匹配。
3. **多語系履歷生成 (Multi-Language Pipeline)**
   - 支援自動產出符合國際標準之繁體中文 (zh)、英文 (en) 與日文 (ja) 履歷草稿。
4. **邊界防護與品質審查 (Boundary Guard & QA)**
   - 內建 boundary_guard.py 與 resume_qa.py，嚴防模型幻覺並確保內容真實客觀。
5. **Google Drive / Docs 雲端同步 (Cloud Integration)**
   - 支援將生成履歷無縫同步發布至 Google Drive 與雲端簡報/文件。

---

## 📂 專案架構 (Project Structure)

- `candidate_matcher.py`：候選人條件與職缺需求對齊引擎
- `jd_parser.py`：職缺描述 (JD) 結構化萃取器
- `career_bridge.py`：調度溝通橋接器
- `career_runner.py`：管線執行入口
- `resume_version_manager.py`：履歷多版本管理
- `resume_qa.py`：履歷生成品質稽核 (QA)
- `boundary_guard.py`：安全防護與格式校驗閘門
- `workspace.py`：工作區管理
- `tool.py`：輔助工具集合
- `prompts/`：結構化 Prompt 契約
- `google/`：Google Drive / OAuth 整合模組
- `examples/`：合成範例資料 (Profile & Sample JD)
- `requirements.txt`：專案相依套件

---

## 🚀 快速開始 (Quick Start)

### 1. 安裝環境依賴

```bash
git clone https://github.com/<your-username>/GitHub-Career.git
cd GitHub-Career
pip install -r requirements.txt
```

### 2. 配置環境變數

```bash
cp .env.example .env
# 編輯 .env 填入您的 Google API 金鑰 (選用)
```

### 3. 執行範例對齊流程

```bash
python3 candidate_matcher.py
```

---

## 🔒 隱私與安全聲明 (Privacy & Security)

- 本開源版本已完全剔除任何個人敏感資料 (PII)、真實求職檔案與 API 私鑰。
- 所有測試與範例資料均使用合成數據 (Synthetic Fixtures)。
- 如需啟用 Google Drive 自動同步，請於本機安全配置自己的 Google Cloud OAuth 憑證。

---

## 📄 開源授權 (License)

本專案採用 [MIT License](LICENSE) 授權。
