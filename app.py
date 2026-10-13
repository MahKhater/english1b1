import random
from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'ser_el_tafouk_secret_key' # مفتاح الجلسة لتخزين الأسئلة والإجابات
def check_user_answer(user_answer, correct_answer):
    """
    دالة موحدة للتحقق من صحة الإجابة بغض النظر عن كونها True/False أو اختيار من متعدد
    تقوم بتوحيد الصيغة (Lower case وتنزع المسافات الزائدة) لتجنب أخطاء المطابقة.
    """
    # إذا كانت الإجابة أسئلة صواب وخطأ (True/False)
    if isinstance(correct_answer, bool) or str(correct_answer).lower() in ['true', 'false']:
        # توحيد إجابة المستخدم والإجابة الصحيحة إلى صيغة نصية بحروف صغيرة
        if isinstance(user_answer, bool):
            user_str = str(user_answer).lower()
        else:
            user_str = str(user_answer).strip().lower()
            
        correct_str = str(correct_answer).strip().lower()
        return user_str == correct_str

    # إذا كانت أسئلة اختيار من متعدد (MCQ)
    else:
        # مقارنة النص بعد إزالة المسافات الزائدة وتوحيد الحروف الكبيرة والصغيرة
        user_str = str(user_answer).strip().lower()
        correct_str = str(correct_answer).strip().lower()
        return user_str == correct_str
QUESTIONS_DB = {

    "مبتدئ": [
           {
             "id": 1,
        "type": "mcq",
        "prompt": "...........means protecting nature and natural resources.",
        "options": ["Loyalty", "Conservation", "Wisdom", "Connection"],
        "answer": "Conservation"
    },
    {
        "id": 2,
        "type": "mcq",
        "prompt": "He trained hard every day to ............ more goals for his team.",
        "options": ["score", "pass", "miss", "save"],
        "answer": "score"
    },
    {
        "id": 3,
        "type": "mcq",
        "prompt": "The opposite of 'courage' is ............ .",
        "options": ["kindness", "fear", "pride", "calmness"],
        "answer": "fear"
    },
    {
        "id": 4,
        "type": "mcq",
        "prompt": "The suffix '-ed' turns the verb 'interest' into a/an ............",
        "options": ["verb", "adjective", "adverb", "noun"],
        "answer": "adjective"
    },
    {
        "id": 5,
        "type": "mcq",
        "prompt": "The Arabic meaning of the word 'leader' is ............ .",
        "options": ["بطل", "قائد", "مدرب", "مشجع"],
        "answer": "قائد"
    },
    {
        "id": 6,
        "type": "mcq",
        "prompt": "The word 'empathy' means ............ .",
        "options": ["تعاطف", "حكمة", "شجاعة", "صبر"],
        "answer": "تعاطف"
    },
    {
        "id": 7,
        "type": "mcq",
        "prompt": "'Schedules' means ............ .",
        "options": ["عادات مجتمعية", "جداول مواعيد ثابتة", "ألعاب قوى", "كرم الضيافة"],
        "answer": "جداول مواعيد ثابتة"
    },
    {
        "id": 8,
        "type": "mcq",
        "prompt": "The Arabic meaning of the word 'trust' is ............ .",
        "options": ["يظن", "يثق / ثقة", "يكرم", "ينافس"],
        "answer": "يثق / ثقة"
    },
    {
        "id": 9,
        "type": "mcq",
        "prompt": "'Victory' means ............ .",
        "options": ["انتصار", "معركة", "خوف", "هزيمة"],
        "answer": "انتصار"
    },
    {
        "id": 10,
        "type": "mcq",
        "prompt": "Which word means 'رمي القرص'?",
        "options": ["fencing", "archery", "discus throwing", "athletics"],
        "answer": "discus throwing"
    },
    {
        "id": 11,
        "type": "mcq",
        "prompt": "'Sportsmanship' means ............ .",
        "options": ["قتال المصارعين", "الروح الرياضية", "ألعاب القوى", "كرم الضيافة"],
        "answer": "الروح الرياضية"
    },
    {
        "id": 12,
        "type": "mcq",
        "prompt": "'The elderly' refers to ............ .",
        "options": ["الشباب", "كبار السن", "الأطفال", "أجيال"],
        "answer": "كبار السن"
    },
    {
        "id": 13,
        "type": "mcq",
        "prompt": "'Wisdom' means ............ .",
        "options": ["صبر", "ثقافة", "حكمة", "عادات"],
        "answer": "حكمة"
    },
    {
        "id": 14,
        "type": "mcq",
        "prompt": "Letters added to the beginning of a word are called a ............ .",
        "options": ["suffix", "prefix", "noun", "verb"],
        "answer": "prefix"
    },
    {
        "id": 15,
        "type": "mcq",
        "prompt": "Letters added to the end of a word are called a ............ .",
        "options": ["prefix", "suffix", "sentence", "tense"],
        "answer": "suffix"
    },
    {
        "id": 16,
        "type": "mcq",
        "prompt": "The prefix 're-' means doing something ............ .",
        "options": ["wrongly", "again", "opposite", "without"],
        "answer": "again"
    },
    {
        "id": 17,
        "type": "mcq",
        "prompt": "The prefix 'mis-' means doing something ............ .",
        "options": ["again", "rightly", "wrongly", "never"],
        "answer": "wrongly"
    },
    {
        "id": 18,
        "type": "mcq",
        "prompt": "To make the opposite of 'happy', we add the prefix ............ .",
        "options": ["im-", "dis-", "un-", "re-"],
        "answer": "un-"
    },
    {
        "id": 19,
        "type": "mcq",
        "prompt": "The suffix '-less' means ............ .",
        "options": ["again", "without", "very", "full of"],
        "answer": "without"
    },
    {
        "id": 20,
        "type": "mcq",
        "prompt": "He ............ travelled to Sinai. (Present Perfect Active)",
        "options": ["have", "has", "had", "having"],
        "answer": "has"
    },
    {
        "id": 21,
        "type": "mcq",
        "prompt": "In the Present Perfect Passive, we use: Object + have/has + ............ + p.p.",
        "options": ["being", "been", "had", "did"],
        "answer": "been"
    },
    {
        "id": 22,
        "type": "mcq",
        "prompt": "Which of the following is a key word for the Present Perfect tense?",
        "options": ["yesterday", "tomorrow", "yet", "ago"],
        "answer": "yet"
    },
    {
        "id": 23,
        "type": "mcq",
        "prompt": "The form of the Past Perfect Tense is ............ + p.p.",
        "options": ["have", "has", "had", "was"],
        "answer": "had"
    },
    {
        "id": 24,
        "type": "mcq",
        "prompt": "After Hassan had done his homework, he ............ .",
        "options": ["sleep", "slept", "has slept", "had slept"],
        "answer": "slept"
    },
    {
        "id": 25,
        "type": "mcq",
        "prompt": "According to exam specifications, Question 1 asks students to choose ............ correct answers out of 5 options.",
        "options": ["one", "two", "three", "four"],
        "answer": "two"
    },
    {
        "id": 26,
        "type": "tf",
        "prompt": "The prefix changes the word type like converting a noun to an adjective.",
        "options": ["True", "False"],
        "answer": "False"
    },
    {
        "id": 27,
        "type": "tf",
        "prompt": "'Praise' means 'يكرم / يمدح' in Arabic.",
        "options": ["True", "False"],
        "answer": "True"
    },
    {
        "id": 28,
        "type": "tf",
        "prompt": "'Fencing' is the English word for 'المبارزة'.",
        "options": ["True", "False"],
        "answer": "True"
    },
    {
        "id": 29,
        "type": "tf",
        "prompt": "'Patience' means 'ثقافة' in Arabic.",
        "options": ["True", "False"],
        "answer": "False"
    },
    {
        "id": 30,
        "type": "tf",
        "prompt": "'Hospitality' means 'كرم الضيافة'.",
        "options": ["True", "False"],
        "answer": "True"
    },
    {
        "id": 31,
        "type": "tf",
        "prompt": "Prefixes are letters added after the word.",
        "options": ["True", "False"],
        "answer": "False"
    },
    {
        "id": 32,
        "type": "tf",
        "prompt": "Suffixes are letters added to the end of a word.",
        "options": ["True", "False"],
        "answer": "True"
    },
    {
        "id": 33,
        "type": "tf",
        "prompt": "The prefix 'un-' is used to give the opposite meaning.",
        "options": ["True", "False"],
        "answer": "True"
    },
    {
        "id": 34,
        "type": "tf",
        "prompt": "The prefix 're-' + 'write' becomes 'rewrite'.",
        "options": ["True", "False"],
        "answer": "True"
    },
    {
        "id": 35,
        "type": "tf",
        "prompt": "The suffix '-ly' turns a word into a noun.",
        "options": ["True", "False"],
        "answer": "False"
    },
    {
        "id": 36,
        "type": "tf",
        "prompt": "The opposite of 'possible' is 'impossible'.",
        "options": ["True", "False"],
        "answer": "True"
    },
    {
        "id": 37,
        "type": "tf",
        "prompt": "With 'I, We, You, They' we use 'has' in the Present Perfect tense.",
        "options": ["True", "False"],
        "answer": "False"
    },
    {
        "id": 38,
        "type": "tf",
        "prompt": "With 'He, She, It' we use 'has' in the Present Perfect tense.",
        "options": ["True", "False"],
        "answer": "True"
    },
    {
        "id": 39,
        "type": "tf",
        "prompt": "'Just' and 'already' are key words for the Present Perfect tense.",
        "options": ["True", "False"],
        "answer": "True"
    },
    {
        "id": 40,
        "type": "tf",
        "prompt": "The past perfect tense formulation is 'has + p.p.'.",
        "options": ["True", "False"],
        "answer": "False"
    },
    {
        "id": 41,
        "type": "tf",
        "prompt": "'As soon as' is followed by the past perfect tense, then the past simple tense.",
        "options": ["True", "False"],
        "answer": "True"
    },
    {
        "id": 42,
        "type": "tf",
        "prompt": "'Before' is followed by the past perfect tense directly.",
        "options": ["True", "False"],
        "answer": "False"
    },
    {
        "id": 43,
        "type": "tf",
        "prompt": "'By the time' is followed by the past simple, then past perfect.",
        "options": ["True", "False"],
        "answer": "True"
    },
    {
        "id": 44,
        "type": "tf",
        "prompt": "The word 'stunning' has a close meaning to 'breathtaking'.",
        "options": ["True", "False"],
        "answer": "True"
    },
    {
        "id": 45,
        "type": "tf",
        "prompt": "The opposite of the word 'rude' is 'polite'.",
        "options": ["True", "False"],
        "answer": "True"
    },
    {
        "id": 46,
        "type": "tf",
        "prompt": "Question 2 in the exam specifications contains 12 multiple choice questions.",
        "options": ["True", "False"],
        "answer": "True"
    },
    {
        "id": 47,
        "type": "tf",
        "prompt": "The reading comprehension passage in the exam consists of 500 words.",
        "options": ["True", "False"],
        "answer": "False"
    },
    {
        "id": 48,
        "type": "tf",
        "prompt": "The comprehension passage has 7 multiple-choice questions.",
        "options": ["True", "False"],
        "answer": "True"
    },
    {
        "id": 49,
        "type": "tf",
"prompt": "Question 4 in the exam specifications is about translation between Arabic and English.",
"options": ["True", "False"],
"answer": "True"
},
{
"id": 50,
"type": "tf",
"prompt": "Question 5 asks students to answer two open-ended critical thinking questions.",
"options": ["True", "False"],
"answer": "True"

       }
    ],
      
    "متوسط": [
              {
"id": 51,
        "type": "mcq",
        "prompt": "According to page 1, if a student gets 1-2 marks in level 1, they should move to: ............ .",
        "options": ["Level 2", "Grade 10", "Learn & Return Round 1", "Learn & Return Round 2"],
        "answer": "Learn & Return Round 1"
    },
    {
        "id": 52,
        "type": "mcq",
        "prompt": "Based on page 1, what is the correct sentence after rewriting using 'After'?",
        "options": ["After he packed his bag, he went to the station.", "After he went to the station, he packed his bag.", "After he had packed his bag, he went to the station.", "After he packed his bag, he had gone to the station."],
        "answer": "After he packed his bag, he went to the station."
    },
    {
        "id": 53,
        "type": "mcq",
        "prompt": "According to the vocabulary list on page 2, the word 'motivated' translates to: ............ .",
        "options": ["متحد", "متحمس / متحفز", "تعاطف", "انتصار"],
        "answer": "متحمس / متحفز"
    },
    {
        "id": 54,
        "type": "mcq",
        "prompt": "The English word for 'قتال المصارعين' in the sports list is: ............ .",
        "options": ["fencing", "athletics", "battle", "gladiator fights"],
        "answer": "gladiator fights"
    },
    {
        "id": 55,
        "type": "mcq",
        "prompt": "Under the 'Culture and traditions' section, the word for 'أجيال' is: ............ .",
        "options": ["generations", "traditions", "customs", "the elderly"],
        "answer": "generations"
    },
    {
        "id": 56,
        "type": "mcq",
        "prompt": "Based on page 2, the exact definition of a suffix is: letters added ............ .",
        "options": ["before the word", "to the end of a word", "to change meaning only", "to the beginning of a word"],
        "answer": "to the end of a word"
    },
    {
        "id": 57,
        "type": "mcq",
        "prompt": "According to the prefix list on page 3, which of the following prefixes does NOT mean '(opposite)'?",
        "options": ["non-", "mis-", "dis-", "il-"],
        "answer": "mis-"
    },
    {
        "id": 58,
        "type": "mcq",
        "prompt": "To turn a word into a person (Noun / Person), page 3 states we should use the suffix: ............ .",
        "options": ["-ment", "-ist", "-ness", "-ation"],
        "answer": "-ist"
    },
    {
        "id": 59,
        "type": "mcq",
        "prompt": "The suffixes '-ance, -ence, -ation, -ion' are used to convert a word into a/an: ............ .",
        "options": ["Adjective", "Adverb", "Noun", "Person"],
        "answer": "Noun"
    },
    {
        "id": 60,
        "type": "mcq",
        "prompt": "According to the suffix list, which suffixes change a word into an Adjective meaning 'without'?",
        "options": ["-able / -ible", "-ful / -ive", "-less", "-ous / -ious"],
        "answer": "-less"
    },
    {
        "id": 61,
        "type": "mcq",
        "prompt": "Based on the examples on page 3, 'act + -tion' gives the word: ............ .",
        "options": ["active", "action", "activity", "actor"],
        "answer": "action"
    },
    {
        "id": 62,
        "type": "mcq",
        "prompt": "What change occurs when a suffix is added, according to the function rule on page 3?",
        "options": ["Changes meaning only", "Changes the spelling of the root only", "Changes meaning and the word type", "Does not change anything"],
        "answer": "Changes meaning and the word type"
    },
    {
        "id": 63,
        "type": "mcq",
        "prompt": "In the sentence 'Tourists have visited the Pyramids', the passive form must start with: ............ .",
        "options": ["Tourists", "Have visited", "The Pyramids", "Been visited"],
        "answer": "The Pyramids"
    },
    {
        "id": 64,
        "type": "mcq",
        "prompt": "Based on page 4, the correct structure after 'As soon as' is: As soon as + ............ , past simple.",
        "options": ["past perfect (had + p.p.)", "past simple", "present perfect", "present simple"],
        "answer": "past perfect (had + p.p.)"
    },
    {
        "id": 65,
        "type": "mcq",
        "prompt": "Complete the rule from page 4: Before / By the time / When + past simple, ............ .",
        "options": ["present perfect", "past simple", "past perfect (had + p.p.)", "have/has + been + p.p."],
        "answer": "past perfect (had + p.p.)"
    },
    {
        "id": 66,
        "type": "mcq",
        "prompt": "According to the example on page 4, what did Heba do BEFORE she watched TV?",
        "options": ["She slept", "She washed the dishes", "She finished her work", "She visited the museum"],
        "answer": "She washed the dishes"
    },
    {
        "id": 67,
        "type": "mcq",
        "prompt": "According to the specifications for First Year Secondary 2026-2027, MRQ questions must deal with: ............ .",
        "options": ["grammar only", "structures and writing skills", "synonyms and antonyms ONLY", "critical thinking"],
        "answer": "synonyms and antonyms ONLY"
    },
    {
        "id": 68,
        "type": "mcq",
        "prompt": "Based on page 5, the word 'stunning' has a close meaning to 'breathtaking' and: ............ .",
        "options": ["worthless", "impressive", "beneficial", "aggressive"],
        "answer": "impressive"
    },
    {
        "id": 69,
        "type": "mcq",
        "prompt": "Based on page 5, the two correct opposites of the word 'rude' are: ............ .",
        "options": ["impolite, improper", "polite, respectful", "polite, violent", "respectful, violent"],
        "answer": "polite, respectful"
    },
    {
        "id": 70,
        "type": "mcq",
        "prompt": "Question 2 in the exam paper consists of 12 MCQs. How many are allocated for 'writing skills'?",
        "options": ["6 questions", "4 questions", "2 questions", "7 questions"],
        "answer": "2 questions"
    },
    {
        "id": 71,
        "type": "mcq",
        "prompt": "According to the specs, writing skills questions should be related to what students studied in the set book, such as: ............ .",
        "options": ["synonyms and antonyms", "translation options", "essay structure, outline, thesis statement, CV", "skimming and scanning"],
        "answer": "essay structure, outline, thesis statement, CV"
    },
    {
        "id": 72,
        "type": "mcq",
        "prompt": "The unseen text provided in Question 3 can be a: ............ .",
        "options": ["poem or song", "story, a factual text, a letter, or an e-mail", "grammar summary", "translation block"],
        "answer": "story, a factual text, a letter, or an e-mail"
    },
    {
        "id": 73,
        "type": "mcq",
        "prompt": "Which of the following is NOT listed as a reading comprehension skill tested in Question 3?",
        "options": ["giving the main idea", "making prediction", "summarizing", "translating sentences"],
        "answer": "translating sentences"
    },
    {
        "id": 74,
        "type": "mcq",
        "prompt": "According to page 7, the short English text in Question 4A consists of: ............ .",
        "options": ["one long sentence of 50 words", "TWO meaningful sentences of about 10-12 words each", "three sentences of 20 words each", "a full story of 200 words"],
        "answer": "TWO meaningful sentences of about 10-12 words each"
    },
    {
        "id": 75,
        "type": "mcq",
        "prompt": "In Question 5, students are asked to answer two open-ended critical thinking questions. Their responses must be provided with: ............ .",
        "options": ["reasonable justifications", "Arabic translation only", "one word answers", "synonyms and antonyms"],
        "answer": "reasonable justifications"
    },
    {
        "id": 76,
        "type": "tf",
        "prompt": "According to page 1, a student who scores 3-4 marks in level 2 is ready to move to Grade 10.",
        "options": ["True", "False"],
        "answer": "True"
    },
    {
        "id": 77,
        "type": "tf",
        "prompt": "The Arabic translation for 'civilization' in the vocabulary list is 'جداول مواعيد ثابتة'.",
        "options": ["True", "False"],
        "answer": "False"
    },
    {
        "id": 78,
        "type": "tf",
        "prompt": "The word 'admiration' is categorized under 'Sports and competitions' on page 2.",
        "options": ["True", "False"],
        "answer": "True"
    },
    {
        "id": 79,
        "type": "tf",
        "prompt": "'Archery' means 'الرماية (رياضة القوس والسهم)' according to the sports list.",
        "options": ["True", "False"],
        "answer": "True"
    },
    {
        "id": 80,
        "type": "tf",
        "prompt": "The word 'customs' under Culture and traditions translates to 'عادات مجتمعية'.",
        "options": ["True", "False"],
        "answer": "True"
    },
    {
        "id": 81,
        "type": "tf",
        "prompt": "According to page 2, a prefix is added after the word.",
        "options": ["True", "False"],
        "answer": "False"
    },
    {
        "id": 82,
        "type": "tf",
        "prompt": "The prefix 'mis-' is used to express doing something again.",
        "options": ["True", "False"],
        "answer": "False"
    },
    {
        "id": 83,
        "type": "tf",
        "prompt": "The suffixes '-ful, -ive, -ous, -ious, -al, -able, -ible, -ant, -ic, -y' turn a word into an Adjective.",
        "options": ["True", "False"],
        "answer": "True"
    },
    {
        "id": 84,
        "type": "tf",
        "prompt": "The suffixes '-er, -or, -ist, -ian, -ee' turn a word into a Person (Noun).",
        "options": ["True", "False"],
        "answer": "True"
    },
    {
        "id": 85,
        "type": "tf",
        "prompt": "According to page 3, adding '-ly' or '-ily' transforms a word into an Adverb.",
"options": ["True", "False"],
"answer": "True"
},
{
"id": 86,
"type": "tf",
"prompt": "The example 'im- + possible -> impossible' demonstrates the use of a suffix.",
"options": ["True", "False"],
"answer": "False"
},
{
"id": 87,
"type": "tf",
"prompt": "The phrase 'A Small addition to a word can make a big change in meaning or form' is an official rule on page 3.",
"options": ["True", "False"],
"answer": "True"
},
{
"id": 88,
"type": "tf",
"prompt": "The singular noun or pronouns 'He, She, It' take 'have' in the active Present Perfect formation.",
"options": ["True", "False"],
"answer": "False"
},
{
"id": 89,
"type": "tf",
"prompt": "According to the passive example on page 4, 'The Pyramids have been visited by tourists' is correct.",
"options": ["True", "False"],
"answer": "True"
},
{
"id": 90,
"type": "tf",
"prompt": "The past perfect tense example given is: 'Ayman had finished his work before sleeping.'",
"options": ["True", "False"],
"answer": "True"
},
{
"id": 91,
"type": "tf",
"prompt": "In the exam specifications, Question 1 MRQ options are awarded half a mark for each correct option chosen.",
"options": ["True", "False"],
"answer": "True"
},
{
"id": 92,
"type": "tf",
"prompt": "Out of the 12 multiple choice questions in Question 2, 6 questions are based on structures.",
"options": ["True", "False"],
"answer": "False"
},
{
"id": 93,
"type": "tf",
"prompt": "According to page 6, Question 3 tests skills like skimming, scanning, and evaluating characters.",
"options": ["True", "False"],
"answer": "True"
},
{
"id": 94,
"type": "tf",
"prompt": "Each of the 7 multiple-choice questions in the reading comprehension section is worth two marks.",
"options": ["True", "False"],
"answer": "False"
},
{
"id": 95,
"type": "tf",
"prompt": "Question 4B requires choosing the correct English translation from a, b, c or d for a short Arabic text.",
"options": ["True", "False"],
"answer": "True"
},
{
"id": 96,
"type": "tf",
"prompt": "Question 5 critical thinking questions are allocated half a mark each.",
"options": ["True", "False"],
"answer": "True"
},
{
"id": 97,
"type": "tf",
"prompt": "The prefix 'dis-' added to 'agree' gives 'disagree', which means doing something again.",
"options": ["True", "False"],
"answer": "False"
},
{
"id": 98,
"type": "tf",
"prompt": "According to page 4, 'since' and 'for' are key words often used with the Present Perfect Tense.",
"options": ["True", "False"],
"answer": "True"
},
{
"id": 99,
"type": "tf",
"prompt": "The text states that 'When' follows the same past simple / past perfect sequence rule as 'Before' and 'By the time'.",
"options": ["True", "False"],
"answer": "True"
},
{
"id": 100,
"type": "tf",
"prompt": "In the exam specifications, the unseen reading text must be exactly 50 words long.",
"options": ["True", "False"],
"answer": "False"

          }
    ],
       "محترف": [
  { 

"id": 101,
        "type": "mcq",
        "prompt": "According to page 1, if a student scores 1-2 marks in Level 2, they must move to: ............ .",
        "options": ["Grade 10", "Level 2 second chance", "Learn & Return Round 2", "Pre-Assessment Level 1"],
        "answer": "Learn & Return Round 2"
    },
    {
        "id": 102,
        "type": "mcq",
        "prompt": "Based on page 1, what is the correct transformation of 'He said to me, \"Do you like fish?\"' using 'asked'?",
        "options": ["He asked me if I liked fish.", "He asked to me do you like fish.", "He said asked me do you like fish.", "He asked me if he liked fish."],
        "answer": "He asked me if I liked fish."
    },
    {
        "id": 103,
        "type": "mcq",
        "prompt": "Based on page 1, rewrite 'It was his habit to arrive late' using 'used'.",
        "options": ["He used to arriving late.", "He used to arrive late.", "He was used to arrive late.", "He used arrive late."],
        "answer": "He used to arrive late."
    },
    {
        "id": 104,
        "type": "mcq",
        "prompt": "Combine using 'who': 'Ali is my friend. He helped me a lot.' (Page 1)",
        "options": ["Ali is my friend who he helped me a lot.", "Ali, who is my friend, helped me a lot.", "Ali is my friend who helped me a lot.", "Ali who helped me a lot is my friend."],
        "answer": "Ali is my friend who helped me a lot."
    },
    {
        "id": 105,
        "type": "mcq",
        "prompt": "In the vocabulary table on page 2, which word is defined as 'الوحدة / التماسك'?",
        "options": ["united", "unity", "culture", "gather"],
        "answer": "unity"
    },
    {
        "id": 106,
        "type": "mcq",
        "prompt": "Which English word on page 2 matches the Arabic translation 'يمثل'?",
        "options": ["represent", "praise", "compete", "honor"],
        "answer": "represent"
    },
    {
        "id": 107,
        "type": "mcq",
        "prompt": "Under 'Sports and competitions' on page 2, the word 'spirit' translates to: ............ .",
        "options": ["الروح الرياضية", "الروح", "معركة", "إعجاب"],
        "answer": "الروح"
    },
    {
        "id": 108,
        "type": "mcq",
        "prompt": "According to page 3, what is the function of prefixes like 'un-, in-, im-, il-, ir-, dis-, non-'?",
        "options": ["To mean (again)", "To mean (wrongly)", "To give the (opposite) meaning", "To convert words into nouns"],
        "answer": "To give the (opposite) meaning"
    },
    {
        "id": 109,
        "type": "mcq",
        "prompt": "According to the suffix list on page 3, which suffix converts a word into a Noun?",
        "options": ["-age", "-ive", "-able", "-ly"],
        "answer": "-age"
    },
    {
        "id": 110,
        "type": "mcq",
        "prompt": "According to page 3, the suffixes '-or' and '-ee' change a word type into a: ............ .",
        "options": ["Adjective", "Adverb", "Noun (Person)", "Verb"],
        "answer": "Noun (Person)"
    },
    {
        "id": 111,
        "type": "mcq",
        "prompt": "Based on page 3 examples, 'quick + -ly' turns into 'quickly', which represents a/an: ............ .",
        "options": ["Noun", "Adjective", "Adverb", "Verb"],
        "answer": "Adverb"
    },
    {
        "id": 112,
        "type": "mcq",
        "prompt": "According to page 4, the active formation for Present Perfect Tense requires 'have' with plural nouns and: ............ .",
        "options": ["He, She, It", "I, We, You, They", "Object", "Singular nouns"],
        "answer": "I, We, You, They"
    },
    {
        "id": 113,
        "type": "mcq",
        "prompt": "In the passive example 'The Pyramids have been visited by tourists', what is the function of 'The Pyramids'?",
        "options": ["Subject", "Object", "Verb", "Key word"],
        "answer": "Object"
    },
    {
        "id": 114,
        "type": "mcq",
        "prompt": "According to page 4, the past perfect tense is formed using: ............ .",
        "options": ["have + p.p.", "has + p.p.", "had + p.p.", "had + been + p.p."],
        "answer": "had + p.p."
    },
    {
        "id": 115,
        "type": "mcq",
        "prompt": "Complete the example from page 4: 'Before Heba watched TV, she ............ the dishes.'",
        "options": ["was washing", "had washed", "has washed", "washed"],
        "answer": "had washed"
    },
    {
        "id": 116,
        "type": "mcq",
        "prompt": "According to the specifications on page 5, how many multiple response questions (MRQs) are provided in Question 1?",
        "options": ["One question", "Two questions", "Five questions", "Twelve questions"],
        "answer": "Two questions"
    },
    {
        "id": 117,
        "type": "mcq",
        "prompt": "According to page 5, the total marks allocated for Question 1 (MRQ section) is: ............ .",
        "options": ["1 Mark", "2 Marks", "4 Marks", "12 Marks"],
        "answer": "2 Marks"
    },
    {
        "id": 118,
        "type": "mcq",
        "prompt": "According to Question 2 specifications on page 6, how many multiple-choice questions test vocabulary?",
        "options": ["4 questions", "6 questions", "2 questions", "12 questions"],
        "answer": "6 questions"
    },
    {
        "id": 119,
        "type": "mcq",
        "prompt": "Based on page 6, Question 2 multiple-choice layout consists of how many options for each question?",
        "options": ["Three options", "Four options", "Five options", "Two options"],
        "answer": "Four options"
    },
    {
        "id": 120,
        "type": "mcq",
        "prompt": "According to page 6, writing skills questions in Question 2 test structures like: ............ .",
        "options": ["synonyms and antonyms", "descriptive essay, thesis statement, formal/informal email", "skimming and scanning", "Arabic translations"],
        "answer": "descriptive essay, thesis statement, formal/informal email"
    },
    {
        "id": 121,
        "type": "mcq",
        "prompt": "What is the total marks value for Question 2 according to page 6 specs?",
        "options": ["2 marks", "7 marks", "12 marks", "14 marks"],
        "answer": "12 marks"
    },
    {
        "id": 122,
        "type": "mcq",
        "prompt": "According to page 6, the length of the unseen text for Question 3 must be between: ............ .",
        "options": ["100 to 120 words", "150 to 180 words", "200 to 220 words", "250 to 300 words"],
        "answer": "200 to 220 words"
    },
    {
        "id": 123,
        "type": "mcq",
        "prompt": "According to page 7, Question 4A tests choosing the correct Arabic translation for an English text consisting of: ............ .",
        "options": ["A short text of 4 sentences", "A short text of TWO meaningful sentences", "One phrase of 5 words", "A long passage of 200 words"],
        "answer": "A short text of TWO meaningful sentences"
    },
    {
        "id": 124,
        "type": "mcq",
        "prompt": "According to page 7, what is the mark value for Question 4A and 4B individually?",
        "options": ["1 Mark each", "2 Marks each", "0.5 Mark each", "7 Marks each"],
        "answer": "2 Marks each"
    },
    {
        "id": 125,
        "type": "mcq",
        "prompt": "According to page 7, how many critical thinking questions are given in Question 5?",
        "options": ["One open-ended question", "Two open-ended questions", "Three open-ended questions", "Four open-ended questions"],
        "answer": "Two open-ended questions"
    },
    {
        "id": 126,
        "type": "tf",
        "prompt": "According to page 1, getting 3-4 marks in Level 1 allows the student to move directly to Grade 10.",
        "options": ["True", "False"],
        "answer": "False"
    },
    {
        "id": 127,
        "type": "tf",
        "prompt": "The word 'praise' under Leadership and personal qualities on page 2 translates to 'يكرم / يمدح'.",
        "options": ["True", "False"],
        "answer": "True"
    },
    {
        "id": 128,
        "type": "tf",
        "prompt": "The word 'conservation' is categorized under 'Culture and traditions' on page 2.",
        "options": ["True", "False"],
        "answer": "False"
    },
    {
        "id": 129,
        "type": "tf",
        "prompt": "The Arabic meaning of 'hospitality' is 'كرم الضيافة' according to the page 2 list.",
        "options": ["True", "False"],
        "answer": "True"
    },
    {
        "id": 130,
        "type": "tf",
        "prompt": "According to page 2, a prefix is defined as letters added to the end of a word.",
        "options": ["True", "False"],
        "answer": "False"
    },
    {
        "id": 131,
        "type": "tf",
        "prompt": "According to page 3, a prefix changes both the meaning and the word type.",
        "options": ["True", "False"],
        "answer": "False"
    },
    {
        "id": 132,
        "type": "tf",
        "prompt": "The prefix 'mis-' carries the functional meaning of doing something '(wrongly)'.",
        "options": ["True", "False"],
        "answer": "True"
    },
    {
        "id": 133,
        "type": "tf",
        "prompt": "The suffixes '-ness' and '-ity' are listed on page 3 as noun-forming suffixes.",
        "options": ["True", "False"],
        "answer": "True"
    },
    {
        "id": 134,
        "type": "tf",
        "prompt": "The suffixes '-ist' and '-ian' convert words into adjectives on page 3.",
        "options": ["True", "False"],
        "answer": "False"
    },
    {
        "id": 135,
        "type": "tf",
        "prompt": "According to page 3 examples, 'dis- + agree -> disagree' is an example of an opposite prefix.",
        "options": ["True", "False"],
        "answer": "True"
    },
    {
        "id": 136,
        "type": "tf",
"prompt": "According to page 4, the active example provided for Present Perfect is 'He has travelled to Sinai.'",
"options": ["True", "False"],
"answer": "True"
},
{
"id": 137,
"type": "tf",
"prompt": "The passive structure for Present Perfect on page 4 is: Object + have/has + being + p.p.",
"options": ["True", "False"],
"answer": "False"
},
{
"id": 138,
"type": "tf",
"prompt": "'Just', 'never', 'already', and 'ever' are listed as key words for Present Perfect Tense on page 4.",
"options": ["True", "False"],
"answer": "True"
},
{
"id": 139,
"type": "tf",
"prompt": "According to page 4, 'Ayman had finished his work before sleeping' is an example of the past perfect tense.",
"options": ["True", "False"],
"answer": "True"
},
{
"id": 140,
"type": "tf",
"prompt": "According to page 4 diagrams, 'After' and 'As soon as' are followed immediately by the past simple tense.",
"options": ["True", "False"],
"answer": "False"
},
{
"id": 141,
"type": "tf",
"prompt": "The rule on page 4 states: 'Before' and 'By the time' are followed by the past simple tense, then past perfect.",
"options": ["True", "False"],
"answer": "True"
},
{
"id": 142,
"type": "tf",
"prompt": "According to page 5, Question 1 choices are worth half a mark for each correct option selected.",
"options": ["True", "False"],
"answer": "True"
},
{
"id": 143,
"type": "tf",
"prompt": "On page 5, the word 'stunning' is paired with 'worthless' as a close synonym.",
"options": ["True", "False"],
"answer": "False"
},
{
"id": 144,
"type": "tf",
"prompt": "According to page 6, Question 2 has exactly 4 multiple-choice questions allocated for structures (grammar).",
"options": ["True", "False"],
"answer": "True"
},
{
"id": 145,
"type": "tf",
"prompt": "Question 3 reading comprehension skills include inferring the meaning of specialized vocabulary from context.",
"options": ["True", "False"],
"answer": "True"
},
{
"id": 146,
"type": "tf",
"prompt": "According to page 6, the unseen text format can be a story, a factual text, a letter, or an e-mail.",
"options": ["True", "False"],
"answer": "True"
},
{
"id": 147,
"type": "tf",
"prompt": "Question 4A requires translating a short Arabic text into English.",
"options": ["True", "False"],
"answer": "False"
},
{
"id": 148,
"type": "tf",
"prompt": "According to page 7, the short text for translation consists of about 10-12 words per sentence.",
"options": ["True", "False"],
"answer": "True"
},
{
"id": 149,
"type": "tf",
"prompt": "Question 5 critical thinking questions award a total of one mark (half a mark each) if answered with justifications.",
"options": ["True", "False"],
"answer": "True"
},
{
"id": 150,
"type": "tf",
"prompt": "The prefix 'im-' added to 'possible' creates 'impossible', changing its word type from adjective to noun.",
"options": ["True", "False"],
"answer": "False"

   }
  ]
}
@app.route('/', methods=['GET', 'POST'])
def index():
    level = request.form.get('level', 'متوسط')
    num_questions = int(request.form.get('num_questions', 5))
    action = request.form.get('action', 'select')
   
    pool = QUESTIONS_DB.get(level, QUESTIONS_DB.get("متوسط", []))
   
    if request.method == 'GET' or action == 'select':
        return render_template_string(MAIN_TEMPLATE, level=level, num_questions=num_questions)
       
    elif action == 'generate':
        selected_questions = random.sample(pool, min(num_questions, len(pool))) if pool else []
        session['questions'] = selected_questions
        session['level'] = level
        session['current_index'] = 0
        session['user_answers'] = {}
        return redirect(url_for('quiz_step'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz_step():
    questions = session.get('questions', [])
    current_index = session.get('current_index', 0)
    level = session.get('level', 'متوسط')
   
    if not questions:
        return redirect(url_for('index'))
       
    if request.method == 'POST':
        ans = request.form.get('current_answer')
        
        user_answers = session.get('user_answers', {})
        user_answers[str(current_index)] = {
            "prompt": questions[current_index]['prompt'],
            "user_ans": ans if ans else "لم تتم الإجابة",
            "correct_ans": questions[current_index]['answer'],
            "is_correct": check_user_answer(ans, questions[current_index]['answer'])
        }
        session['user_answers'] = user_answers
       
        current_index += 1
        session['current_index'] = current_index
       
    if current_index >= len(questions):
        return redirect(url_for('results'))
       
    current_question = questions[current_index]
   
    return render_template_string(
        QUIZ_TEMPLATE,
        level=level,
        question=current_question,
        current_num=current_index + 1,
        total_questions=len(questions),
        num_questions=len(questions)
    )

@app.route('/results')
def results():
    user_answers = session.get('user_answers', {})
    level = session.get('level', 'متوسط')
   
    score = 0
    total = len(user_answers)
    results_list = []
   
    for idx, data in sorted(user_answers.items(), key=lambda x: int(x[0])):
        if data['is_correct']:
            score += 1
        results_list.append({
            "id": int(idx) + 1,
            "prompt": data['prompt'],
            "user_ans": data['user_ans'],
            "correct_ans": data['correct_ans'],
            "is_correct": data['is_correct']
        })
       
    return render_template_string(
        RESULT_TEMPLATE,
        level=level,
        score=score,
        total=total,
        results=results_list
    )

MAIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة سر التفوق - تصميم الامتحان</title>
    <style>
        body { font-family: 'Tahoma', sans-serif; background-color: #114b3e; color: #333; margin: 0; padding: 20px; direction: rtl; text-align: right; }
        .main-card { max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
        .header-badge { text-align: center; color: #d4a373; font-size: 14px; font-weight: bold; margin-bottom: 5px; }
        h2 { text-align: center; color: #114b3e; margin-top: 0; font-size: 26px; }
        .subtitle { text-align: center; color: #666; font-size: 14px; margin-bottom: 25px; }
        .section-title { font-weight: bold; color: #222; font-size: 15px; margin-bottom: 10px; }
        .levels-container { display: flex; gap: 10px; margin-bottom: 20px; }
        .level-btn { flex: 1; padding: 12px; border: 2px solid #e0e0e0; border-radius: 12px; background: #fff; cursor: pointer; text-align: center; font-weight: bold; font-size: 14px; transition: 0.3s; }
        .level-btn input { display: none; }
        .level-btn.active, .level-btn:hover { border-color: #114b3e; background: #e8f5e9; color: #114b3e; }
        .slider-container { margin-bottom: 25px; background: #f9f9f9; padding: 15px; border-radius: 12px; border: 1px solid #eee; }
        .slider-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; font-weight: bold; color: #114b3e; }
        input[type=range] { width: 100%; accent-color: #114b3e; cursor: pointer; }
        .start-btn { display: block; width: 100%; background: #114b3e; color: white; padding: 14px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 16px; border: none; cursor: pointer; box-shadow: 0 4px 10px rgba(17,75,62,0.3); transition: 0.3s; text-decoration: none; box-sizing: border-box; }
        .start-btn:hover { background: #0d382f; }
        .whatsapp-link-btn { display: block; width: 100%; background: #25d366; color: white; padding: 13px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 15px; text-decoration: none; box-shadow: 0 4px 10px rgba(37,211,102,0.3); transition: 0.3s; margin-top: 15px; box-sizing: border-box; }
        .whatsapp-link-btn:hover { background: #1ebe57; }
    </style>
</head>
<body>
    <div class="main-card">
        <div class="header-badge">منصة سر التفوق التعليمية ✨</div>
        <h2>صمّم امتحانك</h2>
        <div class="subtitle">اختبر معلوماتك الآن بكل سهولة ⏱️</div>
       
        <form method="POST">
            <input type="hidden" name="action" value="generate">
            <div class="section-title">اختيار مستوى الصعوبة الدرس الاول اللغة الإنجليزية اولى بكالوريا الترم الاول</div>
            <div class="levels-container">
                <label class="level-btn {% if level == 'مبتدئ' %}active{% endif %}">
                    <input type="radio" name="level" value="مبتدئ" {% if level == 'مبتدئ' %}checked{% endif %} onchange="updateActive(this)"> مبتدئ
                </label>
                <label class="level-btn {% if level == 'متوسط' %}active{% endif %}">
                    <input type="radio" name="level" value="متوسط" {% if level == 'متوسط' %}checked{% endif %} onchange="updateActive(this)"> متوسط
                </label>
                <label class="level-btn {% if level == 'محترف' %}active{% endif %}">
                    <input type="radio" name="level" value="محترف" {% if level == 'محترف' %}checked{% endif %} onchange="updateActive(this)"> محترف ⏱️
                </label>
            </div>
           
            <div class="slider-container">
                <div class="slider-header">
                    <span>عدد الأسئلة بالاختبار</span>
                    <span id="range-val" style="background: #114b3e; color: white; padding: 2px 10px; border-radius: 20px; font-size: 13px;">{{ num_questions }} أسئلة</span>
                </div>
                <input type="range" name="num_questions" min="5" max="15" value="{{ num_questions }}" oninput="document.getElementById('range-val').innerText = this.value + ' أسئلة'">
            </div>
           
            <button type="submit" class="start-btn">ابدأ مع سر التفوق 🚀</button>
        </form>
       
        <a href="https://wa.me/201221581154?s=t" class="whatsapp-link-btn" target="_blank">💬 للاشتراك اضغط هنا</a>
    </div>
    <script>
        function updateActive(radio) {
            document.querySelectorAll('.level-btn').forEach(b => b.classList.remove('active'));
            radio.closest('.level-btn').classList.add('active');
        }
    </script>
</body>
</html>
"""

QUIZ_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة سر التفوق - حل الاختبار</title>
    <style>
        body { font-family: 'Tahoma', sans-serif; background-color: #114b3e; color: #333; margin: 0; padding: 20px; direction: rtl; text-align: right; }
        .main-card { max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
        h2 { text-align: center; color: #114b3e; margin-top: 0; font-size: 26px; }
        .question-box { background: #fdfdfd; border: 1px solid #ddd; padding: 15px; margin-bottom: 20px; border-radius: 10px; border-right: 5px solid #114b3e; }
        .options-list { margin-top: 10px; display: flex; flex-direction: column; gap: 8px; }
        .option-item { background: #f9f9f9; border: 1px solid #e0e0e0; padding: 10px 12px; border-radius: 8px; cursor: pointer; font-size: 14px; }
        .option-item:hover { background: #e8f5e9; border-color: #114b3e; }
        .option-item input { margin-left: 10px; }
        .badge-type { display: inline-block; background: #e8f5e9; color: #114b3e; padding: 2px 8px; border-radius: 6px; font-size: 12px; font-weight: bold; margin-bottom: 8px; }
        .hint { color: #555; font-size: 13px; margin-top: 10px; background: #f1f8f6; padding: 8px; border-radius: 6px; }
        .start-btn { display: block; width: 100%; background: #114b3e; color: white; padding: 14px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 16px; border: none; cursor: pointer; box-shadow: 0 4px 10px rgba(17,75,62,0.3); transition: 0.3s; text-decoration: none; box-sizing: border-box; }
        .start-btn:hover { background: #0d382f; }
        #timer-box { background: #ffebee; color: #c62828; border: 1px solid #ef9a9a; padding: 10px; border-radius: 10px; text-align: center; font-weight: bold; margin-bottom: 15px; font-size: 16px; display: none; }
        @media print {
            body { display: none !important; }
        }
    </style>
</head>
<body>
    <div class="main-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 2px solid #eee; padding-bottom: 10px;">
            <span style="font-size: 14px; color: #555;">المستوى: <strong style="color: #114b3e;">{{ level }}</strong></span>
            <span style="font-size: 14px; color: #555;">السؤال: <strong style="color: #114b3e;">{{ current_num }} من {{ total_questions }}</strong></span>
        </div>

        <h2>اختبار الدرس الأول الشامل</h2>
       
        <form method="POST" action="{{ url_for('quiz_step') }}" id="quiz-form">
            <div class="question-box">
                <span class="badge-type">اختيار من متعدد</span>
                <p><strong>سؤال {{ current_num }}:</strong> {{ question.prompt }}</p>
               
<div class="options-list">
    {% if question.options %}
        {% for opt in question.options %}
        <label class="option-item">
            <input type="radio" name="current_answer" value="{{ opt }}" required> {{ opt }}
        </label>
        {% endfor %}
    {% else %}
        <label class="option-item">
            <input type="radio" name="current_answer" value="True" required> True (صح)
        </label>
        <label class="option-item">
            <input type="radio" name="current_answer" value="False" required> False (خطأ)
        </label>
    {% endif %}
</div>
                <div class="hint">💡 <em>{{ question.hint }}</em></div>
            </div>
           
            <button type="submit" class="start-btn">السؤال التالي ←</button>
        </form>
    </div>
</body>
</html>
"""

RESULT_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>نتيجة الامتحان - سر التفوق</title>
    <style>
        body { font-family: 'Tahoma', sans-serif; background-color: #114b3e; color: #333; margin: 0; padding: 20px; direction: rtl; text-align: right; }
        .main-card { max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
        h2 { text-align: center; color: #114b3e; margin-top: 0; font-size: 26px; }
        .score-box { background: #e8f5e9; border: 2px solid #2e7d32; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 25px; }
        .score-num { font-size: 32px; font-weight: bold; color: #1b5e20; }
        .res-item { background: #f9f9f9; border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 10px; }
        .correct { border-right: 5px solid #2e7d32; }
        .wrong { border-right: 5px solid #c62828; }
        .start-btn { display: block; width: 100%; background: #114b3e; color: white; padding: 14px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 16px; border: none; cursor: pointer; box-shadow: 0 4px 10px rgba(17,75,62,0.3); transition: 0.3s; text-decoration: none; box-sizing: border-box; }
        .start-btn:hover { background: #0d382f; }
        .wa-btn { background: #25d366; margin-top: 10px; display: block; text-align: center; }
        .wa-btn:hover { background: #1ebe57; }
    </style>
</head>
<body>
    <div class="main-card">
        <h2>نتيجة اختبارك</h2>
       
        <div class="score-box">
            <p style="margin: 0 0 5px 0; font-size: 16px; color: #333;">لقد أتممت الاختبار بنجاح!</p>
            <div class="score-num">{{ score }} / {{ total }}</div>
            <p style="margin: 5px 0 0 0; font-size: 14px; color: #555;">المستوى: {{ level }}</p>
        </div>

        <h3>تفاصيل الإجابات:</h3>
        <div style="margin-top: 15px;">
            {% for r in results %}
                <div class="res-item {% if r.is_correct %}correct{% else %}wrong{% endif %}">
                    <p><strong>سؤال {{ r.id }}:</strong> {{ r.prompt }}</p>
                    <p style="margin: 5px 0; font-size: 14px;">إجابتك: <span style="font-weight: bold; color: {% if r.is_correct %}#2e7d32{% else %}#c62828{% endif %};">{{ r.user_ans }} {% if r.is_correct %}✅{% else %}❌{% endif %}</span></p>
                    {% if not r.is_correct %}
                        <p style="margin: 5px 0; font-size: 14px; color: #2e7d32;">الإجابة الصحيحة هي: <strong>{{ r.correct_ans }}</strong></p>
                    {% endif %}
                </div>
            {% endfor %}
        </div>

        <button type="button" class="start-btn print-btn" onclick="window.print()" style="background: #455a64; margin-top: 15px;">🖨️ طباعة النتيجة</button>
        <a href="/" class="start-btn" style="text-align: center; margin-top: 10px;">🔄 تصميم امتحان جديد</a>
        <a href="https://wa.me/201221581154?s=t" class="start-btn wa-btn" target="_blank">تواصل عبر الواتساب للاشتراك 💬</a>
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
