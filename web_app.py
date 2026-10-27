from flask import Flask, request, redirect
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    message = "<p>Task saved successfully!</p>" if request.args.get("saved") == "1" else ""

    return message + """
<style>
        body {
            font-family: Arial, sans-serif;
            background: #f1f5f9;
            color: #1e293b;
            max-width: 700px;
            margin: 40px auto;
            padding: 20px;
        }
        form {
            background: white;
            padding: 24px;
            border-radius: 12px;
            margin-bottom: 24px;
        }
        input {
            padding: 10px;
            border: 1px solid #64748b;
            border-radius: 6px;
        }
        button {
            background: #0369a1;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }
    </style>

    <h1>Housekeeping Task Tracker</h1>
    <p>Welcome, Nicole!</p>
    <form method="post" action="/save">
          <p>Room numer: <input name="room" required></p>
          <p>Completed task: <input name="task" required></p>
          <button type="submit">Save task</button>
    </form>

    <h2>Room history</h2>
    <form method="get" action="/history">
        <p>Room number: <input name="room" required></p>
        <button type="submit">View history</button>
    </form>
      
    """
@app.route("/save", methods=["POST"])
def save_task():
    room = request.form.get("room", "").strip()
    task = request.form.get("task", "").strip()
    if not room or not task:
        return "Please enter a room and task.", 400
    with sqlite3.connect("housekeeping.db") as conn:
        conn.execute(
            "INSERT INTO tasks (room, task) VALUES (?, ?)",
            (room, task)
        )
    return redirect("/?saved=1")

@app.route("/history")
def history():
    from html import escape
    room = request.args.get("room", "").strip()
    with sqlite3.connect("housekeeping.db") as conn:
        rows = conn.execute(
            "SELECT task FROM tasks WHERE room = ?",
            (room,)
        ).fetchall()
    page = """
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f1f5f9;
            color: #1e293b;
            max-width: 700px;
            margin: 40px auto;
            padding: 20px;
        }
        p {
            background: white;
            padding: 18px;
            border-radius: 8px;
        }
        a {
            color: #0369a1;
        }
    </style>
    """
    page += f"<h1>Room {escape(room)} history</h1>"   
    for row in rows:
        page += f"<p>{escape(row[0])}</p>"
    if not rows:
        page += "<p>No tasks found.</p>"
    return page + '<p><a href="/">Back</a></p>'

if __name__== "__main__" :
    app.run(debug=False)
