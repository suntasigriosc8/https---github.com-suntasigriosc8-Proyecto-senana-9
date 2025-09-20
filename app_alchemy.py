import os
import json
import csv
from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path

# SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = Path(__file__).parent
DATOS_DIR = BASE_DIR / "datos"
DB_DIR = BASE_DIR / "database"
DB_DIR.mkdir(exist_ok=True)
DATOS_DIR.mkdir(exist_ok=True)

TXT_PATH = DATOS_DIR / "datos.txt"
JSON_PATH = DATOS_DIR / "datos.json"
CSV_PATH = DATOS_DIR / "datos.csv"
SQLITE_PATH = DB_DIR / "usuarios.db"

# Configuración SQLAlchemy
engine = create_engine(f"sqlite:///{SQLITE_PATH}", echo=False, future=True)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)

Base.metadata.create_all(bind=engine)

app = Flask(__name__, template_folder="templates", static_folder="static")

# Rutas principales
@app.route("/")
def index():
    return render_template("index.html")

# TXT
@app.route("/guardar_txt", methods=["POST"])
def guardar_txt():
    nombre = request.form.get("nombre", "").strip()
    detalle = request.form.get("detalle", "").strip()
    if not nombre:
        return "Nombre requerido", 400
    with open(TXT_PATH, "a", encoding="utf-8") as f:
        f.write(f"{nombre} | {detalle}\n")
    return redirect(url_for("leer_txt"))

@app.route("/leer_txt")
def leer_txt():
    contenido = []
    if TXT_PATH.exists():
        with open(TXT_PATH, "r", encoding="utf-8") as f:
            contenido = [line.strip() for line in f.readlines()]
    return render_template("resultado.html", titulo="Contenido TXT", items=contenido)

# JSON
@app.route("/guardar_json", methods=["POST"])
def guardar_json():
    item = {"nombre": request.form.get("nombre","").strip(), "detalle": request.form.get("detalle","").strip()}
    if item["nombre"] == "":
        return "Nombre requerido", 400
    data = []
    if JSON_PATH.exists():
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception:
                data = []
    data.append(item)
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return redirect(url_for("leer_json"))

@app.route("/leer_json")
def leer_json():
    data = []
    if JSON_PATH.exists():
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception:
                data = []
    return render_template("resultado.html", titulo="Contenido JSON", items=[f'{d.get("nombre")} - {d.get("detalle")}' for d in data])

# CSV
@app.route("/guardar_csv", methods=["POST"])
def guardar_csv():
    nombre = request.form.get("nombre","").strip()
    detalle = request.form.get("detalle","").strip()
    if nombre == "":
        return "Nombre requerido", 400
    file_exists = CSV_PATH.exists()
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["nombre","detalle"])
        writer.writerow([nombre, detalle])
    return redirect(url_for("leer_csv"))

@app.route("/leer_csv")
def leer_csv():
    rows = []
    if CSV_PATH.exists():
        with open(CSV_PATH, "r", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            rows = [", ".join(row) for row in reader]
    return render_template("resultado.html", titulo="Contenido CSV", items=rows)

# SQLite (Usuarios) usando SQLAlchemy
@app.route("/usuarios")
def usuarios():
    session = SessionLocal()
    try:
        usuarios = session.query(Usuario).all()
        return render_template("resultado.html", titulo="Usuarios (SQLite)", items=[f"{u.id} | {u.nombre} | {u.email}" for u in usuarios])
    finally:
        session.close()

@app.route("/usuarios/agregar", methods=["POST"])
def usuarios_agregar():
    nombre = request.form.get("nombre_usuario","").strip()
    email = request.form.get("email_usuario","").strip()
    if not nombre or not email:
        return "Nombre y email requeridos", 400
    session = SessionLocal()
    try:
        # comprobar duplicado por email
        if session.query(Usuario).filter_by(email=email).first():
            return "Email ya existe", 400
        u = Usuario(nombre=nombre, email=email)
        session.add(u)
        session.commit()
    finally:
        session.close()
    return redirect(url_for("usuarios"))

if __name__ == "__main__":
    app.run(debug=True)