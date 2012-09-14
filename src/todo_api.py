from datetime import datetime
import re
import sys

class TodoItem:
    """Generic item in a todo-list."""
    def __init__(self, description, done=False, priority=None,
                 contexts=None, projects=None, 
                 date_started=None, date_finished=None):

        self.done = done
        self.description = description
        self.priority = priority
        self.contexts = contexts
        self.projects = projects
        self.date_started = date_started
        self.date_finished = date_finished

    def __repr__(self):
        """String representation of TodoItem."""

        rep = ""
        if self.done:
            rep += "x "

        if self.priority is not None:
            rep += "(%s) " % self.priority

        if self.date_finished is not None:
            rep += self.date_finished.strftime("%Y-%m-%d") + " "

        if self.date_started is not None:
            rep += self.date_started.strftime("%Y-%m-%d") + " "

        rep += self.description
        return rep

    def summary(self):
        """
        Gives summary of todo item, consisting of priority, 
        if any, and age.

        """

        if self.date_started is None:
            age = None
        else:
            if self.date_finished is None:
                d = datetime.now()
            else:
                d = self.date_finished

            age = (d - self.date_started).days

        return self.priority, age


def parse_date(s):
    """Parse date in YYYY-MM-DD format."""
    return datetime.strptime(s, "%Y-%m-%d")    


def parse_todo_line(line):
    """Return a TodoItem from a line in a todo/done.txt file."""

    line = line.strip()

    done = False
    description = ""
    priority = None
    contexts = None
    projects = None
    date_started = None
    date_finished = None

    # Regular expression to match the standard skeleton of a todo line
    expr = "(?P<status>x)?\s*(\((?P<priority>[A-Z])\))?\s*" \
        "((?P<date1>[0-9]{4}-[0-9]{2}-[0-9]{2}) )?" \
        "(?P<date2>[0-9]{4}-[0-9]{2}-[0-9]{2})?"

    m = re.match(expr, line)
    if m is None:
        raise ValueError("Unparsable todo line: %s" % line)

    # Extract info from match object
    fields = m.groupdict()

    # Fill in whether task is done
    done = fields['status'] == 'x'

    # Retrive priority, if any
    priority = fields['priority']

    # Parse start and end dates, if any
    # Note: this isn't entirely according to the API, since tasks in progress
    # by definition cannot have an end date...

    if done:
        # Done tasks have a completion date (mandatory) and a starting date
        # optional
        if fields['date1'] is None:
            raise ValueError("No completion date found in completed" \
                                 "todo item: %s" % line)
        date_finished = parse_date(fields['date1'])
        if fields['date2'] is not None:
            date_started = parse_date(fields['date2'])
    else:
        # Tasks in progress have an optional starting date
        if fields['date1'] is not None:
            date_started = parse_date(fields['date1'])

    # The contents of the line are everything that isn't matched
    # Note: we include projects and contexts in the task description
    # since they are often part of the message, e.g. 
    # "finish paper @UCSD on +stochastic_fluids"

    description = line[m.end():].strip()

    # Extract contexts and projects from task description
    contexts = [word[1:] for word in description.split() if word[0] == '@']
    projects = [word[1:] for word in description.split() if word[0] == '+']
        
    return TodoItem(description, done, priority, contexts, 
                    projects, date_started, date_finished)


def parse_todo_file(filename):
    """
    Parse all items in a text file and return array of TodoItems

    """
    todo_items = []

    for todoline in open(filename):
        item = parse_todo_line(todoline)
        todo_items.append(item)

    return todo_items


if __name__ == '__main__':

    items = parse_todo_file(sys.argv[1])
    for item in items:
        print item
