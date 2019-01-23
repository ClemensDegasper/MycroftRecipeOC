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

    @intent_handler(IntentBuilder("").require("give.me").require("Ingredients").build())
    def handle_categorie_cuisine_intent(self, message):
        #print("cuisine handler")
        catCui = message.data.get("Ingredients")
        catCui = self.parseMessage(catCui)
        result = self.getCatOrCui(catCui)
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

    def parseMessage(self, message):
	    # split message
	    message = re.split("\W+", message)
	    # remove and
	    while "and" in message: message.remove("and")
	    return message

    def getCatOrCui(self, catCui):
        result = None
        try:
             result = SparqlCon.getRecipe(cuisine=catCui)[0]
        except IndexError:
            result = SparqlCon.getRecipe(categories=catCui)[0]
        return result
	    
    def ReadNextInstructionStep(self):
        self.currentInstructionStep += 1
        self.ReadInstructionStep()

	
    def ReadInstructionStep(self):
        instructions = self.currentInstructions[self.currentInstructionStep]["text"]["value"]
        self.speak_dialog("read.instructions", data={"instructions": instructions})

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


	

