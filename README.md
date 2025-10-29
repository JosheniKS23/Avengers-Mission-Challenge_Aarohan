🛡 Avengers Mission Game

A Python-based interactive mission challenge built using CustomTkinter.
Players (teams) complete cipher, debug, and logic challenges inspired by the Avengers universe.

🚀 Features

3 Stages + Final Challenge per mission set

Animated background with smooth gradient effect

Soft pulse animation around “MISSION COMPLETE” screen

Dynamic question sets (1–20) stored in a structured dictionary

CSV logging of all team attempts

Records team name, question set, timestamps, and per-stage correctness

Automatically appends new entries — preserving mission history

Auto-validation of correct and skipped answers

Replay option after mission completion

🧩 Question Format

Each mission set includes:

Cipher question

Debug question

Logic question

Final combined answer

All are loaded dynamically based on the selected set number.

🗂 CSV Logging Format

After completing (or skipping) all stages, mission results are saved to mission_log.csv.

team,set,start time,end time,stage1,stage2,stage3,finalstage
jjj,5,29-10-2025 18:31,29-10-2025 18:33,Correct,Correct,Correct,Correct


start time / end time: Recorded automatically

stage1–3 / finalstage: “Correct” or “Incorrect” based on responses

🧠 Gameplay Flow

Enter team name and set number.

Answer the cipher, debug, and logic challenges in sequence.

You can skip a stage (marked as Incorrect).

Final stage combines all previous answers.

Upon mission completion:

Animated “MISSION COMPLETE” screen appears.

Results are logged automatically to CSV.

Replay or exit the game.

⚙️ Installation & Run
Requirements

Install dependencies:

pip install customtkinter pandas

Run the game
python arohan_r4.py


✨ Example Output

Game screen:

Animated background

Stage transitions with progress

Final screen showing:
🛡 MISSION COMPLETE
Team: Avengers | Mission 5
Results: [Correct, Correct, Correct, Correct]

CSV log entry:

avengers,5,29-10-2025 18:31,29-10-2025 18:33,Correct,Correct,Incorrect,Correct

🧑‍💻 Developer Notes

Fully modular question set dictionary (QUESTION_SETS)

Supports easy addition of new missions

Handles skipped answers gracefully

Clean animations and UI consistent across screens

🛠 Future Enhancements

Sound and background effects

Difficulty levels (Easy / Medium / Hard)

Multiplayer leaderboard mode

🕹 Credits

Developed for Aarohan 12th Edition - The Annual Science Fest
Built with ❤️ using Python + CustomTkinter
