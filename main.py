import tkinter as tk
from tkinter import ttk
import requests

API_KEY = "YOUR API KEY"  # app api key
BASE_URL = "https://api.hypixel.net/"
MOJANG_API_URL = "https://api.mojang.com/users/profiles/minecraft/"


def get_uuid_from_name(player_name):
    response = requests.get(MOJANG_API_URL + player_name)
    if response.status_code == 200:
        return response.json()['id']
    elif response.status_code == 204:  # No content, player not found
        return None
    else:
        print(f"Failed to get UUID. Status code: {response.status_code}")
        return None


def get_player_data(player_identifier):
    headers = {
        "API-Key": API_KEY
    }

    # Check if the input is likely a UUID (32 characters without dashes or 36 with)
    if len(player_identifier.replace('-', '')) == 32:
        uuid = player_identifier.replace('-', '')
    else:
        uuid = get_uuid_from_name(player_identifier)
        if uuid is None:
            print("Could not find UUID for the given player name.")
            return None

    response = requests.get(BASE_URL + "player", headers=headers, params={'uuid': uuid})
    data = response.json()

    if not data.get('success', False):
        print(f"Error: {data.get('cause', 'Unknown Error')}")
        return None

    return data.get('player')

def calculate_overall_stats(stats):
    keys_to_sum = ['wins', 'losses', 'kills', 'deaths', 'final_kills', 'final_deaths', 'beds_broken', 'beds_lost']
    overall = {key: 0 for key in keys_to_sum}
    overall['winstreak'] = 0  # Initialize winstreak

    for mode in ['', 'eight_one_', 'eight_two_', 'four_three_', 'four_four_']:
        prefix = mode if mode else "bedwars_"
        for key in keys_to_sum:
            stat_key = f"{prefix}{key}_bedwars"
            if stat_key in stats and not any(dream in stat_key for dream in
                                             ['rush', 'ultimate', 'lucky', 'voidless', 'armed', 'underworld', 'swap']):
                overall[key] += stats.get(stat_key, 0)

        # Check for winstreak across all modes including Dream modes
        ws_key = f"{mode}winstreak"
        if ws_key in stats:
            overall['winstreak'] = max(overall['winstreak'], stats.get(ws_key, 0))

    return overall

def setup_frame(frame, stats, is_overall=False):
    scroll = tk.Scrollbar(frame)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    text = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scroll.set)
    text.pack(fill=tk.BOTH, expand=True)
    scroll.config(command=text.yview)

    for stat, value in stats.items():
        if is_overall:
            if stat in ['wins', 'losses', 'kills', 'deaths', 'final_kills', 'final_deaths', 'beds_broken', 'beds_lost', 'winstreak']:
                display_stat = stat.capitalize() if stat != 'winstreak' else 'Winstreak'
                text.insert(tk.END, f"{display_stat}: {value}\n")
        else:
            if stat != 'winstreak':
                display_stat = stat.replace('_bedwars', '').capitalize()
                text.insert(tk.END, f"{display_stat}: {value}\n")
            elif 'winstreak' in stats:
                text.insert(tk.END, f"Winstreak: {value}\n")

def add_dream_nested_tabs(parent, stats):
    dream_tabs = ttk.Notebook(parent)

    for size in ['Doubles', '4v4v4v4']:
        size_tab = ttk.Frame(dream_tabs)
        dream_tabs.add(size_tab, text=size)
        size_nested = ttk.Notebook(size_tab)

        dream_modes = ['rush', 'ultimate', 'lucky', 'voidless', 'armed', 'underworld', 'swap']
        for mode in dream_modes:
            mode_prefix = f"eight_two_{mode}_" if size == 'Doubles' else f"four_four_{mode}_"
            mode_stats = {k.replace(mode_prefix, ''): v for k, v in stats.items() if k.startswith(mode_prefix)}
            if mode_stats:
                frame = ttk.Frame(size_nested)
                size_nested.add(frame, text=mode)
                setup_frame(frame, mode_stats)

        size_nested.pack(fill=tk.BOTH, expand=True)

    dream_tabs.pack(fill=tk.BOTH, expand=True)

def add_nested_tabs(parent, stats):
    nested_tabs = ttk.Notebook(parent)
    for mode in ['Overall', 'Solo', 'Doubles', '3v3v3v3', '4v4v4v4']:
        frame = ttk.Frame(nested_tabs)
        if mode == 'Overall':
            mode_stats = calculate_overall_stats(stats)
            nested_tabs.add(frame, text=mode)
            setup_frame(frame, mode_stats, is_overall=True)
        else:
            mode_prefix = {
                'Solo': 'eight_one_',
                'Doubles': 'eight_two_',
                '3v3v3v3': 'four_three_',
                '4v4v4v4': 'four_four_'
            }[mode]
            mode_stats = {
                k.replace(mode_prefix, ''): v for k, v in stats.items()
                if k.startswith(mode_prefix) and not any(m in k for m in ['rush', 'ultimate', 'lucky', 'voidless', 'armed', 'underworld', 'swap'])
            }
            nested_tabs.add(frame, text=mode)
            setup_frame(frame, mode_stats)
    nested_tabs.pack(fill=tk.BOTH, expand=True)

def display_gui():
    def show_stats():
        player_identifier = name_entry.get()
        player_data = get_player_data(player_identifier)
        if player_data:
            for tab in tabs.tabs():
                tabs.forget(tab)
            bedwars_stats = player_data.get('stats', {}).get('Bedwars', {})
            bedwars_tab = ttk.Frame(tabs)
            dream_tab = ttk.Frame(tabs)
            tabs.add(bedwars_tab, text="BedWars")
            tabs.add(dream_tab, text="Dream")

            add_nested_tabs(bedwars_tab, bedwars_stats)
            add_dream_nested_tabs(dream_tab, bedwars_stats)

    root = tk.Tk()
    root.title("Hypixel BedWars Stats")

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(frame, text="Enter Player Name or UUID:").grid(column=0, row=0, sticky=tk.W, pady=5)
    name_entry = ttk.Entry(frame, width=40)
    name_entry.grid(column=1, row=0, pady=5)

    ttk.Button(frame, text="Get Stats", command=show_stats).grid(column=2, row=0, pady=5)

    tabs = ttk.Notebook(frame)
    tabs.grid(column=0, row=1, columnspan=3, pady=5, sticky=(tk.N, tk.S, tk.E, tk.W))
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)

    root.mainloop()

display_gui()
