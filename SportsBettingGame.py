import random

class Team:
    def __init__(self, name):
        self.name = name
        self.wins = 0
        self.losses = 0
        self.games_played = 0

    def record(self):
        return f"{self.wins}-{self.losses}"

    def win_percentage(self):
        return self.wins / self.games_played if self.games_played > 0 else 0

    def update_record(self, result):
        if self.games_played < 5:  # Change to 5 for testing
            self.games_played += 1
            if result == 'win':
                self.wins += 1
            elif result == 'loss':
                self.losses += 1

    def reset(self):
        self.wins = 0
        self.losses = 0
        self.games_played = 0


class Match:
    def __init__(self, team1, team2):
        self.sport = "Football"  # Only one sport
        self.team1 = team1
        self.team2 = team2

        # Calculate odds based on the team standings
        self.odds_team1, self.odds_team2 = self.generate_odds()

        # Assign scores to ensure a winner
        self.score_team1, self.score_team2 = self.assign_scores()

        # Determine winner based on scores
        self.winner = 1 if self.score_team1 > self.score_team2 else 2

    def display_match(self):
        print(f"Sport: {self.sport}")
        print(f"{self.team1.name} (Record: {self.team1.record()}, Odds: {self.format_odds(self.odds_team1)})")
        print(f"vs")
        print(f"{self.team2.name} (Record: {self.team2.record()}, Odds: {self.format_odds(self.odds_team2)})")
        print(f"Score: {self.team1.name} {self.score_team1} - {self.team2.name} {self.score_team2}")

    def format_odds(self, odds):
        return f"+{odds}" if odds > 0 else str(odds)

    def generate_odds(self):
        win_percent_team1 = self.team1.win_percentage()
        win_percent_team2 = self.team2.win_percentage()

        if self.team1.wins > self.team2.wins:
            odds_team1 = -240 + (self.team1.wins - self.team2.wins) * 20
            odds_team2 = 100 + (self.team2.wins - self.team1.wins) * 20
        elif self.team1.wins < self.team2.wins:
            odds_team1 = 100 + (self.team1.wins - self.team2.wins) * 20
            odds_team2 = -240 + (self.team2.wins - self.team1.wins) * 20
        else:
            odds_team1 = 100
            odds_team2 = 100

        odds_team1 = max(-1000, min(odds_team1, 1000))
        odds_team2 = max(-1000, min(odds_team2, 1000))

        odds_team1 = odds_team1 if abs(odds_team1) >= 100 else (100 if odds_team1 > 0 else -100)
        odds_team2 = odds_team2 if abs(odds_team2) >= 100 else (100 if odds_team2 > 0 else -100)

        return odds_team1, odds_team2

    def assign_scores(self):
        score_team1 = random.randint(21, 50)  # Random score for team 1
        score_team2 = random.randint(0, score_team1 - 1)  # Random score for team 2, ensuring it's lower
        return score_team1, score_team2

    def calculate_winnings(self, odds, bet_amount):
        if odds > 0:
            return bet_amount + (bet_amount * (odds / 100))
        else:
            return bet_amount + (bet_amount * (100 / abs(odds)))

    def resolve_bet(self, chosen_team, bet_amount, player):
        if chosen_team == self.winner:
            if chosen_team == 1:
                winnings = self.calculate_winnings(self.odds_team1, bet_amount)
                self.team1.update_record('win')
                self.team2.update_record('loss')
            else:
                winnings = self.calculate_winnings(self.odds_team2, bet_amount)
                self.team2.update_record('win')
                self.team1.update_record('loss')
            player.add_winnings(winnings)
            print(f"You won! Payout: {winnings:.2f}")
        else:
            print("You lost the bet.")
            if chosen_team == 1:
                self.team1.update_record('loss')
                self.team2.update_record('win')
            else:
                self.team2.update_record('loss')
                self.team1.update_record('win')

        print(f"{player.name}'s updated balance: ${player.get_balance():.2f}")


class Player:
    def __init__(self, name, initial_balance):
        self.name = name
        self.balance = initial_balance

    def get_balance(self):
        return self.balance

    def place_bet(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def add_winnings(self, amount):
        self.balance += amount

    def deposit(self, amount):
        if amount < 0:
            print("Deposit amount must be positive.")
            return
        self.balance += amount
        print(f"${amount:.2f} deposited to {self.name}'s profile.")

    def withdraw(self, amount):
        if amount < 0:
            print("Withdrawal amount must be positive.")
            return
        if amount > self.balance:
            print("Insufficient funds for withdrawal.")
        else:
            self.balance -= amount
            print(f"${amount:.2f} withdrawn from {self.name}'s profile.")


class BettingGame:
    def __init__(self):
        self.profiles = {}
        self.logged_in_player = None
        self.teams = [Team(name) for name in ["Lions", "Tigers", "Bears", "Hawks", "Sharks", "Dragons"]]
        self.total_games = 5  # Set to 5 for testing

    def add_player(self, name, initial_balance):
        if name in self.profiles:
            print("Profile with this name already exists.")
        elif initial_balance <= 0:
            print("Initial balance must be greater than zero.")
        else:
            self.profiles[name] = Player(name, initial_balance)
            print(f"Profile created for {name} with balance ${initial_balance:.2f}.")

    def delete_player(self, name):
        if name in self.profiles:
            del self.profiles[name]
            print(f"Profile {name} deleted.")
        else:
            print("Profile not found.")

    def login(self, name):
        if self.logged_in_player:
            print(f"Already logged in as {self.logged_in_player.name}. Please log out first.")
            return False
        if name in self.profiles:
            self.logged_in_player = self.profiles[name]
            print(f"Logged in as {self.logged_in_player.name}.")
            return True
        else:
            print("Profile not found.")
            return False

    def logout(self):
        if self.logged_in_player:
            print(f"Logged out of {self.logged_in_player.name}'s profile.")
            self.logged_in_player = None
        else:
            print("No profile is currently logged in.")

    def switch_profile(self, name):
        if name in self.profiles:
            self.logout()
            self.login(name)
        else:
            print("Profile not found.")

    def display_rankings(self):
        print("\n--- Team Rankings ---")
        rankings = sorted(self.teams, key=lambda team: (team.wins, team.losses), reverse=True)
        for team in rankings:
            print(f"{team.name}: {team.record()} (Win Percentage: {team.win_percentage():.2%})")

    def start_betting(self):
        if self.logged_in_player is None:
            print("You need to log into a profile before starting.")
            return

        print(f"Current logged-in player: {self.logged_in_player.name}")

        while True:
            # Check if all teams have played the max games
            if all(team.games_played >= self.total_games for team in self.teams):
                print("All teams have played 5 games. Resetting standings...")
                for team in self.teams:
                    team.reset()

            if self.logged_in_player.get_balance() <= 0:
                print(f"{self.logged_in_player.name}, you're out of money! Game over.")
                break

            # Get the team with the least games played
            least_played_team = min(self.teams, key=lambda t: t.games_played)

            # Find another team to match against, ensuring it doesn't exceed the limit
            eligible_teams = [team for team in self.teams if team != least_played_team and team.games_played < self.total_games]
            if not eligible_teams:
                eligible_teams = [team for team in self.teams if team != least_played_team]  # Fallback

            team2 = random.choice(eligible_teams)

            match = Match(least_played_team, team2)
            match.display_match()

            while True:
                try:
                    choice = int(input(f"Bet on {match.team1.name} (1) or {match.team2.name} (2)? "))
                    if choice not in [1, 2]:
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid choice. Please enter 1 or 2.")

            while True:
                try:
                    bet_amount = float(input("Enter bet amount: $"))
                    if bet_amount <= 0 or bet_amount > self.logged_in_player.get_balance():
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid bet amount.")

            if self.logged_in_player.place_bet(bet_amount):
                match.resolve_bet(choice, bet_amount, self.logged_in_player)
            else:
                print("Insufficient funds to place this bet.")

            play_again = input("Would you like to bet on another match? (y/n): ").lower()
            while play_again not in ['y', 'n']:
                play_again = input("Invalid input. Would you like to bet on another match? (y/n): ").lower()
            if play_again == 'n':
                break

    def display_profiles(self):
        print("\nAvailable profiles:")
        for name, profile in self.profiles.items():
            print(f"{name} (Balance: ${profile.get_balance():.2f})")

    def main_menu(self):
        while True:
            print("\n--- Betting Game Menu ---")
            if self.logged_in_player:
                print(f"Current logged-in player: {self.logged_in_player.name}")

            print("1. Create a new profile")
            print("2. Delete a profile")
            print("3. Log in to a profile")
            print("4. Log out of current profile")
            print("5. Switch profile")
            print("6. Show profiles")
            print("7. Start betting")
            print("8. Deposit money")
            print("9. Withdraw money")
            print("10. Show team rankings")
            print("11. Quit")

            while True:
                try:
                    choice = int(input("Choose an option: "))
                    if choice < 1 or choice > 11:
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid input. Please enter a number between 1 and 11.")

            if choice == 1:
                name = input("Enter profile name: ")
                initial_balance = float(input("Enter starting balance: $"))
                self.add_player(name, initial_balance)
            elif choice == 2:
                name = input("Enter profile name to delete: ")
                self.delete_player(name)
            elif choice == 3:
                name = input("Enter profile name to log in: ")
                self.login(name)
            elif choice == 4:
                self.logout()
            elif choice == 5:
                name = input("Enter profile name to switch to: ")
                self.switch_profile(name)
            elif choice == 6:
                self.display_profiles()
            elif choice == 7:
                self.start_betting()
            elif choice == 8:
                if self.logged_in_player:
                    amount = float(input("Enter amount to deposit: $"))
                    self.logged_in_player.deposit(amount)
                else:
                    print("You need to log into a profile first.")
            elif choice == 9:
                if self.logged_in_player:
                    amount = float(input("Enter amount to withdraw: $"))
                    self.logged_in_player.withdraw(amount)
                else:
                    print("You need to log into a profile first.")
            elif choice == 10:
                self.display_rankings()
            elif choice == 11:
                print("Exiting the game. Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")


if __name__ == "__main__":
    game = BettingGame()
    game.main_menu()
