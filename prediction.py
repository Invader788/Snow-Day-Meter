
def calculate_probability(weather):
    snow = weather["snowfall"]
    temperature = weather["temperature"]
    wind = weather["wind"]
    freezing_rain = weather["freezing_rain"]

    score = 5

    # Overnight snowfall
    if snow >= 15:
        score += 45
    elif snow >= 10:
        score += 35
    elif snow >= 5:
        score += 23
    elif snow >= 2:
        score += 12

    # Freezing rain
    score += freezing_rain * 0.30

    # Strong winds
    if wind >= 60:
        score += 15
    elif wind >= 40:
        score += 10
    elif wind >= 30:
        score += 5

    # Extreme cold
    if temperature <= -20:
        score += 15
    elif temperature <= -15:
        score += 10
    elif temperature <= -10:
        score += 5

    return round(min(score, 95))

