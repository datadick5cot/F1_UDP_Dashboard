class RaceDash extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.raceData = {};
    }

    setRaceData(data) {
        this.raceData = data;
        this.render();
    }

    render() {
        this.shadowRoot.innerHTML = `
            <style>
                .dash-container {
                    width: 100vw;
                    height: 100vh;
                    display: grid;
                    grid-template-rows: auto 1fr;
                    background-color: #1E1E1E;
                    color: white;
                    font-family: 'Roboto Mono', monospace;
                }
                    
                .dash-No-signal {
                    width: 100vw;
                    height: 100vh;
                    display: grid;
                    grid-template-rows: auto 1fr;
                    background-color: #ffffffff;
                    color: white;
                    font-family: 'Roboto Mono', monospace;
                }

                .rpm-light-bar {
                    display: flex;
                    justify-content: center;
                    gap: 0.2rem;
                    padding: 0.5rem 0;
                    background-color: #1E1E1E;
                }

                .rpm-light {
                    width: 1.5rem;
                    height: 0.5rem;
                    border-radius: 0.25rem;
                    transition: all 0.2s;
                }

                .alert-bar {
                    height: 60px;
                    padding: 10px;
                    background-color: #E10600;
                    color: white;
                    padding: 0.5rem 1rem;
                    font-weight: bold;
                    text-align: center;
                    text-transform: uppercase;
                    font-size: 1.2rem;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    gap: 1rem;
                }
.dash-content {
                    display: grid;
                    grid-template-columns: 1fr 1fr 1fr;
                    padding: 1rem;
                    gap: 1rem;
                }

                .panel {
                    background-color: rgba(30, 30, 30, 0.8);
                    border: 2px solid #333;
                    border-radius: 0.5rem;
                    padding: 1rem;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                }

                .speed-display {
                    font-size: 4rem;
                    font-weight: bold;
                    color: #FFD700;
                }

                .rpm-display {
                    font-size: 3rem;
                    color: #E10600;
                }

                .gear-display {
                    font-size: 5rem;
                    font-weight: bold;
                    color: #FFD700;
                }

                .small-display {
                    font-size: 1.2rem;
                    color: #CCC;
                }

                .value-display {
                    font-size: 2rem;
                    font-weight: bold;
                    color: white;
                }

                .progress-bar {
                    width: 100%;
                    height: 0.5rem;
                    background-color: #333;
                    border-radius: 0.25rem;
                    margin-top: 0.5rem;
                    overflow: hidden;
                }

                .progress-fill {
                    height: 100%;
                    background-color: #E10600;
                    transition: width 0.3s;
                }

                .alert-pulse {
                    animation: pulse 1.5s infinite;
                }
            </style>
            <div class="dash-container">
                ${this.renderRpmLights()}
                ${this.renderAlertBar()}
<div class="dash-content">
                    ${this.renderSpeedPanel()}
                    ${this.renderGearPanel()}
                    ${this.renderInfoPanel()}
                </div>
            </div>
        `;
    }

    renderAlertBar() {
        const activeAlert = this.raceData.alerts[0] || {};
        const activeFlag = this.raceData.flags[0] || null;

        let alertClass = '';
        if (activeAlert.type) {
            alertClass = `bg-${activeAlert.type} alert-pulse`;
        } else if (activeFlag) {
            alertClass = 'bg-warning alert-pulse';
        }

        return `
            <div class="alert-bar ${alertClass}">
                ${activeAlert.text || activeFlag || 'RACE STATUS'}
                ${activeFlag ? '<i data-feather="flag"></i>' : ''}
            </div>
        `;
    }
    renderRpmLights() {
        const rpmPercentage = Math.min(100, (this.raceData.m_revLightsPercent / 12000) * 100);
        const activeLights = Math.min(15, Math.ceil(rpmPercentage / (100/15)));
        
        let lightsHTML = '';
        for (let i = 1; i <= 15; i++) {
            let color;
            if (i <= 5) {
                color = i <= activeLights ? '#00BFFF' : '#1E1E1E'; // Blue
            } else if (i <= 10) {
                color = i <= activeLights ? '#FFA500' : '#1E1E1E'; // Amber
            } else {
                color = i <= activeLights ? '#FF0000' : '#1E1E1E'; // Red
            }
            lightsHTML += `<div class="rpm-light" style="background-color: ${color}"></div>`;
        }
        
        return `
            <div class="rpm-light-bar">
                ${lightsHTML}
            </div>
        `;
    }

    renderSpeedPanel() {
        const rpmPercentage = Math.min(100, (this.raceData.rpm / 12000) * 100);
return `
            <div class="panel">
                <div class="small-display">SPEED</div>
                <div class="speed-display">${this.raceData.m_speed}</div>
                <div class="small-display">KPH</div>
                <div class="small-display mt-4">RPM</div>
                <div class="rpm-display">${this.raceData.m_revLightsBitValue}</div>
</div>
        `;
    }

    renderGearPanel() {
        return `
            <div class="panel">
                <div class="small-display">GEAR</div>
                <div class="gear-display">${this.raceData.m_gear}</div>
                
                <div class="small-display mt-4">DELTA</div>
                <div class="value-display">${this.raceData.delta}</div>
            </div>
        `;
    }

    renderInfoPanel() {
        return `
            <div class="panel">
                <div class="small-display">LAP</div>
                <div class="value-display">${this.raceData.lap}</div>
                
                <div class="small-display mt-4">POSITION</div>
                <div class="value-display">P${this.raceData.position}</div>
                
                <div class="small-display mt-4">FUEL</div>
                <div class="value-display">${this.raceData.fuel.toFixed(1)}%</div>
                
                <div class="small-display mt-4">TEMP</div>
                <div class="value-display">${this.raceData.temp}°C</div>
            </div>
        `;
    }
}

customElements.define('race-dash', RaceDash);