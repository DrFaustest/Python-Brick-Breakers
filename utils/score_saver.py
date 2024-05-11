import csv
import os
from typing import List, Tuple

class ScoreSaver:
    def __init__(self) -> None:
        """
        Initializes the ScoreSaver object.

        If the high score file does not exist, it creates an empty file.
        Loads the high scores from the file.
        """
        self.filename: str = "high_score.csv"
        if not os.path.isfile(self.filename):
            self.file = open(self.filename, 'w')
            self.file.close()
        self.scores: List[Tuple[str, int]] = self.load_scores()
        self.scores: List[Tuple[str, int]] = self.sort_scores()

    def load_scores(self) -> List[Tuple[str, int]]: 
        """
        Loads the high scores from the file.

        Returns:
        - scores (list): A list of tuples representing the high scores, where each tuple contains the name and score.
        """
        scores: List[Tuple[str, int]] = []
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    try:
                        name: str = row[0]
                        score: int = int(row[1])
                        scores.append((name, score))
                    except ValueError:
                        continue                
        return scores
    
    def check_high_score(self, score: int) -> bool:
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
        
    def sort_scores(self) -> List[Tuple[str, int]]:
        """
        Sorts the high scores in descending order.

        Returns:
        - sorted_scores (list): A list of tuples representing the sorted high scores.
        """
        sorted_scores: List[Tuple[str, int]] = sorted(self.scores, key=lambda x: x[1], reverse=True)
        return sorted_scores

    def add_score(self, name: str, score: int) -> None:
        """
        Adds a new score to the high scores.

        If the number of scores exceeds 10, removes the lowest score.

        Args:
        - name (str): The name associated with the score.
        - score (int): The score to be added.
        """
        if len(self.scores) == 10:
            self.scores.pop()
        self.scores.append((name, score))
        self.sort_scores()
        self.save_scores()

    def save_scores(self) -> None:
        """
        Saves the high scores to the file.
        """
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            for score in self.scores:
                writer.writerow(score)

    def score_display(self) -> List[str]:
        """
        Generates a formatted display of the high scores.

        Returns:
        - display (list): A list of strings representing the formatted high scores.
        """
        display: List[str] = []
        for i, score in enumerate(self.scores):
            display.append(f"{i + 1}. {score[0]}: {score[1]}")
        return display