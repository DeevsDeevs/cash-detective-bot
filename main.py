import asyncio
import logging
import sys
import os
from dotenv import load_dotenv
import time

from pydantic import ValidationError

from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    FSInputFile
)

import models as md
import storage as st
import charts as ch

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML) 

cash_router = Router()

default_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить трату")],
        [KeyboardButton(text="Добавить средств")],
        [KeyboardButton(text="Категории")],
        [KeyboardButton(text="Посмотреть баланс")],
        [KeyboardButton(text="Посмотреть статистику")],
    ],
    resize_keyboard=True,
)

cancel_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отменить"),
        ]
    ],
    resize_keyboard=True
)

class CashDetective(StatesGroup):
    waiting_for_purchase_description = State()
    waiting_for_purchase_cost = State()
    waiting_for_purchase_category = State()

    waiting_for_category = State()

    waiting_for_funds = State()

    check_balance = State()

    check_stats = State()

@cash_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Привет, я твой личный детектив. Давай разберемся, куда утекают твои деньги?",
        reply_markup=default_markup,
    )

@cash_router.message(F.text == "Отменить")
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Операция отменена", reply_markup=default_markup)

@cash_router.message(F.text == "Добавить трату")
async def add_purchase(message: Message, state: FSMContext):
    await state.set_state(CashDetective.waiting_for_purchase_description)
    await message.reply("Введите описание траты:", reply_markup=cancel_markup)

@cash_router.message(CashDetective.waiting_for_purchase_description)
async def process_purchase_description(message: Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)
    await state.set_state(CashDetective.waiting_for_purchase_cost)
    await message.reply("Введите стоимость:")

@cash_router.callback_query(F.data.startswith("category:"))
async def callback_category(callback: CallbackQuery, state: FSMContext):
    category = callback.data[9:]
    await state.update_data(category=category)
    await callback.message.edit_text(f"Выбрана категория: {category}")
    await callback.answer()
    user_id = callback.from_user.id
    user_data = await state.get_data()
    description = user_data.get("description")
    cost = user_data.get("cost")
    purchase = {"description": description, "cost": cost, "category": category, "timestamp": time.time()}
    await st.save_purchase(user_id, purchase)
    await bot.send_message(
        user_id,
        text=f"*Добавлена покупка:* \nОписание: {description}\nСтоимость: {cost}\nКатегория: {category}",
        reply_markup=default_markup,
        parse_mode= 'Markdown',
    )
    await state.clear()

@cash_router.message(CashDetective.waiting_for_purchase_cost)
async def process_purchase_cost(message: Message, state: FSMContext):
    cost_text = message.text
    try:
        cost_data = md.PurchaseCostModel(cost=int(cost_text))
        await state.update_data(cost=cost_data.cost)
        await state.set_state(CashDetective.waiting_for_purchase_category)

        user_id = message.from_user.id
        balance = await st.get_balance(user_id)
        if balance - cost_data.cost < 0:
            await state.clear()
            await message.reply("Это выходит за рамки вашего бюджета. *Добавление отклонено.*", reply_markup=default_markup, parse_mode= 'Markdown')
            return

        user_data = await st.get_user_data(user_id)
        categories = user_data.get("categories", [])

        if not categories:
            await state.clear()
            await message.reply("У вас еще нет категорий. Добавьте категории перед тем, как продолжить.", reply_markup=default_markup)
            return

        buttons = []
        for category in categories:
            buttons.append([InlineKeyboardButton(
                text=category,
                callback_data=f"category:{category}")
            ])
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)
        await message.answer(
            "Выберите категорию траты",
            reply_markup = markup
        )

    except (ValueError, ValidationError) as e:
        print(e)
        await message.reply("Введите валидную стоимость.")

@cash_router.message(F.text == "Категории")
async def view_categories(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = await st.get_user_data(user_id)
    categories = user_data.get("categories", [])
    categories_text = '\n'.join(categories) if categories else "Нет категорий"
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Добавить категорию"),
                KeyboardButton(text="Отменить"),
            ]
        ],
        resize_keyboard=True
    )
    await message.answer(f"Категории:\n{categories_text}", reply_markup=markup)

@cash_router.message(F.text == "Добавить категорию")
async def add_category(message: Message, state: FSMContext):
    await state.set_state(CashDetective.waiting_for_category)
    await message.answer("Введите название категории:", reply_markup=cancel_markup)

@cash_router.message(CashDetective.waiting_for_category)
async def process_category(message: Message, state: FSMContext):
    category_info = message.text
    user_id = message.from_user.id
    await st.save_category(user_id, category_info)
    await message.answer(f"Добавлена категория: *{category_info}*", reply_markup=default_markup, parse_mode= 'Markdown')
    await state.clear()

@cash_router.message(F.text == "Добавить средств")
async def add_funds(message: Message, state: FSMContext):
    await state.set_state(CashDetective.waiting_for_funds)
    await message.answer("Введите сумму средств:", reply_markup=cancel_markup)

@cash_router.message(CashDetective.waiting_for_funds)
async def process_funds(message: Message, state: FSMContext):
    funds_info = message.text
    try:
        funds_data = md.FundsModel(amount=float(funds_info))
        user_id = message.from_user.id
        balance = await st.get_balance(user_id)
        await message.answer(f"Ваш баланс: {balance} -> *{balance + funds_data.amount}*", reply_markup=default_markup, parse_mode= 'Markdown')
        await st.save_balance(user_id, funds_data.amount)
        await state.clear()
    except ValueError:
        await message.reply("Введите валидное число.")

@cash_router.message(F.text == "Посмотреть баланс")
async def check_balance(message: Message, state: FSMContext):
    await state.set_state(CashDetective.check_balance)
    user_id = message.from_user.id
    await message.answer(f"Ваш баланс сейчас: *{await st.get_balance(user_id)}*", reply_markup=default_markup, parse_mode= 'Markdown')
    await state.clear()

@cash_router.callback_query(F.data.startswith("chart:"))
async def callback_category(callback: CallbackQuery, state: FSMContext):
    chart = int(callback.data[6:])
    await callback.message.edit_text(f"Выбран график: {ch.charts[chart][0]}")
    await callback.answer()
    user_id = callback.from_user.id
    user_data = await st.get_user_data(user_id)
    chart_file = await ch.charts[chart][1](user_data)
    print(chart_file)
    await bot.send_photo(
        user_id,
        photo=FSInputFile(path=chart_file),
        caption=ch.charts[chart][0],
        reply_markup=default_markup
    )
    os.remove(chart_file)
    await state.clear()

@cash_router.message(F.text == "Посмотреть статистику")
async def check_stats(message: Message, state: FSMContext):
    await state.set_state(CashDetective.check_stats)

    buttons = []
    for chart in range(0,len(ch.charts)):
        buttons.append([InlineKeyboardButton(
            text=ch.charts[chart][0],
            callback_data=f"chart:{chart}")
        ])
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(
        "Выберите статистику, которую хотите посмотреть",
        reply_markup=markup
    )


async def main():
    dp = Dispatcher()
    dp.include_router(cash_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())