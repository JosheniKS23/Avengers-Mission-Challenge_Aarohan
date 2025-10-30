
import customtkinter as ctk
import random, math, threading, csv, os
from tkinter import messagebox, PhotoImage
from datetime import datetime

try:
    import winsound
    def play_tone(freq=800, dur=100):
        threading.Thread(target=winsound.Beep, args=(freq, dur), daemon=True).start()
except Exception:
    def play_tone(*a, **k): pass

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# ----------------------------- CONFIG -----------------------------
TIME_LIMITS = {1:300, 2:300, 3:300, 4:300}
POINTS_PER_STAGE = {1:40, 2:30, 3:20, 4:10}

# ----------------------------- QUESTION SETS -----------------------------
QUESTION_SETS = {
    1: {"cipher":{"question":"Decrypt ‘UCXG’ using Caesar cipher (+2).","answer":"SAVE"},
        "debug":{"question":"Find result of 101 AND 111 in decimal.","answer":"5"},
        "logic":{"question":"What is the 5th letter of the alphabet?","answer":"E"},"final":"SAVE5E"},
    2: {"cipher":{"question":"Decode letter G using Caesar cipher (shift +3).","answer":"D"},
        "debug":{"question":"If A=True and B=False, find A AND B (1/0).","answer":"0"},
        "logic":{"question":"I am a red fruit and a tech brand. What am I?","answer":"APPLE"},"final":"D0APPLE"},
    3: {"cipher":{"question":"If A=1, B=2 ... what number does E represent?","answer":"5"},
        "debug":{"question":"NOT gate with input 1 outputs?","answer":"0"},
        "logic":{"question":"A 6-letter word meaning opposite of vulnerable.","answer":"SECURE"},"final":"50SECURE"},
    4: {"cipher":{"question":"Sum of letters in 'IT' (A=1...Z=26).","answer":"29"},
        "debug":{"question":"If MONDAY=36, TUESDAY=49, FRIDAY=36, WEDNESDAY=?","answer":"81"},
        "logic":{"question":"Next letter: A, S, O, N, ?","answer":"D"},"final":"2981D"},
    5: {"cipher":{"question":"Decrypt KTQPOCP (+2 shift) to reveal Avenger.","answer":"IRONMAN"},
        "debug":{"question":"Binary 1001 to decimal?","answer":"9"},
        "logic":{"question":"If 5 Avengers take 5 min to beat 5 enemies, time for 1 Avenger for 1 enemy?","answer":"1"},"final":"IRONMAN91"},
    6: {"cipher":{"question":"Decrypt letter B using Caesar cipher (+1).","answer":"A"},
        "debug":{"question":"Decimal 10 in binary?","answer":"1010"},
        "logic":{"question":"Common wireless internet connection (4 letters).","answer":"WIFI"},"final":"A1010WIFI"},
    7: {"cipher":{"question":"Decrypt SRZHU using Caesar cipher (+3).","answer":"POWER"},
        "debug":{"question":"If Iron Man=1, Thanos=0, Iron Man AND Thanos=?","answer":"0"},
        "logic":{"question":"Next in sequence 2,4,8,16,__","answer":"32"},"final":"POWER032"},
    8: {"cipher":{"question":"Decode LURQPDQ (each letter shifted +3).","answer":"IRONMAN"},
        "debug":{"question":"Missing term: 3,6,12,24,48,?","answer":"96"},
        "logic":{"question":"I am odd; remove one letter and become even.","answer":"SEVEN"},"final":"IRONMAN96SEVEN"},
    9: {"cipher":{"question":"Using A=1..Z=26, find numeric value of 'KEY'.","answer":"41"},
        "debug":{"question":"Missing number: 2,6,12,20,30,?","answer":"42"},
        "logic":{"question":"You see me once in a year, twice in a week, never in a day.","answer":"E"},"final":"4142E"},
    10:{"cipher":{"question":"Decrypt BQQMF (shift -1).","answer":"APPLE"},
        "debug":{"question":"Next in 1,8,27,64,?","answer":"125"},
        "logic":{"question":"Comes once in a MINUTE, twice in a MOMENT, never in thousand years?","answer":"M"},"final":"APPLE125M"},
    11:{"cipher":{"question":"If all Avengers are heroes and some heroes are humans, are some Avengers humans?","answer":"YES"},
        "debug":{"question":"9×4–6=?","answer":"30"},
        "logic":{"question":"Decrypt Caesar(Shift 3): PLQG","answer":"MIND"},"final":"YES30MIND"},
    12:{"cipher":{"question":"Which doesn’t belong? HAMMER, AXE, SHIELD, LIGHTNING","answer":"SHIELD"},
        "debug":{"question":"You see me once in June, twice in November, not in May. What am I?","answer":"E"},
        "logic":{"question":"Reactor doubles every min, full at 60 — when half-full?","answer":"59"},"final":"SHIELDE59"},
    13:{"cipher":{"question":"If Time Stone controls time, which stone controls time?","answer":"TIMESTONE"},
        "debug":{"question":"Solve 3^x = 81","answer":"4"},
        "logic":{"question":"Vigenère decrypt HHKRV(key=POWER)","answer":"STONE"},"final":"TIMESTONE4STONE"},
    14:{"cipher":{"question":"I’m always ahead of you but never seen.","answer":"FUTURE"},
        "debug":{"question":"A clock at 6:00 rotated 150°. What hour now?","answer":"10"},
        "logic":{"question":"Caesar(shift3): LQILQLWB","answer":"INFINITY"},"final":"FUTURE10INFINITY"},
    15:{"cipher":{"question":"If half disappears, then half of remainder disappears, fraction remains?","answer":"QUARTER"},
        "debug":{"question":"If 5 Avengers take 5 min for 5 enemies, time for 1?","answer":"5"},
        "logic":{"question":"Caesar shift3: WKDQRV","answer":"THANOS"},"final":"QUARTER5THANOS"},
    16:{"cipher":{"question":"I am taken from you, yet you still have me.","answer":"MEMORY"},
        "debug":{"question":"Average of 6,8,10,12","answer":"9"},
        "logic":{"question":"Caesar decrypt UMKNN (shift 2)","answer":"SKILL"},"final":"MEMORY9SKILL"},
    17:{"cipher":{"question":"I have cities, but no houses; mountains, no trees; water, no fish.","answer":"MAP"},
        "debug":{"question":"Mission takes 12 days, +4 agents → 3 days less. Initial agents?","answer":"8"},
        "logic":{"question":"Caesar shift2 decrypt: UJKGNF","answer":"SHIELD"},"final":"MAP8SHIELD"},
    18:{"cipher":{"question":"I am not alive, but I grow; I need air but have no lungs.","answer":"FIRE"},
        "debug":{"question":"If each portal takes 3s, how many open in 1 min?","answer":"20"},
        "logic":{"question":"Caesar decrypt(2 shift) NQMK","answer":"LOKI"},"final":"FIRE20LOKI"},
    19:{"cipher":{"question":"If you drop me I crack, if you smile I smile back.","answer":"MIRROR"},
        "debug":{"question":"In a mirror world, east↔west. Facing east there=facing?","answer":"WEST"},
        "logic":{"question":"Vigenère decrypt PVOEB (key=IRON)","answer":"HEART"},"final":"MIRRORWESTHEART"},
    20:{"cipher":{"question":"The more you take, the more you leave behind.","answer":"FOOTSTEPS"},
        "debug":{"question":"Sequence 2,6,12,20 — next?","answer":"30"},
        "logic":{"question":"Caesar decrypt(+7): AOLYLT","answer":"TRUTH"},"final":"FOOTSTEPS30TRUTH"}
}

# ----------------------------- APP CLASS -----------------------------
class AvengersApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🛡 Avengers: Mission Control - Round 4 ")
        self.geometry("1000x650")
        self.configure(fg_color="#0b0c10")
        self.resizable(False, False)

        self.bg_canvas = ctk.CTkCanvas(self, bg="#0b0c10", highlightthickness=0)
        self.bg_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.tk.call('lower', self.bg_canvas._w)
        self.shapes = []
        self.generate_geometry()
        self.animate_background()

        ctk.CTkLabel(self, text="🛡 AVENGERS: ROUND 4 MISSION 🛡",
                     font=("Orbitron", 26, "bold"), text_color="#66fcf1").pack(pady=15)

        self.team_name = ""
        self.set_number = None
        self.current_stage = 0
        self.remaining_time = 0
        self.stage_results = {}

        self.show_team_entry()

    # ---------- Animated Background ----------
    def generate_geometry(self):
        self.shapes.clear()
        for _ in range(25):
            x, y = random.randint(0, 1000), random.randint(0, 650)
            dx, dy = random.choice([-1, 1]) * random.uniform(0.4, 1), random.choice([-1, 1]) * random.uniform(0.4, 1)
            size = random.randint(10, 40)
            color = random.choice(["#45a29e", "#1f2833", "#66fcf1"])
            self.shapes.append([x, y, dx, dy, size, color])

    def animate_background(self):
        self.bg_canvas.delete("all")
        for shape in self.shapes:
            x, y, dx, dy, size, color = shape
            x += dx; y += dy
            if x < 0 or x > 1000: dx *= -1
            if y < 0 or y > 650: dy *= -1
            shape[0], shape[1], shape[2], shape[3] = x, y, dx, dy
            self.bg_canvas.create_oval(x-size, y-size, x+size, y+size, outline=color, width=2)
            self.bg_canvas.create_line(x, y, x + math.sin(x/30)*40, y + math.cos(y/30)*40, fill=color, width=2)
        self.after(30, self.animate_background)

    # ---------- UI Screens ----------
    def clear_main(self):
        for w in self.winfo_children():
            if isinstance(w, ctk.CTkFrame): w.destroy()

    def show_team_entry(self):
        self.clear_main()
        frame = ctk.CTkFrame(self, fg_color="#0b0c10")
        frame.pack(pady=80)

        ctk.CTkLabel(frame, text="🦸 Enter Your Team Name 🦸",
                     font=("Orbitron", 22, "bold"), text_color="#66fcf1").pack(pady=25)
        self.team_entry = ctk.CTkEntry(frame, placeholder_text="Team Name", width=300, font=("Arial", 18))
        self.team_entry.pack(pady=10)

        ctk.CTkButton(frame, text="Choose Mission", fg_color="#45a29e", hover_color="#66fcf1",
                      font=("Arial Black", 20), command=self.show_cards).pack(pady=25)

    def show_cards(self):
        name = self.team_entry.get().strip()
        if not name:
            messagebox.showwarning("Wait", "Enter team name.")
            return
        self.team_name = name
        self.clear_main()

        grid = ctk.CTkFrame(self, fg_color="#0b0c10")
        grid.pack(pady=30)
        ctk.CTkLabel(grid, text=f"Select your Mission, {self.team_name}",
                     font=("Orbitron", 22, "bold"), text_color="#66fcf1").pack(pady=15)

        cards = ctk.CTkFrame(grid, fg_color="#0b0c10")
        cards.pack()
        for r in range(4):
            for c in range(5):
                i = r * 5 + c + 1
                card = ctk.CTkFrame(cards, width=150, height=100, corner_radius=15, fg_color="#1e293b")
                card.grid(row=r, column=c, padx=10, pady=10)
                ctk.CTkLabel(card, text=f"MISSION {i}", font=("Orbitron", 16, "bold"),
                             text_color="#66fcf1").pack(pady=10)
                ctk.CTkButton(card, text="START", fg_color="#45a29e", hover_color="#66fcf1",
                              command=lambda n=i: self.start_mission(n)).pack()

    # ---------- Mission Flow ----------
    def start_mission(self, n):
        self.set_number = n
        self.current_stage = 1
        self.stage_results = {}
        self.start_time = datetime.now()
        self.show_stage()

    def show_stage(self):
        self.clear_main()
        q = QUESTION_SETS[self.set_number]
        stage_map = {1:("Cipher Decryption", q["cipher"]["question"]),
                     2:("Debug Console", q["debug"]["question"]),
                     3:("Logic Puzzle", q["logic"]["question"]),
                     4:("Final Code", "Combine all clues and enter the Infinity Code.")}
        title, question = stage_map[self.current_stage]
        frame = ctk.CTkFrame(self, fg_color="#0b0c10")
        frame.pack(pady=60)

        ctk.CTkLabel(frame, text=f"Stage {self.current_stage}: {title}",
                     font=("Orbitron", 22, "bold"), text_color="#66fcf1").pack(pady=20)
        lbl = ctk.CTkLabel(frame, text=question, wraplength=800, text_color="#d1d5db", font=("Arial", 16))
        lbl.pack(pady=10)

        self.ans = ctk.CTkEntry(frame, width=500, placeholder_text="Type your answer...", font=("Arial", 18))
        self.ans.pack(pady=10)

        btns = ctk.CTkFrame(frame, fg_color="#0b0c10"); btns.pack(pady=15)
        ctk.CTkButton(btns, text="Submit", width=120, command=self.check_stage).pack(side="left", padx=10)
        ctk.CTkButton(btns, text="Skip", width=120, fg_color="#f59e0b", command=self.skip_stage).pack(side="left", padx=10)
        ctk.CTkButton(btns, text="Exit", width=120, fg_color="#dc2626", command=self.exit_game).pack(side="left", padx=10)

        self.remaining_time = TIME_LIMITS[self.current_stage]
        self.update_timer()

    def update_timer(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.after(1000, self.update_timer)
        else:
            messagebox.showinfo("Time Up", "Time's up!")
            self.stage_results[self.current_stage] = "Skipped"
            self.next_stage()

    def check_stage(self):
        ans = self.ans.get().strip().upper()
        q = QUESTION_SETS[self.set_number]
        expected = (q["cipher"]["answer"] if self.current_stage==1 else
                    q["debug"]["answer"] if self.current_stage==2 else
                    q["logic"]["answer"] if self.current_stage==3 else
                    q["final"])
        if ans == expected.upper():
            play_tone(1000, 150)
            messagebox.showinfo("Correct", "Correct! Moving ahead.")
            self.stage_results[self.current_stage] = "Correct"
            self.next_stage()
        else:
            play_tone(600, 80)
            messagebox.showwarning("Incorrect", "Incorrect. Try again or skip.")

    def skip_stage(self):
        play_tone(500, 60)
        self.stage_results[self.current_stage] = "Skipped"
        self.next_stage()

    def next_stage(self):
        self.current_stage += 1
        if self.current_stage <= 4:
            self.show_stage()
        else:
            self.finish_mission()

    def finish_mission(self):
        # ---- Save results to CSV ----
        end_time = datetime.now()
        log_path = "mission_log.csv"
        header = ["team","set","start time","end time","stage1","stage2","stage3","finalstage"]
        data = [
            self.team_name,
            self.set_number,
            self.start_time.strftime("%d-%m-%Y %H:%M"),
            end_time.strftime("%d-%m-%Y %H:%M"),
            self.stage_results.get(1,"Skipped"),
            self.stage_results.get(2,"Skipped"),
            self.stage_results.get(3,"Skipped"),
            self.stage_results.get(4,"Skipped")
        ]
        file_exists = os.path.exists(log_path)
        with open(log_path, "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(header)
            writer.writerow(data)

        # ---- Show completion screen ----
        self.clear_main()
        frame = ctk.CTkFrame(self, fg_color="#0b0c10")
        frame.pack(pady=80)
        ctk.CTkLabel(frame, text="🛡 MISSION COMPLETE 🛡",
                     font=("Orbitron", 26, "bold"), text_color="#66fcf1").pack(pady=20)
        ctk.CTkLabel(frame, text=f"Team: {self.team_name} | Mission {self.set_number}",
                     font=("Arial", 18), text_color="#d1d5db").pack(pady=5)
        ctk.CTkLabel(frame, text=f"Results: {self.stage_results}",
                     font=("Arial", 16), text_color="#45a29e").pack(pady=10)
        ctk.CTkLabel(frame, text=f"Data saved to mission_log.csv !",
                     font=("Arial", 14), text_color="#66fcf1").pack(pady=10)
        ctk.CTkButton(frame, text="Play Again", fg_color="#45a29e", hover_color="#66fcf1",
                      command=self.show_team_entry).pack(pady=20)

    def exit_game(self):
        self.destroy()

# ----------------------------- RUN APP -----------------------------
if __name__ == "__main__":
    AvengersApp().mainloop()


