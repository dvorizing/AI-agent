# AI Procurement Agent – Bank of Israel

סוכן רכש חכם: מחפש מוצרים באינטרנט, בוחר 3 הצעות מחיר, ושולח מייל.

## מבנה

```
src/bank_of_israel_ai/
  agents/procurement_agent.py   # CrewAI agent (Gemini LLM)
  tools/search_tool.py          # חיפוש Google (Serper API)
  tools/email_tool.py           # שליחת מייל (SendGrid)
  web_server.py                 # Flask web server
  templates/index.html          # ממשק צ'אט בעברית
  tests/test_llm_connection.py  # בדיקת חיבור ל-LLM
  tests/test_email_sending.py   # בדיקת שליחת מייל
```

## התקנה

```bash
venv313\Scripts\python.exe -m pip install -r requirements.txt
```

## הגדרת .env

```
GOOGLE_AI_API_KEY=your-key
SERPER_API_KEY=your-key
SENDGRID_API_KEY=your-key
EMAIL_FROM=sender@example.com
EMAIL_TO=default-recipient@example.com
```

## בדיקות

```bash
# בדיקת חיבור ל-LLM
venv313\Scripts\python.exe src/bank_of_israel_ai/tests/test_llm_connection.py

# בדיקת שליחת מייל
venv313\Scripts\python.exe src/bank_of_israel_ai/tests/test_email_sending.py
```

## הפעלה

```bash
venv313\Scripts\python.exe -m bank_of_israel_ai
```

פתח בדפדפן: http://127.0.0.1:5000

הקלד שם מוצר + כתובת מייל, לדוגמה:
> מחשב נייד Dell ושלח ל-user@example.com
