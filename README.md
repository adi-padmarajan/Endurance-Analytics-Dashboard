# 🏃‍♂️ Endurance Analytics Dashboard

Link: https://marathonsdashboard-adityapadmarajan.streamlit.app/

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.52.2-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

An interactive data visualization dashboard tracking marathon performance improvement from 4:46:07 to 3:26:00 over three years through data-driven training optimization.

## 📊 Project Overview

This dashboard analyzes **3+ years of endurance training data** from Strava, documenting the journey from recreational runner to sub-3:30 marathoner. It showcases the power of consistent training, Zone 2 base building, and data-driven decision making in athletic performance.

### Key Achievements Visualized
- **80-minute improvement** across 6 marathons (2022-2025)
- **1,712 km** annual training volume (2025)
- **Heart rate efficiency gains** through aerobic base development
- **VO₂ Max progression** from recreational to competitive levels

---

## 🎯 Features

### 📈 Interactive Pages

1. **Home** - Project overview with key performance metrics and navigation
2. **Marathon Performance Analytics** - Race-by-race progression with pace, VO₂ Max, and split analysis
3. **Training Metrics Analysis** - Annual volume, consistency tracking, and RVM 2025 prep deep-dive
4. **Heart Rate Efficiency** - Cardiovascular adaptation analysis with Zone 2 training insights
5. **Route Visualization** - GPS route maps for marathons and training runs
6. **Project Background** - Methodology, training philosophy, and data collection approach
7. **Contact** - Professional links and collaboration opportunities

### 🎨 Design Highlights

- **Cyberpunk-inspired theme** with electric cyan and neon purple aesthetics
- **Dark mode optimized** for immersive data exploration
- **Fully responsive** design for mobile and desktop
- **Interactive Plotly charts** with hover details and zoom capabilities
- **Professional typography** with custom color gradients and glows

---

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/endurance-analytics-dashboard.git
   cd endurance-analytics-dashboard
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run App.py
   ```

5. **Open in browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in your terminal

---

## 📦 Project Structure

```
endurance-analytics-dashboard/
├── App.py                          # Main application entry point
├── home.py                         # Home page module
├── marathon_performance.py         # Marathon analytics module
├── training_metrics.py            # Training volume analysis
├── heart_rate_analysis.py         # HR efficiency analysis
├── route_visualization.py         # GPS route mapping
├── background.py                  # Project background page
├── contact.py                     # Contact information page
├── gpx_utils.py                   # GPX/TCX/FIT file parsing utilities
├── styles.css                     # Custom CSS styling
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
├── .streamlit/
│   └── config.toml               # Streamlit configuration
├── datasets/
│   ├── activities_dataset.csv    # Strava activities data
│   ├── VO₂ Max.csv               # VO₂ Max progression data
│   └── global_challenges.csv     # Challenge participation data
├── activities/                    # GPS activity files (.fit.gz, .tcx.gz)
└── DEPLOYMENT_GUIDE.md           # Comprehensive deployment guide
```

---

## 🛠️ Technology Stack

### Core Framework
- **Streamlit 1.52.2** - Interactive web application framework
- **Python 3.13** - Programming language

### Data Processing
- **Pandas 2.2.3** - Data manipulation and analysis
- **NumPy 2.2.1** - Numerical computing

### Visualization
- **Plotly 6.0.0** - Interactive charts and graphs
- **Matplotlib 3.10.0** - Additional plotting capabilities

### GPS Data Processing
- **gpxpy 1.6.2** - GPX file parsing
- **fitparse 1.2.0** - FIT file parsing (Garmin devices)

### Styling
- **Custom CSS** - Cyberpunk-inspired theme with neon gradients

---

## 📊 Data Sources

### Primary Data
- **Strava Activities** - GPS-tracked runs with heart rate, pace, elevation
- **Garmin Watch Data** - FIT files with detailed metrics
- **Manual Race Data** - Official marathon results and split times

### Metrics Tracked
- Distance, pace, heart rate, elevation gain
- VO₂ Max estimates
- Training zones (Zone 2, Threshold, Maximum)
- Weekly/monthly/yearly volume aggregations

---

## 🎨 Color Palette

The dashboard uses a carefully curated **"Electric Dreams"** cyberpunk palette:

```css
--electric-cyan: #00d9ff    /* Primary highlights, titles */
--neon-purple: #b957ff      /* Data lines, charts */
--deep-violet: #1a0d2e      /* Containers, backgrounds */
--dark-abyss: #0a0420       /* Secondary backgrounds */
--ice-blue: #e0f4ff         /* Text, high readability */
```

---

## 💡 Key Insights

### Training Philosophy
1. **Progressive Overload** - Gradual volume increases from 246 km (2022) to 1,712 km (2025)
2. **Aerobic Foundation** - Majority of training at Zone 2 (60-70% of max HR = 118-137 bpm)
3. **Data-Driven Decisions** - Every run logged and analyzed for optimization

### Performance Improvements
- **Marathon PR**: 4:46:07 → 3:26:00 (80 minutes faster)
- **Average Pace**: 6:50/km → 4:50/km
- **VO₂ Max**: ~42 → ~56 ml/kg/min
- **Heart Rate Efficiency**: Lower HR at faster paces

---

## 🔧 Configuration

### Heart Rate Zones
The dashboard uses personalized heart rate zones based on **MAX_HEART_RATE = 196 bpm**:

- **Recovery**: < 118 bpm (< 60%)
- **Zone 2**: 118-137 bpm (60-70%)
- **Moderate**: 137-157 bpm (70-80%)
- **Threshold**: 157-176 bpm (80-90%)
- **Maximum**: > 176 bpm (> 90%)

These can be adjusted in [heart_rate_analysis.py](heart_rate_analysis.py#L7-L9)

---

## 🚢 Deployment

### Streamlit Community Cloud (Recommended)

1. Push to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Select your repository
4. Deploy!

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions including Docker and Heroku options.

---

## 📝 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2025 Aditya Padmarajan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👤 Author

**Aditya Padmarajan**

- **LinkedIn**: [linkedin.com/in/aditya-padmarajan](https://www.linkedin.com/in/aditya-padmarajan/)
- **GitHub**: [github.com/adi-padmarajan](https://github.com/adi-padmarajan)
- **Email**: aditya.padmarajan@gmail.com

---

## 🙏 Acknowledgments

- **Strava** - For comprehensive activity tracking and API access
- **Streamlit** - For the excellent web framework
- **Plotly** - For interactive visualization capabilities
- **Royal Victoria Marathon** - For providing the races that inspired this project
- **BMO Vancouver Marathon** - For additional race opportunities

---

## 📸 Screenshots

### Home Page
Interactive overview with key metrics and navigation

### Marathon Performance
Race-by-race progression visualization with pace analysis

### Training Metrics
Annual volume tracking and RVM 2025 prep analysis

### Heart Rate Efficiency
Cardiovascular adaptation through Zone 2 training

### Route Visualization
GPS maps of marathon routes and training runs

---

## 🔮 Future Enhancements

- [ ] Real-time Strava API integration for live data updates
- [ ] Predictive race time calculator based on training volume
- [ ] Advanced pace zone distribution analysis
- [ ] Training load and recovery metrics
- [ ] Comparative analysis with other athletes (anonymized)
- [ ] Mobile app version
- [ ] Export reports as PDF

---

## 🐛 Bug Reports & Feature Requests

Found a bug or have a feature request? Please open an issue on GitHub with:
- Clear description of the issue/feature
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Screenshots if applicable

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📈 Performance Stats

- **Total Runs Analyzed**: 200+
- **Total Distance Tracked**: 3,000+ km
- **Data Points Visualized**: 10,000+
- **Marathon Races**: 6
- **Years of Training Data**: 3+

---

## 🔒 Privacy & Data

- All data is sourced from the author's personal Strava account
- No user authentication required (public dashboard)
- No tracking or analytics beyond Streamlit's defaults
- GPS data includes only public race routes and select training routes

---

## ⚡ Performance Notes

- **Load Time**: 2-3 seconds on standard connections
- **Memory Usage**: ~200-300 MB
- **Suitable for**: Streamlit Community Cloud free tier
- **Responsive**: Optimized for screens 320px - 2560px wide

---

## 📚 Learn More

### Training Methodology
- **80/20 Training** - Majority low-intensity, minority high-intensity
- **Polarized Training** - Zone 2 base building with targeted speedwork
- **Progressive Overload** - Systematic volume increases with recovery

### Data Science Tools
- [Streamlit Documentation](https://docs.streamlit.io)
- [Plotly Python Graphing Library](https://plotly.com/python/)
- [Pandas User Guide](https://pandas.pydata.org/docs/user_guide/index.html)

---

<div align="center">

**Built by Aditya Padmarajan**

⭐ Star this repo if you found it helpful!



</div>

---

