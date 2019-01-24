# TODO: Add an appropriate license to your skill before publishing.  See
# the LICENSE file for more information.

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG
import RecipeSkill.SPARQLConnector as SparqlCon
import re

class RecipeSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(RecipeSkill, self).__init__(name="RecipeSkill")
        self.currentRecipe = None
        self.currentInstructions = None
        self.currentInstructionStep = 0

    @intent_handler(IntentBuilder("").require("search.recipe.with").require("Ingredients").build())
    def handle_hello_world_intent(self, message):
        ingredients = message.data.get("Ingredients")
        ingredients = self.parseMessage(ingredients)
        #print(ingredients)
        result = SparqlCon.getRecipe(ingredients=ingredients)[0]
        self.ResetGlobalVars()
        self.currentRecipe = result
        name = result["name"]["value"]
        description = result["description"]["value"]
        self.speak_dialog("looking.for.recipe", data={"name": name, "description": description})

    @intent_handler(IntentBuilder("").require("search").require("CatCui").require("recipe").optionally("with").optionally("Ingredients").build())
    def handle_categorie_cuisine_intent(self, message):
        #print("cuisine handler")
        catCui = message.data.get("CatCui")
        ingredients = message.data.get("Ingredients")
        print(ingredients)
        catCui = self.parseMessage(catCui)
        if (ingredients != None):
            ingredients = self.parseMessage(ingredients)
        result = self.getCatOrCuiAndIngri(catCui, ingredients)
        self.ResetGlobalVars()
        self.currentRecipe = result
        name = result["name"]["value"]
        description = result["description"]["value"]
        self.speak_dialog("looking.for.recipe", data={"name": name, "description": description})

    @intent_handler(IntentBuilder("").require("give.me.ingredients").build())
    def handle_give_ingredients_intent(self, message):
        if(self.currentRecipe == None):
            self.speak_dialog("no.recipe")
            return
        ingredients = SparqlCon.getRecipeIngredientsById(self.currentRecipe["id"]["value"])                
        self.speak_dialog("read.ingredients", data={"ingredients": ingredients})

    @intent_handler(IntentBuilder("").require("read.info").build())
    def handle_read_info_intent(self, message):
        if(self.currentRecipe == None):
            self.speak_dialog("no.recipe")
            return
        SparqlCon.getCategories
        dialog = self.currentRecipe["keywords"]["value"]
        dialog += ", the cuisine is " + self.currentRecipe["cui"]["value"]
        dialog += ", the preperation time is " + self.parseTime(self.currentRecipe["prepTime"]["value"])
        dialog += ", the cooking time is "+ self.parseTime(self.currentRecipe["cookTime"]["value"])
        dialog += ", and the total time is "+ self.parseTime(self.currentRecipe["totalTime"]["value"])
        self.speak_dialog("read.info", data={"info": dialog})



    @intent_handler(IntentBuilder("").require("read.instructions").build())
    def handle_read_instructions_intent(self, message):
        if(self.currentRecipe == None):
            self.speak_dialog("no.recipe")
            return
        self.currentInstructions = SparqlCon.getInstructionsById(self.currentRecipe["id"]["value"])
        self.ReadInstructionStep()
        
    @intent_handler(IntentBuilder("").require("read.next.step").build())
    def handle_read_next_step_intent(self, message):
        if(self.currentInstructions == None):
            self.handle_read_instructions_intent(message)
            return
        
        self.ReadNextInstructionStep()

    @intent_handler(IntentBuilder("").require("repeat.step").build())
    def handle_repeat_step_intent(self, message):
        if(self.currentInstructions == None):
            self.handle_read_instructions_intent(message)
            return
        
        self.ReadInstructionStep()

    def parseTime(self, timeStr):
        timeMessage = ""
        print(timeStr)
        time = re.split('(\d+)',timeStr)
        for i in range(len(time)):
            if time[i].isdigit():
                if time[i] != "00":
                    if time[i+1] == "H":
                        if timeMessage != "":
                            timeMessage += " and "
                        timeMessage += time[i] + " hours "
                    elif time[i+1] == "M":
                        if timeMessage != "":
                            timeMessage += " and "
                        timeMessage += time[i] + " minutes"
        return timeMessage

    def parseMessage(self, message):
	    # split message
	    message = re.split("\W+", message)
	    # remove and
	    while "and" in message: message.remove("and")
	    return message

    def getCatOrCuiAndIngri(self, catCui, ingredients):
        result = None
        try:
            if ingredients == None:
                result = SparqlCon.getRecipe(cuisine=catCui)[0]
            else:
                result = SparqlCon.getRecipe(cuisine=catCui, ingredients=ingredients)[0]
        except IndexError:
            if ingredients == None:
                result = SparqlCon.getRecipe(categories=catCui)[0]
            else:
                result = SparqlCon.getRecipe(categories=catCui, ingredients=ingredients)[0]
        return result
	    
    def ReadNextInstructionStep(self):
        self.currentInstructionStep += 1
        self.ReadInstructionStep()

	
    def ReadInstructionStep(self):
        try:
            instructions = self.currentInstructions[self.currentInstructionStep]["text"]["value"]
            self.speak_dialog("read.instructions", data={"instructions": instructions})
        except IndexError:
            self.speak_dialog("no.steps")

    # this function should be called every time before a new recipe is set
    def ResetGlobalVars(self):
        self.currentRecipe = None
        self.currentInstructions = None
        self.currentInstructionStep = 1
   
    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, there is no need to override it.  If you DO
    # need to implement stop, you should return True to indicate you handled
    # it.
    #
    # def stop(self):
    #    return False

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return RecipeSkill()


	

