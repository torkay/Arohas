import requests
import utils

class check():
    def serverStatus():
        response = requests.get("https://wizard101.com")

        # Check the response status code
        if response.status_code == 200:
            # Retrieve the website source code
            source_code = response.text

            # Check website entails down status
            if source_code == utils.text.websiteGuts():
                # Server is down
                return(False)
            
            # Server is up
            else:
                return(True)
            
    def quest(input):
        url = utils.text.findQuest.placeholder
        list = utils.text.findQuest.worlds
        answer = ""


        for i in list:
            print(f"Checking {utils.text.findQuest.worldNames[list.index(i)]}'s quests")
            response = requests.get(url+i)

            # Check the response status code
            if response.status_code == 200:
                # Retrieve the website source code
                source_code = response.text

                # Check website entails user's input
                if input.lower() in source_code.lower():
                    # Quest is in 'i' world
                    lines = source_code.lower().split('\n')
                    for line in lines:
                        if input.lower() in line:
                            answer = line.strip()
                            break
                    index = answer.find("<")
                    if index != -1:
                        answer = answer[:index]
                    answer = f"{utils.text.findQuest.worldNames[list.index(i)]}: {answer.capitalize()}"
                    break
        if answer:
            return(f"I found your quest in {answer}")
        else:
            return("I couldn't find your quest, sorry")

                