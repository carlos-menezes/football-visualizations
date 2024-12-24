from matplotlib import pyplot as plt
import pandas as pd
from pandas import DataFrame
from statsbombpy import sb as statsbomb
from mplsoccer import Pitch

SEASON_ID = 27 # 2015/2016
COMPETITION_ID = 2 # Premier League
TEAM_NAME = 'Leicester City'
PLAYER_NAME = 'Jamie Vardy'
EVENT_TYPE = 'Shot'

def plot_shot_clusters(shots: DataFrame):
    outcome_counts = shots['shot_outcome'].value_counts(normalize=True) * 100
    print("Shot Outcome Percentages:")
    print(outcome_counts)

    pitch = Pitch(pitch_type='statsbomb', line_color='black')  # StatsBomb-style pitch
    fig, ax = pitch.draw(figsize=(10, 8))

    outcome_markers = {
        'Blocked': 'd',
        'Goal': 'o', 
        'Off T': 'x',
        'Post': '^', 
        'Saved': 's',
    }

    # Use the JET colormap for color based on shot xG (Expected Goals)
    colormap = plt.get_cmap('magma')

    # Plot each outcome type
    for outcome, marker in outcome_markers.items():
        filtered_shots = shots[shots['shot_outcome'] == outcome]
        locations = filtered_shots['location'].tolist()
        xG = filtered_shots['shot_statsbomb_xg']

        if locations:
            x, y = zip(*locations)

            norm = plt.Normalize(min(xG), max(xG))
            colors = [colormap(norm(val)) for val in xG]  # Get colors based on xG value

            pitch.scatter(
                x, y, 
                s=[500 * value for value in xG],  # Size based on xG
                c=colors,  # Color based on xG
                marker=marker,  # Different marker for each shot outcome
                label=outcome, 
                ax=ax, 
                alpha=0.7,  
                linewidth=0.8,
                edgecolors='black'
            )

    # Add minimalist legend
    ax.legend(
        loc='upper center',
        bbox_to_anchor=(0.5, -0.001),  # Adjust position slightly lower
        ncol=5,  # Arrange in a single row
        frameon=False,  # No border for the legend
        fontsize=8,  # Smaller font size
        title_fontsize=10  # Title font size
    )

    # Clean minimalist title
    plt.title(f"Jamie Vardy's Shot Clusters (2015/2016)", fontsize=24, fontweight='bold', family='SF Pro Display')

    ax.set_xticks([])  # Remove x-axis ticks
    ax.set_yticks([])  # Remove y-axis ticks

    plt.tight_layout()
    plt.show()

def extract_player_events(match_events: DataFrame, event_type: str):
    player_events = match_events[(match_events['player'] == PLAYER_NAME) & (match_events['type'] == event_type)]
    return player_events

def main():
    matches: DataFrame = statsbomb.matches(competition_id=COMPETITION_ID, season_id=SEASON_ID)
    leicester_city_matches = matches[(matches['home_team'] == TEAM_NAME) | (matches['away_team'] == TEAM_NAME)]
    
    all_player_events = []

    for match_index, match in leicester_city_matches.iterrows():
        match_events: DataFrame = statsbomb.events(match_id=match['match_id'])
        player_events = extract_player_events(match_events, EVENT_TYPE)
        
        all_player_events.append(player_events)
        if match_index == 3:
            break

    all_player_events = pd.concat(all_player_events, ignore_index=True)
    plot_shot_clusters(all_player_events)
    return all_player_events

if __name__ == '__main__':
    main()