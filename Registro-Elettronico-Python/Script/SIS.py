import datetime as dt
import re
import pickle
from pathlib import Path


all_subjects = ['Italiano', 'Matematica', 'Storia', 'Inglese', 'Informatica']
all_classes = ['1A', '1B', '1C', '2A', '2B', '2C']
hours_lessons = [1, 2, 3, 4, 5, 6]
pswAdmin = "2RsnMU~^{o#'"

def loadD():
    global all_subjects
    global all_classes
    global hours_lessons
    global pswAdmin

    try:
        with open("files/DEFAULTS.pickle", "rb") as file:
            DEFAULTS = pickle.load(file)
            
            all_subjects = DEFAULTS['subjects']
            all_classes = DEFAULTS['classes']
            hours_lessons = DEFAULTS['hours_x_lesson']
            pswAdmin = DEFAULTS['admin-password']
    except FileNotFoundError:
        print("DEFAULTS file not found or not generated yet")
    except EOFError:
        print("DEFAULTS file is empty")


loadD()

def dumpD():
    global all_subjects
    global all_classes
    global hours_lessons
    global pswAdmin

    dFile = "files/DEFAULTS.pickle"
    P_d = Path(dFile)
    P_d.parent.mkdir(parents=True, exist_ok=True)

    with open("files/DEFAULTS.pickle", "wb") as file:
        defaults = {
            'subjects' : all_subjects,
            'classes' : all_classes,
            'hours_x_lesson' : hours_lessons,
            'admin-password': pswAdmin
        }

        pickle.dump(defaults, file)


all_students = dict()
all_teachers = dict()

lfs = 0000 #Last-Freshman in students
lft = 0000 #Last-Freshman in teachers

def load1():
    global all_teachers
    global all_students
    global lfs
    global lft

    try:
        with open("files/students.pickle", 'rb') as file:
            all_students = pickle.load(file)
        with open("files/teachers.pickle", 'rb')as file:
            all_teachers = pickle.load(file)
        with open("files/freshmans.pickle", 'rb')as file:
            lf = pickle.load(file)
            lfs = lf['s']
            lft = lf['t']
    except FileNotFoundError:
        print("Student, Teacher or Freshmans file has not been created yet")

lessons = list(hours_lessons)
grades = []
events = []

today = dt.datetime.now()
#date = today.strftime('%d/%m/%Y')
hour = None

classmates = []


def load2(cl, date):

    global lessons
    lessons = list(hours_lessons)
    lessonsfile = "Files" + '/' + "Classes" + "/" + cl + '/' + "lessons" + '/' + date.replace("/", "-") + ".pickle"
    
    """
    with open(f'files/classes/{clss}/classmates.txt', 'r') as file:
        for line in file:
            classmates.append(line)
    """
        
    try:
        with open(lessonsfile, "rb") as file:
            lessons = pickle.load(file)
        
        print(lessonsfile)
    except FileNotFoundError:
        print("No lessons registerd for date and class given")

def dump():
    stFile = "files/students.pickle"
    P_st = Path(stFile)
    P_st.parent.mkdir(parents=True, exist_ok=True)

    tcFile = "files/teachers.pickle"
    P_tc = Path(tcFile)
    P_tc.parent.mkdir(parents=True, exist_ok=True)

    with open("files/students.pickle", 'wb') as file:
        pickle.dump(all_students, file)

    with open("files/teachers.pickle", 'wb')as file:
        pickle.dump(all_teachers, file)

    with open("files/freshmans.pickle", 'wb')as file:
        lf = {
            's': lfs,
            't': lft
        }
        pickle.dump(lf, file)
    

def dumpT(cl, date):
    
    lessonsfile = "Files" + '/' + "Classes" + "/" + cl + '/' + "lessons" + '/' + date.replace("/", "-") + ".pickle"
    Plf = Path(lessonsfile)
    Plf.parent.mkdir(parents=True, exist_ok=True)
    with open(lessonsfile, "wb") as file:
        pickle.dump(lessons, file)
    
    print(lessonsfile)

class User:
    
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self._password = "firstlogin"
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if re.search('[a-zA-Z ]+[a-zA-Z ]*', name):
            self._name = name.lower().strip().title()

    @property
    def surname(self):
        return self._surname
    
    @surname.setter
    def surname(self, surname):
        if re.search('[a-zA-Z ]+[a-zA-Z ]*', surname):
            self._surname = surname.lower().strip().title()

    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, password):
        if len(password) < 8:
            raise ValueError("La password deve essere lunga almeno 8 caratteri")

        # Controlla se la password contiene almeno una lettera maiuscola
        if not re.search(r'[A-Z]', password):
            raise ValueError("La password deve contenere almeno una lettera maiuscola")

        # Controlla se la password contiene almeno una lettera minuscola
        if not re.search(r'[a-z]', password):
            raise ValueError("La password deve contenere almeno una lettera minuscola")

        # Controlla se la password contiene almeno un numero
        if not re.search(r'[0-9]', password):
            raise ValueError("La password deve contenere almeno un numero")

        # Controlla se la password contiene almeno un carattere speciale
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValueError("La password deve contenere almeno un carattere speciale")
        
        self._password = password


class Student(User):
    def __init__(self, name, surname, cl):
        super().__init__(name, surname)
        self.userID = self.ID_generator()
        self.cl = cl
        self.absences = []
        self.grades = []
        all_students[self.userID] = self
        


    def __str__(self):
        return f' ID generato: {self.userID} \n Surname: {self.surname} \n Name: {self.name} \n Class: {self.cl}'

    def ID_generator(self):
        id = int(lfs) + 1
        return str(f'02-{str(id).zfill(4)}')
    
    @property
    def cl(self):
        return self._cl
    
    @cl.setter
    def cl(self, cl):
        if cl not in all_classes:
            raise ValueError
        self._cl = cl
    
    def set_presence(self, hour, presence: bool):
        global date
        try:
            if hour in lessons:
                raise SystemError("Ora non firmata")
            
            if not presence:
                lessons[hour-1]['absences'].append({self.userID: presence})
                if [date, any(range(1, len(lessons)))] not in self.absences:
                    self.absences.append([date, hour])
        except SystemError:
            pass

    def new_grade(self, subject, grade: float, topic: str, description: str = None, date = today):
        global grades

        self.grades.append(
            {
                'subject': subject, 
                'topic': topic,
                'description': description, 
                'grade': grade, 
                'date': date
            }
        )
        grades[topic].append(
            {
                'student': self.userID,
                'subject': subject, 
                'description': description, 
                'grade': grade, 
                'date': date
            }
        )

    def justifie(self, date, reason, description = ""):
        try:
            if reason not in ['family', 'health', 'strike', 'medic certificate', 'other']:
                raise ValueError
            if [date, any(1, len(lessons))] not in self.absences:
                raise ValueError
        except ValueError:
            pass
        
    

    
class Teacher(User):
    def __init__(self, name, surname, subjects: set, clss: dict):
        super().__init__(name, surname)
        self.userID = self.ID_generator()
        self.subjects = subjects
        self.clss = clss
        self.events = []
        all_teachers[self.userID] = self
        

    def __str__(self):
        clss = ""
        for key, value in self.clss.items():
            clss += f"{key}:"
            first_element = True
            for v in value:
                if first_element:
                    clss += f" {v}"
                    first_element = False
                else:
                    clss += f", {v}"
            clss += "; "
        
        subj = ""
        first_element = True
        for value in self.subjects:
            if first_element:
                    subj += f"{value}"
                    first_element = False
            else:
                subj += f", {value}"


        return f' ID generato: {self.userID} \n Cognome: {self.surname} \n Nome: {self.name} \n Materie: {subj} \n Classi: {clss}'
    
    @property
    def clss(self):
        return self._clss
    
    @clss.setter
    def clss(self, clss: dict):
        for cl in clss.keys():
            if cl.upper() not in all_classes:
                raise ValueError("Given class is not in 'all_classes' list")
        
        self._clss = clss

    @property
    def subjects(self):
        return self._subjects
    
    @subjects.setter
    def subjects(self, subjects):
        for sb in subjects:
            if sb.lower().capitalize() not in all_subjects:
                raise ValueError("Given subject is not in 'all_subjects' list")
        
        self._subjects = subjects

    def ID_generator(self):
        id = int(lft) + 1
        return str(f'01-{str(id).zfill(4)}')
    
    def sign(self, hour, cl, subject, description: str = None):
        global lessons
        if subject not in self.subjects:
            raise ValueError
        if cl not in self.clss:
            raise ValueError
        if hour not in lessons:
            raise ValueError
        lessons[hour-1] = ({'lesson': hour,'class': cl,'subject': subject, 'teacher': self.surname + ' ' + self.name, 'absences': set(), 'presences': set([s for s in all_students if all_students[s].cl == cl]), 'description': description})
    
    def event(self, type, description, date, clss):
        if type not in ['homework', 'test', 'information']:
            raise ValueError
        
        event = {
            'class': clss,
            'date': date,
            'type': type,
            'description': description,
        }

        global events
        events.append(event)
        self.events.append(event)

if __name__ == '__main__':
   ...    

clssXadmin = {}
for cl in all_classes:
    clssXadmin[cl] = all_subjects
AdminT = Teacher('Admin', 'Admin', all_subjects, clssXadmin)
AdminT.userID = "01-0000"
AdminT.password = pswAdmin
try:
    del all_teachers[AdminT.userID]
except KeyError:
    pass