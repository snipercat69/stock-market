#!/usr/bin/env python3
"""Daily stock market update script - comprehensive market coverage"""
import urllib.request
import json
from datetime import datetime

def get_stock_data():
    """Fetch stock market data via Yahoo Finance API"""
    
    tickers = [
        # === MAJOR INDICES ===
        ("^GSPC", "S&P 500", "index"),
        ("^DJI", "Dow Jones", "index"),
        ("^IXIC", "NASDAQ", "index"),
        ("^RUT", "Russell 2000", "index"),
        ("^VIX", "VIX (Fear Index)", "index"),
        ("^SOX", "PHLX Semiconductor", "index"),
        
        # === CRYPTO ===
        ("BTC-USD", "Bitcoin", "crypto"),
        ("ETH-USD", "Ethereum", "crypto"),
        ("SOL-USD", "Solana", "crypto"),
        
        # === COMMODITIES ===
        ("GC=F", "Gold", "commodity"),
        ("CL=F", "Oil (WTI)", "commodity"),
        ("SI=F", "Silver", "commodity"),
        ("NG=F", "Natural Gas", "commodity"),
        
        # === FOREX INDICATORS ===
        ("DX-Y.NYB", "US Dollar Index", "forex"),
        
        # === TECH LARGE-CAP ===
        ("AAPL", "Apple", "tech"),
        ("MSFT", "Microsoft", "tech"),
        ("GOOGL", "Alphabet (Google)", "tech"),
        ("AMZN", "Amazon", "tech"),
        ("META", "Meta", "tech"),
        ("NVDA", "NVIDIA", "tech"),
        ("TSLA", "Tesla", "tech"),
        ("AMD", "AMD", "tech"),
        ("INTC", "Intel", "tech"),
        ("CRM", "Salesforce", "tech"),
        ("ORCL", "Oracle", "tech"),
        ("ADBE", "Adobe", "tech"),
        ("PYPL", "PayPal", "tech"),
        ("NFLX", "Netflix", "tech"),
        ("DIS", "Disney", "tech"),
        ("CMCSA", "Comcast", "tech"),
        ("PEP", "PepsiCo", "consumer"),
        ("KO", "Coca-Cola", "consumer"),
        
        # === FINANCE ===
        ("JPM", "JPMorgan", "finance"),
        ("BAC", "Bank of America", "finance"),
        ("GS", "Goldman Sachs", "finance"),
        ("MS", "Morgan Stanley", "finance"),
        ("WFC", "Wells Fargo", "finance"),
        ("C", "Citigroup", "finance"),
        ("V", "Visa", "finance"),
        ("MA", "Mastercard", "finance"),
        ("AXP", "American Express", "finance"),
        ("COIN", "Coinbase", "finance"),
        ("SQ", "Block (Square)", "finance"),
        
        # === AI / CHIP STOCKS ===
        ("AVGO", "Broadcom", "chip"),
        ("QCOM", "Qualcomm", "chip"),
        ("TXN", "Texas Instruments", "chip"),
        ("MU", "Micron", "chip"),
        ("ASML", "ASML", "chip"),
        ("AMAT", "Applied Materials", "chip"),
        ("LRCX", "Lam Research", "chip"),
        
        # === EV / ENERGY / SOLAR ###
        ("SPWR", "SunPower", "energy"),
        ("ENPH", "Enphase Energy", "energy"),
        ("FSLR", "First Solar", "energy"),
        ("SEDG", "SolarEdge", "energy"),
        ("NEE", "NextEra Energy", "energy"),
        ("IBDRY", "iShares MSCI World ETF", "etf"),
        
        # === ETFs ###
        ("QQQ", "Invesco QQQ", "etf"),
        ("SPY", "SPDR S&P 500 ETF", "etf"),
        ("QQQ", "Nasdaq-100 ETF", "etf"),
        ("IWM", "iShares Russell 2000 ETF", "etf"),
        ("VTI", "Vanguard Total Market ETF", "etf"),
        ("ARKK", "ARK Innovation ETF", "etf"),
        ("XOM", "ExxonMobil", "energy"),
        ("CVX", "Chevron", "energy"),
        
        # === PHARMA / HEALTH ###
        ("UNH", "UnitedHealth", "health"),
        ("JNJ", "Johnson & Johnson", "health"),
        ("PFE", "Pfizer", "health"),
        ("ABBV", "AbbVie", "health"),
        ("MRK", "Merck", "health"),
        ("LLY", "Eli Lilly", "health"),
        ("BMY", "Bristol Myers", "health"),
        ("ABT", "Abbott Labs", "health"),
        ("TMO", "Thermo Fisher", "health"),
        ("DHR", "Danaher", "health"),
        ("ISRG", "Intuitive Surgical", "health"),
        
        # === DEFENSE ###
        ("BA", "Boeing", "defense"),
        ("LMT", "Lockheed Martin", "defense"),
        ("RTX", "Raytheon", "defense"),
        ("NOC", "Northrop Grumman", "defense"),
        
        # === RETAIL / GAMES ###
        ("WMT", "Walmart", "retail"),
        ("COST", "Costco", "retail"),
        ("TGT", "Target", "retail"),
        ("LOW", "Lowe's", "retail"),
        ("HD", "Home Depot", "retail"),
        ("DKNG", "DraftKings", "gaming"),
        ("MCD", "McDonald's", "retail"),
        ("SBUX", "Starbucks", "retail"),
        ("NKE", "Nike", "retail"),
        
        # === REAL ESTATE / INFRA ===
        ("AMT", "American Tower", "reit"),
        ("PLD", "Prologis", "reit"),
        ("CCI", "Crown Castle", "reit"),
        ("EQIX", "Equinix", "reit"),
        
        # === TELECOM ###
        ("T", "AT&T", "telecom"),
        ("VZ", "Verizon", "telecom"),
        ("TMUS", "T-Mobile", "telecom"),
        
        # === SPAC / TRENDING ###
        ("GME", "GameStop", "meme"),
        ("AMC", "AMC Theaters", "meme"),
        ("PLTR", "Palantir", "tech"),
        ("SNOW", "Snowflake", "tech"),
        ("UBER", "Uber", "tech"),
        ("LYFT", "Lyft", "tech"),
        ("ABNB", "Airbnb", "tech"),
    ]
    
    results = {}
    errors = []
    
    for ticker, name, category in tickers:
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=5d"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read().decode())
                result = data['chart']['result']
                if not result:
                    continue
                r = result[0]
                closes = r['indicators']['quote'][0].get('close', [])
                
                if closes and len(closes) >= 2:
                    current_price = closes[-1]
                    prev_close = None
                    for c in reversed(closes[:-1]):
                        if c is not None:
                            prev_close = c
                            break
                    
                    if prev_close and current_price and current_price > 0:
                        change = current_price - prev_close
                        change_pct = (change / prev_close) * 100
                        
                        if current_price >= 10000:
                            price_fmt = f"${current_price:,.0f}"
                        elif current_price >= 1000:
                            price_fmt = f"${current_price:,.2f}"
                        else:
                            price_fmt = f"${current_price:.2f}"
                        
                        results[name] = {
                            'price': current_price,
                            'change': change,
                            'change_pct': change_pct,
                            'price_fmt': price_fmt,
                            'category': category
                        }
        except Exception as e:
            errors.append((ticker, name, str(e)[:50]))
    
    return results, errors

def format_update(results, errors=None):
    if not results:
        return "⚠️ Could not fetch stock data. Please try again later."
    
    now = datetime.now().strftime("%B %d, %Y")
    
    lines = [
        f"📊 **Market Summary — {now}**",
        "══════════════════════════════════",
    ]
    
    def print_group(title, group):
        if not group:
            return
        lines.append(f"\n__{title}__")
        for name, data in sorted(group.items(), key=lambda x: abs(x[1]['change_pct']), reverse=True):
            arrow = "🟢" if data['change'] >= 0 else "🔴"
            sign = "+" if data['change'] >= 0 else ""
            lines.append(
                f"{arrow} {name}: {data['price_fmt']}  "
                f"({sign}{data['change']:.2f} / {sign}{data['change_pct']:.2f}%)"
            )
    
    groups = {
        '📈 Major Indices': {k: v for k, v in results.items() if v['category'] == 'index'},
        '₿ Crypto': {k: v for k, v in results.items() if v['category'] == 'crypto'},
        '🪙 Commodities': {k: v for k, v in results.items() if v['category'] == 'commodity'},
        '💻 Tech & AI': {k: v for k, v in results.items() if k in (
            'Apple', 'Microsoft', 'Alphabet (Google)', 'Amazon', 'Meta', 'NVIDIA', 'Tesla', 
            'AMD', 'Intel', 'Salesforce', 'Oracle', 'Adobe', 'PayPal', 'Netflix', 
            'Disney', 'Comcast', 'Palantir', 'Snowflake', 'Uber', 'Lyft', 'Airbnb'
        )},
        '🔮 Chips & Semiconductors': {k: v for k, v in results.items() if v['category'] == 'chip'},
        '🏦 Finance': {k: v for k, v in results.items() if v['category'] == 'finance'},
        '⚡ Energy & Solar': {k: v for k, v in results.items() if v['category'] == 'energy'},
        '🏥 Healthcare': {k: v for k, v in results.items() if v['category'] == 'health'},
        '✈️ Defense': {k: v for k, v in results.items() if v['category'] == 'defense'},
        '🛒 Retail & Consumer': {k: v for k, v in results.items() if v['category'] in ('retail', 'consumer')},
        '🎮 Gaming & Meme': {k: v for k, v in results.items() if v['category'] in ('gaming', 'meme')},
        '🏠 REITs & Infra': {k: v for k, v in results.items() if v['category'] == 'reit'},
        '📡 Telecom': {k: v for k, v in results.items() if v['category'] == 'telecom'},
    }
    
    for title, group in groups.items():
        print_group(title, group)
    
    lines.extend([
        "\n══════════════════════════════════",
        f"_Sources: Yahoo Finance (delayed prices)_ | Tracked: {len(results)} assets"
    ])
    
    return "\n".join(lines)

if __name__ == "__main__":
    results, errors = get_stock_data()
    output = format_update(results, errors)
    print(output)
    
    if errors:
        print(f"\n⚠️ Errors loading {len(errors)} tickers")
    
    with open("/home/guy/.openclaw/workspace/apps/stock-market/latest_update.txt", "w") as f:
        f.write(output)