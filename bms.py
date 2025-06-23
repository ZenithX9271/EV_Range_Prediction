import time
from fuel_system import get_battery_specs

BATTERY_SPECS = get_battery_specs()
NUM_CELLS = BATTERY_SPECS["num_cells"]
BATTERY_CAPACITY = BATTERY_SPECS["capacity"]
FULL_VOLTAGE = BATTERY_SPECS["full_voltage"]
EMPTY_VOLTAGE = BATTERY_SPECS["empty_voltage"]

SOC, P, Q, R, K = 1.0, 1, 0.01, 0.1, 0
previousTime = time.time()

def readBatteryVoltage():
    return 12.0

def readBatteryCurrent():
    return 1.5

def updateSOC(deltaT):
    global SOC, P, K
    measuredVoltage = readBatteryVoltage()
    measuredCurrent = readBatteryCurrent()

    delta_SOC = (measuredCurrent * deltaT) / (BATTERY_CAPACITY * 3600)
    SOC_pred = max(0.0, min(1.0, SOC - delta_SOC))
    P_pred = P + Q

    SOC_measured = max(0.0, min(1.0, (measuredVoltage - EMPTY_VOLTAGE) / (FULL_VOLTAGE - EMPTY_VOLTAGE)))

    K = P_pred / (P_pred + R)
    SOC = SOC_pred + K * (SOC_measured - SOC_pred)
    P = (1 - K) * P_pred

def estimateSOH():
    voltage = readBatteryVoltage()
    estimatedCapacity = ((voltage - EMPTY_VOLTAGE) / (FULL_VOLTAGE - EMPTY_VOLTAGE)) * BATTERY_CAPACITY
    return max(0.0, (estimatedCapacity / BATTERY_CAPACITY) * 100)

def main():
    global previousTime
    while True:
        currentTime = time.time()
        deltaT = currentTime - previousTime

        if deltaT >= 1:
            previousTime = currentTime
            updateSOC(deltaT)
            soh = estimateSOH()
            print(f"Voltage: {readBatteryVoltage():.2f} V | Current: {readBatteryCurrent():.2f} A | SOC: {SOC * 100:.1f}% | SOH: {soh:.1f}%")

        time.sleep(0.1)

if __name__ == "__main__":
    main()
