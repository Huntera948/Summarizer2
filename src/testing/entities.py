# Define the entities to exclude
exclude_entities = {'$100m', '1', '10', '12', '2', '2020', '2021', '2022', '2023', '2024', 'a busy week', 'a day', 'African', 'a week', 'a year', 'annual', 'BBC', 'Billboard', 'daily', 'decades', 'dozens', 'eight', 'first', 'five', 'Forbes Lifestyle Travel', 'four', 'Friday', 'half', 'hundreds', 'last month', 'last week', 'last year', 'millions', 'Monday', 'months', 'more than 30 years', 'more than a decade', 'more than 100', 'next week', 'next year', 'night', 'one', 'One', 'recent years', 'Saturday', 'second', 'Six', 'seventh', 'six', 'summer', 'Sunday', 'Sunday night', 'the coming months', 'the coming years', 'the day', 'the next five years', 'the next 10 years', 'the International Business Times', 'the past year', 'the Forbes Business Council', 'the Forbes Small Business Council', 'the next few years', 'the past 24 hours', 'the past few days', 'the past few weeks', 'the past few years', 'the past week', 'the summer', 'the week', 'the year', 'three-year', 'This week', 'third', 'thousands', 'this summer', 'this week', 'this weekend', 'this year', 'three', 'Thursday', 'Today', 'today', 'tomorrow', 'Tuesday', 'Two', 'two', 'two-day', 'Wednesday', 'Wednesday night', 'week', 'West', 'yesterday', 'year', 'years'}
# Define a map for normalizing entities
normalize_entities = {
    "African-Americans": "African American",
    "America": "United States",
    "American": "United States",
    "Americans": "United States",
    "BBC": "BBC News",
    "Britain": "United Kingdom",
    "Donald Trump's": "Donald Trump",
    "Trump": "Donald Trump",
    "England": "United Kingdom",
    "the European Union": "European Union",
    "EU": "European Union",
    "European": "Europe",
    "German": "Germany",
    "Iranian": "Iran",
    "Israeli": "Israel",
    "Japanese": "Japan",
    "Kyiv": "Ukraine",
    "Prince Harry": "Prince Harry & Meghan Markle",
    "Meghan Markle": "Prince Harry & Meghan Markle",
    "Nato": "NATO",
    "New York's": "New York",
    "North Korean": "North Korea",
    "Palestinians": "Palestine",
    "Palestinian": "Palestine",
    "Russian": "Russia",
    "Supreme Court": "The Supreme Court",
    "Tehran": "Iran",
    "the South China Sea": "South China Sea",
    "the Supreme Court’s": "The Supreme Court",
    "the Supreme Court": "The Supreme Court",
    "the Federal Reserve": "Federal Reserve",
    "the Middle East": "Middle East",
    "the United Nations": "United Nations",
    "the United States": "United States",
    "The United States": "United States",
    "the United States'": "United States",
    "the US Federal Reserve": "Federal Reserve",
    "the White House": "The White House",
    "Treasury": "US Treasury",
    "USA": "United States",
    "UK": "United Kingdom",
    "Ukrainian": "Ukraine",
    "UN": "United Nations",
    "US": "United States",
    "West Bank": "Palestine",
    "White House": "The White House",
}