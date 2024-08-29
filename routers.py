from aiogram import Router, types, F, Bot
from aiogram.filters import or_f, Command, CommandStart, StateFilter, Filter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import sqlite3
import datetime
from keyboards import *  

class assessment_text_filter(Filter):
    def __init__(self, l : dict):
        self.l = l.keys()

    async def __call__(self, msg : types.Message):
        return msg.text in self.l

main_router = Router()

est_dict = {
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

filial_list = ['A1 - Nurofshon(eski/старый)', 
                          'A4 - Lunacharski', 
                          'A5 - Shimoliy/Северный', 
                          'A6 - Kadisheva',
                          'A7 - Taraqiyot',
                          'A8 - Depo']

@main_router.message(Command('get_id'))
async def getter_id(bot : Bot, msg : types.Message):
    await bot.send_message(chat_id=389193809, text=str(msg.chat.id))

class user(StatesGroup):
    #WAITING FOR LANGUAGE
    lang_choosing = State()

    #WAITING FOR REVIEW
    rus_review = State()
    uzb_review = State()

    #WAITING FOR USER'S AFILLIATE
    rus_filial = State()
    uzb_filial = State()

    #WAITING FOR FOOD VARIETY ASSESSMENT
    rus_var = State()
    uzb_var = State()

    #WAITING FOR FOOD QUALITY ASSESSMENT
    rus_delic = State()
    uzb_delic = State()

    #WAITING FOR HYGIENE ASSESSMENT
    rus_hygiene = State()
    uzb_hygiene = State()

    #WAITING FOR TABLE TOOLS ASSESSMENT
    rus_table_tools = State()
    uzb_table_tools = State()

    #WAITING FOR EATERY PURITY ASSESSMENT
    rus_eatery_purity = State()
    uzb_eatery_purity = State()

    #WAITING FOR STAFF POLITNESS ASSESSMENT
    rus_staff_politeness = State()
    uzb_staff_politeness = State() 

    #WAITING FOR PORTION SIZE ASSESSMENT
    rus_portion_size = State()
    uzb_portion_size = State()

@main_router.message(CommandStart())
async def starter(msg : types.Message, state : FSMContext):
    #DATABASE CHECKING WHETHER USER_ID IN TABLE
    conn = sqlite3.connect('poll_database.db')
    cursor = conn.cursor()
    query = '''
            SELECT * FROM user_lang_data
            '''
    cursor.execute(query)

    #LIST OF ALL ID'S CONTAINING TUPLES
    result = cursor.fetchall()

    #CLOSE CONNECTION
    conn.commit()
    conn.close()

    #CREATING PURE LIST WITHOUT TUPLES
    final_result = []
    for tup in result:
        for value in tup:
            final_result.append(value)

    #CHECK ID'S EXISTENCE IN LIST
    if msg.from_user.id in final_result:
        #IF REGISTERED
        if final_result[final_result.index(msg.from_user.id)+1] == 'Ru🇷🇺':
            await msg.answer(f'Здравствуйте, {msg.from_user.full_name}. Ответьте, пожалуйста, на несколько вопросов, чтобы предоставить отзыв о нашей столовой.', reply_markup=provide_a_rus_review)
            await state.set_state(user.rus_review)
        elif final_result[final_result.index(msg.from_user.id)+1] == 'Uz🇺🇿':
            await msg.answer(f'Assalom alleykum, {msg.from_user.full_name}. Ovqatlanish xonamiz haqida fikr yuborish uchun bir nechta savollarga javob bering.', reply_markup=provide_an_uzb_review)
            await state.set_state(user.uzb_review)
    else:
        #OTHERWISE
        await msg.answer('Выберите язык:', reply_markup=choose_lang)
    #DATABASE CHECKING WHETHER USER_ID IN TABLE

@main_router.message(F.text == 'Ru🇷🇺', StateFilter(None))
@main_router.message(F.text == 'Uz🇺🇿', StateFilter(None))
async def lang_keeper(msg : types.Message, state : FSMContext):
    #DATABASE INSERTING
    conn = sqlite3.connect('poll_database.db')
    cursor = conn.cursor()
    query = '''
            INSERT INTO user_lang_data VALUES(?, ?)
            '''
    
    #INSERT DATA ABOUT USER ID AND LANG INTO THE DATABASE
    cursor.execute(query, (msg.from_user.id, msg.text))

    #CLOSE CONNECTION
    conn.commit()
    conn.close()

    #DATABASE INSERTING

    if msg.text == 'Ru🇷🇺':
        await msg.answer('Ваши данные успешно внесены в базу данных', reply_markup=ReplyKeyboardRemove())
        await msg.answer(f'Здравствуйте, {msg.from_user.full_name}. Ответьте, пожалуйста, на несколько вопросов, чтобы предоставить отзыв о нашей столовой.', reply_markup=provide_a_rus_review)
        await state.set_state(user.rus_review)
    else:
        await msg.answer('Ma\'lumotlaringiz ma\'lumotlar bazasiga muvaffaqiyatli kiritildi', reply_markup=ReplyKeyboardRemove())
        await msg.answer(f'Assalom alleykum, {msg.from_user.full_name}. Ovqatlanish xonamiz haqida fikr yuborish uchun bir nechta savollarga javob bering.', reply_markup=provide_an_uzb_review)
        await state.set_state(user.uzb_review)

@main_router.message(Command('change_lang'))
async def change_lang(msg : types.Message, state : FSMContext):
    #DATABASE CHECK USER'S ID EXISTENCE
    conn = sqlite3.connect('poll_database.db')
    cursor = conn.cursor()
    query = '''
            SELECT * FROM user_lang_data
            '''
    
    #LANG CHANGING
    #LANG CHANGING
    cursor.execute(query)

    #LIST OF ALL ID'S CONTAINING TUPLES
    result = cursor.fetchall()

    #CLOSE CONNECTION
    conn.commit()
    conn.close()

    #CREATING PURE LIST WITHOUT TUPLES
    final_result = []
    for tup in result:
        for value in tup:
            final_result.append(value)

    #CHECK ID'S EXISTENCE IN LIST
    if msg.from_user.id in final_result:
        #IF REGISTERED
        await state.set_state(user.lang_choosing)
        if final_result[final_result.index(msg.from_user.id)+1] == 'Ru🇷🇺':
            await msg.answer('Выберите язык, на который хотите переключиться:', reply_markup=choose_lang)
        elif final_result[final_result.index(msg.from_user.id)+1] == 'Uz🇺🇿':
            await msg.answer('O\'tishni xohlagan tilni tanlang:', reply_markup=choose_lang)
    else:
        #OTHERWISE
        await msg.answer('Вы ещё не зарегестрировались.\nНажмите на команду старт и авторизуйтесь.', reply_markup=ReplyKeyboardRemove())
    #LANG CHANGING
    #LANG CHANGING

    #DATABASE CHECK USER'S ID EXISTENCE

@main_router.message(F.text == 'Ru🇷🇺', StateFilter(user.lang_choosing))
@main_router.message(F.text == 'Uz🇺🇿', StateFilter(user.lang_choosing))
async def database_update(msg : types.Message, state : FSMContext):
    #DATABASE UPDATING
    conn = sqlite3.connect('poll_database.db')
    cursor = conn.cursor()
    query = '''
            UPDATE user_lang_data
            SET lang = ?
            WHERE id = ?
            '''
    
    #EXECUTING UPDATE QUERY
    cursor.execute(query, (msg.text, msg.from_user.id))

    #CLOSE CONNECTION
    conn.commit()
    conn.close()
    #DATABASE UPDATING

    if msg.text == 'Ru🇷🇺':
        await msg.answer('Язык изменён успешно', reply_markup=ReplyKeyboardRemove())
    else:
        await msg.answer('Til muvaffaqiyatli o\'zgartirildi', reply_markup=ReplyKeyboardRemove())

#CANCELLING
@main_router.message(F.text == 'Отмена')
@main_router.message(F.text == 'Bekor qilish')
async def main_menu(msg : types.Message, state : FSMContext):
    await state.clear()

    #SETTING APPROPRIATE ANSWER ACCORDING TO THE LANG OF THE MESSAGE
    if msg.text == 'Отмена':
        await msg.answer('Отправка отзыва отменена. Чтобы вернуться в главное меню, нажмите на команду "start"', reply_markup=ReplyKeyboardRemove())
    elif msg.text == 'Bekor qilish':
        await msg.answer('Fikr-mulohaza yuborilmoqda bekor qilindi. Asosiy menyuga qaytish uchun "start" komandosini bosing.', reply_markup=ReplyKeyboardRemove())
#CANCELLING


@main_router.message(F.text == 'Оставить отзыв', StateFilter(user.rus_review))
async def first_q(msg : types.Message, state : FSMContext):
    #DEFINE, WHETHER USER IS ATTACHED TO ANY AFILLIATE
    conn = sqlite3.connect('poll_database.db')
    cursor = conn.cursor()
    query = '''
            SELECT * FROM user_filial
            '''

    #EXECUTING QUERY
    cursor.execute(query)

    #SETTING DATA INTO THE LIST CONTAINING TUPLES
    primary_result = cursor.fetchall()


    #CLOSE CONNECTION
    conn.commit()
    conn.close()


    #CREATING PURE LIST
    final_res_list = []

    for i in primary_result:
        for value in i:
            final_res_list.append(value)


    #IF USER'S AFILLIATE REGISTERED
    if msg.from_user.id in final_res_list:
        #SAVING AFILLIATE_INFO IN TEMPORARY DICTIONARY
        await state.update_data(fil=final_res_list[final_res_list.index(msg.from_user.id)+1])

        await msg.answer('Отлично. Как вы оцените разнообразие блюд в вашей столовой?', reply_markup=rus_assessment_keyboard)

        #SETTING STATE IN ORDER TO WAIT FOR FOOD VARIETY ESTIMATION
        await state.set_state(user.rus_var)  


    #OTHERWISE
    else:
        #DETERMINATION OF USER'S AFILLIATE
        await msg.answer('Укажите филиал, в котором вы обедаете:', reply_markup=afilliate_keyboard)   

        #SETTING STATE IN ORDER TO WAIT FOR AFILLIATE  
        await state.set_state(user.rus_filial)

@main_router.message(F.text == 'Fikr qoldiring', StateFilter(user.uzb_review))
async def first_q(msg : types.Message, state : FSMContext):
    #DEFINE, WHETHER USER IS ATTACHED TO ANY AFILLIATE
    conn = sqlite3.connect('poll_database.db')
    cursor = conn.cursor()
    query = '''
            SELECT * FROM user_filial
            '''

    #EXECUTING QUERY
    cursor.execute(query)

    #SETTING DATA INTO THE LIST CONTAINING TUPLES
    primary_result = cursor.fetchall()


    #CLOSE CONNECTION
    conn.commit()
    conn.close()


    #CREATING PURE LIST
    final_res_list = []

    for i in primary_result:
        for value in i:
            final_res_list.append(value)

    #CHECK, IF AFILLIATE IS REGISTERED
    if msg.from_user.id in final_res_list:
        await state.update_data(fil=final_res_list[final_res_list.index(msg.from_user.id)+1])
    
        await msg.answer('Yaxshi. Ovqatlanish xonangizdagi taomlarning xilma-xilligini qanday baholaysiz?', reply_markup=uzb_assessment_keyboard)

        #SETTING STATE IN ORDER TO WAIT FOR FOOD VARIETY ESTIMATION
        await state.set_state(user.uzb_var) 

    #OTHERWISE
    else:
        #DETERMINATION OF USER'S AFILLIATE
        await msg.answer('Iltimos, siz ovqatlanadigan filialni ko\'rsating:', reply_markup=afilliate_keyboard)   

        #SETTING STATE IN ORDER TO WAIT FOR AFILLIATE  
        await state.set_state(user.uzb_filial)   


@main_router.message(StateFilter(user.rus_filial))
async def second_q(msg : types.Message, state : FSMContext):
    #CHECK WHETHER THE MESSAGE TEXT IS APPROPRIATE ACCORDING TO THE LIST OF AFILLIATES
    global filial_list
    if msg.text in filial_list:
        #SAVING AFILLIATE_INFO IN TEMPORARY DICTIONARY
        await state.update_data(fil=msg.text)
        
        #KEEPING INFO ABOUT USER'S ID AND AFILLIATE IN DATABASE
        conn = sqlite3.connect('poll_database.db')
        cursor = conn.cursor()
        query = '''
                INSERT INTO user_filial
                VALUES(?, ?)
                '''

        #EXECUTING QUERY
        cursor.execute(query, (msg.from_user.id, msg.text))


        #CLOSE CONNECTION
        conn.commit()
        conn.close()

        await msg.answer('Отлично. Как вы оцените разнообразие блюд в вашей столовой?', reply_markup=rus_assessment_keyboard)

        #SETTING STATE IN ORDER TO WAIT FOR FOOD VARIETY ESTIMATION
        await state.set_state(user.rus_var)  
    else:
        return

@main_router.message(StateFilter(user.uzb_filial))
async def second_q(msg : types.Message, state : FSMContext):
    #CHECK WHETHER THE MESSAGE TEXT IS APPROPRIATE ACCORDING TO THE LIST OF AFILLIATES
    global filial_list
    if msg.text in filial_list:
        #SAVING AFILLIATE_INFO IN TEMPORARY DICTIONARY
        await state.update_data(fil=msg.text)
        
        #KEEPING INFO ABOUT USER'S ID AND AFILLIATE IN DATABASE
        conn = sqlite3.connect('poll_database.db')
        cursor = conn.cursor()
        query = '''
                INSERT INTO user_filial
                VALUES(?, ?)
                '''

        #EXECUTING QUERY
        cursor.execute(query, (msg.from_user.id, msg.text))


        #CLOSE CONNECTION
        conn.commit()
        conn.close()


        await msg.answer('Yaxshi. Ovqatlanish xonangizdagi taomlarning xilma-xilligini qanday baholaysiz?', reply_markup=uzb_assessment_keyboard)

        #SETTING STATE IN ORDER TO WAIT FOR FOOD VARIETY ESTIMATION
        await state.set_state(user.uzb_var)  
    else:
        return

@main_router.message(F.text, StateFilter(user.rus_var), assessment_text_filter(est_dict))
async def third_q(msg : types.Message, state : FSMContext):
    #SETTING VALUE FOR VARIETY
    await state.update_data(variety=msg.text) 

    await msg.answer('Следующий вопрос. Как вы оцените то, насколько вкусная еда в столовой?', reply_markup=rus_assessment_keyboard)

    #SETTING STATE IN ORDER TO WAIT FOR FOOD QUALITY ESTIMATION
    await state.set_state(user.rus_delic)

@main_router.message(F.text, StateFilter(user.uzb_var), assessment_text_filter(est_dict))
async def third_q(msg : types.Message, state : FSMContext):
    #SETTING VALUE FOR VARIETY
    await state.update_data(variety=msg.text) 

    await msg.answer('Keyingi savol. Bufetdagi taomlar qanchalik mazali ekanligini qanday baholaysiz?', reply_markup=uzb_assessment_keyboard)

    #SETTING STATE IN ORDER TO WAIT FOR FOOD QUALITY ESTIMATION
    await state.set_state(user.uzb_delic)

@main_router.message(F.text, StateFilter(user.rus_delic), assessment_text_filter(est_dict))
async def fourth_q(msg : types.Message, state : FSMContext):
    #SETTING DATA FOR INFO ABOUT HOW THE FOOD DELICIOUS IS
    await state.update_data(food_delic=msg.text)

    await msg.answer('Хорошо. Дайте оценку чистоте и гигиеничности посуды, в которой подаётся еда.', reply_markup=rus_assessment_keyboard)

    #SETTING STATE IN ORDER TO WAIT FOR HYGIENE ASSESSMENT
    await state.set_state(user.rus_hygiene)

@main_router.message(F.text, StateFilter(user.uzb_delic), assessment_text_filter(est_dict))
async def fourth_q(msg : types.Message, state : FSMContext):
    #SETTING DATA FOR INFO ABOUT HOW THE FOOD DELICIOUS IS
    await state.update_data(food_delic=msg.text)

    await msg.answer('Yaxshi. Ovqat beriladigan idishlarning tozaligi va gigienasiga baho bering.', reply_markup=uzb_assessment_keyboard)

    #SETTING STATE IN ORDER TO WAIT FOR HYGIENE ASSESSMENT
    await state.set_state(user.uzb_hygiene)

@main_router.message(F.text, StateFilter(user.rus_hygiene), assessment_text_filter(est_dict))
async def fifth_q(msg : types.Message, state : FSMContext):
    #SETTING VALUE FOR DISHES PURITY
    await state.update_data(purity=msg.text)

    await msg.answer('Следующий вопрос. Как бы вы оценили наличие столовых приборов в вашей столовой?', reply_markup=rus_assessment_keyboard)

    #SETTING STATE IN ORDER TO WAIT FOR TABLE TOOLS EXISTENCE ASSESSMENT
    await state.set_state(user.rus_table_tools)

@main_router.message(F.text, StateFilter(user.uzb_hygiene), assessment_text_filter(est_dict))
async def fifth_q(msg : types.Message, state : FSMContext):
    #SETTING VALUE FOR DISHES PURITY
    await state.update_data(purity=msg.text)

    await msg.answer('Keyingi savol. Ovqatlanish xonangizda vilkalar pichoqlari mavjudligini qanday baholaysiz?', reply_markup=uzb_assessment_keyboard)

    #SETTING STATE IN ORDER TO WAIT FOR TABLE TOOLS EXISTENCE ASSESSMENT
    await state.set_state(user.uzb_table_tools)

@main_router.message(F.text, StateFilter(user.rus_table_tools), assessment_text_filter(est_dict))
async def sixth_q(msg : types.Message, state : FSMContext):
    #SETTING VALUE FOR TABLE TOOLS EXISTENCE ASSESSMENT
    await state.update_data(table_tools=msg.text)

    await msg.answer('Ок. Как вы оцените чистоту столов, стульев и полов в вашей столовой.', reply_markup=rus_assessment_keyboard)

    #SET STATE IN ORDER TO WAIT FOR EATERY PURITY ESTIMATION
    await state.set_state(user.rus_eatery_purity)

@main_router.message(F.text, StateFilter(user.uzb_table_tools), assessment_text_filter(est_dict))
async def sixth_q(msg : types.Message, state : FSMContext):
    #SETTING VALUE FOR TABLE TOOLS EXISTENCE ASSESSMENT
    await state.update_data(table_tools=msg.text)

    await msg.answer('Yaxshi. Ovqatlanish xonangizdagi stol, stul va pollarning tozaligiga qanday baho bergan bo\'lardingiz?', reply_markup=uzb_assessment_keyboard)

    #SET STATE IN ORDER TO WAIT FOR EATERY PURITY ESTIMATION
    await state.set_state(user.uzb_eatery_purity)

@main_router.message(F.text, StateFilter(user.rus_eatery_purity), assessment_text_filter(est_dict))
async def seventh_q(msg : types.Message, state : FSMContext):
    #SETTING VALUE FOR EATERY PURITY
    await state.update_data(eatery_purity=msg.text)

    await msg.answer('Следующий вопрос. Как вы оцените приветливость персонала на кухне?', reply_markup=rus_assessment_keyboard) 

    #SET STATE IN ORDER TO WAIT FOR STAFF POLITENESS ASSESSMENT
    await state.set_state(user.rus_staff_politeness)   

@main_router.message(F.text, StateFilter(user.uzb_eatery_purity), assessment_text_filter(est_dict))
async def seventh_q(msg : types.Message, state : FSMContext):
    #SETTING VALUE FOR EATERY PURITY
    await state.update_data(eatery_purity=msg.text)

    await msg.answer('Keyingi savol. Oshxona xodimlarining samimiyligini qanday baholaysiz?', reply_markup=uzb_assessment_keyboard) 

    #SET STATE IN ORDER TO WAIT FOR STAFF POLITENESS ASSESSMENT
    await state.set_state(user.uzb_staff_politeness)   

@main_router.message(F.text, StateFilter(user.rus_staff_politeness), assessment_text_filter(est_dict))
async def eight_q(msg : types.Message, state : FSMContext):
    #SETTING VALUE FOR STAFF POLITENESS
    await state.update_data(staff_politeness=msg.text)

    await msg.answer('Хорошо. Последний вопрос. Как бы вы оценили размер порций в вашей столовой?', reply_markup=rus_assessment_keyboard)

    #SET STATE IN ORDER TO WAIT FOR PORTION SIZE ASSESSMENT
    await state.set_state(user.rus_portion_size)

@main_router.message(F.text, StateFilter(user.uzb_staff_politeness), assessment_text_filter(est_dict))
async def eight_q(msg : types.Message, state : FSMContext):
    #SETTING VALUE FOR STAFF POLITENESS
    await state.update_data(staff_politeness=msg.text)

    await msg.answer('Yaxshi. Oxirgi savol. Sizning kafeteriyangizdagi porsiya o\'lchamlarini qanday baholaysiz?', reply_markup=uzb_assessment_keyboard)

    #SET STATE IN ORDER TO WAIT FOR PORTION SIZE ASSESSMENT
    await state.set_state(user.uzb_portion_size)

@main_router.message(F.text, StateFilter(user.rus_portion_size), assessment_text_filter(est_dict))
async def reporting(msg : types.Message, state : FSMContext):
    #SETTING VALUE FOR PORTION SIZE
    await state.update_data(portion_size=msg.text)

    #CREATING TEMPORARY DICTIONARY TO SAVE DATA AND INSERT IT INTO THE DATABASE
    reviewer_data_dictionary = await state.get_data()

    #STOP STATE
    await state.clear()

    #INSERTING TOTAL DATA INTO THE DATABASE
    conn = sqlite3.connect('poll_database.db')
    cursor = conn.cursor()
    query = '''
            INSERT INTO poll_data(afilliate, id, food_variety, food_quality, purity_of_dishes, table_tools_existance, purity_of_space, staff_politeness, portion_size, date)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
    
    #EXECUTING
    cursor.execute(query, (reviewer_data_dictionary['fil'], 
                           msg.from_user.id, 
                           reviewer_data_dictionary['variety'],
                           reviewer_data_dictionary['food_delic'],
                           reviewer_data_dictionary['purity'],
                           reviewer_data_dictionary['table_tools'],
                           reviewer_data_dictionary['eatery_purity'],
                           reviewer_data_dictionary['staff_politeness'],
                           reviewer_data_dictionary['portion_size'],
                           datetime.datetime.now().day))
    
    #CLOSE CONNECTION
    conn.commit()
    conn.close()

    await msg.answer('Ваш отзыв успешно добавлен в базу данных.', reply_markup=ReplyKeyboardRemove())

@main_router.message(F.text, StateFilter(user.uzb_portion_size), assessment_text_filter(est_dict))
async def reporting(msg : types.Message, state : FSMContext):
    #SETTING VALUE FOR PORTION SIZE
    await state.update_data(portion_size=msg.text)

    #CREATING TEMPORARY DICTIONARY TO SAVE DATA AND INSERT IT INTO THE DATABASE
    reviewer_data_dictionary = await state.get_data()

    #STOP STATE
    await state.clear()

    #INSERTING TOTAL DATA INTO THE DATABASE
    conn = sqlite3.connect('poll_database.db')
    cursor = conn.cursor()
    query = '''
            INSERT INTO poll_data(afilliate, id, food_variety, food_quality, purity_of_dishes, table_tools_existance, purity_of_space, staff_politeness, portion_size, date)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
    
    #EXECUTING
    cursor.execute(query, (reviewer_data_dictionary['fil'], 
                           msg.from_user.id, 
                           reviewer_data_dictionary['variety'],
                           reviewer_data_dictionary['food_delic'],
                           reviewer_data_dictionary['purity'],
                           reviewer_data_dictionary['table_tools'],
                           reviewer_data_dictionary['eatery_purity'],
                           reviewer_data_dictionary['staff_politeness'],
                           reviewer_data_dictionary['portion_size'],
                           datetime.datetime.now().day))
    
    #CLOSE CONNECTION
    conn.commit()
    conn.close()
    
    await msg.answer('Sizning sharhingiz ma\'lumotlar bazasiga muvaffaqiyatli qo\'shildi.', reply_markup=ReplyKeyboardRemove())