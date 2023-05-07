import customtkinter
from PIL import Image, ImageTk
import requests as requests

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "9ZCN4JMKEJGNMYJN"
NEWS_API_KEY = "4a30e3d7d1b54f8d96c6abcf9085f4dc"


def check_news():
    ticker_symbol = ticker.get()  # Gets the ticker in the input section in the GUI
    from_date = start_date.get()
    to_date = end_date.get()

    stock_params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": ticker_symbol,
        "apikey": STOCK_API_KEY,
    }
    response = requests.get(STOCK_ENDPOINT, params=stock_params)
    data = response.json()["Time Series (Daily)"]
    data_list = [value for (key, value) in data.items()]
    yesterday_data = data_list[0]
    yesterday_closing_price = yesterday_data["4. close"]

    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": ticker_symbol,
        "from_param": from_date,
        "to": to_date,
        "sortBy": "popularity",

    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    print(news_response)
    articles = news_response.json()["articles"]
    two_articles = articles[:10]

    formatted_articles = []
    for article in two_articles:
        headline = article["title"]
        brief = article["description"]
        url = article["url"]
        formatted_article = f"Header: {ticker_symbol} - {headline}\n\nBrief: {brief}\nLink: {url}\n\n\n\n"
        formatted_articles.append(formatted_article)

    # Clear the text box before displaying new information
    text_listbox.delete("1.0", "end")

    # Display the stock information and news articles in the text box
    text_listbox.insert("end", "News articles:\n\n\n")
    for formatted_article in formatted_articles:
        text_listbox.insert("end", formatted_article)


# GUI SETTING ==========================================================

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("700x600")
app.title("News Request App")

# Open and resize the image
image = Image.open("img.png")
image = image.resize((120, 50))

# Convert the image to a Tkinter PhotoImage object
photo = ImageTk.PhotoImage(image)

# Create the left frame
left_frame = customtkinter.CTkFrame(app, width=233, height=500)
left_frame.pack(side="left", fill="y", padx=5, pady=5)

# Create a label to display the image
label = customtkinter.CTkLabel(left_frame, image=photo, text="")
label.pack(pady=5)

# Ticker Entry Field
stock_label = customtkinter.CTkLabel(left_frame, text="\nTicker")
stock_label.pack(side="top", pady=2)

ticker = customtkinter.CTkEntry(left_frame, width=80)
ticker.pack(side="top", pady=5)

# Start date part
stock_label = customtkinter.CTkLabel(left_frame, text="\nStart Date")
stock_label.pack(side="top", pady=2)

start_date = customtkinter.CTkEntry(left_frame, width=80)
start_date.pack(side="top", pady=5)

# End date part
stock_label = customtkinter.CTkLabel(left_frame, text="\nEnd Date")
stock_label.pack(side="top", pady=2)

end_date = customtkinter.CTkEntry(left_frame, width=80)
end_date.pack(side="top", pady=5)

# Monitor button
check_button = customtkinter.CTkButton(left_frame, text="Monitor", command=check_news)
check_button.pack(side="top", pady=5)

# Create the right frame
right_frame = customtkinter.CTkFrame(app, width=467, height=500)
right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

# Add the scrollable listbox
text_listbox = customtkinter.CTkTextbox(right_frame)
text_listbox.pack(side="left", fill="both", expand=True)

# Add the scrollbar to the listbox
scrollbar = customtkinter.CTkScrollbar(right_frame)
scrollbar.configure(command=text_listbox.yview)

# Start the app
app.mainloop()
