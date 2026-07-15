TYPE_META = {
    "bar-chart": {
        "name": "Bar Chart",
        "emoji": "chart",
        "description": "Compare quantities across categories or time periods",
    },
    "line-graph": {
        "name": "Line Graph",
        "emoji": "chart",
        "description": "Show trends and changes over time",
    },
    "pie-chart": {
        "name": "Pie Chart",
        "emoji": "pie",
        "description": "Show proportions and percentages of a whole",
    },
    "table": {
        "name": "Table",
        "emoji": "clipboard",
        "description": "Summarise numerical data in rows and columns",
    },
    "process-diagram": {
        "name": "Process Diagram",
        "emoji": "process",
        "description": "Describe stages in a cycle or linear process",
    },
    "map": {
        "name": "Map",
        "emoji": "map",
        "description": "Describe changes to a location over time",
    },
    "mixed-charts": {
        "name": "Mixed Charts",
        "emoji": "trend-down",
        "description": "Two different chart types shown together",
    },
}

TASK_INSTRUCTION = (
    "Summarise the information by selecting and reporting the main features, "
    "and make comparisons where relevant. Write at least 150 words."
)

QUESTIONS = [
    {
        "id": 1,
        "type": "bar-chart",
        "title": "Transport to Work",
        "prompt": "The chart below shows the percentage of households in one country that used selected forms of transport to travel to work in 2005 and 2015.",
        "chart": {
            "kind": "bar",
            "title": "Percentage of households using each transport type (%)",
            "groups": ["Car", "Public transport", "Bicycle", "Walking", "Motorcycle"],
            "series": [
                {"name": "2005", "color": "#1e3a5f", "values": [67, 24, 8, 18, 5]},
                {"name": "2015", "color": "#4b9cf0", "values": [71, 31, 15, 12, 3]},
            ],
        },
    },
    {
        "id": 2,
        "type": "bar-chart",
        "title": "Energy Consumption by Sector",
        "prompt": "The chart below shows energy consumption in millions of tonnes of oil equivalent across four sectors in a country in 1990, 2000, and 2010.",
        "chart": {
            "kind": "bar",
            "title": "Energy consumption by sector (million tonnes oil equivalent)",
            "groups": ["Industry", "Transport", "Residential", "Services"],
            "series": [
                {"name": "1990", "color": "#1e3a5f", "values": [62, 38, 44, 18]},
                {"name": "2000", "color": "#4b9cf0", "values": [58, 50, 41, 24]},
                {"name": "2010", "color": "#2d6a0a", "values": [49, 61, 37, 29]},
            ],
        },
    },
    {
        "id": 3,
        "type": "bar-chart",
        "title": "University Subjects by Gender",
        "prompt": "The chart below shows the percentage of male and female students enrolled in four university subject areas in a country in 2018.",
        "chart": {
            "kind": "bar",
            "title": "Students enrolled by subject area (%)",
            "groups": ["Engineering", "Education", "Medicine", "Law"],
            "series": [
                {"name": "Male", "color": "#1e3a5f", "values": [78, 28, 44, 51]},
                {"name": "Female", "color": "#4b9cf0", "values": [22, 72, 56, 49]},
            ],
        },
    },
    {
        "id": 4,
        "type": "line-graph",
        "title": "Internet Usage by Age Group",
        "prompt": "The line graph shows internet usage percentages by age group from 2010 to 2020.",
        "chart": {
            "kind": "line",
            "title": "Internet usage by age group (%)",
            "x": ["2010", "2012", "2014", "2016", "2018", "2020"],
            "series": [
                {"name": "16–24", "color": "#1e3a5f", "values": [72, 80, 87, 93, 96, 99]},
                {"name": "25–44", "color": "#4b9cf0", "values": [54, 63, 71, 80, 87, 93]},
                {"name": "45–64", "color": "#2d6a0a", "values": [28, 37, 48, 58, 68, 78]},
                {"name": "65+", "color": "#b45309", "values": [8, 13, 20, 29, 38, 50]},
            ],
        },
    },
    {
        "id": 5,
        "type": "line-graph",
        "title": "Unemployment Rates",
        "prompt": "The line graph compares unemployment rates in three countries between 2008 and 2018.",
        "chart": {
            "kind": "line",
            "title": "Unemployment rates (%)",
            "x": ["2008", "2010", "2012", "2014", "2016", "2018"],
            "series": [
                {"name": "Country A", "color": "#1e3a5f", "values": [5, 8, 11, 9, 7, 4]},
                {"name": "Country B", "color": "#4b9cf0", "values": [4, 5, 5.5, 5, 4.5, 3.5]},
                {"name": "Country C", "color": "#b91c1c", "values": [6, 12, 22, 26, 22, 16]},
            ],
        },
    },
    {
        "id": 6,
        "type": "line-graph",
        "title": "Average House Prices",
        "prompt": "The line graph shows average house prices (in thousands USD) in four cities from 2000 to 2020.",
        "chart": {
            "kind": "line",
            "title": "Average house prices (thousand USD)",
            "x": ["2000", "2004", "2008", "2012", "2016", "2020"],
            "series": [
                {"name": "City A", "color": "#1e3a5f", "values": [180, 220, 310, 260, 340, 490]},
                {"name": "City B", "color": "#4b9cf0", "values": [120, 145, 190, 170, 220, 310]},
                {"name": "City C", "color": "#2d6a0a", "values": [95, 110, 130, 115, 145, 195]},
                {"name": "City D", "color": "#b45309", "values": [200, 280, 420, 340, 390, 520]},
            ],
        },
    },
    {
        "id": 7,
        "type": "pie-chart",
        "title": "Energy Sources 1990 vs 2020",
        "prompt": "The two pie charts compare energy sources in 1990 and 2020.",
        "chart": {
            "kind": "pie",
            "title": "Energy sources (%)",
            "left_year": "1990",
            "right_year": "2020",
            "labels": ["Coal", "Gas", "Nuclear", "Renewables", "Other"],
            "left": [45, 28, 18, 5, 4],
            "right": [18, 25, 20, 32, 5],
        },
    },
    {
        "id": 8,
        "type": "pie-chart",
        "title": "Household Spending 2000 vs 2020",
        "prompt": "The two pie charts compare household spending categories in 2000 and 2020.",
        "chart": {
            "kind": "pie",
            "title": "Household spending composition (%)",
            "left_year": "2000",
            "right_year": "2020",
            "labels": ["Housing", "Food", "Transport", "Leisure", "Other"],
            "left": [30, 28, 15, 12, 15],
            "right": [38, 19, 17, 18, 8],
        },
    },
    {
        "id": 9,
        "type": "table",
        "title": "International Tourist Arrivals",
        "prompt": "The table below shows international tourist arrivals by region in 2000, 2010 and 2020, with the overall change from 2000 to 2020.",
        "chart": {
            "kind": "table",
            "title": "International tourist arrivals",
            "headers": ["Region", "2000", "2010", "2020", "Change 2000–2020"],
            "rows": [
                ["Europe", "386m", "478m", "312m", "↓ −19%"],
                ["Asia Pacific", "110m", "205m", "168m", "↑ +53%"],
                ["Americas", "128m", "150m", "98m", "↓ −23%"],
                ["Middle East", "24m", "61m", "18m", "↓ −25%"],
                ["Africa", "28m", "50m", "38m", "↑ +36%"],
            ],
        },
    },
    {
        "id": 10,
        "type": "table",
        "title": "Working Hours and Productivity",
        "prompt": "The table compares average weekly working hours, GDP per worker, paid holiday days and minimum wage in five countries.",
        "chart": {
            "kind": "table",
            "title": "Working hours and productivity",
            "headers": ["Country", "Avg weekly hours", "GDP per worker", "Paid holiday days", "Min wage ($/hr)"],
            "rows": [
                ["Germany", "34.2", "$82k", "30 days", "$12.00"],
                ["USA", "38.6", "$119k", "10 days", "$7.25"],
                ["Japan", "39.8", "$47k", "20 days", "$9.10"],
                ["France", "35.1", "$72k", "25 days", "$11.40"],
                ["Mexico", "43.2", "$19k", "6 days", "$1.10"],
            ],
        },
    },
    {
        "id": 11,
        "type": "process-diagram",
        "title": "Water Treatment Process",
        "prompt": "The process diagram shows how water is treated before being distributed to households.",
        "chart": {
            "kind": "process",
            "title": "Water treatment process",
            "steps": [
                "River or reservoir — raw water source",
                "Screening — large debris removed",
                "Sedimentation tank — particles settle",
                "Filtration — sand and gravel layers",
                "Chemical treatment — chlorine and fluoride added",
                "Storage reservoir — purified water stored",
                "Distribution network — piped to homes",
            ],
        },
    },
    {
        "id": 12,
        "type": "process-diagram",
        "title": "Glass Recycling Process",
        "prompt": "The process diagram illustrates the stages of glass bottle recycling.",
        "chart": {
            "kind": "process",
            "title": "Glass recycling process",
            "steps": [
                "Glass bottles collected from households",
                "Transported to recycling centre",
                "Sorted by colour: clear, green, brown",
                "Crushed into small pieces called cullet",
                "Cullet melted in furnace at 1500°C",
                "Moulded into new bottles",
                "Quality checked and labelled",
                "Distributed to shops and consumers",
            ],
        },
    },
    {
        "id": 13,
        "type": "map",
        "title": "Grantley Town: 1990 vs 2030",
        "prompt": "The maps show Grantley Town in 1990 and the planned layout for 2030.",
        "chart": {
            "kind": "map",
            "title": "Grantley Town: 1990 vs 2030 (planned)",
            "left_label": "1990",
            "right_label": "2030",
            "left": ["Town Hall", "Market", "Old Factory", "Park", "Station", "Farmland"],
            "right": ["Town Hall", "Shopping Centre", "Apartments", "Expanded Park", "Station", "Business Park"],
        },
    },
    {
        "id": 14,
        "type": "map",
        "title": "Island Resort Development",
        "prompt": "The maps illustrate an island before and after tourism development.",
        "chart": {
            "kind": "map",
            "title": "Island resort development",
            "left_label": "Before",
            "right_label": "After",
            "left": ["Beach", "Forest", "Coral reef", "Hills", "Village", "Farmland"],
            "right": ["Beach and pier", "Hotel complex", "Water sports area", "Footpaths", "Reception", "Restaurant"],
        },
    },
    {
        "id": 15,
        "type": "mixed-charts",
        "title": "Population and GDP Growth",
        "prompt": "The mixed charts show population growth and GDP per capita from 1990 to 2020.",
        "chart": {
            "kind": "mixed",
            "title": "Population and GDP per capita growth",
            "x": ["1990", "1995", "2000", "2005", "2010", "2015", "2020"],
            "bars": [32, 38, 46, 56, 68, 80, 95],
            "line": [1.2, 1.8, 2.9, 4.1, 6.2, 8.8, 12.4],
        },
    },
]


def question_type_list():
    return list(TYPE_META.keys())


def get_questions_by_type(question_type):
    return [q for q in QUESTIONS if q["type"] == question_type]


def get_question(question_type, question_id):
    for q in QUESTIONS:
        if q["type"] == question_type and int(q["id"]) == int(question_id):
            return q
    return None
