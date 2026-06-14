# alert_system.py

def send_alert(defect, level):

    if level == "Critical":
        print(f"🚨 ALERT: {defect} detected!")

    elif level == "High":
        print(f"⚠️ WARNING: {defect} detected!")

    elif level == "Medium":
        print(f"ℹ️ Attention: {defect} detected!")

    else:
        print("Track is safe.")
