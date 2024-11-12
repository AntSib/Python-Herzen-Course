import matplotlib.pyplot as plt
import urllib.request
from bs4 import BeautifulSoup


# Getting data
data = urllib.request.urlopen("https://wttr.in/saint-petersburg").read().decode('utf-8')

# Parsing
soup = BeautifulSoup(data, 'html.parser')

# There is no way to get all data automatically.

# something very odd happens with finding items for temp50
# temp50 is ['0', '0', '+1', '1', '+1', '+1'], then it must be ['+1', '0', '+1', '+1', '1', '+1', '+1']
temp49 = soup.find_all('span', class_="ef049")
temp50 = soup.find_all('span', class_="ef050")
# THIS WILL NOT WORK FOR ANY OTHER DAY THAN 04.11.2024
# BECAUSE TEMPERATURES WILL HAVE DIFFERENT SPAN CLASS

temp49 = list(map(lambda x: x.string, temp49))
temp50 = list(map(lambda x: x.string, temp50))

# for today
today_morning = soup.find('span', class_="ef051").string
today_noon = temp49[0]
today_evening = temp50[0]
today_night = temp50[2]

# for tomorrow
tomorrow_morning = temp50[4]
tomorrow_noon = temp49[1]
tomorrow_evening = temp50[4]
today_night = temp50[5]

temp_today = [today_morning, today_noon, today_evening, today_night]
temp_tomorrow = [tomorrow_morning, tomorrow_noon, tomorrow_evening, today_night]

for i in range(len(temp_today)):
    temp_today[i] = int(temp_today[i])
    temp_tomorrow[i] = int(temp_tomorrow[i])


# Plotting

# Create subplots
fig, axs = plt.subplots(1, 2, figsize=(10, 5))
time_of_day = ['Morning', 'Noon', 'Evening', 'Night']  # Labels for the x-axis

# Bar graph for today's temperatures
axs[0].bar(range(len(temp_today)), temp_today, color='blue')    # Make 4 bars
axs[0].set_title('Temperatures Today')                          # Set title
axs[0].set_xlabel('Time Interval')                              # Set x-axis label
axs[0].set_ylabel('Temperature (°C)')                           # Set y-axis label
axs[0].set_xticks(range(len(temp_today)))                       # Set x-axis ticks (bars)
axs[0].set_xticklabels(time_of_day)                             # Set x-axis tick labels
axs[0].axhline(0, color='black', linewidth=1, linestyle='--')  # Zero line

# Bar graph for tomorrow's temperatures
axs[1].bar(range(len(temp_tomorrow)), temp_tomorrow, color='orange')
axs[1].set_title('Temperatures Tomorrow')
axs[1].set_xlabel('Time Interval')
axs[1].set_ylabel('Temperature (°C)')
axs[1].set_xticks(range(len(temp_tomorrow)))
axs[1].set_xticklabels(time_of_day)
axs[1].axhline(0, color='black', linewidth=1, linestyle='--')

# adjust layout
plt.tight_layout()

# Save the figure
plt.savefig('weather_temperatures.png')
