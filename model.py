import numpy as np
from datetime import datetime, timedelta

def analyze_cycle_data(logged_cycles, is_irregular=False, user_fixed_length=28):
    now = datetime.now().replace(tzinfo=None)
    
    if len(logged_cycles) == 0:
        return {
            "predicted_date": "Log a cycle! 📅",
            "current_day": 0,
            "phase": "Awaiting Data 🌙",
            "notification": "Welcome to Tsuki! Log your first period start date to activate daily phase tracking notices."
        }
        
    logged_cycles.sort(key=lambda x: x["start"])
    last_cycle = logged_cycles[-1]
    
    days_since_last_period = (now - last_cycle["start"]).days + 1 
    
    if not is_irregular and user_fixed_length:
        predicted_length = user_fixed_length
    else:
        predicted_length = 28 
        
    if len(logged_cycles) > 1:
        intervals = [(logged_cycles[i]["start"] - logged_cycles[i-1]["start"]).days for i in range(1, len(logged_cycles))]
        
        if is_irregular:
            weights = np.logspace(0.1, 1.0, num=len(intervals))
            weighted_avg = np.average(intervals, weights=weights)
            predicted_length = round(weighted_avg)
        elif not user_fixed_length:
            predicted_length = round(float(np.mean(intervals)))
            
    next_period_date = last_cycle["start"] + timedelta(days=predicted_length)
    formatted_next_date = next_period_date.strftime("%B %d, %Y")
    
    phase_name = ""
    notification = ""
    
    if last_cycle["end"]:
        bleeding_duration = (last_cycle["end"] - last_cycle["start"]).days + 1
    else:
        bleeding_duration = 5 
    
    # --- SMART NOTIFICATION MESSAGE COMPILER ---
    if days_since_last_period <= bleeding_duration:
        phase_name = "Menstrual Phase 🩸"
        notification = f"You are currently in your Menstrual Phase (Day {days_since_last_period}). Your body is working hard and resting. Keep cozy, grab a heat pad, and prioritize sleep today! 🧘‍♀️🏼"
    else:
        ovulation_day = predicted_length - 14
        if (ovulation_day - 1) <= days_since_last_period <= (ovulation_day + 1):
            phase_name = "Ovulation Phase 🥚"
            notification = f"You have entered your Ovulation Phase today! Estrogen is peak, energy levels are soaring, and your skin is glowing. It's a fantastic day to try challenging tasks! ⚡✨"
        elif days_since_last_period < (ovulation_day - 1):
            phase_name = "Follicular Phase 🌱"
            notification = f"You are in your Follicular Phase (Day {days_since_last_period}). Your body is ramping up estrogen production. You'll feel your mental sharpness and physical stamina returning!"
        else:
            phase_name = "Luteal Phase 🍂"
            notification = f"You are moving through your Luteal Phase. Progesterone is dominant, meaning your body is naturally winding down. You might experience minor bloating or sleepiness—go easy on yourself."

    return {
        "predicted_date": formatted_next_date,
        "current_day": days_since_last_period,
        "phase": phase_name,
        "notification": notification
    }