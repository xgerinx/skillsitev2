"""
Examples of response json for Course and Module retrieve APIs
"""

clients = [
    {
        "name": "alidi",
        "logo": "alidi.svg"
    },
    {
        "name": "1с-битрикс",
        "logo": "bistrix.svg"
    },
    {
        "name": "danfoss",
        "logo": "danfoss.svg"
    }
]


course_data = {
        "name": "Excel",
        "mnemo": "excel",
        "logo": "default.png",
        "description": "Microsoft Excel course description",
        "price": 5000,
        "oldPrice": 6000,
        "currency": "₽",
        "video": None,
        "sloganGoal": "Девиз курса / Главная цель курса...",
        "category": "Office",
        "modules": [
            {
                "name": "Basic",
                "mnemo": "excel_bas",
                "course": "Excel",
                "logo": "default.png",
                "description": "Basic module description",
                "bought": None,
                "price": 1000,
                "currency": "₽"
            },
        ],
        "courseFeatures": [
            {
                "title": "ТЕСТЫ",
                "text": "Интересные",
                "logo": "test.svg"
            },
        ],
        "targetAudience": [
            {
                "profession": "Менеджеры по продажам",
                "logo": "sell_manager.svg"
            },
        ],
        "filling": [
            {
                "title": "Предварительное тестиование",
                "logo": "pre_test.svg"
            }
        ],
        "studyInCourse": [
            {
                "topic": "Работать с таблицами"
            },
        ],
        "getToKnow": [
            {
                "text": "Как устроена программа"
            },
        ],
        "clients": clients
}


module_data = {
            "name": "Basic",
            "mnemo": "excel_bas",
            "logo": "default.png",
            "description": "Basic module description",
            "bought": None,
            "price": 1000,
            "oldPrice": 1200,
            "currency": "₽",
            "video": None,
            "moduleFeatures": [
                {
                    "title": "ТЕСТЫ",
                    "text": "Интересные",
                    "logo": "test.svg"
                }
            ],
            "studyInModule": [
                {
                    "topic": "Работать с таблицами"
                }
            ],
            "sections": [
                {
                    "name": "Introduction",
                    "duration": "06:15",
                    "lessons_count": 2,
                    "lessons": [
                        {
                            "name": "Lesson 1",
                            "duration": "00:02:00",
                            "express": False,
                            "demo": False,
                            "status": [
                                {
                                    "completed": False,
                                    "bought": False,
                                }
                            ]
                        },
                        {
                            "name": "Lesson 2",
                            "duration": "00:04:15",
                            "express": False,
                            "demo": False,
                            "status": [
                                {
                                    "completed": False,
                                    "bought": False
                                }
                            ]
                        }
                    ]
                }
            ]
        }

home_data = {
    "font": "Montserrat",
    "opportunities": [
        {
            "logo": "comfort.svg",
            "text": "Если учиться, то в максимально удобных условиях! Ведь теперь вы решаете, где проходить курсы. Хотите дома? Никаких проблем. Или предпочитаете в кафе за чашечкой кофе? Отличный выбор. А может быть за окном тепло и солнечно? Супер! Ведь можно пойти в парк и учиться там. И даже по пути на работу вы можете проходить курсы с телефона! ",
            "title": "Комфорт"
        },
        {
            "logo": "flexibility.svg",
            "text": "Вы сами выбираете время обучения! Учитесь тогда, когда вам удобно! С дистанционным обучением вы не зависите от других людей, их планов или обстоятельств и можете без проблем совмещать онлайн-учебу с работой или другими планами.",
            "title": "Гибкость"
        }
    ],
    "why_us": [
        {
            "logo": "course_entirety.svg",
            "text": "Каждый курс раскрывает максимум возможностей той или иной программы",
            "title": "Полнота курса"
        },
        {
            "logo": "approach.svg",
            "text": "Каждый урок посвящен решению конкретных задач, а не просто описанию функционала",
            "title": "Подход"
        }
    ],
    "leaders": [
        {
            "course": {
                "mnemo": course_data['mnemo'],
                "title": "Microsoft",
                "name": course_data['name'],
                "color": "00FF00"
            }
        }
    ],
    "clients": clients
}