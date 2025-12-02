# Fundamentals of Data Engineering Exercise 2 Correction

### Student: Ángel Moliné

---

## Correction Notes

### Issues to solve:

#### (scrapper) Modify get_songs to use catalog (2 points)
- [ ] Points awarded: 2
- [ ] Comments: 

#### (scrapper) Check logs for strange messages (0.5 points)
- [ ] Points awarded: 0
- [ ] Comments: 
    Looking at your response:
    ```
    Several issues can be observed:
    Many songs are being installed again even though they were already downloaded previously.
    Some song titles differ from the actual ones.
    Some log messages are incorrect. For example, it says it will install lyrics from a certain source, but the real source is: acordes.lacuerda.net.
    ```
    No examples provided for each of the wrong log entries. It is important, when you see some issues, to give examples that reproduces the errors so you or someone else can trace it. Keep it in mind for future projects.

    The first one you are noticing: is it an error? Maybe is ok to do that in case an update has been made on the source. I was not able to reproduce any of the log message issues you pointed.

    Also you say nothing about errors in the catalog load, that has the main issue here, though it does not affect the functionality.

    

 
#### (cleaner) Avoid processing catalogs (0.5 points)
- [ ] Points awarded: 0.5
- [ ] Comments:

#### (Validator) Fix directory creation issue (0.5 points)
- [ ] Points awarded: 0.5
- [ ] Comments:

#### (Validator) Additional validation rule (0.5 points)
- [ ] Points awarded: 0.3
- [ ] Comments: Good approach, it can be useful to have that. But you should have considered using the variables in tab_cleaner/utils/chords.py here, coping tha utils file in the validation module, so you can avoid hardcoded validation inputs on chords, as the rule you added is incomplete. For example chords like "F#5" are not considered in your validation rule, but they are used in the cleaner.

#### Code improvements (0.5 points)
- [ ] Points awarded: 0.1
- [ ] Comments: Your response was:
```
- Avoid repeating the same file-handling code by moving it into a small helper function.
- Add basic type hints to make the functions easier to understand.
- Reduce the number of global variables by grouping paths into a single config section.
- Add short docstrings to explain what each function does.
- Unify the logging format so all modules print consistent messages. 
```
You need to provide examples. All your comments on the code are very general, and does not reflect the impact on the usability, readability or performance on the code. Maybe the 'Reduce the number of global variables by grouping paths into a single config section.' is the most straightfordward to do, but how will you handle this? a config file? Which type?. You need to specify.

### Functionalities to add:

#### 'results' module (0.5 points)
- [ ] Points awarded: 0.3
- [ ] Comments: there are a couple of issues here:
- - Your code only prints the results. You are not storing anywhere those results. What if it was a pipeline that needs to be executed daily and you need to track these results to monitor them?
- - '@click.command()' being defined, but not used. It is doing nothing there.
- - You are not logging anything from this module. You could use a log file to both log the execution and the results to keep track.

But the main functionality is there, and you distinguished between the outputs of the validator, so its fine.

#### 'lyrics' module (2 points)
- [ ] Points awarded: 0.2
- [ ] Comments: Code runs, but is not working properly. This is one output I am seeing:
``` 
rumba_sin_nombre_lyrics.txt


si todos quieren juzgarme
#
yo aquí estoy en alma y cuerpo.

#
No puedo seguir callándome

no puedo ni tampoco quiero

yo quiero gritarle al viento
#
y que se entere el mundo entero.
```
So the chords are not being removed completely.

Also there are several issues:
- - You did not modularized your code. For example 'list_txt_files_recursive' function could be placed on an utility file like 'utils/files.py' as we are doing in other modules.
- - '@click.command()' being defined, but functionality not used. It is doing nothing there.
- - You are not logging anything from this module.
- - You should have considered using the variables in tab_cleaner/utils/chords.py.
- - You are storing the results in the same validation folder. *This is a critical failure*. You should have created a new directory called 'lyrics' inside the files directory so you can access the lyrics only easily.

#### 'insights' module (2 points)
- [ ] Points awarded: 0.5
- [ ] Comments: Code does not work as it states:
```
Directory not found: files/validations/ok/cleaned/songs
```
Probably, it is because you worked on the validator issues after working on that. I changed the directory, and it worked well. The aproach is good but several issues with the code, the same ones as stated in the lyrics part. Also lacking comments on functionality and code is not ordered.

As the code works after the directory change, I am giving 0.5. But the fact is that your script as it is, does not work. Keep atention to detail and always test the code before going to production!

#### Main execution file (1 point)
- [ ] Points awarded: 1
- [ ] Comments: Good job here. Good approach on using the subprocess library.

---

## Total Score: 5.4 / 10 points

## General Comments:
In general, good job on the code, the full pipeline almost works as expected. You need to have more attention to detail, put logging on all scripts you make, and most importantly, test carefully before sending the final code. There are several issues as stated in each of the parts of the exercise, being the most critical error the path in the 'lyrics' module. A missing bug like that could have mayor issues in real projects, so it is critical. Also, when you report bugs or improvements, you need to be specific and provide examples for other people (and you) to understand. 