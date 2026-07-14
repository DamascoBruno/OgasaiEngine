from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import sqlite3
import random
import math

app = FastAPI(title="OGASAI Physical Twin Simulator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "ogasai.db"

# --- INICIALIZAÇÃO DO BANCO (SQLITE) ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS work_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Abertas',
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# --- ESTADO INTERNO DO SIMULADOR (Inércia Física) ---
# Mantém os valores anteriores para criar transições suaves e realistas
sim_state = {
    "TC-01": {
        "temperature": 182.5,  # °C (Inércia ao redor de 180°C)
        "vibration": 3.20,     # mm/s RMS
        "pressure": 8.40,      # bar
        "efficiency": 91.5     # %
    },
    "BT-02": {
        "temperature": 58.2,   # °C
        "vibration": 1.65,     # mm/s RMS
        "pressure": 3.45,      # bar
        "efficiency": 95.2     # %
    }
}

def update_physics():
    """Simula o comportamento físico real das máquinas (Random Walk com limites)."""
    # --- TURBOCOMPRESSOR (TC-01) ---
    # Temperatura: Inércia térmica lenta
    sim_state["TC-01"]["temperature"] += random.uniform(-0.4, 0.4)
    sim_state["TC-01"]["temperature"] = max(178.0, min(188.0, sim_state["TC-01"]["temperature"]))
    
    # Vibração: Flutuações mecânicas normais com leve ruído de processo
    sim_state["TC-01"]["vibration"] += random.uniform(-0.15, 0.15)
    sim_state["TC-01"]["vibration"] = max(2.5, min(4.8, sim_state["TC-01"]["vibration"]))
    
    # Pressão: Oscilação senoidal rápida em torno da linha de centro
    sim_state["TC-01"]["pressure"] = 8.4 + 0.25 * math.sin(datetime.now().second / 5.0) + random.uniform(-0.05, 0.05)
    
    # Eficiência: Cai levemente se a temperatura subir muito (relação termodinâmica)
    temp_deviation = sim_state["TC-01"]["temperature"] - 182.0
    sim_state["TC-01"]["efficiency"] = 92.0 - (temp_deviation * 0.15) + random.uniform(-0.2, 0.2)
    sim_state["TC-01"]["efficiency"] = max(88.0, min(95.0, sim_state["TC-01"]["efficiency"]))

    # --- BOMBA DE TRANSFERÊNCIA (BT-02) ---
    sim_state["BT-02"]["temperature"] += random.uniform(-0.1, 0.1)
    sim_state["BT-02"]["temperature"] = max(55.0, min(62.0, sim_state["BT-02"]["temperature"]))
    
    sim_state["BT-02"]["vibration"] += random.uniform(-0.05, 0.05)
    sim_state["BT-02"]["vibration"] = max(1.1, min(2.2, sim_state["BT-02"]["vibration"]))
    
    sim_state["BT-02"]["pressure"] = 3.5 + 0.1 * math.sin(datetime.now().second / 8.0) + random.uniform(-0.02, 0.02)
    
    sim_state["BT-02"]["efficiency"] = 95.5 + random.uniform(-0.1, 0.1)

def generate_fft_spectrum(base_vibration: float) -> List[float]:
    """
    Gera um espectro FFT realista com picos harmônicos clássicos de desalinhamento:
    Frequência Fundamental (1x RPM), Harmônica (2x RPM) e ruído de alta frequência.
    """
    spectrum = []
    for f in range(40):  # 40 canais de frequência
        noise = random.uniform(0.01, 0.04) # Ruído de fundo (piso de ruído)
        
        # Pico em 1x RPM (frequência fundamental no canal 10)
        peak_1x = 0.7 * base_vibration * math.exp(-((f - 10) / 1.8) ** 2)
        # Pico em 2x RPM (harmônica no canal 20)
        peak_2x = 0.25 * base_vibration * math.exp(-((f - 20) / 1.2) ** 2)
        # Pico de alta frequência (mancais/rolamentos no canal 32)
        peak_bearing = 0.12 * base_vibration * math.exp(-((f - 32) / 0.8) ** 2)
        
        amplitude = round(noise + peak_1x + peak_2x + peak_bearing, 3)
        spectrum.append(amplitude)
    return spectrum

# --- MODELOS ---
class TelemetryData(BaseModel):
    asset_id: str
    timestamp: datetime
    vibration: float
    temperature: float
    pressure: float
    co2: float
    efficiency: float
    fft_spectrum: List[float]  # Canal dedicado para o gráfico de FFT!

class WorkOrderCreate(BaseModel):
    asset_id: str
    title: str
    description: str
    priority: str

class WorkOrderResponse(BaseModel):
    id: int
    asset_id: str
    title: str
    description: str
    priority: str
    status: str
    created_at: str

# --- ENDPOINTS ---

@app.get("/api/v1/telemetry/current", response_model=List[TelemetryData])
async def get_current_telemetry():
    """Retorna dados de simulação de alta fidelidade física."""
    update_physics()
    
    # CO₂ emitido estimado (ton/h) correlacionado inversamente com a eficiência:
    # Menos eficiência = mais combustível queimado = maior emissão de carbono!
    co2_tc01 = 3.5 * (100.0 - sim_state["TC-01"]["efficiency"]) / 10.0
    co2_bt02 = 0.8 * (100.0 - sim_state["BT-02"]["efficiency"]) / 10.0

    return [
        TelemetryData(
            asset_id="TC-01",
            timestamp=datetime.now(),
            vibration=round(sim_state["TC-01"]["vibration"], 2),
            temperature=round(sim_state["TC-01"]["temperature"], 1),
            pressure=round(sim_state["TC-01"]["pressure"], 2),
            co2=round(co2_tc01, 2),
            efficiency=round(sim_state["TC-01"]["efficiency"], 1),
            fft_spectrum=generate_fft_spectrum(sim_state["TC-01"]["vibration"])
        ),
        TelemetryData(
            asset_id="BT-02",
            timestamp=datetime.now(),
            vibration=round(sim_state["BT-02"]["vibration"], 2),
            temperature=round(sim_state["BT-02"]["temperature"], 1),
            pressure=round(sim_state["BT-02"]["pressure"], 2),
            co2=round(co2_bt02, 2),
            efficiency=round(sim_state["BT-02"]["efficiency"], 1),
            fft_spectrum=generate_fft_spectrum(sim_state["BT-02"]["vibration"])
        )
    ]

@app.get("/api/v1/work-orders", response_model=List[WorkOrderResponse])
async def get_work_orders(status_filter: Optional[str] = Query(None, alias="status")):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if status_filter:
        cursor.execute("SELECT * FROM work_orders WHERE status = ?", (status_filter,))
    else:
        cursor.execute("SELECT * FROM work_orders")
        
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.post("/api/v1/work-orders", response_model=WorkOrderResponse, status_code=status.HTTP_201_CREATED)
async def create_work_order(payload: WorkOrderCreate):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO work_orders (asset_id, title, description, priority, status, created_at)
        VALUES (?, ?, ?, ?, 'Abertas', ?)
    """, (payload.asset_id, payload.title, payload.description, payload.priority, now))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return WorkOrderResponse(
        id=new_id,
        asset_id=payload.asset_id,
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
        status="Abertas",
        created_at=now
    )