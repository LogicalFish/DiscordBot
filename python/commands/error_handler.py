import settings

# Dictionary translating error-codes to phrases.

ERROR_DICT = {"command_not_found": "Het commando '*{}*' is niet gevonden.",
              "string_too_long": "Het veld '*{}*' is te lang.",
              "number_not_valid": "'*{}*' is geen valide getal.",
              "required_field_missing": "Het verplichte veld '*{}*' mist.",
              "database_error": "Er is geen valide database gevonden.",
              # EVENTS
              "event_not_found": "Er is geen event met het ID '*{}*' gevonden.",
              "not_authorized": "Jij bent niet de eigenaar van dit evenement.",
              "invalid_reminder": "'*{}*' is geen valide input voor reminders.",
              "invalid_date": "'*{}*' is geen valide tijd/datum combinatie.",
              "invalid_future_date": "'*{}*' is in het verleden.",
              "invalid_shadow": "{} is geen valide schaduw-event.",
              # DICE
              "invalid_dice": "Er zijn geen valide dobbelstenen gevonden. "
                              "(Dobbelstenen hoger dan een d{} worden genegeerd.)\n".format(settings.MAXDIETYPE),
              # MINESWEEPER
              "board_too_small": "Het opgegeven bord is te klein.",
              "too_many_bombs": "Er kunnen niet meer bommen dan vakjes zijn.",
              }

ERROR_DICT_ENGLISH = {"command_not_found": "There is no command '*{}*'.",
                      "string_too_long": "Field '{}' is too long.",
                      "number_not_valid": "'{}' is not a valid number.",
                      "required_field_missing": "The required field '*{}*' is missing.",
                      "database_error": "No operational database has been found.",
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
                          settings.MAXDIETYPE),
                      # MINESWEEPER
                      "board_too_small": "The board dimensions are too small.",
                      "too_many_bombs": "Can't have more bombs than squares.",
                      }
