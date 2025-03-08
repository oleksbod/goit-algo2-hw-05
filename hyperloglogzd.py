import json
import time
import mmh3  # Для хешування IP-адрес
from collections import defaultdict
from hyperloglog import HyperLogLog

# Функція для завантаження IP-адрес із лог-файлу
def load_ips_from_log(file_path):
    ip_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                log_entry = json.loads(line)
                ip = log_entry.get("remote_addr")
                if ip:
                    ip_list.append(ip)
            except json.JSONDecodeError:
                continue
    return ip_list

def exact_count(ips):
    unique_set = set(ips)
    return len(unique_set)

def approximate_count(ips, p=5):
    hll = HyperLogLog(p)
    for ip in ips:
        hll.add(ip)
    return hll.count()

# Основний блок виконання
if __name__ == "__main__":
    log_file = "lms-stage-access.log"
    
    # Завантажуємо дані
    start_time = time.time()
    ip_addresses = load_ips_from_log(log_file)
    load_time = time.time() - start_time
    
    # Точний підрахунок
    start_time = time.time()
    exact_result = exact_count(ip_addresses)
    exact_time = time.time() - start_time
    
    # HyperLogLog підрахунок
    start_time = time.time()
    approx_result = approximate_count(ip_addresses)
    approx_time = time.time() - start_time
    
    # Вивід результатів
    print("Результати порівняння:")
    print(f"{'Метод':<25}{'Точний підрахунок':<20}{'HyperLogLog':<20}")
    print(f"{'Унікальні елементи':<25}{exact_result:<20}{approx_result:<20}")
    print(f"{'Час виконання (сек.)':<25}{exact_time:<20.6f}{approx_time:<20.6f}")