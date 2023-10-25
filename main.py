import machine
import time
import _thread
import ota  # Este es tu módulo de actualización

# Configuraciones
FIRMWARE_VERSION = 1.1  # Debe ser un float
UPDATE_URL = "https://nachobeta07.github.io/firmware.json"
LED_PIN = 18  # GPIO para el LED

# Definir el LED
led = machine.Pin(LED_PIN, machine.Pin.OUT)

def led_blink(led_pin, interval, stop_event):
    """
    Esta función maneja el parpadeo del LED.
    """
    while not stop_event.is_set():
        led_pin.value(not led_pin.value())  # Cambia el estado del LED
        time.sleep(interval)

def main():
    """
    Función principal que ejecuta las tareas requeridas.
    """
    # Crea un evento para detener el hilo
    stop_event = _thread.allocate_lock()

    # Inicia un nuevo hilo que maneja el parpadeo del LED
    _thread.start_new_thread(led_blink, (led, 30, stop_event))  # Parpadea cada 30 segundos

    while True:
        # El script principal sólo necesita llamar a la función de verificación de actualización.
        # No necesita conocer los detalles internos de cómo se realiza la actualización.
        if ota.check_for_update(FIRMWARE_VERSION, UPDATE_URL):
            print("Actualización encontrada y aplicada. El dispositivo se reiniciará.")
            machine.reset()  # Reinicia el dispositivo si la actualización fue exitosa

        time.sleep(60)  # Espera antes de la próxima verificación

# Ejecuta la función main si este script está en el punto de entrada principal
if _name_ == '_main_':
    main()