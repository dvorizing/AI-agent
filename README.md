# BankOfIsrael AI

פרויקט פייתון למימוש רעיונות AI עבור בנק ישראל.

## מבנה בסיסי

- `src/` - קוד המקור של החבילה
- `tests/` - בדיקות יחידה
- `pyproject.toml` - קונפיגורציה של הפרויקט

## התחלה

1. התקן תלותים:

```bash
venv313\Scripts\python.exe -m pip install -r requirements.txt
```

> **חשוב:** הפרויקט משתמש ב-Python 3.13 (מותקן אוטומטית). ה-venv נקרא `venv313`.

2. הרץ בדיקות:

```bash
venv313\Scripts\python.exe -m pytest
```

## הרצת סוכן הרכש (Procurement Agent) עם CREWAI

1. התקן תלותים נוספות (כולל SendGrid):

```bash
venv313\Scripts\python.exe -m pip install -r requirements.txt
```

2. העתק את הקובץ `.env.example` ל־`.env` ומלא בו את ההגדרות (SendGrid API Key, OpenAI API Key, Serper API Key).

3. הרץ את הסוכן עם שאלה (בקשת רכש):

```bash
venv313\Scripts\python.exe -m bank_of_israel_ai --query "בקשת מחיר למדפסת לייזר"
```

4. אם תרצה רק להדפיס את התוצאות מבלי לשלוח מייל:

```bash
venv313\Scripts\python.exe -m bank_of_israel_ai --query "בקשת מחיר" --no-email
```

5. לשליחת מייל ללא אישור ידני (דילוג על HITL prompt):

```bash
venv313\Scripts\python.exe -m bank_of_israel_ai --query "בקשת מחיר" --no-confirm
```
