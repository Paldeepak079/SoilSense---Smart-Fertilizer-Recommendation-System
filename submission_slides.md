# Quasa Submission - SoilSense Presentation Content

**Constraint:** Max 6 Slides
**Focus:** Hardware (Automatic Irrigation) & Software (Fertilizer Recommendation)

---

## Slide 1: Title Slide

**Title:** SoilSense - Intelligent Agriculture System
**Subtitle:** Smart Irrigation Hardware & Fertilizer Recommendation Engine
**Hackathon:** Re-Gen & Quasa 4.0
**Team:** [Your Team Name]
**Theme:** AgriTech / Sustainable Farming

*(Visual Suggestion: SoilSense Logo, Project Image, Team Photos)*

---

## Slide 2: The Problem

**Title:** Challenges in Modern Agriculture

**Core Issues:**
1.  **Imbalanced Fertilization:** Farmers often apply excess chemical fertilizers (Urea), degrading soil health and increasing costs (₹).
2.  **Water Scarcity & Wastage:** Traditional irrigation floods fields, wasting up to 50% of water and stressing crops.
3.  **Lack of Scientific Data:** Lack of real-time soil data (pH, moisture, nutrients) leads to guesswork farming.

**Impact:**
*   Reduced soil fertility (Salinity/Acidity).
*   Lower crop yields & financial losses.
*   Environmental damage due to nutrient runoff.

---

## Slide 3: Hardware Solution (Automatic Irrigation)

**Title:** Smart IoT & Automatic Irrigation Control

**Components:**
*   **Microcontroller:** ESP32 (Wi-Fi enabled).
*   **Sensors:** Capacitive Soil Moisture, pH Sensor, EC Sensor, DHT11 (Temp/Humidity).
*   **Actuators:** 5V Relay Module controlling Water Pump/Solenoid Valve.

**How It Works (Logic):**
1.  **Real-Time Monitoring:** Sensors continuously monitor soil moisture levels (%) and temperature.
2.  **Thirsty Crop Detection:** If Moisture < Threshold (e.g., 30%), the ESP32 signals the relay.
3.  **Weather-Aware Override:** System checks Weather Forecast (Open-Meteo API) for rain.
    *   *If Rain Predicted:* Pump stays OFF (saves water).
    *   *If Clear:* Pump turns ON automatically.
4.  **Auto-Shutoff:** Once Moisture > Threshold (e.g., 80%), pump turns OFF.

**Key Feature:** "Smart Dry-Run Protection" & "Rain Delay" integration.

---

## Slide 4: Software Solution (Fertilizer Recommendation)

**Title:** AI-Driven Fertilizer Engine

**Core Functionality:**
*   **Input Flexibility:** Accepts data via IoT Sensors, Manual Entry, or Soil Health Card (OCR from Images/PDFs).
*   **Nutrient Requirement Logic:**
    *   Uses **Random Forest Regressor** (ML) trained on crop-specific N-P-K needs.
    *   Predicts exact deficit of Nitrogen (N), Phosphorus (P), and Potassium (K) for specific crops (Rice, Wheat, Cotton, etc.).

**Cost-Optimized Recommendation Algorithm:**
1.  **Converts Deficit to Products:** Maps pure N-P-K values to commercial fertilizers: *Urea, DAP, MOP, NPK 17-17-17*.
2.  **Greedy Cost Minimization:**
    *   Prioritizes **DAP** for Phosphorus (cheaper source of P + N).
    *   Uses **MOP** for Potassium.
    *   Tops up remaining Nitrogen with **Urea**.
3.  **Output:** Precise quantity in **kg/acre** and estimated Cost in **₹ (INR)**.

---

## Slide 5: Technical Architecture

**Title:** System Architecture & Tech Stack

**Tech Stack:**
*   **Hardware:** ESP32, C++, IoT Sensors.
*   **Backend:** FastAPI (Python), PostgreSQL (Database).
*   **Frontend:** React.js, Material-UI (responsive dark theme).
*   **AI/ML:** Scikit-Learn (Random Forest), Tesseract OCR (File parsing).
*   **External APIs:** Open-Meteo (Weather).

**Data Flow:**
`Sensors` → `ESP32` → `REST API` → `PostgreSQL` → `ML Engine` → `React Dashboard`

**Unique Integrations:**
*   **OCR Parsing:** Extracts data from physical Soil Health Cards photos.
*   **PDF Generation:** Auto-generates official Gov-style Soil Health Cards for farmers.

---

## Slide 6: Impact & Future Scope

**Title:** Impact & Roadmap

**Business & Social Impact:**
*   **Economic:** Reduces fertilizer costs by 15-20% via precision application.
*   **Environmental:** Prevents soil degradation and groundwater pollution.
*   **Resource Efficiency:** Saves 30-40% water via smart irrigation.

**Future Roadmap:**
*   **Drone Integration:** For aerial spectral imaging of large fields.
*   **Vernacular Voice Bot:** AI Chatbot in Hindi/Regional languages for easier access.
*   **Marketplace:** Direct link to fertilizer vendors based on recommendations.

*(Conclusion: empowering farmers with data, not just intuition.)*
