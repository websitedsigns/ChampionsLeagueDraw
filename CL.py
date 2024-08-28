import random
from collections import defaultdict, Counter
import altair as alt
import pandas as pd 

# Define the teams in each pot (adjusted for no same-country rule)
pot_1 = ['Bayern Munich', 'Borussia Dortmund', 'Real Madrid', 'PSG',
        'Inter Milan', 'RB Leipzig', 'FC Barcelona']

pot_2 = ['Bayer Leverkusen', 'Atletico Madrid', 'Atalanta', 'Benfica',
        'Juventus', 'Club Brugge', 'Shakhtar Donetsk', 'AC Milan']

pot_3 = ['Feyenoord', 'Sporting CP', 'Lille', 'PSV Eindhoven', 'Dinamo Zagreb',
        'RB Salzburg', 'Celtic FC', 'Young Boys', 'Bodo Glimt']

pot_4 = ['FC Midtjylland', 'AS Monaco', 'Sparta Prague', 'Aston Villa',
        'Bologna', 'Girona', 'Stuttgart', 'Sturm Graz', 'Stade Brestois']

# Exclude Aston Villa from Pot 4 for the draw
pot_4.remove('Aston Villa')

# Function to simulate one draw for Aston Villa (adjusted for no same-country rule)
def simulate_draw():
   opponents = defaultdict(list)

   # Draw two teams from each pot (adjusted)
   def draw_teams(pot, drawn_teams):
       selected_teams = []
       for _ in range(2):
           # Filter out already drawn teams and teams from the same country as already selected teams
           available_teams = [t for t in pot if t not in drawn_teams and not any(team.split()[-1] == t.split()[-1] for team in selected_teams)]
           team = random.choice(available_teams)
           selected_teams.append(team)
           drawn_teams.add(team)
       return selected_teams

   # Draw for each pot (excluding English teams)
   drawn_teams = set()
   opponents["Pot 1"].extend(draw_teams(pot_1, drawn_teams))
   opponents["Pot 2"].extend(draw_teams(pot_2, drawn_teams))
   opponents["Pot 3"].extend(draw_teams(pot_3, drawn_teams))
   opponents["Pot 4"].extend(draw_teams(pot_4, drawn_teams))

   return opponents

# Perform the simulation 100,000 times
def run_simulation(num_draws=5000000):
   simulations = [simulate_draw() for _ in range(num_draws)]

   # Count how often each team is drawn against Aston Villa
   results = {pot: Counter(team for sim in simulations for team in sim[pot]) for pot in ["Pot 1", "Pot 2", "Pot 3", "Pot 4"]}

   return results

# Run the simulation and print the results
if __name__ == "__main__":
   results = run_simulation()

   # List of pots to iterate over
   pots = ["Pot 1", "Pot 2", "Pot 3", "Pot 4"]

   # Create a horizontal concatenation of subplots
   fig = alt.hconcat() 

   # Iterate over each pot
   for i, pot in enumerate(pots):
       # Get the top two teams and their counts
       top_two = results[pot].most_common(2)
       df = pd.DataFrame(top_two, columns=["Team", "Count"])

       # Create a bar chart for the top two teams
       chart = alt.Chart(df).mark_bar().encode(
           x=alt.X('Team:N', axis=alt.Axis(labelAngle=-45)),
           y=alt.Y('Count:Q', title='Number of Times Drawn'),
           tooltip=['Team', 'Count']
       ).properties(
           title=f'Top 2 Teams from {pot}'
       )

       # Add the chart to the figure
       fig |= chart

   # Display the plot
   fig.show()  # Use fig.show() to display in VS Code