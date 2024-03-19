from datetime import timedelta, timezone
import datetime
import pytz

from AemetAntartica import AemetAntartica

# Create AEMET API client
api_key = "your_api_key_here" ##insert API key here
aemet = AemetAntartica(api_key)

# Set time zone
tz = timezone("Europe/Madrid")

# Set date range
init_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SUTC")
end_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%SUTC")

# Set station and aggregation
station = "Meteo Station Gabriel de Castilla"
TimeAggregation = "Hourly"

# Retrieve data
df = aemet.get_data(init_date, end_date, station, TimeAggregation)

# Print data
print(df)