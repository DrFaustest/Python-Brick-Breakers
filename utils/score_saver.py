import csv
import os

# Class to save the top 10 high scores and names in a csv file in name, score format
# At initialization, the class checks if the file exists and creates it if it doesn't
# The class also loads the scores from the file and stores them in a list
# The class also checks if a score is a high score and returns a boolean
# If the score makes the list of high scores, the class will save the new score list to the file
# This class will also arrange and format the list for display in the high score screen

class ScoreSaver:
    def __init__(self):
        self.filename = "high_score.csv"
        if not os.path.isfile(self.filename):
            self.file = open(self.filename, 'w')
            self.file.close()
        self.scores = self.load_scores()

    def load_scores(self) -> list: 
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
        self.sort_scores()
        if len(self.scores) < 10:
            return True
        elif score > int(self.scores[-1][1]):
            return True
        return False
        
    def sort_scores(self):
        self.scores.sort(key=lambda x: x[1], reverse=True)
        return self.scores

    def add_score(self, name, score):
        self.scores.append((name, score))
        self.sort_scores()
        if len(self.scores) > 10:
            self.scores.pop()
        self.save_scores()

    def save_scores(self):
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            for score in self.scores:
                writer.writerow(score)

    def score_display(self):
        self.sort_scores()
        display = []
        for i, score in enumerate(self.scores):
            display.append(f"{i + 1}. {score[0]}: {score[1]}")
        return display
    