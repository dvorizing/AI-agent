# Setup Guide: Real Google Search with CREWAI SerperDevTool

## Step 1: Get Serper API Key (Free)

1. Go to https://serper.dev
2. Sign up for a free account
3. Get your API key (you get 50 free searches/month)
4. Copy your API key

## Step 2: Configure .env

Update `.env` file with your real Serper API key:

```
SERPER_API_KEY=your-actual-api-key-here
```

Replace `your-actual-api-key-here` with the API key from Step 1.

## Step 3: How It Works

The system now uses **CREWAI's SerperDevTool** for real Google searches:

- **search_web()** in `search_tool.py` → Uses Serper API → Real Google results
- **search_product()** CREWAI tool → Calls search_web() → Passes to Gemini LLM
- **run_procurement_agent()** → CREWAI orchestrates the search

## Step 4: Test It

```bash
# Option 1: Web interface  
python -m bank_of_israel_ai

# Option 2: CLI
python -m bank_of_israel_ai --cli

# Option 3: Direct query
python -m bank_of_israel_ai --query "Lenovo laptop"
```

## Features

✅ **Real Google Search** - Uses Serper API for actual internet search
✅ **CREWAI Integration** - Official CREWAI tool (SerperDevTool)
✅ **Hebrew Support** - Works with Hebrew and English queries
✅ **Fallback** - Returns empty results if no Serper key (can add fallback)
✅ **Smart Parsing** - Handles multiple response formats from Serper

## Free Tier Limits

- **50 searches/month** (free tier)
- Each search returns top 10 results
- Perfect for testing and development

## Example Queries

```
Input: "תחפש לי Lenovo ותשלח ל DVORIZING@GMAIL.COM"
Output: Real Google search results + email delivery

Input: "diamond chain"
Output: Top suppliers from Google search

Input: "best iPhone prices 2026"  
Output: Current market prices from real searches
```

## Troubleshooting

If you get "SERPER_API_KEY not found":
1. Make sure you added the key to `.env`
2. Restart the application
3. Check that the API key is correct

If search returns no results:
1. Check your Serper API quota (50/month free)
2. Verify internet connection
3. Try a different search query

## Next Steps

Once working:
1. Integrate real pricing data from search results
2. Add price comparison logic
3. Generate PDF procurement reports
4. Set up email notifications

---

Good luck! Your system now has real Google search capabilities! 🎉
