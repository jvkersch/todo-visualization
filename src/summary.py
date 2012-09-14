import json
import sys

class SummaryList:
    """
    Maintains a list of summaries of todo-items, where a summary is a pair 
    (priority, age). Both priority and age can be None.

    The class has some functionality for saving/reading from file.

    """
    def __init__(self):
        self.summaries = []

    def add_items(self, todo_items):
        """Add summaries to list"""
        for item in todo_items:
            self.summaries.append(item.summary())

    def clear(self):
        """Clear summaries"""
        self.summaries = []

    def save(self, filename):
        """Save summaries to file using JSON"""

        summaries_dict = dict(zip(
            range(0, len(self.summaries)),
            self.summaries))

        f = open(filename, 'w')
        json.dump(summaries_dict, f)
        f.close()

    def load(self, filename):
        """Load summaries from filename and add them to list"""

        f = open(filename, 'r')
        summaries_dict = json.load(f)
        f.close()

        # Append loaded values to summaries list
        self.summaries.extend(summaries_dict.values())


if __name__ == '__main__':
    # Process todo file on command line and store summaries

    from datetime import datetime
    from todo_api import parse_todo_file

    try: 
        todo_file = sys.argv[1]
    except IndexError:
        print "Usage: %s [todo file]" % sys.argv[0]

    # Standard file name is summary-<date>.dat
    summary_filename = "summaries/summary-%s.dat" % \
        datetime.now().strftime("%Y%m%d")

    items = parse_todo_file(todo_file)

    s = SummaryList()
    s.add_items(items)
    s.save(summary_filename)
