import re

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

class Location:
  def __init__(self, location=None):
    self.states = states
    if location:
      self.city, self.state, self.abbreviation = self.find_city_data(location)
      self.zipcode = self.find_zipcode(location)
      self.location = location

  def split_location(self, location):
    return re.split("\s|\,\s", location)

  def find_zipcode(self, location):
    check = re.search("\d{5}", location)
    if check:
      return check.group()
    return None

  def find_abbreviation(self, statename):
    for a, state in states.items():
      if statename.title() == state:
        return a
    return None


  def find_city_data(self, location):
    a = self.split_location(location)
    c = a[:]
    check = a.pop()
    abbreviation = None
    state = None
    city = None

    while not state and len(a) > 0:
      if check.isnumeric():
        c = a[:]
        check = a.pop()
      elif check.upper() in states:
        state = check.upper()
      elif check.title() in states.values():
        state = check.title()
      else:
        check = a.pop() + " " + check

    if state in states:
      abbreviation, state = state, states[state]
    elif state in states.values():
      abbreviation = self.find_abbreviation(state)

    if state:
      city = " ".join(a).title()
    elif " ".join(c).isnumeric():
      city = None
    else:
      city = " ".join(c).title()

    return (city, state, abbreviation)
