=========================================
  PYTHON DAY-1 ASSIGNMENT - README
=========================================

HOW TO RUN EACH FILE
---------------------

All basic question files (q1 to q19) can be run like this:
    python q1_remove_duplicates.py
    python q2_second_largest.py
    ... and so on


HOW TO RUN THE USER MANAGEMENT SYSTEM (Q20)
---------------------------------------------
1. Open your terminal / command prompt
2. Navigate into the user_management folder:
       cd user_management
3. Run the main file:
       python main.py
4. A menu will appear - use numbers 1-5 to navigate


FILE STRUCTURE
--------------
python_day1_assignment/
│
├── q1_remove_duplicates.py        -> Remove duplicates without set()
├── q2_second_largest.py           -> Second largest without sorting
├── q3_group_anagrams.py           -> Group anagram words
├── q4_top_k_frequent.py           -> Top K frequent elements
├── q5_word_frequency.py           -> Word count from file
├── q6_json_validation.py          -> Check if JSON is valid
├── q7_custom_exception.py         -> Custom exception for low salary
├── q8_flatten_list.py             -> Flatten nested list recursively
├── q9_lambda_sort.py              -> Sort dicts using lambda
├── q10_env_loader.py              -> Load .env file variables
├── q11_logging.py                 -> Log errors with timestamp
├── q12_to_q16_comprehensions.py   -> All list/dict comprehension questions
├── q17_banking_system.py          -> OOP banking with encapsulation
├── q18_bird_lsp.py                -> LSP bird hierarchy fix
├── q19_ecommerce_checkout.py      -> SOLID checkout system
│
└── user_management/               -> Final CLI project (Q20)
    ├── main.py                    -> Run this to start the app
    ├── utils.py                   -> register, login, view, delete functions
    ├── storage.py                 -> load/save users.json
    ├── logger.py                  -> log_message() function
    ├── users.json                 -> User data storage
    └── logs.txt                   -> Activity log file


TIPS FOR BEGINNERS
------------------
- Read the comments in each file carefully - they explain every line
- Run one file at a time to understand what it does
- Try changing the input values to see how output changes
- If you get an error, read the error message - Python tells you exactly what went wrong
