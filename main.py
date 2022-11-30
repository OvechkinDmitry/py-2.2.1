import taskTables
import taskStatistics
#изменение из develop
>>>>>>> develop
dataInput = input("Введите данные для печати:")

if dataInput == 'Вакансии':
    taskTables.getTable()
elif dataInput == 'Статистика':
    taskStatistics.getStatistics()




