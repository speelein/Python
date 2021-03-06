from concurrent import futures
from time import sleep, time

def test(t):
    sleep(t)
    print("Ich habe {} Sekunden gewartet. Zeit: {:.0f}".format(t, time()))
    
if __name__ == "__main__":
    print("Startzeit:                          {:.0f}".format(time()))
    with futures.ProcessPoolExecutor(max_workers=3) as e:
        e.submit(test, 9)
        e.submit(test, 2)
        e.submit(test, 5)
        e.submit(test, 6)
        print("Alle Aufgaben gestartet.")
    print("Alle Aufgaben erledigt.")