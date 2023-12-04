from selenium import webdriver
import csv

##### NOTE: User input #####
element_atomic_number = 12
min_energy_KeV = 1
max_energy_KeV = 300
############################

length = max_energy_KeV-min_energy_KeV+1
browser = webdriver.Chrome()
browser.get(
    f"https://srdata.nist.gov/SRD64/Elastic/SelInitEnergy/{element_atomic_number}")

initial_energy = browser.find_element_by_id("EnergyInp")
initial_energy.clear()
initial_energy.send_keys(f"{min_energy_KeV*1000}")
display_cross_sections = browser.find_element_by_id("submitId")
display_cross_sections.click()
element = browser.find_element_by_xpath(
    '//*[@id="myForm"]/div/div[1]/div/div[2]/div[1]/div[1]')
element_symbol = str(element.text).split()[1]

all_cross_sections = []
for i in range(length):
    cross_section = browser.find_element_by_xpath(
        '/html/body/div[3]/div[2]/div/form[1]/div/div[1]/div/div[2]/div[2]/div[2]')
    total_cross_section = str(cross_section.text).split()[3]
    all_cross_sections.append(total_cross_section)
    increase_energy = browser.find_element_by_xpath('//*[@id="radStp4"]')
    increase_energy.click()
    plus_enegy_button = browser.find_element_by_id("IncEnergy")
    plus_enegy_button.click()

print("leng_of_all_data: ", len(all_cross_sections))

with open(f"cross_section_{element_symbol}.csv", 'w') as file:
    writer = csv.writer(file)
    counter = 0
    for energy in range(min_energy_KeV, max_energy_KeV+1):
        writer.writerow([energy, all_cross_sections[counter]])
        counter += 1

browser.quit()

print("...Done...")
