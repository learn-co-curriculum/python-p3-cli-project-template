from . import CURSOR, CONN
import sqlite3

class Session:

    def __init__(self, date, language, level, exercise_type, points_earned, points_possible, id=None):
        self.date = date
        self.language = language
        self.level = level
        self.exercise_type = exercise_type
        self.points_earned = points_earned
        self.points_possible = points_possible
        self.id = id


    def __repr__(self):
        return "Session("\
            f"date={self.date}, "\
            f"language={self.language}, "\
            f"level={self.level},  "\
            f"exercise_type={self.exercise_type}, "\
            f"points_earned={self.points_earned}, "\
            f"points_possible={self.points_possible}, "\
            f"id={self.id})"
    

    @classmethod
    def create_table(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY,
            date TEXT,
            language TEXT,
            level TEXT,
            exercise_type TEXT,
            points_earned REAL,
            points_possible REAL
        )   
        """
        CURSOR.execute(sql)

    def create(self):
        sql = """
        INSERT INTO sessions (date, language, level, exercise_type, points_earned, points_possible)
        VALUES(?, ?, ?, ?, ?, ?)
        """
        CURSOR.execute(sql, [self.date, self.language, self.level, self.exercise_type, self.points_earned, self.points_possible])
        CONN.commit()
        self.id = CURSOR.lastrowid


    def delete(self):
        sql = """
        DELETE FROM sessions
        WHERE id = ?
        """
        CURSOR.execute(sql, [self.id])
        CONN.commit()

    @classmethod
    def delete_by_id(cls, id):
        sql = """
        DELETE FROM sessions
        WHERE id = ?
        """
        CURSOR.execute(sql, [id])
        CONN.commit()


    def update(self):
        sql = """
        UPDATE sessions
        SET points_earned = ?,
        points_possible = ?
        WHERE id = ?
        """
        CURSOR.execute(sql, [self.points_earned, self.points_possible, self.id])
        CONN.commit()
        


    @classmethod
    def update_by_id(cls, id, points_earned, points_possible):
        sql = """
        UPDATE sessions
        SET points_earned = ?,
        points_possible = ?
        WHERE id = ?
        """
        CURSOR.execute(sql, [points_earned, points_possible, id])
        CONN.commit()

    
    def save(self):
        if self.id:
            self.update()
        else:
            self.create()

    @classmethod
    def query_all(cls):
        sql = """SELECT * FROM sessions"""
        return [Session(date, lang, lev, ex_type, points_earned, points_possible, id) 
                for (id, date, lang, lev, ex_type, points_earned, points_possible) 
                in CURSOR.execute(sql).fetchall()] 
    
    @classmethod
    def query_by_id(cls, id):
        sql = """
        SELECT * FROM sessions 
        WHERE id = ?
        """
        (id, date, lang, lev, ex_type, points_earned, points_possible) = CURSOR.execute(sql, [id]).fetchone()
        return Session(date, lang, lev, ex_type, points_earned, points_possible, id)
    
    @classmethod
    def total_points_attempted(cls):
        sql = """SELECT SUM(points_possible) FROM sessions"""
        (points,) = CURSOR.execute(sql).fetchone()
        return points

    @classmethod
    def total_points_earned(cls):
        sql = """SELECT SUM(points_earned) FROM sessions"""
        (points,) = CURSOR.execute(sql).fetchone()
        return points

    @classmethod
    def count_sessions(cls):
        sql = """SELECT COUNT(*) FROM sessions"""
        (count,) = CURSOR.execute(sql).fetchone()
        return count

    @classmethod
    def count_distinct_languages(cls):
        sql = """SELECT COUNT (DISTINCT language) FROM sessions"""
        (language,) = CURSOR.execute(sql).fetchone()
        return language

    @classmethod
    def accuracy(cls):
        sql = """SELECT SUM(points_earned)/ SUM(points_possible) FROM sessions"""
        (accuracy,) = CURSOR.execute(sql).fetchone()
        return accuracy

    @classmethod
    def session_high_score(cls):
        sql = """SELECT MAX(points_earned) FROM sessions"""
        (high_score,) = CURSOR.execute(sql).fetchone()
        return high_score
        

class Flashcard:
    def __init__(self, origin, date, language, level, word, translation, definition, example, id=None):
        self.origin = origin
        self.date = date
        self.language = language
        self.level = level
        self.word = word
        self.translation = translation
        self.definition = definition
        self.example = example
        self.id = id

    def __repr__(self):
        return (f"Flashcard(origin={self.origin!r}, date={self.date!r}, language={self.language!r}, "
                f"level={self.level!r}, word={self.word!r}, translation={self.translation!r}, "
                f"definition={self.definition!r}, example={self.example!r}, id={self.id!r})")

    # SQL METHODS
    @classmethod
    def create_table(cls):
        sql = """CREATE TABLE IF NOT EXISTS flashcards (
        id INTEGER PRIMARY KEY,
        origin TEXT,
        date TEXT,
        language TEXT,
        level TEXT,
        word TEXT,
        translation TEXT,
        definition TEXT,
        example TEXT
        )
        """
        CURSOR.execute(sql)

    def create(self):
        sql = """INSERT INTO flashcards (origin, date, language, level, word, translation, definition, example)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        CURSOR.execute(sql, [self.origin, self.date, self.language, self.level, self.word, self.translation, self.definition, self.example])
        CONN.commit()

        self.id = CURSOR.lastrowid
        pass

    def delete(self):
        sql = """
        DELETE FROM flashcards
        WHERE id = ?
        """
        CURSOR.execute(sql, [self.id])
        CONN.commit()

    @classmethod
    def delete_by_id(cls, id):
        sql = """
        DELETE FROM flashcards
        WHERE id = ?
        """
        CURSOR.execute(sql, [id])
        CONN.commit()

    def update(self):
        sql = """
        UPDATE flashcards
        SET origin = ?,
        date = ?,
        language = ?,
        level = ?,
        word = ?,
        translation = ?,
        definition = ?,
        example = ?
        WHERE id = ?
        """
        CURSOR.execute(sql, [self.origin, self.date, self.language, self.level, self.word, self.translation, self.definition, self.example, self.id])
        CONN.commit()

    @classmethod
    def query_all(cls):
        sql = """SELECT * FROM flashcards"""
        return [Flashcard(origin, date, language, level, word, translation, definition, example, id) 
                for (id, origin, date, language, level, word, translation, definition, example) 
                in CURSOR.execute(sql).fetchall()] 

    @classmethod
    def query_by_id(cls, id):
        sql = """
        SELECT * FROM flashcards 
        WHERE id = ?
        """
        
        (id, origin, date, language, level, word, translation, definition, example)  = CURSOR.execute(sql, [id]).fetchone()
        return Flashcard(origin, date, language, level, word, translation, definition, example, id)

    @classmethod
    def query_by_lang_and_level(cls, lang, level):
        sql = """
        SELECT * FROM flashcards
        WHERE language = ?
        AND level = ?
        """
        return [Flashcard(origin, date, language, level, word, translation, definition, example, id) 
                for (id, origin, date, language, level, word, translation, definition, example) 
                in CURSOR.execute(sql, [lang, level]).fetchall()]

    



