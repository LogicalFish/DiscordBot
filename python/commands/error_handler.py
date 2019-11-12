from modules.dice import dice_config

# Dictionary translating error-codes to phrases.

ERROR_DICT = {"command_not_found": "Het commando '*{}*' is niet gevonden.",
              "string_too_long": "Het veld '*{}*' is te lang.",
              "number_not_valid": "'*{}*' is geen valide getal.",
              "required_field_missing": "Het verplichte veld '*{}*' mist.",
              "database_error": "Er is geen valide database gevonden.",
              "already_banned": "Ik ben al verbannen in dit kanaal.",
              "not_banned": "Ik ben niet verbannen in dit kanaal.",
              "command_not_allowed": "Jij mag dit commando niet uitvoeren.",
              # EVENTS
              "event_not_found": "Er is geen event met het ID '*{}*' gevonden.",
              "not_authorized": "Jij bent niet de eigenaar van dit evenement.",
              "invalid_reminder": "'*{}*' is geen valide input voor reminders.",
              "invalid_date": "'*{}*' is geen valide tijd/datum combinatie.",
              "invalid_future_date": "'*{}*' is in het verleden.",
              "invalid_shadow": "{} is geen valide schaduw-event.",
              # DICE
              "invalid_dice": "Er zijn geen valide dobbelstenen gevonden. "
                              "(Dobbelstenen hoger dan een d{} worden genegeerd.)\n".format(dice_config.MAXDIETYPE),
              # MINESWEEPER
              "board_too_small": "Het opgegeven bord is te klein.",
              "too_many_bombs": "Er kunnen niet meer bommen dan vakjes zijn.",
              # WHEEL
              "invalid_character": "{} is geen valide letter.",
              "vowel": "{} is geen medeklinker.",
              "not_a_vowel": "{} is geen klinker.",
              "already_revealed": "De letter {} is al geraden.",
              "no_cash": "Je hebt niet genoeg geld om dat te doen.",
              "no_guess": "Je kan niet raden zonder eerst het rad te draaien.",
              }

ERROR_DICT_ENGLISH = {"command_not_found": "There is no command '*{}*'.",
                      "string_too_long": "Field '{}' is too long.",
                      "number_not_valid": "'{}' is not a valid number.",
                      "required_field_missing": "The required field '*{}*' is missing.",
                      "database_error": "No operational database has been found.",
                      "already_banned": "Can't ban a channel that is already banned.",
                      "not_banned": "Can't unban a channel that is not banned.",
                      "command_not_allowed": "You are not allowed to access this command.",
                      # EVENTS
                      "event_not_found": "No event with ID '{}' gevonden.",
                      "not_authorized": "You do not own this event.",
                      "invalid_date": "'{}' is not a valid time/date combination.",
                      "invalid_future_date": "'{}' is in the past.",
                      "invalid_reminder": "'{}' is not a valid input for reminders.",
                      "invalid_shadow": "Shadow is invalid.",
                      # DICE
                      "invalid_dice": "Did not read valid dice. "
                                      "(Reminder: Any dice higher than a d{} are ignored.)\n".format(
                          dice_config.MAXDIETYPE),
                      # MINESWEEPER
                      "board_too_small": "The board dimensions are too small.",
                      "too_many_bombs": "Can't have more bombs than squares.",
                      # WHEEL
                      "invalid_character": "{} is not a valid letter.",
                      "vowel": "{} is not a consonant.",
                      "not_a_vowel": "{} is not a vowel.",
                      "already_revealed": "The letter {} has already been guessed.",
                      "no_cash": "You need more money to do that.",
                      "no_guess": "You can not guess if you have not spun the wheel.",
                      }
