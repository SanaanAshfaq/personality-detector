# Personality Prediction API using MBTI

## 📦 Installation Process

### 1. Clone the repository (option 1)

```bash
git clone https://github.com/SanaanAshfaq/personality-detector.git
cd personality-detector
```

---

### 📥 Alternative: Download ZIP (option 2)

If you do not want to use Git:

1. Click **Code → Download ZIP** on GitHub
2. Unzip it 
3. Now you can open the extracted folder which you get after extraxt the ZIP file (for example, `personality-detector-main`)
4. Open the terminal inside that folder

---

### 2. Virtual environment setup

🪟 FOr Windows Users (Command Prompt / PowerShell)
```
python -m venv venv
venv\Scripts\activate
```

🍎 For Mac Users
```
python3 -m venv venv
source venv/bin/activate
```
---

### 3. Install the dependencies to run the project successfully

```
pip install -r requirements.txt
```

---

## 🔑 Environment Setup

To use the Groq API to provide personality predictions.

### Step 1: Create a `.env` file in the project root

Create a file named:

```
.env
```

### Step 2: Add this inside `.env` means insert this inside the file created above

```
GROQ_API_KEY="Key is provided in the report"
```

---

## ▶️ Run the Project

```bash
python manage.py runserver
```

---

## 🌐 API Endpoint

Access in browser or Postman:

```
http://127.0.0.1:8000/api/predict/
```

---

## 📥 Input Format

Send POST request in JSON Format:

```json
{
  "text": "I enjoy working independently and thinking deeply about ideas."
}
```

---

## 📤 Output Example

```json
{
  "prediction": {
    "personality_type": "INFP",
    "percentages": {
      "I": 78.3,
      "N": 66.5,
      "F": 72.1,
      "P": 61.4
    },
    "overall_confidence": 69.58
  },
  "personality_type": "INFP",
  "overall_confidence": 69.58,
  "advice": "..."
}
```

---

## 📁 Important Files

* `models/` → contains trained ML models (required)
* `requirements.txt` → dependencies
* `.env` → API key (must be created manually)

---

## ⚠️ Warnings

* Make sure `models/` folder is present before running
* If `.env` is missing, advice feature may not work
* Personality prediction will still work without API key
