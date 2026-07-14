# 🌊 OGASAI — Offshore Gas & Asset Smart Analytics Interface

<p align="center">
<img width="68" height="64" alt="image" src="https://github.com/user-attachments/assets/ed0f5224-2ac8-4d36-aa9e-d2c0ed01ddbc" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/HTML5_Canvas-Nativo-orange?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5 Canvas">
  <img src="https://img.shields.io/badge/SQLite-Persistência_Leve-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/Norma-ISO_10816--3-critical?style=for-the-badge" alt="ISO 10816-3">
  <img src="https://img.shields.io/badge/Norma-ISA_101-blueviolet?style=for-the-badge" alt="ISA 101">
</p>

---

### 📡 Sobre o Projeto

O **OGASAI** é uma plataforma industrial de **telemetria preditiva** e **monitoramento ambiental** de alto desempenho voltada para ativos rotativos críticos em plataformas de petróleo e gás *offshore*. O projeto integra engenharia de confiabilidade mecânica e sustentabilidade operacional, auxiliando indústrias no mapeamento de suas metas de descarbonização Net Zero 2050.

> 💡 **O Diferencial Ecológico:** Maquinários com alta vibração consomem mais energia e combustível devido à perda de eficiência mecânica. O OGASAI correlaciona o nível de desgaste mecânico de turbo-maquinários com as emissões diretas de carbono na mesma tela.

---

## 📸 Demonstração em Tempo Real

Veja abaixo o motor gráfico renderizando a telemetria ao vivo com comportamento estocástico realístico de sensores e zoneamento de severidade mecânica:

<p align="center">
<img width="1873" height="926" alt="image" src="https://github.com/user-attachments/assets/b57018f1-3f4c-4f02-bceb-e85e5469b250" />
</p>

---

## 🎯 Pilares e Recursos Principais

*   **⚡ Renderização Ultraleve (60 FPS):** Interface gráfica desenhada inteiramente no elemento Canvas nativo do HTML5, sem bibliotecas externas pesadas (como Chart.js ou D3), garantindo performance extrema.
*   **⚙️ Confiabilidade Preditiva (ISO 10816-3):** Monitoramento contínuo da velocidade de vibração eficaz do compressor, dividindo a operação em faixas de severidade aceitável, alerta ou perigo.
*   **🌲 Sustentabilidade Aplicada:** Conversão direta do rendimento operacional degradado em toneladas de carbono por hora emitidas à atmosfera.
*   **🎨 Usabilidade HMI (ISA 101):** Paleta de cores neutras projetada para controle operacional em longas jornadas, ativando alertas cromáticos chamativos apenas onde existe perigo operacional real.

---

## ⚙️ Estrutura do Projeto

```text
📂 OgasaiEngine/
├── 📂 Backend/                         # Camada de processamento pesado e persistência
│   ├── 📂 __pycache__/                 # Bytecode compilado do Python
│   ├── 📂 venv/                        # Ambiente virtual isolado (Virtualenv)
│   ├── 📄 .gitignore                   # Exclusão de logs e arquivos temporários do Git
│   ├── 📄 pyvenv.cfg                   # Configuração interna do ambiente Python
│   ├── 📄 main.py                      # API REST, websocket e simulação física de sensores
│   └── 💾 ogasai.db                    # Banco de dados de telemetria histórica SQLite
├── 📄 CHANGELOG.md                     # Histórico de versões e alterações do sistema
├── 📄 index.html                       # Frontend dinâmico com motor gráfico Canvas (V8)
└── 📄 README.md                        # Documentação principal do sistema
