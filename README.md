# Tsuki 🌙 : A Privacy-First Menstrual Tracker

**Tsuki** is a lightweight, privacy-centric desktop menstrual cycle tracker with a built-in interactive chatbot, native system notifications, and a beautiful UI. 

In recent years, the digital privacy of menstrual and reproductive tracking data has become a critical safety concern. 
Mainstream period tracking apps have been heavily criticized for monetizing highly sensitive health data, sharing it with third-party advertisers, and leaving users vulnerable to data breaches. 

**Read more about the current crisis with mainstream tracking apps:**
* **Cambridge University:** [Menstrual tracking app data is a gold mine for advertisers that risks women's safety](https://www.cam.ac.uk/research/news/menstrual-tracking-app-data-is-a-gold-mine-for-advertisers-that-risks-womens-safety-report)
* **BBC News:** [Period tracker apps and data privacy concerns](https://www.bbc.com/news/articles/cgj8eq01vdxo)
* **Health.com:** [Should You Delete Your Period Tracking App?](https://www.health.com/news/should-you-delete-period-tracking-app)
* **ScienceDirect:** [The commercialization of reproductive health data](https://www.sciencedirect.com/science/article/pii/S0267364924001043)

Tsuki operates 100% offline.
There are no account logins, and all of your personal health data is saved exclusively as a local hidden JSON file (`.tsuki_data.json`) locked safely inside your computer's home directory. 
<img width="912" height="744" alt="Screenshot 2026-05-18 at 16 23 21" src="https://github.com/user-attachments/assets/c8bd521d-9b36-4d78-84a3-a79d33049b1a" />

Your data belongs to you and you only. 

## Installation & Usage

### For Mac Users (Downloadable App)
1. Go to the **[Releases](../../releases)** tab on this repository.
2. Download the `Tsuki.zip` file for the latest version release.
3. Double-click the `.zip` file to extract the `Tsuki.app` application.
4. Move `Tsuki.app` to your Applications folder and double-click to open!
   > *Note: If macOS gives an "unidentified developer" warning, simply right-click the app and select "Open" the first time you run it.*

### For Developers
To run Tsuki locally or compile it yourself on Mac, Windows, or Linux:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/archie-2006/Tsuki-menstrual-tracker.git](https://github.com/archie-2006/Tsuki-menstrual-tracker.git)
   cd Tsuki-menstrual-tracker
   ```
2. **Install dependencies:**
   ```bash
   pip install flet
   ```
3. **Run the app:**
   ```bash
   python main.py
   ```
4. **Compile it (if you wish to!):**
   ```bash
   pip install pyinstaller
   flet pack main.py --name "Tsuki"
   ```
