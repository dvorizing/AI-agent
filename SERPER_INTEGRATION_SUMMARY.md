# System Update: Real Google Search Integration

## What Changed

### ✅ Before (Old System)
- ❌ Hardcoded example pricing data
- ❌ No real internet search
- ❌ Limited to pre-defined products

### ✅ After (New System)
- ✅ **Real Google Search** via Serper API
- ✅ **CREWAI SerperDevTool** - Official CREWAI integration
- ✅ **Any product query** - search for anything
- ✅ **Live internet data** - current market results

---

## Files Changed

### 1. `search_tool.py`
**Old:** 
```python
EXAMPLE_PRICES = { "lenovo laptop": [...], ... }
```

**New:**
```python
from crewai_tools import SerperDevTool

def search_web(query: str, max_results: int = 3) -> List[Dict[str, str]]:
    serper_tool = _get_serper_tool()
    search_results = serper_tool.run(query)
    # Parse results and return
```

### 2. `procurement_agent.py`
**Updated:**
- `search_product()` tool - Now handles Serper API results
- `create_search_task()` - Reflects real Google search capability
- Better error handling and formatting

### 3. `.env`
**Updated:**
```
SERPER_API_KEY=your-actual-api-key-here
```

---

## How to Use

### Step 1: Get Serper API Key (Free)
```
1. Visit https://serper.dev
2. Sign up (free account)
3. Copy your API key
4. 50 free searches/month
```

### Step 2: Update `.env`
```
SERPER_API_KEY=your-api-key-from-serper
```

### Step 3: Run the System
```bash
# Web interface
python -m bank_of_israel_ai

# CLI
python -m bank_of_israel_ai --cli

# Query mode
python -m bank_of_israel_ai --query "Lenovo laptop"
```

---

## Example Usage

### Input
```
User: "תחפש לי Lenovo laptop ותשלח ל DVORIZING@GMAIL.COM"
```

### Processing
1. Extract: Query = "Lenovo laptop" | Email = "DVORIZING@GMAIL.COM"
2. Search: CREWAI calls search_product()
3. Search uses: Serper API → Real Google search
4. Results: Top 3 actual retailers/sellers
5. Format: Gemini LLM processes results
6. Email: Sends to DVORIZING@GMAIL.COM

### Output
```
🔍 GOOGLE SEARCH RESULTS
============================================================

#1 - Lenovo Official Store - IdeaPad Laptops
   Link: https://www.lenovo.com/us/en/
   Preview: Find the best Lenovo IdeaPad laptop...

#2 - Amazon - Lenovo IdeaPad 3
   Link: https://www.amazon.com/...
   Preview: Lenovo IdeaPad 3 laptop with...

#3 - Best Buy - Lenovo Laptops
   Link: https://www.bestbuy.com/...
   Preview: Huge selection of Lenovo laptops...
```

---

## Architecture

```
User Input (Hebrew/English)
    ↓
Extract: query + email + send flag
    ↓
CREWAI Agent
    ├─ search_product() @tool
    │   └─ search_web()
    │       └─ SerperDevTool.run() ← REAL GOOGLE SEARCH
    │           └─ Serper API
    │               └─ Google Search Results
    │
    └─ Gemini LLM processes results
        └─ Formats professional report
    ↓
Email (optional) → DVORIZING@GMAIL.COM
```

---

## Response Format from Serper

### Result Dictionary
```python
{
    "url": "https://example.com",
    "title": "Product Title",
    "snippet": "Description...",
    # Optional fields:
    "price": "$399",  # When available
    "source": "Amazon"  # When available
}
```

---

## Benefits

| Feature | Old System | New System |
|---------|-----------|-----------|
| Search Type | Hardcoded | Real Google |
| Products | 3 examples | Unlimited |
| Currency | USD | Current market |
| Results | Static | Live data |
| Tool | Custom | CREWAI official |
| Hebrew | ✅ | ✅ |
| Email | ✅ | ✅ |
| CREWAI | ✅ | ✅ |

---

## Testing Commands

```bash
# Test search_web function directly
python -c "
from src.bank_of_israel_ai.tools.search_tool import search_web
results = search_web('Lenovo laptop')
for r in results:
    print(r['url'])
"

# Test with Agent
python -m bank_of_israel_ai --query 'diamond chain'

# Interactive web UI
python -m bank_of_israel_ai
# Then open http://localhost:5000
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "SERPER_API_KEY not found" | Add key to .env and restart |
| No search results | Check Serper quota (50/month free) or API key validity |
| Results not formatted | Check Serper API response format |
| Slow searches | Serper API rate limits - try fewer max_results |

---

## Next Steps (Optional)

1. **Price Extraction**: Parse results for price data
2. **Comparison**: Rank by price, rating, availability
3. **Notifications**: Alert on price drops
4. **Reports**: Generate PDF procurement reports
5. **History**: Track search history and trends

---

## Summary

Your procurement system now has **REAL GOOGLE SEARCH** capabilities instead of hardcoded data.

✅ Simply add your Serper API key to `.env` and you're ready!
✅ Fully compatible with CREWAI and Gemini LLM
✅ Works with Hebrew and English
✅ Professional formatting and email delivery

**The system is production-ready! 🚀**

