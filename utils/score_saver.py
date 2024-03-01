import csv
import os

class ScoreSaver:
    def __init__(self):
        """
        Initializes the ScoreSaver object.

        If the high score file does not exist, it creates an empty file.
        Loads the high scores from the file.
        """
        self.filename = "high_score.csv"
        if not os.path.isfile(self.filename):
            self.file = open(self.filename, 'w')
            self.file.close()
        self.scores = self.load_scores()

    def load_scores(self) -> list: 
        """
        Loads the high scores from the file.

        Returns:
        - scores (list): A list of tuples representing the high scores, where each tuple contains the name and score.
        """
        scores = []
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    try:
                        name = row[0]
                        score = int(row[1])
                        scores.append((name, score))
                    except ValueError:
                        continue                
        return scores
    
    def check_high_score(self, score):
        """
        Checks if a given score is a high score.

        Args:
        - score (int): The score to be checked.

        Returns:
        - True if the score is a high score, False otherwise.
        """
        self.sort_scores()
        if len(self.scores) < 10:
            return True
        elif score > int(self.scores[-1][1]):
            return True
        return False
        
    def sort_scores(self):
        """
        Sorts the high scores in descending order.
        """
        self.scores.sort(key=lambda x: x[1], reverse=True)
        return self.scores

    def add_score(self, name, score):
        """
        Adds a new score to the high scores.

        If the number of scores exceeds 10, removes the lowest score.

        Args:
        - name (str): The name associated with the score.
        - score (int): The score to be added.
        """
        self.scores.append((name, score))
        self.sort_scores()
        if len(self.scores) > 10:
            self.scores.pop()
        self.save_scores()

    def save_scores(self):
        """
        Saves the high scores to the file.
        """
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            for score in self.scores:
                writer.writerow(score)

    def score_display(self):
        """
        Generates a formatted display of the high scores.

        Returns:
        - display (list): A list of strings representing the formatted high scores.
        """
        self.sort_scores()
        display = []
        for i, score in enumerate(self.scores):
            display.append(f"{i + 1}. {score[0]}: {score[1]}")
        return display
    