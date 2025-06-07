def get_stock_price(ticker: str, date: str) -> dict:
    """
    Retrieves the lowest and highest stock prices for a given ticker and date.
    Args:
    ticker: The stock ticker symbol, e.g., "IBM".
    date: The date in "YYYY-MM-DD" format for which you want to get stock prices.
    Returns:
    A dictionary containing the low and high stock prices on the given date.
    """
    print(f"Getting stock price for {ticker} on {date}")
    try:
        return {"low": 20, "high": 35}
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return {"low": "none", "high": "none"}
