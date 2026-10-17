import argparse
import json
import relationships
import sys
class Person :
    """Represent a person and their family connections.

    Attributes:
        name (str): The person's name.
        gender (str): The person's gender.
        parents (list of Person): The person's known parents.
        spouse (Person or None): The person's spouse, if applicable.
    """

    def __init__(self, name, gender ):
        """Initialize a person.

        Args:
            name (str): The person's name.
            gender (str): The person's gender.

        Side effects:
            Sets the person's name, gender, parents, and spouse attributes.
        """
        self.name = name 
        self.gender = gender
        self.parents =  []
        self.spouse = None
    def add_parent(self , parent):
        """Add a parent to the person's list of parents.

        Args:
            parent (Person): The parent to add.

        Side effects:
            Adds a Person object to the parents attribute.
        """
        self.parents.append(parent)
        
    def set_spouse(self , spouse):
        """Set the person's spouse.

        Args:
            spouse (Person): The person to assign as the spouse.

        Side effects:
            Sets the spouse attribute.
        """
        self.spouse = spouse
    
    def connections(self):
        """Find the shortest paths to the person's family connections.

        Returns:
            dict: Person objects mapped to their shortest connection paths.
        """
        cdict = {self : ""}
        queue = [self]
        while queue != []: 
            person = queue.pop(0)
            personpath = cdict[person]
            for parent in person.parents:
                if parent not in cdict:
                    cdict[parent] = personpath + "P"
                    queue.append(parent)
            if "S" not in personpath and person.spouse is not None and person.spouse not in cdict:
                cdict[person.spouse] = personpath + "S"
                queue.append(person.spouse)
        return cdict
    def relation_to(self , other):
       """Determine how this person is related to another person.

        Args:
            other (Person): The other person in the relationship.

        Returns:
            str or None: The kinship term, or None if they are unrelated.
        """ 
       self_connections = self.connections()
       other_connections = other.connections()
       if not (self_connections.keys() & other_connections.keys()):
           return None;
       common_keys = self_connections.keys() & other_connections.keys()
       combined_paths = []
       for key in common_keys:
          combined_path = f'{self_connections[key]}:{other_connections[key]}'
          combined_paths.append(combined_path)
       lcr_path = min(combined_paths , key = len)
       if lcr_path in relationships.relationships:
            return relationships.relationships[lcr_path][self.gender]
       return "distant relative"

class Family:
    """Store people and their family relationships.

    Attributes:
        people (dict of str to Person): Names mapped to Person objects.
    """
    def __init__(self, family_data):
        """Create people and connect their family relationships.

        Args:
            family_data (dict): Information about individuals, parents,
                and couples.

        Side effects:
            Creates the people attribute and connects parents and spouses.
        """
        self.people = {}

        for name, gender in family_data["individuals"].items():
            self.people[name] = Person(name, gender)

        for child_name, parent_names in family_data["parents"].items():
            child = self.people[child_name]

            for parent_name in parent_names:
                parent = self.people[parent_name]
                child.add_parent(parent)

        for couple in family_data["couples"]:
            name1, name2 = couple

            person1 = self.people[name1]
            person2 = self.people[name2]

            person1.set_spouse(person2)
            person2.set_spouse(person1)
    def relation(self , name1, name2):
        
    
        """Determine how the first person is related to the second.

        Args:
            name1 (str): Name of the first person.
            name2 (str): Name of the second person.

        Returns:
            str or None: The kinship term, or None if they are unrelated.
        """
        person1 = self.people[name1]
        person2 = self.people[name2]
        return person1.relation_to(person2)
def main(filepath, name1, name2):
    """Load family data and print how two people are related.

    Args:
        filepath (str): Path to the JSON family-data file.
        name1 (str): Name of the first person.
        name2 (str): Name of the second person.

    Side effects:
        Reads a JSON file and prints the relationship to the console.
    """
    with open(filepath, "r", encoding="utf-8") as file:
        family_data = json.load(file)

    family = Family(family_data)
    relation = family.relation(name1, name2)

    if relation is None:
        print(f"{name1} is not related to {name2}")
    else:
        print(f"{name1} is {name2}'s {relation}")


def parse_args(arglist):
    """Parse the command-line arguments.

    Args:
        arglist (list of str): Command-line arguments to parse.

    Returns:
        argparse.Namespace: The parsed command-line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filepath",
        help="path to the JSON family-data file",
    )
    parser.add_argument(
        "name1",
        help="name of the first person",
    )
    parser.add_argument(
        "name2",
        help="name of the second person",
    )
    return parser.parse_args(arglist)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.filepath, args.name1, args.name2)