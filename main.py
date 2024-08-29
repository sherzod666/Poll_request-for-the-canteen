import asyncio
import datetime
import sqlite3
import openpyxl
from aiogram.filters import Command
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.strategy import FSMStrategy
from aiogram.types import BufferedInputFile
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats
from config import TOKEN
from routers import main_router

bot = Bot(token = TOKEN)
dp = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_CHAT)

cmds_list = [BotCommand(command='start', description='Запустить бота'), BotCommand(command='change_lang', description='Выбрать язык')]

dp.include_router(main_router)
 
@dp.message(Command('get_id'))
async def getter_id(msg : types.Message):
    await bot.send_message(chat_id=389193809, text=str(msg.chat.id))

#SET STATUS ALLOW_TO_SEND AND UPDATE IT ONCE A WEEK IN ORDER TO FILTER SENDING

#SEND EXCEL
async def send_excel(bot : Bot):
    while True:
        conn = sqlite3.connect('poll_database.db')
        cursor = conn.cursor()
        query = '''
                SELECT food_variety, food_quality, purity_of_dishes, table_tools_existance, purity_of_space, staff_politeness, portion_size FROM poll_data
                WHERE afilliate = ? AND allow_to_send = ?
                '''

        afilliate_list = ['A1 - Nurofshon(eski/старый)', 
                          'A4 - Lunacharski', 
                          'A5 - Shimoliy/Северный', 
                          'A6 - Kadisheva',
                          'A7 - Taraqiyot',
                          'A8 - Depo']

        estimation_dict = {
            'Juda yomon' : 1,
            'Yomon' : 2,
            'Qoniqarli' : 3,
            'Yaxshi' : 4,
            'Ajoyib' : 5,
            'Очень плохо' : 1,
            'Плохо' : 2,
            'Удовлетворительно' : 3,
            'Хорошо' : 4,
            'Отлично' : 5
        }

        excel_data = []
        name = ['Филиал', 'Разнообразие блюд', 'Вкусовые качества блюд', 'Чистота посуды', 'Наличие столовых приборов', 'Чистота столовой', 'Приветливость персонала', 'Размер порций']

        for i in afilliate_list:
            cursor.execute(query, (i, 'True'))
            res = cursor.fetchall()
            final_res = []
            for g in res:
                for q in g:
                    final_res.append(q)

            food_var = final_res[0::7]
            food_qual = final_res[1::7]
            dish_purity = final_res[2::7]
            tabtol_exist = final_res[3::7]
            eat_purity = final_res[4::7]
            staff_pol = final_res[5::7]
            port_size = final_res[6::7]

            for l in range(len(food_var)):
                food_var[l] = estimation_dict[food_var[l]]

            for n in range(len(food_qual)):
                food_qual[n] = estimation_dict[food_qual[n]]

            for q in range(len(dish_purity)):
                dish_purity[q] = estimation_dict[dish_purity[q]]

            for w in range(len(tabtol_exist)):
                tabtol_exist[w] = estimation_dict[tabtol_exist[w]]

            for d in range(len(eat_purity)):
                eat_purity[d] = estimation_dict[eat_purity[d]]

            for t in range(len(staff_pol)):
                staff_pol[t] = estimation_dict[staff_pol[t]]

            for f in range(len(port_size)):
                port_size[f] = estimation_dict[port_size[f]]

            try:
                food_var_est = float(sum(food_var) / len(food_var))
                food_qual_est = float(sum(food_qual) / len(food_qual))
                dish_purity_est = float(sum(dish_purity) / len(dish_purity))
                tabtol_exist_est = float(sum(tabtol_exist) / len(tabtol_exist))
                eat_purity_est = float(sum(eat_purity) / len(eat_purity))
                staff_pol_est = float(sum(staff_pol) / len(staff_pol))
                port_size_est = float(sum(port_size) / len(port_size))

                print(f'Filial : {i}, Разнообразие блюд : {food_var_est}\n Вкусовые качества еды : {food_qual_est}\n Чистота посуды : {dish_purity_est}\n Наличие столовых прибоворов : {tabtol_exist_est}\n Чистота столовой : {eat_purity_est}\n Приветливость персонала : {staff_pol_est}\n Размер порций : {port_size_est}')

                excel_data.append([
                    i, food_var_est, food_qual_est, dish_purity_est,
                    tabtol_exist_est, eat_purity_est, staff_pol_est, port_size_est
                ])  
            except Exception:
                pass

        def exceller():
            nonlocal name
            nonlocal excel_data

            book = openpyxl.Workbook()
            book.remove(book.active)  #REMOVE EXCESSIVE COLUMN

            sheet = book.create_sheet('Средняя статистика')
            sheet.append(name)

            #ADD ROWS TO THE TABLE
            for row in excel_data:
                sheet.append(row)

            for column_cells in sheet.columns:
                length = max(len(str(cell.value)) for cell in column_cells)
                sheet.column_dimensions[column_cells[0].column_letter].width = length + 2

            book.save('test.xlsx')

        exceller()

 
        #READING EXCEL FILE IN BYTES IN ORDER TO SET THIS VALUE TO 'FILE'
        with open('test.xlsx', 'rb') as file:
            file_data = file.read()

        if datetime.datetime.now().hour == 17 and datetime.datetime.now().minute == 0:
            await bot.send_document(chat_id=1820268210, document=BufferedInputFile(file=file_data, filename='test.xlsx'), caption='Статистика за сегодняшний день.')
            await bot.send_document(chat_id=389193809, document=BufferedInputFile(file=file_data, filename='test.xlsx'), caption='Статистика за сегодняшний день.')
            await bot.send_document(chat_id=86285361, document=BufferedInputFile(file=file_data, filename='test.xlsx'), caption='Статистика за сегодняшний день.')
            #CONNECT TO DATABASE AND CHANGE allow_to_send STATUS IN ORDER TO SEND STATISTICS ONLY FOR THE LAST WEEK
            # conn = sqlite3.connect('poll_database.db')
            # cursor = conn.cursor()
            # query = '''
            #         UPDATE poll_data
            #         SET allow_to_send = 'False'
            #         '''
            
            # #EXECUTING
            # cursor.execute(query)
            
            # #CLOSE CONNECTION
            # conn.commit()
            # conn.close()

        await asyncio.sleep(60)

async def main_func():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(cmds_list, BotCommandScopeAllPrivateChats())
    asyncio.create_task(send_excel(bot=bot))
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main_func())