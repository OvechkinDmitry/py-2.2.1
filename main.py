import taskTables
import taskStatistics
#изменение один 
dataInput = input("Введите данные для печати:")

if dataInput == 'Вакансии':
    taskTables.getTable()
elif dataInput == 'Статистика':
    taskStatistics.getStatistics()




