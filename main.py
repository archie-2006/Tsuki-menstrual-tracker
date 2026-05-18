import flet as ft
import json
import os  
import platform  
import asyncio  
from datetime import datetime
from model import analyze_cycle_data
from chatbot import TsukiBot

# Define a safe, cross-platform path in the user's home directory to bypass read-only sandbox limits
DATA_FILE = os.path.join(os.path.expanduser("~"), ".tsuki_data.json")

def main(page: ft.Page):
    # --- PHYSICAL WINDOW GEOMETRY CONTROL ---
    page.title = "Tsuki 🌙"
    page.window_width = 400
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = "adaptive"
    page.padding = 10
    
    # FORCE ROOT ENGINE TO STICK TO TOP WINDOW GLASS EDGE
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Custom Typography 
    page.fonts = {
        "CustomFont": "https://fonts.gstatic.com/s/sofia/v14/4UaDfGZ5N_w14_76dfxl.ttf"
    }
    page.theme = ft.Theme(font_family="CustomFont")
    
    BG_COLOR = "#FFF0F5"       
    ACCENT_COLOR = "#F48FB1"   
    TEXT_COLOR = "#880E4F"     
    CARD_BG = "#FFFFFF"        
    
    page.bgcolor = BG_COLOR
    bot = TsukiBot()
    
    state = {
        "logged_cycles": [], 
        "is_irregular": False,
        "user_fixed_length": 28,
        "condition": "Standard",
        "current_predicted_date": "Log a cycle! 📅"
    }

    # --- CROSS-PLATFORM NATIVE NOTIFICATION ROUTER ---
    def trigger_push_notification(title, message):
        current_os = platform.system().lower()
        try:
            if "darwin" in current_os:
                os.system(f"osascript -e 'display notification \"{message}\" with title \"{title}\"'")
            elif "windows" in current_os:
                powershell_cmd = (
                    f"[reflection.assembly]::loadwithpartialname('System.Windows.Forms'); "
                    f"$toast = New-Object System.Windows.Forms.NotifyIcon; "
                    f"$toast.Icon = [System.Drawing.SystemIcons]::Information; "
                    f"$toast.BalloonTipTitle = '{title}'; "
                    f"$toast.BalloonTipText = '{message}'; "
                    f"$toast.Visible = $True; "
                    f"$toast.ShowBalloonTip(5000)"
                )
                os.system(f'powershell -Command "{powershell_cmd}"')
            else:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"📢 {title}: {message}", color=CARD_BG),
                    bgcolor=ACCENT_COLOR
                )
                page.snack_bar.open = True
                page.update()
        except Exception as e:
            print(f"Notification Error: {e}")

    # --- NATIVE FILE MEMORY STAGE (HOME DIRECTORY SAFE) ---
    def save_data_to_device():
        serializable_cycles = []
        for c in state["logged_cycles"]:
            serializable_cycles.append({
                "start": c["start"].isoformat(),
                "end": c["end"].isoformat() if c["end"] else None
            })
        payload = {
            "logged_cycles": serializable_cycles,
            "is_irregular": state["is_irregular"],
            "user_fixed_length": state["user_fixed_length"]
        }
        with open(DATA_FILE, "w") as f:
            json.dump(payload, f)

    def load_data_from_device():
        try:
            with open(DATA_FILE, "r") as f:
                payload = json.load(f)
            state["is_irregular"] = payload.get("is_irregular", False)
            state["user_fixed_length"] = payload.get("user_fixed_length", 28)
            if "logged_cycles" in payload:
                state["logged_cycles"] = [
                    {
                        "start": datetime.fromisoformat(c["start"]),
                        "end": datetime.fromisoformat(c["end"]) if c["end"] else None
                    } for c in payload["logged_cycles"]
                ]
            return True
        except FileNotFoundError:
            return False

    def trigger_phase_notification():
        data = analyze_cycle_data(state["logged_cycles"], is_irregular=state["is_irregular"], user_fixed_length=state["user_fixed_length"])
        if len(state["logged_cycles"]) > 0:
            daily_insights_container.controls.clear()
            daily_insights_container.controls.append(
                ft.Container(
                    content=ft.Text(f"📢 Daily Insight: {data['notification']}", color=TEXT_COLOR, size=12, weight=ft.FontWeight.W_500),
                    bgcolor="#FCE4EC", padding=15, border_radius=15, margin=10
                )
            )

    # --- SYSTEM TIME MONITORING WORKER (7:00 AM CHRONO INJECTOR) ---
    async def morning_insight_scheduler_loop():
        last_notified_day = None
        while True:
            now = datetime.now()
            if now.hour == 7 and now.minute == 0 and now.day != last_notified_day:
                if state["logged_cycles"]:
                    analytics = analyze_cycle_data(state["logged_cycles"], is_irregular=state["is_irregular"], user_fixed_length=state["user_fixed_length"])
                    trigger_push_notification("Tsuki Morning Insight 🌙", analytics["notification"])
                else:
                    trigger_push_notification("Tsuki 🌙", "Good morning! Drop your cycle logs into your timeline to unlock customized daily metrics.")
                last_notified_day = now.day
            await asyncio.sleep(30)

    def refresh_ui():
        for cycle in state["logged_cycles"]:
            if cycle["end"] and cycle["end"] < cycle["start"]:
                cycle["end"] = None

        data = analyze_cycle_data(state["logged_cycles"], is_irregular=state["is_irregular"], user_fixed_length=state["user_fixed_length"])
        
        state["current_predicted_date"] = data["predicted_date"]
        next_date_display.value = data["predicted_date"]
        phase_display.value = f"{data['phase']} (Day {data['current_day']})" if state["logged_cycles"] else "Awaiting Data 🌙"
        
        cycle_progress_ring.value = min(data["current_day"] / state["user_fixed_length"], 1.0) if state["logged_cycles"] else 0.0
        cycle_day_lbl.value = f"Day {data['current_day']}" if state["logged_cycles"] else "Day 0"
        cycle_phase_lbl.value = data["phase"]
        
        dates_list_ui.controls.clear()
        if not state["logged_cycles"]:
            dates_list_ui.controls.append(ft.Text("No dates logged yet.", color="#9E9E9E", size=12, italic=True))
        else:
            for cycle in sorted(state["logged_cycles"], key=lambda x: x["start"]):
                start_str = cycle["start"].strftime('%b %d')
                end_str = cycle["end"].strftime('%b %d') if cycle["end"] else "Ongoing"
                dates_list_ui.controls.append(ft.Text(f"🩸 {start_str} - {end_str}", color=TEXT_COLOR, size=13, weight=ft.FontWeight.W_500))
        page.update()

    # --- CALENDAR CORE ACTION SETS ---
    def handle_start_date(e):
        if start_picker.value:
            # Safely grab the exact calendar date bypassing UTC offset traps
            local_dt = start_picker.value.astimezone() if start_picker.value.tzinfo else start_picker.value
            clean_start = datetime(local_dt.year, local_dt.month, local_dt.day)
            
            if any(c["start"].date() == clean_start.date() for c in state["logged_cycles"]):
                trigger_push_notification("Tsuki 🌙", "This start date is already logged!")
                return
                
            state["logged_cycles"].append({"start": clean_start, "end": None})
            save_data_to_device()
            trigger_push_notification("Tsuki 🌙", f"Cycle started on {clean_start.strftime('%b %d')}.")
            trigger_phase_notification()
            refresh_ui()

    def handle_end_date(e):
        if end_picker.value and len(state["logged_cycles"]) > 0:
            local_dt = end_picker.value.astimezone() if end_picker.value.tzinfo else end_picker.value
            clean_end = datetime(local_dt.year, local_dt.month, local_dt.day)
            
            valid_open_cycles = [
                c for c in state["logged_cycles"] 
                if c["end"] is None and c["start"] <= clean_end
            ]
            if valid_open_cycles:
                target_cycle = max(valid_open_cycles, key=lambda x: x["start"])
                target_cycle["end"] = clean_end
                save_data_to_device()
                trigger_push_notification("Tsuki 🌙", f"Cycle ending saved for {target_cycle['start'].strftime('%b %d')}.")
            else:
                trigger_push_notification("Tsuki 🌙", "No open cycle matching that end date found.")
            trigger_phase_notification()
            refresh_ui()

    start_picker = ft.DatePicker(on_change=handle_start_date, first_date=datetime(2023, 1, 1), last_date=datetime.now())
    end_picker = ft.DatePicker(on_change=handle_end_date, first_date=datetime(2023, 1, 1), last_date=datetime.now())
    page.overlay.extend([start_picker, end_picker])

    def undo_last_cycle(e):
        if len(state["logged_cycles"]) > 0:
            state["logged_cycles"].sort(key=lambda x: x["start"])
            state["logged_cycles"].pop()
            save_data_to_device()
            trigger_push_notification("Tsuki Tracker 🗑️", "Last entry removed.")
            trigger_phase_notification()
            refresh_ui()

    def send_msg(e):
        if not chat_input.value.strip():
            return
        user_text = chat_input.value
        chat_history.controls.append(ft.Text(f"You: {user_text}", color=TEXT_COLOR, weight=ft.FontWeight.BOLD))
        
        cleaned_text = user_text.lower()
        if "started" in cleaned_text and "today" in cleaned_text and "period" in cleaned_text:
            today_date = datetime.now().replace(tzinfo=None)
            if not any(c["start"].date() == today_date.date() for c in state["logged_cycles"]):
                state["logged_cycles"].append({"start": today_date, "end": None})
                reply = "Oh sweetie, I've got you covered! I just marked today as your cycle Start Date on your timeline. Rest up! 💆‍♀️🏼"
                save_data_to_device()
                trigger_push_notification("Tsuki Chat Auto-Log 🩸", "Period logged directly via chat interaction.")
                trigger_phase_notification()
                refresh_ui()
            else:
                reply = "I already see an entry marked for today on your timeline! 💕"
        else:
            reply = bot.get_response(user_text, condition=state["condition"], next_date=state["current_predicted_date"])
            
        chat_history.controls.append(ft.Text(f"TsukiBot 🌙: {reply}", color="#D81B60"))
        chat_input.value = ""
        page.update()

    def on_tab_change(e):
        tab_index = e.control.selected_index
        app_body.controls.clear()
        if tab_index == 0:
            app_body.controls.append(home_screen_layout)
        elif tab_index == 1:
            app_body.controls.append(chatbot_screen_layout)
        elif tab_index == 2:
            app_body.controls.append(cycle_view_screen_layout)
        page.update()

    # ==========================================
    # SCREENS DESIGN ASSEMBLY
    # ==========================================
    
    # 1. HOME SCREEN: CEILING-ANCHORED PATTERN
    app_title_header = ft.Text("Tsuki 🌙", size=32, weight=ft.FontWeight.BOLD, color=TEXT_COLOR)
    
    setup_back_btn = ft.Button(
        content=ft.Text("↩ Setup", color=TEXT_COLOR, size=11, weight=ft.FontWeight.BOLD), 
        bgcolor="#FCE4EC", 
        on_click=lambda e: page.controls.clear() or page.add(setup_view) or page.update()
    )
    
    next_date_display = ft.Text("Log a cycle! 📅", size=26, weight=ft.FontWeight.BOLD, color=CARD_BG)
    phase_display = ft.Text("Awaiting Data 🌙", size=14, color=CARD_BG, italic=True)
    prediction_card = ft.Container(content=ft.Column([ft.Text("Next Predicted Period", color=CARD_BG, size=14), next_date_display, phase_display], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER), margin=10, padding=20, bgcolor=ACCENT_COLOR, border_radius=25, shadow=ft.BoxShadow(blur_radius=10, color="#FCE4EC"))
    
    daily_insights_container = ft.Column()
    
    start_button = ft.Button(content=ft.Text("Start Date 🩸", color=CARD_BG, weight=ft.FontWeight.BOLD, size=11), bgcolor=ACCENT_COLOR, on_click=lambda e: setattr(start_picker, "open", True) or page.update())
    end_button = ft.Button(content=ft.Text("End Date 🛑", color=CARD_BG, weight=ft.FontWeight.BOLD, size=11), bgcolor=ACCENT_COLOR, on_click=lambda e: setattr(end_picker, "open", True) or page.update())
    undo_button = ft.Button(content=ft.Text("Undo ↩", color=TEXT_COLOR, weight=ft.FontWeight.BOLD, size=11), bgcolor="#FCE4EC", on_click=undo_last_cycle)
    button_row = ft.Row([start_button, end_button, undo_button], alignment=ft.MainAxisAlignment.CENTER)
    dates_list_ui = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    history_card = ft.Container(content=ft.Column([button_row, dates_list_ui], horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=10)
    
# Structural layout fix: Anchors components right against the frame ceiling
    home_screen_layout = ft.Container(
        content=ft.Column(
            [
                app_title_header,
                setup_back_btn,
                ft.Container(height=10),
                prediction_card, 
                daily_insights_container, 
                history_card
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START
        ),
        alignment=ft.Alignment(0, -1),
        margin=0  # Fixed: Unified zero value replaces the broken margin module!
    )

    # 2. CHAT SCREEN
    chat_history = ft.ListView(expand=True, spacing=10, auto_scroll=True, height=450)
    chat_box = ft.Container(content=chat_history, bgcolor=CARD_BG, border_radius=20, padding=15)
    chat_input = ft.TextField(hint_text="Type here...", border_color=ACCENT_COLOR, expand=True, color=TEXT_COLOR, on_submit=send_msg)
    send_button = ft.Button(content=ft.Text("Send ✨", color=CARD_BG, weight=ft.FontWeight.BOLD), bgcolor=ACCENT_COLOR, on_click=send_msg)
    input_row = ft.Row([chat_input, send_button])
    chatbot_screen_layout = ft.Column([ft.Text("Chat with Tsuki 💬", size=22, weight=ft.FontWeight.BOLD, color=TEXT_COLOR), chat_box, input_row], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # 3. CYCLE WHEEL SCREEN
    cycle_progress_ring = ft.ProgressRing(value=0.0, stroke_width=14, color=ACCENT_COLOR, width=180, height=180)
    cycle_day_lbl = ft.Text("Day 0", size=24, weight=ft.FontWeight.BOLD, color=TEXT_COLOR)
    cycle_phase_lbl = ft.Text("Awaiting Logs", size=14, color=TEXT_COLOR, italic=True)
    wheel_stack = ft.Stack([cycle_progress_ring, ft.Container(content=ft.Column([cycle_day_lbl, cycle_phase_lbl], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER), top=55, left=35, width=110)], width=180, height=180)
    cycle_view_screen_layout = ft.Column([ft.Text("Visual Cycle Phase Indicator", size=22, weight=ft.FontWeight.BOLD, color=TEXT_COLOR), ft.Container(height=40), wheel_stack], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # Base shell wrappers
    app_body = ft.Column(expand=True)
    app_body.controls.append(home_screen_layout) 

    nav_tabs = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Home Screen"),
            ft.NavigationBarDestination(icon=ft.Icons.CHAT, label="Chatbot Tsuki"),
            ft.NavigationBarDestination(icon=ft.Icons.AUTORENEW, label="Cycle View")
        ],
        selected_index=0,
        on_change=on_tab_change,
        bgcolor=CARD_BG
    )

    app_dashboard_scaffolding = ft.Column([app_body, nav_tabs], expand=True, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    days_input = ft.TextField(label="Regular Cycle Length (Days)", value="28", border_color=ACCENT_COLOR, color=TEXT_COLOR, width=260)
    irregular_checkbox = ft.Checkbox(label="My cycle is highly Irregular 👑", fill_color=ACCENT_COLOR, value=False)
    setup_view = ft.Column([ft.Text("Welcome to Tsuki 🌙", size=32, weight=ft.FontWeight.BOLD, color=TEXT_COLOR), days_input, irregular_checkbox, ft.Button(content=ft.Text("Enter Dashboard ✨", color=CARD_BG), bgcolor=ACCENT_COLOR, on_click=lambda e: page.controls.clear() or page.add(app_dashboard_scaffolding) or trigger_phase_notification() or refresh_ui())], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # Boot up the background time monitor for 7:00 AM push notifications
    page.run_task(morning_insight_scheduler_loop)

    if load_data_from_device() and state["logged_cycles"]:
        page.add(app_dashboard_scaffolding)
        trigger_phase_notification()
        refresh_ui()
    else:
        chat_history.controls.append(ft.Text("TsukiBot: Welcome! Ask me for a joke, period facts, or track updates! 💕", color=TEXT_COLOR))
        page.add(setup_view)

if __name__ == "__main__":
    ft.run(main)