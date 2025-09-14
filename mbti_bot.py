from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# توکن رباتت رو اینجا بذار
TOKEN = "YOUR_BOT_TOKEN_HERE"

# لیست سؤال‌ها با ترجمه‌ها. برای کامل بودن، 93 سؤال اضافه شده اما برای اختصار، نمونه‌ها گذاشته شده.
QUESTIONS = [
    {
        "text": {
            "en": "When you go somewhere for the day, would you rather",
            "fa": "وقتی برای یک روز جایی می‌روید، ترجیح می‌دهید",
            "ar": "عندما تذهب إلى مكان ليوم واحد، هل تفضل"
        },
        "options": [
            (
                {"en": "Plan what you will do and when", "fa": "برنامه‌ریزی کنید چه کنید و کی", "ar": "تخطيط ما ستفعله ومتى"},
                "J", "JP"
            ),
            (
                {"en": "Just go", "fa": "فقط بروید", "ar": "فقط الذهاب"},
                "P", "JP"
            )
        ]
    },
    {
        "text": {
            "en": "If you were a teacher, would you rather teach",
            "fa": "اگر معلم بودید، ترجیح می‌دادید تدریس کنید",
            "ar": "إذا كنت معلماً، هل تفضل تدريس"
        },
        "options": [
            (
                {"en": "Facts-based courses", "fa": "دوره‌های مبتنی بر واقعیت", "ar": "دورات مبنية على الحقائق"},
                "S", "SN"
            ),
            (
                {"en": "Courses involving opinion or theory", "fa": "دوره‌های شامل نظر یا تئوری", "ar": "دورات تشمل الرأي أو النظرية"},
                "N", "SN"
            )
        ]
    },
    {
        "text": {
            "en": "Are you usually",
            "fa": "معمولاً هستید",
            "ar": "عادة ما تكون"
        },
        "options": [
            (
                {"en": "A 'good mixer' with groups of people", "fa": "یک مخلوط‌کننده خوب با گروه‌های مردم", "ar": "مختلط جيد مع مجموعات من الناس"},
                "E", "EI"
            ),
            (
                {"en": "Rather quiet and reserved", "fa": "نسبتاً ساکت و محافظه‌کار", "ar": "بدلاً من ذلك هادئ ومحتفظ"},
                "I", "EI"
            )
        ]
    },
    {
        "text": {
            "en": "Do you more often let",
            "fa": "آیا اغلب اجازه می‌دهید",
            "ar": "هل تترك غالباً"
        },
        "options": [
            (
                {"en": "Your heart rule your head", "fa": "قلب‌تان بر ذهن‌تان حاکم شود", "ar": "قلبك يحكم عقلك"},
                "F", "TF"
            ),
            (
                {"en": "Your head rule your heart", "fa": "ذهن‌تان بر قلب‌تان حاکم شود", "ar": "عقلك يحكم قلبك"},
                "T", "TF"
            )
        ]
    },
    # برای کامل بودن، 89 سؤال دیگر با ترجمه‌های دقیق اضافه کن. این نمونه‌ها الگو هستند.
    # مثال سؤال اضافی:
    {
        "text": {
            "en": "In doing something that many other people do, would you rather",
            "fa": "در انجام کاری که بسیاری از افراد انجام می‌دهند، ترجیح می‌دهید",
            "ar": "في القيام بشيء يقوم به العديد من الأشخاص، هل تفضل"
        },
        "options": [
            (
                {"en": "Invent a way of your own", "fa": "روش خودتان را ابداع کنید", "ar": "ابتكار طريقة خاصة بك"},
                "N", "SN"
            ),
            (
                {"en": "Do it in the accepted way", "fa": "آن را به روش پذیرفته‌شده انجام دهید", "ar": "القيام به بالطريقة المقبولة"},
                "S", "SN"
            )
        ]
    },
    # ... (تا 93 سؤال کامل شود. از منابع استاندارد MBTI مثل Form M استفاده کن)
]

# توضیحات شخصیت با ترجمه‌ها. هر توضیح مفصل و دقیق است.
type_descriptions = {
    'INTJ': {
        "en": """INTJ (Architect): You are a strategic thinker and innovator. **Strengths**: Exceptional at long-term planning, independent, adept at solving complex problems, and deeply committed to your goals. You thrive on creating efficient systems and envisioning future possibilities. **Weaknesses**: You may come across as overly critical, struggle to express emotions, and your perfectionism can lead to procrastination. You might seem distant to others due to your focus on ideas over social interactions. **Relationships**: You prefer deep, intellectual connections and are fiercely loyal, but you need personal space. Emotional relationships can be challenging as you prioritize logic over feelings, which may create misunderstandings. **Careers**: Ideal roles include executive manager, scientist, software engineer, strategic lawyer, or university professor, where your analytical and visionary skills shine. **Personal Growth**: Focus on developing emotional intelligence, practicing active listening, and embracing flexibility to balance your structured approach. **Full Interpretation**: INTJs are visionaries who see the world as a puzzle to solve or a system to optimize. You excel in scientific, technical, or strategic fields, often leading with bold ideas. However, your tendency to avoid casual social interactions can make you seem aloof. At work, you are a natural leader who values efficiency, but you may need to inspire rather than direct your team. In personal life, you are a loyal partner but require someone who respects your need for independence. If you're an INTJ, balancing work with personal relationships and cultivating empathy can make your life richer. Statistically, INTJs make up about 2% of the population, often excelling in leadership but risking isolation if relationships are neglected. Their strategic mindset makes them pioneers in innovation.""",
        "fa": """INTJ (معمار): شما یک متفکر استراتژیک و نوآور هستید. **نقاط قوت**: در برنامه‌ریزی بلندمدت بی‌نظیرید، مستقل عمل می‌کنید، در حل مسائل پیچیده مهارت دارید و به اهداف‌تان عمیقاً متعهد هستید. شما از ایجاد سیستم‌های کارآمد و تصور امکانات آینده لذت می‌برید. **نقاط ضعف**: ممکن است بیش از حد انتقادی به نظر برسید، در بیان احساسات مشکل داشته باشید و کمال‌گرایی‌تان منجر به تعلل شود. به دلیل تمرکز بر ایده‌ها به جای تعاملات اجتماعی، گاهی دور از دیگران به نظر می‌رسید. **روابط**: روابط عمیق و فکری را ترجیح می‌دهید و بسیار وفادار هستید، اما به فضای شخصی نیاز دارید. روابط عاطفی ممکن است برای‌تان چالش‌برانگیز باشد زیرا منطق را بر احساسات مقدم می‌دانید، که می‌تواند باعث سوءتفاهم شود. **شغل‌ها**: نقش‌های ایده‌آل شامل مدیر اجرایی، دانشمند، مهندس نرم‌افزار، وکیل استراتژیک یا استاد دانشگاه است، جایی که مهارت‌های تحلیلی و آینده‌نگرانه شما می‌درخشد. **رشد شخصی**: روی هوش عاطفی، تمرین گوش دادن فعال و پذیرش انعطاف‌پذیری برای متعادل کردن رویکرد ساختارمندتان کار کنید. **تفسیر کامل**: INTJها آینده‌نگر هستند و جهان را به عنوان یک پازل می‌بینند که باید حل شود یا سیستمی که باید بهینه شود. شما در زمینه‌های علمی، فنی یا استراتژیک عالی هستید و اغلب با ایده‌های جسورانه رهبری می‌کنید. اما تمایل به اجتناب از تعاملات اجتماعی روزمره ممکن است شما را منزوی نشان دهد. در کار، شما رهبر طبیعی هستید که به کارایی اهمیت می‌دهید، اما ممکن است نیاز باشد به جای دستور دادن، تیم را الهام ببخشید. در زندگی شخصی، شما شریک وفاداری هستید اما به کسی نیاز دارید که استقلال‌تان را درک کند. اگر INTJ هستید، متعادل کردن کار با روابط شخصی و پرورش همدلی می‌تواند زندگی‌تان را غنی‌تر کند. از نظر آماری، INTJها حدود 2% جمعیت را تشکیل می‌دهند و اغلب در نقش‌های رهبری موفق‌اند اما اگر روابط را نادیده بگیرند، ممکن است احساس انزوا کنند. ذهن استراتژیک آنها را پیشگامان نوآوری می‌کند.""",
        "ar": """INTJ (المهندس المعماري): أنت مفكر استراتيجي ومبتكر. **نقاط القوة**: متميز في التخطيط طويل الأمد، مستقل، بارع في حل المشكلات المعقدة، وملتزم بشدة بأهدافك. تستمتع بإنشاء أنظمة فعالة وتخيل الإمكانيات المستقبلية. **نقاط الضعف**: قد تبدو ناقدًا زائدًا، تواجه صعوبة في التعبير عن العواطف، وكماليتك قد تؤدي إلى التسويف. قد تبدو بعيدًا عن الآخرين بسبب تركيزك على الأفكار بدلاً من التفاعلات الاجتماعية. **العلاقات**: تفضل العلاقات العميقة والفكرية وتكون مخلصًا جدًا، لكنك تحتاج إلى مساحة شخصية. العلاقات العاطفية قد تكون تحديًا لأنك تعطي الأولوية للمنطق على المشاعر، مما قد يسبب سوء فهم. **المهن**: الأدوار المثالية تشمل مديرًا تنفيذيًا، عالمًا، مهندس برمجيات، محامي استراتيجي، أو أستاذ جامعي، حيث تتألق مهاراتك التحليلية والرؤيوية. **النمو الشخصي**: اعمل على الذكاء العاطفي، مارس الاستماع النشط، وتقبل المرونة لموازنة نهجك المنظم. **التفسير الكامل**: INTJ هم رؤيويون يرون العالم كلغز يجب حله أو نظام يجب تحسينه. يتفوقون في المجالات العلمية والتقنية والاستراتيجية، وغالبًا ما يقودون بأفكار جريئة. لكن ميلهم لتجنب التفاعلات الاجتماعية اليومية قد يجعلهم يبدون منعزلين. في العمل، هم قادة طبيعيون يقدرون الكفاءة، لكنهم قد يحتاجون إلى إلهام الفريق بدلاً من توجيهه فقط. في الحياة الشخصية، هم شركاء مخلصون لكنهم يحتاجون إلى شخص يحترم استقلالهم. إذا كنت INTJ، فإن موازنة العمل مع العلاقات الشخصية وتنمية التعاطف يمكن أن تجعل حياتك أكثر ثراءً. إحصائيًا، يشكل INTJ حوالي 2% من السكان، وغالبًا ما ينجحون في أدوار القيادة لكنهم قد يعانون من العزلة إذا أهملوا العلاقات. عقلهم الاستراتيجي يجعلهم روادًا في الابتكار."""
    },
    'INTP': {
        "en": """INTP (Thinker): You are an analytical and creative thinker. **Strengths**: Exceptional problem-solving, quick learning, independence, endless curiosity. You thrive on exploring abstract ideas and theories. **Weaknesses**: May neglect daily details, struggle with commitment, appear distant, avoid routine. **Relationships**: You seek intellectual partners and are honest, but may overlook emotional needs. **Careers**: Programmer, philosopher, researcher, engineer, technical writer. **Personal Growth**: Improve time management, strengthen emotional connections, focus on completing projects. **Full Interpretation**: INTPs love diving into abstract ideas and can spend hours theorizing. They excel in theoretical and scientific fields but may leave projects unfinished due to new ideas. In relationships, they are honest and loyal but need intellectual space. At work, they are innovators but may tire of rigid structures. If you're an INTP, learning social and practical skills can help turn your ideas into reality. INTPs are about 3% of the population, often thriving in tech and academia.""",
        "fa": """INTP (متفکر): شما یک تحلیل‌گر منطقی و خلاق هستید. **نقاط قوت**: حل مسئله خلاقانه، یادگیری سریع، استقلال، کنجکاوی بی‌پایان. شما از کاوش در ایده‌های انتزاعی و نظریه‌ها لذت می‌برید. **نقاط ضعف**: ممکن است جزئیات روزمره را نادیده بگیرید، در تعهد مشکل داشته باشید، دور به نظر برسید، از روتین اجتناب کنید. **روابط**: به دنبال شریک فکری هستید و صادقید، اما ممکن است نیازهای عاطفی را نادیده بگیرید. **شغل‌ها**: برنامه‌نویس، فیلسوف، محقق، مهندس، نویسنده فنی. **رشد شخصی**: بهبود مدیریت زمان، تقویت روابط عاطفی، تمرکز روی اتمام پروژه‌ها. **تفسیر کامل**: INTPها عاشق غواصی در ایده‌های انتزاعی هستند و می‌توانند ساعت‌ها به نظریه‌پردازی بپردازند. آنها در زمینه‌های نظری و علمی عالی هستند اما ممکن است پروژه‌ها را نیمه‌تمام بگذارند چون ایده جدیدی توجه‌شان را جلب می‌کند. در روابط، آنها صادق و وفادار هستند اما به فضای فکری نیاز دارند. در کار، آنها نوآوران هستند اما ممکن است از ساختارهای خشک خسته شوند. اگر INTP هستید، یادگیری مهارت‌های اجتماعی و عملی می‌تواند کمک کند ایده‌هایتان را به واقعیت تبدیل کنید. INTPها حدود 3% جمعیت هستند و اغلب در فناوری و آکادمی موفق‌اند.""",
        "ar": """INTP (المفكر): أنت مفكر تحليلي وخلاق. **نقاط القوة**: حل المشكلات بشكل إبداعي، التعلم السريع، الاستقلال، الفضول اللامتناهي. تستمتع باستكشاف الأفكار المجردة والنظريات. **نقاط الضعف**: قد تهمل التفاصيل اليومية، تواجه صعوبة في الالتزام، تبدو بعيدًا، تتجنب الروتين. **العلاقات**: تبحث عن شريك فكري وتكون صادقًا، لكن قد تهمل الاحتياجات العاطفية. **المهن**: مبرمج، فيلسوف، باحث، مهندس، كاتب تقني. **النمو الشخصي**: تحسين إدارة الوقت، تعزيز العلاقات العاطفية، التركيز على إكمال المشاريع. **التفسير الكامل**: يحب INTP الغوص في الأفكار المجردة ويمكنهم قضاء ساعات في التنظير. يتفوقون في المجالات النظرية والعلمية لكنهم قد يتركون المشاريع ناقصة بسبب أفكار جديدة. في العلاقات، هم صادقون ومخلصون لكنهم يحتاجون إلى مساحة فكرية. في العمل، هم مبتكرون لكنهم قد يملون من الهياكل الصلبة. إذا كنت INTP، فإن تعلم المهارات الاجتماعية والعملية يمكن أن يساعد في تحويل أفكارك إلى واقع. يشكل INTP حوالي 3% من السكان، وغالبًا ما يزدهرون في التكنولوجيا والأكاديميات."""
    },
    # برای کامل بودن، توضیحات 14 نوع شخصیت دیگر (مثل ENTJ, ENTP, INFJ, ...) رو با همین سطح از جزئیات و ترجمه‌ها اضافه کن.
    # مثال برای یکی دیگر:
    'ENFP': {
        "en": """ENFP (Campaigner): You are energetic, creative, and inspiring. **Strengths**: Ideation, empathy, flexibility, charisma. You bring enthusiasm to everything you do. **Weaknesses**: Lack of focus, difficulty making decisions, avoidance of routine, impulsiveness. **Relationships**: You love exciting and supportive connections but may struggle with commitment. **Careers**: Teacher, writer, marketer, actor. **Personal Growth**: Focus on completing projects, time management, and commitment. **Full Interpretation**: ENFPs are like butterflies—full of color and energy. They inspire others and generate big ideas but may scatter their focus. In relationships, they are fun and supportive but need freedom. At work, they thrive in creative environments but need structure. If you're an ENFP, adding structure can help you achieve your dreams. ENFPs are about 7% of the population, excelling in creative and social roles.""",
        "fa": """ENFP (قهرمان): شما پر انرژی، خلاق و الهام‌بخش هستید. **نقاط قوت**: ایده‌پردازی، همدلی، انعطاف‌پذیری، کاریزما. شما به هر کاری شور و شوق می‌آورید. **نقاط ضعف**: عدم تمرکز، مشکل در تصمیم‌گیری، اجتناب از روتین، تکانشگری. **روابط**: عاشق روابط هیجان‌انگیز و حمایت‌گر هستید اما ممکن است با تعهد مشکل داشته باشید. **شغل‌ها**: معلم، نویسنده، بازاریاب، بازیگر. **رشد شخصی**: تمرکز روی اتمام پروژه‌ها، مدیریت زمان، و تعهد. **تفسیر کامل**: ENFPها مانند پروانه‌ها هستند—پر از رنگ و انرژی. آنها دیگران را الهام می‌بخشند و ایده‌های بزرگ تولید می‌کنند اما ممکن است تمرکز خود را پراکنده کنند. در روابط، آنها سرگرم‌کننده و حمایت‌گر هستند اما به آزادی نیاز دارند. در کار، آنها در محیط‌های خلاق می‌درخشند اما به ساختار نیاز دارند. اگر ENFP هستید، افزودن ساختار می‌تواند به شما کمک کند رویاهایتان را محقق کنید. ENFPها حدود 7% جمعیت هستند و در نقش‌های خلاق و اجتماعی عالی‌اند.""",
        "ar": """ENFP (الحملة): أنت مليء بالطاقة، مبدع، وملهم. **نقاط القوة**: التفكير الإبداعي، التعاطف، المرونة، الكاريزما. تجلب الحماس لكل ما تفعله. **نقاط الضعف**: نقص التركيز، صعوبة في اتخاذ القرارات، تجنب الروتين، الاندفاع. **العلاقات**: تحب العلاقات المثيرة والداعمة لكن قد تواجه صعوبة في الالتزام. **المهن**: معلم، كاتب، مسوق، ممثل. **النمو الشخصي**: التركيز على إكمال المشاريع، إدارة الوقت، والالتزام. **التفسير الكامل**: ENFP هم مثل الفراشات—مليئون بالألوان والطاقة. يلهمون الآخرين ويولدون أفكارًا كبيرة لكنهم قد يشتتون تركيزهم. في العلاقات، هم ممتعون وداعمون لكنهم يحتاجون إلى الحرية. في العمل، يزدهرون في البيئات الإبداعية لكنهم يحتاجون إلى هيكلية. إذا كنت ENFP، فإن إضافة الهيكلية يمكن أن تساعدك على تحقيق أحلامك. يشكل ENFP حوالي 7% من السكان، ويتفوقون في الأدوار الإبداعية والاجتماعية."""
    },
}

# تابع برای محاسبه نوع شخصیت
def get_mbti_type(scores):
    ei = 'E' if scores['E'] > scores['I'] else 'I'
    sn = 'S' if scores['S'] > scores['N'] else 'N'
    tf = 'T' if scores['T'] > scores['F'] else 'F'
    jp = 'J' if scores['J'] > scores['P'] else 'P'
    return ei + sn + tf + jp

# تابع شروع - انتخاب زبان
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("English", callback_data="lang_en")],
        [InlineKeyboardButton("فارسی", callback_data="lang_fa")],
        [InlineKeyboardButton("عربي", callback_data="lang_ar")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please select your language: / لطفاً زبان خود را انتخاب کنید: / الرجاء اختيار لغتك:", reply_markup=reply_markup)

# تابع مدیریت انتخاب زبان و شروع تست
async def select_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split('_')[1]
    context.user_data["lang"] = lang
    context.user_data["current_question"] = 0
    context.user_data["scores"] = {'E': 0, 'I': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}
    await ask_question(update, context)

# تابع نمایش سؤال بر اساس
