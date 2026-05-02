**User:**

<task>
Explain the architecture of this codebase? Read only the README.md file.
</task>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs


# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T04:10:42.224Z
User time zone: America/New_York, UTC-4:00

# Current Cost
$0.00

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>ask</slug>
<name>❓ Ask</name>


# Current Workspace Directory (c:/Users/shawn/bob/f1-race-replay) Files
.gitattributes
.gitignore
contributors.md
main.py
README.md
requirements.txt
roadmap.md
telemetry.md
docs/
docs/InsightsMenu.md
docs/PitWallWindow.md
images/
images/controls/
images/controls/arrow-down.png
images/controls/arrow-left.png
images/controls/arrow-right.png
images/controls/arrow-up.png
images/controls/pause.png
images/controls/play.png
images/controls/rewind.png
images/controls/speed-.png
images/controls/speed+.png
images/tyres/
images/tyres/0.0.png
images/tyres/1.0.png
images/tyres/2.0.png
images/tyres/3.0.png
images/tyres/4.0.png
images/weather/
images/weather/drop.png
images/weather/rain.png
images/weather/thermometer.png
images/weather/wind.png
resources/
resources/cli-menu.gif
resources/gui-menu.png
resources/insights-menu.png
resources/pit-wall-window-template.png
resources/preview.png
resources/telemetry-logger.png
src/
src/bayesian_tyre_model.py
src/f1_data.py
src/run_session.py
src/tyre_degradation_integration.py
src/ui_components.py
src/cli/
src/cli/race_selection.py
src/gui/
src/gui/insights_menu.py
src/gui/pit_wall_window_template.py
src/gui/pit_wall_window.py
src/gui/race_selection.py
src/gui/settings_dialog.py
src/insights/
src/insights/driver_telemetry_window.py
src/insights/example_pit_wall_window.py
src/insights/telemetry_stream_viewer.py
src/insights/track_position_window.py
src/interfaces/
src/interfaces/qualifying.py
src/interfaces/race_replay.py
src/lib/
src/lib/season.py
src/lib/settings.py
src/lib/time.py
src/lib/tyres.py
src/services/
src/services/stream.py
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I'll read the README.md file to explain the architecture of this codebase.

<read_file>
<args>
  <file>
    <path>README.md</path>
  </file>
</args>
</read_file>

---

**User:**

[read_file for 'README.md'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
<file><path>README.md</path>
<content lines="1-258">
  1 | # F1 Race Replay 🏎️ 🏁
  2 | 
  3 | A Python application for visualizing Formula 1 race telemetry and replaying race events with interactive controls and a graphical interface.
  4 | 
  5 | ![Race Replay Preview](./resources/preview.png)
  6 | 
  7 | > **HUGE NEWS:** The telemetry stream feature is now in a usable state. See the [telemetry demo documentation](./telemetry.md) for access instructions, data format details, and usage ideas.
  8 | 
  9 | ## Features
 10 | 
 11 | - **Race Replay Visualization:** Watch the race unfold with real-time driver positions on a rendered track.
 12 | - **Safety Car Visualization:** See the Safety Car deploy from pit lane, lead the field, and return to pits — with animated transitions and pulsing glow effects.
 13 | - **Insights Menu:** Floating menu for quick access to telemetry analysis tools (launches automatically with replay).
 14 | - **Leaderboard:** See live driver positions and current tyre compounds.
 15 | - **Lap & Time Display:** Track the current lap and total race time.
 16 | - **Driver Status:** Drivers who retire or go out are marked as "OUT" on the leaderboard.
 17 | - **Interactive Controls:** Pause, rewind, fast forward, and adjust playback speed using on-screen buttons or keyboard shortcuts.
 18 | - **Legend:** On-screen legend explains all controls.
 19 | - **Driver Telemetry Insights:** View speed, gear, DRS status, and current lap for selected drivers when selected on the leaderboard.
 20 | 
 21 | ## Controls
 22 | 
 23 | - **Pause/Resume:** SPACE or Pause button
 24 | - **Rewind/Fast Forward:** ← / → or Rewind/Fast Forward buttons
 25 | - **Playback Speed:** ↑ / ↓ or Speed button (cycles through 0.5x, 1x, 2x, 4x)
 26 | - **Set Speed Directly:** Keys 1–4
 27 | - **Restart**: **R** to restart replay
 28 | - **Toggle DRS Zone**: **D** to hide/show DRS Zone
 29 | - **Toggle Progress Bar**: **B** to hide/show progress bar
 30 | - **Toggle Driver Names**: **L** to hide/show driver names on track
 31 | - **Select driver/drivers**: Click to select driver or shift click to select multiple drivers
 32 | 
 33 | 
 34 | ## Safety Car
 35 | 
 36 | The replay includes a **simulated Safety Car** that appears on track whenever the F1 data indicates a Safety Car deployment (track status code `4`). Since the F1 API does not provide GPS telemetry for the actual Safety Car, its position is simulated based on the race leader's position.
 37 | 
 38 | ### How it works
 39 | 
 40 | - **Data source:** The Safety Car deployment timing comes from the real F1 track status data via FastF1 (`session.track_status`).
 41 | - **Position simulation:** The SC is placed ~500 meters ahead of the race leader on the track reference polyline. This approximates where the real SC would be relative to the field.
 42 | - **Three animation phases:**
 43 |   - **Deploying** — The SC animates from the pit lane onto the track over ~3 seconds, with a pulsing glow and "SC DEPLOYING" label.
 44 |   - **On Track** — The SC drives ahead of the leader with a steady amber glow and "SC" label.
 45 |   - **Returning** — The SC animates back to the pit lane over ~3 seconds, with a fading pulsing glow and "SC IN" label.
 46 | - **Visual appearance:** The SC is drawn as a larger orange/amber circle (8px radius vs 6px for regular cars) with an orange outline ring and always-visible "SC" label.
 47 | 
 48 | ### Technical details
 49 | 
 50 | The SC position computation happens in `_compute_safety_car_positions()` in `src/f1_data.py`. Each frame gets a `safety_car` field:
 51 | 
 52 | ```json
 53 | {
 54 |   "safety_car": {
 55 |     "x": 1234.56,
 56 |     "y": 7890.12,
 57 |     "phase": "on_track",
 58 |     "alpha": 1.0
 59 |   }
 60 | }
 61 | ```
 62 | 
 63 | | Field | Description |
 64 | |-------|-------------|
 65 | | `x`, `y` | World coordinates of the SC |
 66 | | `phase` | `"deploying"`, `"on_track"`, or `"returning"` |
 67 | | `alpha` | Opacity value from `0.0` (invisible) to `1.0` (fully visible), used for fade in/out animation |
 68 | 
 69 | > **Note:** If you have existing cached `.pkl` files from previous runs, you must re-run with `--refresh-data` to generate SC position data. Older cached files will simply show no Safety Car.
 70 | 
 71 | ## Qualifying Session Support (in development)
 72 | 
 73 | Recently added support for Qualifying session replays with telemetry visualization including speed, gear, throttle, and brake over the lap distance. This feature is still being refined.
 74 | 
 75 | ## Requirements
 76 | 
 77 | - Python 3.11+
 78 | - [FastF1](https://github.com/theOehrly/Fast-F1)
 79 | - [Arcade](https://api.arcade.academy/en/latest/)
 80 | - numpy
 81 | 
 82 | Install dependencies:
 83 | ```bash
 84 | pip install -r requirements.txt
 85 | ```
 86 | 
 87 | FastF1 cache folder will be created automatically on first run. If it is not created, you can manually create a folder named `.fastf1-cache` in the project root.
 88 | 
 89 | ## Environment Setup
 90 | 
 91 | To get started with this project locally, you can follow these steps:
 92 | 
 93 | 1. **Clone the Repository:**
 94 |    ```bash
 95 |    git clone https://github.com/IAmTomShaw/f1-race-replay
 96 |     cd f1-race-replay
 97 |     ```
 98 | 2. **Create a Virtual Environment:**
 99 |     This process differs based on your operating system.
100 |     - On macOS/Linux:
101 |       ```bash
102 |       python3 -m venv venv
103 |       source venv/bin/activate
104 |       ```
105 |     - On Windows:
106 |       ```bash
107 |       python -m venv venv
108 |       .\venv\Scripts\activate
109 |       ```
110 | 3. **Install Dependencies:**
111 |     ```bash
112 |     pip install -r requirements.txt
113 |     ```
114 | 
115 | 4. **Run the Application:**
116 |     You can now run the application using the instructions in the Usage section below.
117 | 
118 | ## Usage
119 | 
120 | **DEFAULT GUI MENU:** To use the new GUI menu system, you can simply run:
121 | ```bash
122 | python main.py
123 | ```
124 | 
125 | ![GUI Menu Preview](./resources/gui-menu.png)
126 | 
127 | This will open a graphical interface where you can select the year and round of the race weekend you want to replay. This is still a new feature, so please report any issues you encounter.
128 | 
129 | **OPTIONAL CLI MENU:** To use the CLI menu system, you can simply run:
130 | ```bash
131 | python main.py --cli
132 | ```
133 | 
134 | ![CLI Menu Preview](./resources/cli-menu.gif)
135 | 
136 | This will prompt you with series of questions and a list of options to make your choice from using the arrow keys and enter key.
137 | 
138 | If you would already know the year and round number of the session you would like to watch, you run the commands directly as follows:
139 | 
140 | Run the main script and specify the year and round:
141 | ```bash
142 | python main.py --viewer --year 2025 --round 12
143 | ```
144 | 
145 | To run without HUD:
146 | ```bash
147 | python main.py --viewer --year 2025 --round 12 --no-hud
148 | ```
149 | 
150 | To run a Sprint session (if the event has one), add `--sprint`:
151 | ```bash
152 | python main.py --viewer --year 2025 --round 12 --sprint
153 | ```
154 | 
155 | The application will load a pre-computed telemetry dataset if you have run it before for the same event. To force re-computation of telemetry data, use the `--refresh-data` flag:
156 | ```bash
157 | python main.py --viewer --year 2025 --round 12 --refresh-data
158 | ```
159 | 
160 | ### Qualifying Session Replay
161 | 
162 | To run a Qualifying session replay, use the `--qualifying` flag:
163 | ```bash
164 | python main.py --viewer --year 2025 --round 12 --qualifying
165 | ```
166 | 
167 | To run a Sprint Qualifying session (if the event has one), add `--sprint`:
168 | ```bash
169 | python main.py --viewer --year 2025 --round 12 --qualifying --sprint
170 | ```
171 | 
172 | ## File Structure
173 | 
174 | ```
175 | f1-race-replay/
176 | ├── main.py                    # Entry point, handles session loading and starts the replay
177 | ├── requirements.txt           # Python dependencies
178 | ├── README.md                  # Project documentation
179 | ├── roadmap.md                 # Planned features and project vision
180 | ├── resources/
181 | │   └── preview.png           # Race replay preview image
182 | ├── src/
183 | │   ├── f1_data.py            # Telemetry loading, processing, frame generation & SC position simulation
184 | │   ├── arcade_replay.py      # Visualization and UI logic
185 | │   └── ui_components.py      # UI components like buttons and leaderboard
186 | │   ├── interfaces/
187 | │   │   └── qualifying.py     # Qualifying session interface and telemetry visualization
188 | │   │   └── race_replay.py    # Race replay interface, SC rendering & telemetry visualization
189 | │   └── lib/
190 | │       └── tyres.py          # Type definitions for telemetry data structures
191 | │       └── time.py           # Time formatting utilities
192 | └── .fastf1-cache/            # FastF1 cache folder (created automatically upon first run)
193 | └── computed_data/            # Computed telemetry data (created automatically upon first run)
194 | ```
195 | 
196 | ## Building Custom Telemetry Windows
197 | 
198 | When you start a race replay, an **Insights Menu** automatically appears, providing quick access to various telemetry analysis tools. You can easily create custom insight windows that receive live telemetry data using the `PitWallWindow` base class:
199 | 
200 | ```python
201 | from src.gui.pit_wall_window import PitWallWindow
202 | 
203 | class MyInsightWindow(PitWallWindow):
204 |     def setup_ui(self):
205 |         # Create your custom UI
206 |         pass
207 |     
208 |     def on_telemetry_data(self, data):
209 |         # Process telemetry data
210 |         pass
211 | ```
212 | 
213 | The `PitWallWindow` base class handles all telemetry stream connection logic automatically, allowing you to focus solely on your window's functionality.
214 | 
215 | **Key Features:**
216 | - Automatic connection to telemetry stream
217 | - Built-in status bar with connection state
218 | - Proper cleanup on window close
219 | - Simple API - just implement `setup_ui()` and `on_telemetry_data()`
220 | 
221 | **Documentation & Examples:**
222 | - See [docs/PitWallWindow.md](./docs/PitWallWindow.md) for complete guide
223 | - See [docs/InsightsMenu.md](./docs/InsightsMenu.md) for adding insights to the menu
224 | - Run the example: `python -m src.gui.example_pit_wall_window`
225 | - Test the menu: `python -m src.gui.insights_menu`
226 | 
227 | ## Customization
228 | 
229 | - Change track width, colors, and UI layout in `src/arcade_replay.py`.
230 | - Adjust telemetry processing in `src/f1_data.py`.
231 | - Create custom telemetry windows using `PitWallWindow` base class (see above).
232 | 
233 | ## Contributing
234 | 
235 | There have been several contributions from the community that have helped enhance this project. I have added a [contributors.md](./contributors.md) file to acknowledge those who have contributed features and improvements.
236 | 
237 | If you would like to contribute, feel free to:
238 | 
239 | - Open pull requests for UI improvements or new features.
240 | - Report issues on GitHub.
241 | 
242 | Please see [roadmap.md](./roadmap.md) for planned features and project vision.
243 | 
244 | # Known Issues
245 | 
246 | - The leaderboard appears to be inaccurate for the first few corners of the race. The leaderboard is also temporarily affected by a driver going in the pits. At the end of the race, the leaderboard is sometimes affected by the drivers' final x,y positions being further ahead than other drivers. These are known issues caused by inaccuracies in the telemetry and are being worked on for future releases. It's likely that these issues will be fixed in stages as improving the leaderboard accuracy is a complex task.
247 | 
248 | ## 📝 License
249 | 
250 | This project is licensed under the MIT License.
251 | 
252 | ## ⚠️ Disclaimer
253 | 
254 | No copyright infringement intended. Formula 1 and related trademarks are the property of their respective owners. All data used is sourced from publicly available APIs and is used for educational and non-commercial purposes only.
255 | 
256 | ---
257 | 
258 | Built with ❤️ by [Tom Shaw](https://tomshaw.dev)
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs


# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T04:10:57.775Z
User time zone: America/New_York, UTC-4:00

# Current Cost
$0.02

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>ask</slug>
<name>❓ Ask</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

Based on the README.md file, here's an explanation of the **F1 Race Replay** codebase architecture:

## Overview
This is a Python application for visualizing Formula 1 race telemetry and replaying race events with interactive controls and a graphical interface.

## Architecture Diagram

```mermaid
graph TB
    subgraph "Entry Point"
        A[main.py]
    end
    
    subgraph "User Interface Layer"
        B[GUI Menu System]
        C[CLI Menu System]
        D[Race Replay Viewer]
    end
    
    subgraph "Core Components"
        E[src/f1_data.py<br/>Telemetry Processing]
        F[src/arcade_replay.py<br/>Visualization Engine]
        G[src/ui_components.py<br/>UI Components]
    end
    
    subgraph "Session Interfaces"
        H[interfaces/race_replay.py<br/>Race Interface]
        I[interfaces/qualifying.py<br/>Qualifying Interface]
    end
    
    subgraph "Insights & Analysis"
        J[gui/insights_menu.py<br/>Insights Menu]
        K[gui/pit_wall_window.py<br/>Base Window Class]
        L[insights/*<br/>Telemetry Windows]
    end
    
    subgraph "Utilities"
        M[lib/tyres.py<br/>Type Definitions]
        N[lib/time.py<br/>Time Formatting]
        O[lib/season.py<br/>Season Data]
        P[lib/settings.py<br/>Settings]
    end
    
    subgraph "External Dependencies"
        Q[FastF1 API<br/>F1 Data Source]
        R[Arcade Library<br/>Graphics Engine]
    end
    
    A --> B
    A --> C
    A --> D
    D --> E
    D --> F
    F --> G
    E --> H
    E --> I
    D --> J
    J --> K
    K --> L
    E --> M
    F --> N
    E --> Q
    F --> R
    
    style A fill:#ff6b6b
    style E fill:#4ecdc4
    style F fill:#4ecdc4
    style Q fill:#95e1d3
    style R fill:#95e1d3
```

## Core Architecture Components

### 1. **Entry Point** ([`main.py`](main.py:1))
- Handles command-line arguments
- Manages session loading
- Routes to GUI or CLI menu systems
- Starts the replay viewer

### 2. **Data Processing Layer** ([`src/f1_data.py`](src/f1_data.py:1))
- **Telemetry Loading**: Fetches data from FastF1 API
- **Frame Generation**: Processes raw telemetry into frame-by-frame data
- **Safety Car Simulation**: Computes SC positions based on track status
- **Caching**: Stores computed data in `computed_data/` directory

### 3. **Visualization Layer** ([`src/arcade_replay.py`](src/arcade_replay.py:1))
- Built on **Arcade** graphics library
- Renders track, driver positions, and UI elements
- Handles animation and visual effects
- Manages Safety Car rendering with phase-based animations

### 4. **UI Components** ([`src/ui_components.py`](src/ui_components.py:1))
- Reusable UI elements (buttons, leaderboard)
- Interactive controls for playback
- Status displays and legends

### 5. **Session Interfaces**
- [`interfaces/race_replay.py`](src/interfaces/race_replay.py:1): Race-specific logic and rendering
- [`interfaces/qualifying.py`](src/interfaces/qualifying.py:1): Qualifying session support with telemetry visualization

### 6. **Insights System**
- [`gui/insights_menu.py`](src/gui/insights_menu.py:1): Floating menu for telemetry tools
- [`gui/pit_wall_window.py`](src/gui/pit_wall_window.py:1): Base class for custom telemetry windows
- [`insights/*`](src/insights/): Pre-built telemetry analysis windows
  - Driver telemetry viewer
  - Track position viewer
  - Telemetry stream viewer

### 7. **Utility Libraries**
- [`lib/tyres.py`](src/lib/tyres.py:1): Type definitions for telemetry structures
- [`lib/time.py`](src/lib/time.py:1): Time formatting utilities
- [`lib/season.py`](src/lib/season.py:1): Season data management
- [`lib/settings.py`](src/lib/settings.py:1): Application settings

## Data Flow

```mermaid
sequenceDiagram
    participant User
    participant Main
    participant Menu
    participant F1Data
    participant FastF1
    participant Arcade
    participant Insights

    User->>Main: Launch application
    Main->>Menu: Show GUI/CLI menu
    Menu->>User: Select year/round
    User->>Menu: Choose session
    Menu->>F1Data: Load session data
    F1Data->>FastF1: Fetch telemetry
    FastF1-->>F1Data: Raw telemetry data
    F1Data->>F1Data: Process & compute frames
    F1Data->>F1Data: Simulate Safety Car
    F1Data-->>Main: Frame data ready
    Main->>Arcade: Initialize replay viewer
    Main->>Insights: Launch insights menu
    loop Playback
        Arcade->>F1Data: Request frame data
        F1Data-->>Arcade: Frame telemetry
        Arcade->>Arcade: Render track & drivers
        Arcade->>User: Display visualization
        Insights->>F1Data: Stream telemetry
        F1Data-->>Insights: Live data
    end
```

## Key Features Architecture

### **Safety Car System**
- Data source: Real F1 track status via FastF1
- Position simulation: ~500m ahead of race leader
- Three animation phases: deploying → on_track → returning
- Computed in [`_compute_safety_car_positions()`](src/f1_data.py:1)

### **Telemetry Streaming**
- Real-time data broadcast to insight windows
- [`PitWallWindow`](src/gui/pit_wall_window.py:1) base class handles connections
- Extensible architecture for custom analysis tools

### **Caching Strategy**
- FastF1 cache: `.fastf1-cache/` (raw API data)
- Computed data: `computed_data/` (processed frames)
- `--refresh-data` flag forces recomputation

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Graphics Engine | [Arcade](https://api.arcade.academy/en/latest/) |
| F1 Data Source | [FastF1](https://github.com/theOehrly/Fast-F1) |
| Language | Python 3.11+ |
| Data Processing | NumPy |

## Extensibility Points

1. **Custom Telemetry Windows**: Extend [`PitWallWindow`](src/gui/pit_wall_window.py:1)
2. **UI Customization**: Modify [`arcade_replay.py`](src/arcade_replay.py:1)
3. **Data Processing**: Adjust [`f1_data.py`](src/f1_data.py:1)
4. **New Session Types**: Add interfaces in `interfaces/`

This architecture follows a **layered pattern** with clear separation between data processing, visualization, and user interaction, making it maintainable and extensible for future enhancements.

---

**User:**

[ERROR] You did not use a tool in your previous response! Please retry with a tool use.

# Reminder: Instructions for Tool Use

Tool uses are formatted using XML-style tags. The tool name itself becomes the XML tag name. Each parameter is enclosed within its own set of tags. Here's the structure:

<actual_tool_name>
<parameter1_name>value1</parameter1_name>
<parameter2_name>value2</parameter2_name>
...
</actual_tool_name>

For example, to use the attempt_completion tool:

<attempt_completion>
<result>
I have completed the task...
</result>
</attempt_completion>

Always use the actual tool name as the XML tag name for proper parsing and execution.

# Next Steps

If you have completed the user's task, use the attempt_completion tool.
If you require additional information from the user, use the ask_followup_question tool.
Otherwise, if you have not completed the task and do not need additional information, then proceed with the next step of the task.
(This is an automated message, so do not respond to it conversationally.)
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs


# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T04:11:24.839Z
User time zone: America/New_York, UTC-4:00

# Current Cost
$0.06

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>ask</slug>
<name>❓ Ask</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<attempt_completion>
<result>
Based on the README.md file, here's the **F1 Race Replay** codebase architecture:

## Overview
Python application for visualizing Formula 1 race telemetry with interactive replay controls and graphical interface.

## Architecture Layers

**1. Entry Point** ([`main.py`](main.py:1))
- Handles CLI arguments and session loading
- Routes to GUI/CLI menu systems
- Starts replay viewer

**2. Data Processing** ([`src/f1_data.py`](src/f1_data.py:1))
- Fetches telemetry from FastF1 API
- Generates frame-by-frame data
- Simulates Safety Car positions
- Manages caching in `computed_data/`

**3. Visualization** ([`src/arcade_replay.py`](src/arcade_replay.py:1))
- Built on Arcade graphics library
- Renders track, drivers, and UI
- Handles animations and effects

**4. UI Components** ([`src/ui_components.py`](src/ui_components.py:1))
- Buttons, leaderboard, controls
- Interactive playback elements

**5. Session Interfaces**
- [`interfaces/race_replay.py`](src/interfaces/race_replay.py:1): Race logic
- [`interfaces/qualifying.py`](src/interfaces/qualifying.py:1): Qualifying support

**6. Insights System**
- [`gui/insights_menu.py`](src/gui/insights_menu.py:1): Telemetry tools menu
- [`gui/pit_wall_window.py`](src/gui/pit_wall_window.py:1): Base class for custom windows
- [`insights/*`](src/insights/): Pre-built analysis windows

**7. Utilities**
- [`lib/tyres.py`](src/lib/tyres.py:1): Type definitions
- [`lib/time.py`](src/lib/time.py:1): Time formatting
- [`lib/season.py`](src/lib/season.py:1): Season data
- [`lib/settings.py`](src/lib/settings.py:1): Settings

## Key Technologies
- **Graphics**: Arcade library
- **F1 Data**: FastF1 API
- **Language**: Python 3.11+
- **Processing**: NumPy

## Notable Features
- **Safety Car**: Simulated positioning ~500m ahead of leader with 3 animation phases
- **Telemetry Streaming**: Real-time data to insight windows via [`PitWallWindow`](src/gui/pit_wall_window.py:1)
- **Caching**: Two-tier system (FastF1 raw + computed frames)

The architecture follows a layered pattern with clear separation between data processing, visualization, and user interaction.
</result>
</attempt_completion>

