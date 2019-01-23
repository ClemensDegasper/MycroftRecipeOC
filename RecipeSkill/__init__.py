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

    @intent_handler(IntentBuilder("").require("search.recipe.with").require("Ingredients").build())
    def handle_hello_world_intent(self, message):
        ingredients = message.data.get("Ingredients")
        ingredients = parseMessage(ingredients)
        #print(ingredients)
        result = SparqlCon.getRecipe(ingredients=ingredients)[0]
        self.currentRecipe = result
        name = result["name"]["value"]
        description = result["description"]["value"]
        self.speak_dialog("looking.for.recipe", data={"name": name, "description": description})
        self.set_context("recipe", result["id"]["value"])

    @intent_handler(IntentBuilder("").require("give.me").require("Ingredients").build())
    def handle_categorie_cuisine_intent(self, message):
        print("cuisine handler")
        catCui = message.data.get("Ingredients")
        catCui = parseMessage(catCui)
        result = SparqlCon.getRecipe(cuisine=catCui)[0]
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
        print(ingredients)                    
        #self.speak_dialog("looking.for.recipe", data={"name": name, "description": description})

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

def parseMessage(message):
	# split message
	message = re.split("\W+", message)
	# remove and
	while "and" in message: message.remove("and")
	return message
