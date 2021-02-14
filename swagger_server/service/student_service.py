import json
import logging
import os
import tempfile

from tinydb import TinyDB, Query
from tinydb.middlewares import CachingMiddleware
from functools import reduce
import uuid

from swagger_server.models import Student

db_dir_path = tempfile.gettempdir()
db_file_path = os.path.join(db_dir_path, "students.json")
student_db = TinyDB(db_file_path)


def add_student(student):
    if student.first_name == "" or student.last_name == "":
        return 'not allowed', 405

    queries = []
    query = Query()
    queries.append(query.first_name == student.first_name)
    queries.append(query.last_name == student.last_name)
    query = reduce(lambda a, b: a & b, queries)
    res = student_db.search(query)
    if res:
        return 'already exists', 409

    doc_id = student_db.insert(student.to_dict())
    student.student_id = doc_id
    return student.student_id, 200


def get_student_by_id(student_id, subject):
    student = student_db.get(doc_id=int(student_id))
    if not student:
        return "Not Found", 404

    if subject is not None:
        if subject not in student.grades:
            return "Not Found", 404

    return student, 200

def delete_student(student_id):
    student = student_db.get(doc_id=int(student_id))
    if not student:
        return "Not Found", 404
    student_db.remove(doc_ids=[int(student_id)])
    return student_id, 200
